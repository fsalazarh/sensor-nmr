"""Module for requests to backend api"""
import logging
import gspread
import requests

from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

from connection.data_processor import DataProcessor

from datetime import datetime

from models.peak import Peak
from models.noise import Noise

class RequestHandler():
    """Handler for request to the google drive backend
    """
    def __init__(self):
        self.book = None
        self.sheet = None
        self.client = None
        self.date = None
        self.row = 2
        self.folder_name = 'Colegio1'

    def authenticate(self):
        """Connects to the server and gets the headers"""
        scope = ['https://www.googleapis.com/auth/drive']
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name('secrets.json',scope)
            self.client = gspread.authorize(creds)
            self.book = 0
            self.date_update()
            return True
        except Exception as e:
            logging.error('Authentication to Google Drive backend failed, server does not respond: '+ str(e))
            return False

    def date_update(self):
        actual_date = datetime.utcnow().strftime('%Y-%m-%d')
        self.date = actual_date
        for element in self.client.list_spreadsheet_files():
            if element['name'] == 'Noise_'+actual_date:
                self.book = self.client.open('Noise_'+actual_date)
        if self.book == 0:
            gauth = GoogleAuth()
            # Try to load saved client credentials
            gauth.LoadCredentialsFile("mycreds.txt")
            if gauth.credentials is None:
                # Authenticate if they're not there
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                # Refresh them if expired
                gauth.Refresh()
            else:
                # Initialize the saved creds
                gauth.Authorize()
            # Save the current credentials to a file
            gauth.SaveCredentialsFile("mycreds.txt")
            drive = GoogleDrive(gauth)
            list_folders = drive.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
            folder = None
            for folder_from_list in list_folders:
                if folders['title'] == self.folder_name:
                    folder = folder_from_list
            if folder is None:
                folder = drive.CreateFile({'title': self.folder_name,
                                        "mimeType": "application/vnd.google-apps.folder"})
                folder.Upload()
                folder.InsertPermission({'type': 'user',
                            'value': 'smartcitizen@smartcitizen-240518.iam.gserviceaccount.com',
                            'role': 'writer'})
            file = drive.CreateFile({'title': 'Noise_'+actual_date,
                                    'mimeType': 'application/vnd.google-apps.spreadsheet',
                                    'parents': [{'kind': 'drive#fileLink','id': folder['id']}]})
            file.Upload()
            file.InsertPermission({'type': 'user',
                        'value': 'smartcitizen@smartcitizen-240518.iam.gserviceaccount.com',
                        'role': 'writer'})
            self.book = self.client.open('Noise_'+actual_date)
        self.sheet_update(actual_date)

    def sheet_update(self,date):
        for sheet in self.book.worksheets():
            if sheet.title == self.date:
                self.sheet = self.book.worksheet(self.date)
                self.row = len(self.sheet.col_values(1))+1
                return
        self.sheet = self.book.add_worksheet(title=date, rows="3000", cols="7")
        for sheet in self.book.worksheets():
            if sheet.title == 'Hoja 1':
                self.book.del_worksheet(sheet)
        cell_list = self.sheet.range('A1:G1')
        cell_list[0].value = 'Registered at'
        cell_list[1].value = 'Synchronized at'
        cell_list[2].value = 'Peak value'
        cell_list[3].value = '1 percent peak'
        cell_list[4].value = '5 percent peak'
        cell_list[5].value = '10 percent peak'
        cell_list[6].value = 'Average'
        self.sheet.update_cells(cell_list)
        self.row = 2

    def post_peak(self):
        """POST all peak value to Google Drive"""
        if self.authenticate():
            logging.info('Posting noise data to GoogleDrive')
            time = datetime.utcnow()
            Noise.destroy_synchronized()
            noises_base = Noise.find_unsynchronized()
            noises = noises_base.all()
            noises_rows = len(noises)
            logging.info('Noises posted: '+str(noises_rows))
            if len(noises) == 0:
                return
            if self.row+noises_rows-1 > 3000:
                logging.error('Exceded maximum data per day at drive')
            cell_list = self.sheet.range(self.row,1,self.row+noises_rows-1,7)
            for noise_row in range(noises_rows):
                cell_list[noise_row*7+0].value = noises[noise_row].registered_at.isoformat()
                cell_list[noise_row*7+1].value = time.isoformat()
                cell_list[noise_row*7+2].value = noises[noise_row].peak
                cell_list[noise_row*7+3].value = noises[noise_row].var1
                cell_list[noise_row*7+4].value = noises[noise_row].var5
                cell_list[noise_row*7+5].value = noises[noise_row].var10
                cell_list[noise_row*7+6].value = noises[noise_row].avg
                noises[noise_row].synchronized_at = time
                noises[noise_row].save()
            self.sheet.update_cells(cell_list)
            self.row += noises_rows

    def post_peak_big_query(self):
        logging.info('Posting noise data to BigQuery')
        time = datetime.utcnow()
        Noise.destroy_synchronized()
        noises_base = Noise.find_unsynchronized()
        noises = noises_base.all()
        noises_rows = len(noises)
        logging.info('Noises posted: '+str(noises_rows))
        if len(noises) == 0:
            return

        for noise_row in range(noises_rows):
            payload = {
                 'hw_id': 'Sensor test',
                 'registered_at': noises[noise_row].registered_at.strftime('%Y-%m-%d %H:%M:%S'),
                 'synchronized_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                 'peak_value': noises[noise_row].peak,
                 'percent_1': noises[noise_row].var1,
                 'percent_5': noises[noise_row].var5,
                 'percent_10': noises[noise_row].var10,
                 'avg': noises[noise_row].avg,
            }

            try:
                request = requests.post('http://apiecological.com/api/v1/docs', data=payload, timeout=5)
                noises[noise_row].synchronized_at = time
                noises[noise_row].save()

            except (requests.ConnectionError) as e:
                print('No internet connection.')

            
        