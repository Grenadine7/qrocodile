# qrocodile

A kid-friendly system for controlling Sonos with QR codes.

## Origin

This is a fork of the qrocodile project originally developed by https://github.com/chrispcampbell

Changes to the original:
* support for Spotify Albums & Playlists
* generation of  cards for the Sonos Zones (Rooms) available in your house
* for the generation of QR codes, using the **pyqrcode** Python module instead of the OS package
* replaced urllib with **requests** python module
* updated to python3
* disabled use of webkit2png

For the whole story behind qrocodile, see the original project https://github.com/chrispcampbell/qrocodile

## What Is It?

On the hardware side, it's just a camera-attached Raspberry Pi nested inside some LEGO and running some custom software that scans QR codes and translates them into commands that control your Sonos system:

<p align="center">
<img src="docs/images/qroc-photo-front.jpg" width="40%" height="40%"> <img src="docs/images/qroc-photo-back.jpg" width="40%" height="40%">
</p>

On the software side, there are two separate Python scripts:

* Run `qrgen.py` on your primary computer.  It takes a list of songs (from your local music library and/or Spotify) and commands (e.g. play/pause, next) and spits out an HTML page containing little cards imprinted with an icon and text on one side, and a QR code on the other. Print them out, then cut, fold, and glue until you're left with a neat little stack of cards.

* Run `qrplay.py` on your Raspberry Pi. It launches a process that uses the attached camera to scan for QR codes, then translates those codes into commands (e.g. "speak this phrase", "play [song] in this room", "build a queue").

Python requirements:

* Python 3
* Python modules:
  * spotipy
  * requests
  * pyqrcode

## Installation and Setup

### 1. Prepare your Raspberry Pi

Originally built this using a Raspberry Pi 3 Model B (running Raspbian), it also works using a Raspberry Pi Zero W and an Arducam OV5647 camera module.  Things may or may not work with other models (for example, how you control the onboard LEDs varies by model).

To set up the camera module, I had to add an entry in `/etc/modules`:

```
% sudo emacs /etc/modules
# Add bcm2835-v4l2
% sudo reboot
# After reboot, verify that camera is present
% ls -l /dev/video0
```

Next, install `zbar-tools` (used to scan for QR codes) and test it out:

```
% sudo apt-get install zbar-tools
% zbarcam --prescale=300x200
```

Optional: Make a little case to hold your RPi and camera along with a little slot to hold a card in place.

### 2. Start `node-sonos-http-api`

Currently `qrplay` relies on a [custom fork](https://github.com/chrispcampbell/node-sonos-http-api/tree/qrocodile) of `node-sonos-http-api` that has been modified by chriscampbell to do things like:

* look up library tracks using only a hash string (to keep the QR codes simple)
* return a list of all available library tracks and their associated hashes
* speak the current/next track
* play the album associated with a song
* other things I'm forgetting at the moment

(Note: `node-sonos-http-api` made it easy to bootstrap this project, as it already did much of what I needed.  However, it would probably make more sense to use something like [SoCo](https://github.com/SoCo/SoCo) (a Sonos controller API for Python) so that we don't need to run a separate server, and `qrplay` could control the Sonos system directly.)

It's possible to run `node-sonos-http-api` directly on the Raspberry Pi, so that you don't need an extra machine running, but I found that it's kind of slow this way (especially when the QR scanner process is already taxing the CPU), so I usually have it running on a separate machine or Raspberry Pi to keep things snappy.

To install, clone the fork, check out the `qrocodile` branch, install, and start:

```
% git clone -b qrocodile https://github.com/chrispcampbell/node-sonos-http-api.git
% cd node-sonos-http-api
% npm install --production
% npm start
```

### 3. Generate some cards with `qrgen`

First, clone the `qrocodile` repo if you haven't already on your primary computer:

```
% git clone https://github.com/dernorberto/qrocodile
% cd qrocodile
```

Spotify track/album/playlist URIs can be found in the Spotify app by clicking a song, then selecting "Share > Copy Spotify URI".  For `qrgen` to access your Spotify account, you'll need to set up your own Spotify app token.  (More on that in the `spotipy` [documentation](http://spotipy.readthedocs.io/en/latest/).)

You can use `qrgen` to list out URIs for all available tracks in your music library (these examples assume `node-sonos-http-api` is running on `localhost`):

```
% python3 qrgen.py --hostname <IP of node-sonos-http-api host> --list-library
```

Next, create a text file that lists the different cards you want to create.  (See `example.txt` for some possibilities.)

Finally, generate some cards and view the output in your browser:

```
% python3 qrgen.py --hostname <IP of node-sonos-http-api host> --input example.txt --generate-images --spotify-user <spotify username>
% open out/index.html
```

The cards for Commands and Sonos Zones are generated separately.

Create Sonos Zone cards using qrgen, it does not require a list file:

```
% python3 qrgen.py --zones --hostname <IP of node-sonos-http-api host>
% open out/zones.html
```


Create Command cards using qrgen and the text file command_cards.txt:

```
% python3 qrgen.py --commands
% open out/commands.html
```


It'll look something like this:

<p align="center">
<img src="docs/images/sheet.jpg" width="50%" height="50%">
</p>



### 4. Start `qrplay`

On your Raspberry Pi, clone this `qrocodile` repo:

```
% git clone https://github.com/dernorberto/qrocodile
% cd qrocodile
```

Then, launch `qrplay`, specifying the hostname of the machine running `node-sonos-http-api`:

```
% python3 qrplay.py --hostname <IP of node-sonos-http-api host>
```

If you want to use your own `qrocodile` as a standalone thing (not attached to a monitor, etc), you'll want to set up your RPi to launch `qrplay` when the device boots:

```
% emacs ~/.config/lxsession/LXDE-pi/autostart
# Add an entry to launch `qrplay.py`, pipe the output to a log file, etc
```

## The Cards

Currently `qrgen` and `qrplay` have built-in support for five different kinds of cards: song, album, playlist, commands and zone cards

Song cards can be generated for tracks in your music library or from Spotify, and can be used to play just that song, add that song to the queue, or play the entire album. For example:

<p align="center">
<img src="docs/images/song.png" width="40%" height="40%" style="border: 1px #ddd solid;">
</p>

Command cards are used to control your Sonos system, performing actions like switching to a different room, activating the line-in input on a certain device, or pausing/playing the active device.  Here are the commands that are currently supported:

<p align="center">
<img src="docs/images/cmd-living.png" width="20%" height="20%" style="border: 1px #ddd solid;"> <img src="docs/images/cmd-dining.png" width="20%" height="20%" style="border: 1px #ddd solid;">
</p>

<p align="center">
<img src="docs/images/cmd-pause.png" width="20%" height="20%" style="border: 1px #ddd solid;"> <img src="docs/images/cmd-skip.png" width="20%" height="20%" style="border: 1px #ddd solid;">
</p>

<p align="center">
<img src="docs/images/cmd-songonly.png" width="20%" height="20%" style="border: 1px #ddd solid;"> <img src="docs/images/cmd-wholealbum.png" width="20%" height="20%" style="border: 1px #ddd solid;">
</p>

<p align="center">
<img src="docs/images/cmd-buildlist.png" width="20%" height="20%" style="border: 1px #ddd solid;"> <img src="docs/images/cmd-turntable.png" width="20%" height="20%" style="border: 1px #ddd solid;">
</p>

<p align="center">
<img src="docs/images/cmd-whatsong.png" width="20%" height="20%" style="border: 1px #ddd solid;"> <img src="docs/images/cmd-whatnext.png" width="20%" height="20%" style="border: 1px #ddd solid;">
</p>


## Acknowledgments

This project was a great inspiration to develop something that my kids can use. It was a relatively easy project because the groundwork was already laid down by chriscampbell and a series of other people.

Many thanks to the authors following libraries and tools:

* [qrocodile](https://github.com/chrispcampbell/qrocodile)
* [node-sonos-http-api](https://github.com/jishi/node-sonos-http-api)
* [spotipy](https://github.com/plamere/spotipy)

## License

`qrocodile` is released under an MIT license. See the LICENSE file for the full license.
