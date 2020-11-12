"""Main module for execution of sinestesia software"""
import logging
import os
from datetime import datetime

from connection.audio_retriever import AudioRetriever
from connection.data_processor import DataProcessor
from connection.light_manager import LightManager
from databases.database import Database
from synchronization.synchronizers import DriveSynchronizer

from thread_manager import ThreadManager
from utils.singleton import SingletonMixin

class MenuMessages(SingletonMixin):
    """Class to obtains menu messages"""
    def print_main_menu(self):
        """Prints the main menu"""
        print('\nWelcome to Sinestesia! please choose an action:')
        print('1. Raspberry services')
        print('2. Exit')

    def print_services_menu(self):
        """Prints the services menu"""
        print('\nWhat would you like to do?')
        print('1. View services status')
        print('2. Start a service')
        print('3. Stop a service')
        print('4. Back to main menu')

    def print_start_service_menu(self):
        """Prints the start services menu"""
        print('\nWhat service would you like to start?')
        print('1. Audio retrieving')
        print('2. Data processor')
        print('3. Light manager')
        print('4. Drive synchronization')
        print('5. Back to previous menu')

    def print_stop_service_menu(self):
        """Prints the start services menu"""
        print('\nWhat service would you like to stop?')
        print('1. Audio retrieving')
        print('2. Data processor')
        print('3. Light manager')
        print('4. Drive synchronization')
        print('5. Back to previous menu')

    def print_raspberry_configuration_menu(self):
        """Prints the raspberry configuration menu"""
        print('\nWhat would you like to do?')
        print('1. Get temperature and voltage values')
        print('2. Back to previous menu')

class ServiceManager():
    """Class for controlling all services that can be run in the controller menu"""
    def __init__(self):
        self.create_database()
        self.audio_retriever = AudioRetriever()
        self.data_processor = DataProcessor()
        self.light_manager = LightManager()
        # define the base status of the services
        self.drive_synchronizer = DriveSynchronizer()
        self.services_running = {
            'AudioRetriever': False,
            'DataProcessor': False,
            'LightManager': False,
            'DriveSynchronizer': False
        }

        # start services
        self.start_audio_retriever()
        self.start_data_processor()
        self.start_light_manager()
        self.start_drive_synchronizer()

    def parse_integer(self, value):
        """Parses entered input to a valid integer"""
        try:
            return int(value)
        except ValueError:
            return 0

    def create_database(self):
        """Creates the database if it doesn't exist"""
        db = Database.instance()
        db.Base.metadata.create_all(bind=db.engine)
        db.set_session()

    def start_service(self, service_name):
        """Starts a service on the thread manager"""
        thread_manager = ThreadManager.instance()
        if thread_manager.is_thread_alive(service_name):
            print('Service is already running')
            return
        if service_name == 'AudioRetriever':
            self.start_audio_retriever()
        if service_name == 'DataProcessor':
            self.start_data_processor()
        if service_name == 'LightManager':
            self.start_light_manager()
        if service_name == 'DriveSynchronizer':
            self.start_drive_synchronizer()

    def start_audio_retriever(self, show_message=True):
        """Starts the audio retrieving service"""
        thread_manager = ThreadManager.instance()
        if not self.audio_retriever.is_recorder_device_ready():
            if show_message:
                print('\nCannot start audio retrieving, verify audio devices\n')
            return
        thread_manager.add_thread('AudioRetriever', self.audio_retriever.retrieve_audio)
        thread_manager.start_thread('AudioRetriever')
        print('\nStarted audio retrieving successfully\n')
        self.services_running['AudioRetriever'] = True

    def start_data_processor(self, show_message=True):
        """Starts the data processor service"""
        thread_manager = ThreadManager.instance()
        thread_manager.add_thread('DataProcessor',
                                    self.data_processor.convert_data,
                                    sleep_time=60)
        thread_manager.start_thread('DataProcessor')
        print('\nStarted data processor successfully\n')
        self.services_running['DataProcessor'] = True

    def start_light_manager(self, show_message=True):
        """Starts the light maanager service"""
        thread_manager = ThreadManager.instance()
        thread_manager.add_thread('LightManager',
                                    self.light_manager.rgb_set)
        thread_manager.start_thread('LightManager')
        print('\nStarted light manager successfully\n')
        self.services_running['LightManager'] = True

    def start_drive_synchronizer(self, show_message=True):
        thread_manager = ThreadManager.instance()
        self.drive_synchronizer.authenticate()
        if not self.drive_synchronizer._is_authenticated:
            if show_message:
                print('\nNot authenticated, cannot start drive synchronization\n')
            return
        thread_manager.add_thread('DriveSynchronizer',
                                  self.drive_synchronizer.synchronize,
                                  sleep_time=300)
        thread_manager.start_thread('DriveSynchronizer')
        print('\nStarted service drive synchronization successfully\n')
        self.services_running['DriveSynchronizer'] = True

    def stop_service(self, service_name):
        """Stops a service on the thread manager"""
        thread_manager = ThreadManager.instance()
        if thread_manager.is_thread_alive(service_name):
            if service_name == 'AudioRetriever':
                self.audio_retriever.stop_audio()
            ThreadManager.instance().stop_thread(service_name)
            print('\nService stopped successfully\n')
        else:
            print('\nCannot stop service that is not running\n')

    def temperature_and_voltage(self):
        """Obtains information of temperature and voltage"""
        print('\nTemperature:')
        os.system('/opt/vc/bin/vcgencmd measure_temp')
        print('Voltage:')
        os.system('/opt/vc/bin/vcgencmd measure_volts')
        print('Firmare:')
        os.system('/opt/vc/bin/vcgencmd version\n')

    def obtain_services_status(self):
        """Obtains and prints the status of services"""
        print('\n', ThreadManager.instance().status(), '\n')

    def verify_services_status(self):
        """
        Verify the status of the services running in a thread, if one has been stopped
        by an exception it will start it again automatically
        """
        thread_manager = ThreadManager.instance()
        try:
            for key, value in self.services_running.items():
                if value and not thread_manager.stopped_manually(key):
                    if key == 'AudioRetriever':
                        self.start_audio_retriever(show_message=False)
                        logging.info('Restarting automatically service audio retrieving')
                    if key == 'DataProcessor':
                        self.start_data_processor(show_message=False)
                        logging.info('Restarting automatically service data processor')
                    if key == 'LightManager':
                        self.start_light_manager(show_message=False)
                        logging.info('Restarting automatically service light manager')
                    if key == 'DriveSynchronizer':
                        self.start_drive_synchronizer(show_message=False)
                        logging.info('Restarting automatically service drive synchronizer')
        except Exception as error:
            logging.info('Tried to restart a service but a fatal error ocurred ' + str(error))

    def raspberry_last_states(self):
        """View the latest states of the raspberry"""
        count = self.parse_integer(input('\nHow many logs you want to show?'))
        latest_states = StateLog.latest_logs(count)
        print('\nState logs ordered from newest to oldest with limit ' + str(count))
        for state in latest_states:
            start_state = State.find(state.state_start)
            end_state = State.find(state.state_end)
            print('\nRaspberry went from ' + start_state.name+' to ' + end_state.name + ' at '+
                  str(utc_to_local(state.registered_at)))

class Controller():
    """Class for controlling all application services
    """
    def __init__(self):
        self.service_manager = ServiceManager()
        ThreadManager.instance().add_thread('ServicesVerifier',
                                            self.service_manager.verify_services_status,
                                            sleep_time=2)
        ThreadManager.instance().start_thread('ServicesVerifier')

    def parse_option(self, value):
        """Parses entered input to a valid integer option"""
        try:
            return int(value)
        except ValueError:
            return -1

    def parse_time_input(self, value):
        """Parses a string input of type hh:mm into two integers with corresponding hour and minute
        values"""
        values = value.split(':')
        if len(values) == 2:
            try:
                return int(values[0]), int(values[1])
            except Exception:
                return None, None
        return None, None

    def main_menu(self):
        """Choice for main menu"""
        looping = True
        while looping:
            MenuMessages.instance().print_main_menu()
            option = self.parse_option(input())
            if option == 1:
                self.services_menu()
            elif option == 2:
                looping = False
                ThreadManager.instance().stop_all()
            else:
                print('Invalid option')

    def services_menu(self):
        """Menu for services choice"""
        looping = True
        while looping:
            MenuMessages.instance().print_services_menu()
            option = self.parse_option(input())
            if option == 1:
                self.service_manager.obtain_services_status()
                logging.info('Requested services status')
            elif option == 2:
                self.start_service_menu()
            elif option == 3:
                self.stop_service_menu()
            elif option == 4:
                looping = False
            else:
                print('Option not found')

    def start_service_menu(self):
        """Menu for starting a service"""
        looping = True
        while looping:
            MenuMessages.instance().print_start_service_menu()
            option = self.parse_option(input())
            if option == 1:
                self.service_manager.start_service('AudioRetriever')
                logging.info('Requested to start info retrieving service')
            elif option == 2:
                self.service_manager.start_service('DataProcessor')
                logging.info('Requested to start data processor service')
            elif option == 3:
                self.service_manager.start_service('LightManager')
                logging.info('Requested to start light manager service')
            elif option == 4:
                self.service_manager.start_service('DriveSynchronizer')
                logging.info('Requested to start drive synchronizer service')
            elif option == 5:
                looping = False
            else:
                print('Option not found')

    def stop_service_menu(self):
        """Menu for stopping a service"""
        looping = True
        while looping:
            MenuMessages.instance().print_stop_service_menu()
            option = self.parse_option(input())
            if option == 1:
                self.service_manager.stop_service('AudioRetriever')
                logging.info('Requested to stop info retrieving service')
            elif option == 2:
                self.service_manager.stop_service('DataProcessor')
                logging.info('Requested to stop data processor service')
            elif option == 3:
                self.service_manager.stop_service('LightManager')
                logging.info('Requested to stop light manager service')
            elif option == 4:
                self.service_manager.stop_service('DriveSynchronizer')
                logging.info('Requested to stop drive synchronizer service')
            elif option == 5:
                looping = False
            else:
                print('Option not found')

def setup_logger():
    """Setups the logger configuration"""
    # create logger
    if not os.path.exists('logs'):
        os.makedirs('logs')
    log_filename = 'logs/' + str(datetime.utcnow().date()) + '.log'
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s - %(module)s:%(lineno)d - %(message)s'
    )

def main():
    """Main function"""
    setup_logger()
    Controller().main_menu()

if __name__ == "__main__":
    main()
