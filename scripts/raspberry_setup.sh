#!/bin/bash -e

# update and upgrade
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get install raspberrypi-kernel-headers -y

# python
sudo apt-get install screen python python-dev python3 python3-dev python3-pip build-essential  \
portaudio19-dev python-pyaudio python3-pyaudio htop  -y --fix-missing

# clean up installation
sudo apt-get -f install

# # ics43434
# cd
#
# mkdir ics43432
# cd ics43432
# wget https://raw.githubusercontent.com/raspberrypi/linux/rpi-4.4.y/sound/soc/codecs/ics43432.c
# echo "obj-m := ics43432.o" | sudo tee -a Makefile
# echo "" | sudo tee -a Makefile
# echo "all:" | sudo tee -a Makefile
# echo "	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules" | sudo tee -a Makefile
# echo "" | sudo tee -a Makefile
# echo "clean:" | sudo tee -a Makefile
# echo "	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean" | sudo tee -a Makefile
# echo "" | sudo tee -a Makefile
# echo "install:" | sudo tee -a Makefile
# echo "	sudo cp ics43432.ko /lib/modules/$(shell uname -r)" | sudo tee -a Makefile
# echo "	sudo depmod -a" | sudo tee -a Makefile
#
# make all install
#
# echo "/dts-v1/;" | sudo tee -a i2s-soundcard-overlay.dts
# echo "/plugin/;" | sudo tee -a i2s-soundcard-overlay.dts
# echo "" | sudo tee -a i2s-soundcard-overlay.dts
# echo "/ {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "    compatible = \"brcm,bcm2708\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "" | sudo tee -a i2s-soundcard-overlay.dts
# echo "    fragment@0 {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        target = <&i2s>;" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        __overlay__ {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "            status = \"okay\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "    };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "" | sudo tee -a i2s-soundcard-overlay.dts
# echo "    fragment@1 {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        target-path = \"/\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        __overlay__ {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "            card_codec: card-codec {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                #sound-dai-cells = <0>;" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                compatible = \"invensense,ics43432\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                status = \"okay\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "            };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "    };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "" | sudo tee -a i2s-soundcard-overlay.dts
# echo "    fragment@2 {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        target = <&sound>;" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        master_overlay: __dormant__ {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "            compatible = \"simple-audio-card\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "            simple-audio-card,format = \"i2s\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "            simple-audio-card,name = \"soundcard\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "            simple-audio-card,bitclock-master = <&dailink0_master>;" | sudo tee -a i2s-soundcard-overlay.dts
# echo "            simple-audio-card,frame-master = <&dailink0_master>;" | sudo tee -a i2s-soundcard-overlay.dts
# echo "            status = \"okay\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "            simple-audio-card,cpu {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                sound-dai = <&i2s>;" | sudo tee -a i2s-soundcard-overlay.dts
# echo "            };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "            dailink0_master: simple-audio-card,codec {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                sound-dai = <&card_codec>;" | sudo tee -a i2s-soundcard-overlay.dts
# echo "            };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "    };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "" | sudo tee -a i2s-soundcard-overlay.dts
# echo "    fragment@3 {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        target = <&sound>;" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        slave_overlay: __overlay__ {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                compatible = \"simple-audio-card\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                simple-audio-card,format = \"i2s\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                simple-audio-card,name = \"soundcard\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                status = \"okay\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                simple-audio-card,cpu {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                    sound-dai = <&i2s>;" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                dailink0_slave: simple-audio-card,codec {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                    sound-dai = <&card_codec>;" | sudo tee -a i2s-soundcard-overlay.dts
# echo "                };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "    };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "" | sudo tee -a i2s-soundcard-overlay.dts
# echo "    __overrides__ {" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        alsaname = <&master_overlay>,\"simple-audio-card,name\"," | sudo tee -a i2s-soundcard-overlay.dts
# echo "                    <&slave_overlay>,\"simple-audio-card,name\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        compatible = <&card_codec>,\"compatible\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "        master = <0>,\"=2!3\";" | sudo tee -a i2s-soundcard-overlay.dts
# echo "    };" | sudo tee -a i2s-soundcard-overlay.dts
# echo "};" | sudo tee -a i2s-soundcard-overlay.dts
#
# dtc -@ -I dts -O dtb -o i2s-soundcard.dtbo i2s-soundcard-overlay.dts
# sudo cp i2s-soundcard.dtbo /boot/overlays

# Grant permissions
sudo chown -R pi:pi /usr/local/

# configurations of system
echo "hdmi_blanking=1" | sudo tee -a /boot/config.txt
echo "dtparam=i2s=on" | sudo tee -a /boot/config.txt
echo "dtoverlay=i2s-soundcard,alsaname=mems-mic" | sudo tee -a /boot/config.txt

echo "@xset s 0 0" | sudo tee -a ~/.config/lxsession/LXDE-pi/autostart
echo "@xset s noblank" | sudo tee -a ~/.config/lxsession/LXDE-pi/autostart
echo "@xset s noexpose" | sudo tee -a ~/.config/lxsession/LXDE-pi/autostart
echo "@xset dpms 0 0 0" | sudo tee -a ~/.config/lxsession/LXDE-pi/autostart

# Copy init.id file and register
echo "./sinestesia/noise/scripts/noise" | sudo tee -a /etc/bash.bashrc
sudo cp /home/pi/sinestesia/noise/scripts/noise /etc/init.d/
sudo update-rc.d noise defaults

# Install requirements
cd /home/pi/sinestesia/noise
sudo apt-get install python3-scipy
pip3 install gspread
pip3 install -r requirements.txt
pip3 install RPi.GPIO
pip3 install PyDrive
