# Retro gaming video game console + Old French Minitel (DIY)

[![External components](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Doc/ExternalComponents.jpg)](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Doc/ExternalComponents.jpg)

### A SuperSwag Project

The Minitel was a Videotex online service accessible through telephone lines, and is considered one of the world's most successful pre-World Wide Web online services. The service was rolled out in France in 1982 by the *Postes, Télégraphes et Téléphones* compagny. From its early days, users could make online purchases, make train reservations, check stock prices, search the telephone directory, have a mail box, and chat in a similar way to that now made possible by the Internet. Then, this service was retired on 30 June 2012.

Minitel used terminals consisting of a text-based screen, keyboard and modem. Simple graphics could be displayed using a set of predefined graphical characters. It used a half-duplex asymmetric data transmission via its modem. It downlinked at 1200 bit/s and uplinked at 75 bit/s. This allowed fast downloads, for the time.

I decided to reuse an old minitel in order to make a retro gaming console, because the case is cute and contains an embedded screen. To make the system work, I used a Raspberry Pi as a computer, an Arduino Nano to control power and peripherals, a 10'' LCD and a stereo speaker. I managed to reuse the original keyboard (with some DIY) but I also added two front USB ports to connect more modern peripherals, such as gamepads.

Here's how it works:

[![Functionnal schema](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Doc/Functionnal_schema.png)](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Doc/Functionnal_schema.png)

Inside, I had to make a plastic support thanks to a 3D printer to contain all the electronic components. The Arduino Nano manages the life cycle of the system. It communicates with the Raspberry using the I2C connection to send him the sound volume value (which can be changed with the minitel's original pot) and the order of shutdown. The Raspberry contains a special retro gaming linux distribution that ships all the emulators from consoles prior to the PlayStation. The display is ensured by an LCD screen specially bought for the occasion, which I had to cut out to adapt it to the original box.

Here's what it looks like inside the box:

[![Internal components](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Doc/InternalComponents.jpg)](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Doc/InternalComponents.jpg)

### Conception

#### Power management / Electronic design
Naturally, raspberry is not able to handle an on/off button that allows the power supply to be turned off properly once the embedded linux has shutdown. To do this, I have added an arduino that controls the power supply and manages the system life cycle.

[![Electronic schema](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Electronique/Schema_bb.jpg)](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Electronique/Schema_bb.png)

- [Arduino Sketch : INO file](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/blob/master/SuperSwag3615.ino)
- [Python script : I2C connection polling](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/blob/master/Scripts%20Raspberry/polling.py)
- [Bash script : startup process](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/blob/master/Scripts%20Raspberry/startup.sh)

#### Keyboard
The original minitel keyboard is connected directly to the raspberry pi. It works perfectly with the following script:
- [Python script : Keyboard polling](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/blob/master/Scripts%20Raspberry/keyboard.py)

#### 3D printed components
To integrate all the components in the case and offer USB interfaces on the front, I printed several plastic components using a 3D printer. Models are available in the Casing directory.
[![3D prints](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Doc/3D_prints.png)](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Doc/3D_prints.png)

#### Materials

- The Raspberry Pi 3 (Model B) as main engine
- Arduino Nano (from SODIAL)
- [10.1 inch LCD touch screen](https://www.amazon.fr/gp/product/B01E8O5B20/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1)
- A simple USB audio speaker with Jack connector

#### Software

[![RetropieLogo](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Doc/RetropieLogo.jpg)](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Doc/RetropieLogo.jpg)

On the raspberry pi:
- Installed Operating System : [RetroPie](https://retropie.org.uk/)
- Plus some linux packages: i2c-tools and python-smbus, alsa-utils (for sounds), python-uinput (for keyboard)
- I also replaced the [/boot/config.txt](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/blob/master/Scripts%20Raspberry/config.txt) to adapt screen resolution
- See [setup document](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/blob/master/Scripts%20Raspberry/setup.txt) for more details

I also used:
- Scraper : [Universal XML Scraper](https://github.com/Universal-Rom-Tools/Universal-XML-Scraper/releases)

#### Automatic Synch

The console automatically synchronizes game saves backups with an HTTP server. A raspberry-side python script and a server-side PHP script ensure the synchronization of files periodically, thanks to a CRON task.

[![SynchScript](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Doc/UpdateScriptLog.gif)](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/raw/master/Doc/UpdateScriptLog.gif)

[Python](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/blob/master/Scripts%20Raspberry/synch-cloud.py) and [PHP](https://github.com/rbello/Minitel-Raspberry-Retro-gaming/blob/master/Synchro/index.php) scripts uses an OTP authentication using algorithms specified in RFC 6238 and RFC 4226 (also used by Google Authenticator).

*This repository contains all the files allowing the creation of a similar console. This content is copyright free.*