# Introduction

This is the main repository for Sinestesia Noise project. Code documentation goes here, in the Wiki. For more general documentation, such as the design and architecture of the application, refer to [this Confluence](). For hardware documentation INCOMPLETO.

# General information

This project is developed on python > 3.6 running on a Linux -------. It uses sqlite as database storage and SQLAlchemy as Object Relationship Manager (ORM).

## Testing

INCOMPLETO

# Raspberry installation guide

The software runs one main services: controller. Is a python program that manages the interaction between Sensor and RGB leds. Link: raspbian [2017-09-07](http://downloads.raspberrypi.org/raspbian/images/raspbian-2017-09-08/2017-09-07-raspbian-stretch.zip)

## Setting up

sudo python3 $(which easy_install) pip

sudo apt-get install portaudio19-dev python-pyaudio python3-pyaudio

Setup de tarjeta de audio es este [link](https://github.com/mano1979/Pesky-Products-ICS-43434)

<<<<<<< HEAD
sudo apt-get install git
$ sudo git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
$ sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
$ sudo apt-get install python-dev
$ cd pyaudio
$ sudo python setup.py install
=======
wget https://raw.githubusercontent.com/raspberrypi/linux/rpi-4.19.y/sound/soc/codecs/ics43432.c

>>>>>>> 5342a6af83083e805f19935138ba07565c9d3416

## Starting services

Para descargar git y tener permisos se necesita registrar la cuenta, se hace con el comando `ssh-keygen -t rsa -b 4096 -C "your@email.com"`, luego se agrega el codigo de `cat /home/pi/.ssh/id_rsa.pub` a settings->SSH keys en bitbucket.
INCOMPLETO

## Backend

Before starting be sure to have installed python > 3.6 and pip3 installed, create a virtualenv and install all libraries running `pip install -r requirements.txt`, then you can start the controller by running `python controller.py`.


# Contact us

INCOMPLETO
