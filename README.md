# Arduino Serial Audio Player

A simple project that streams audio from a computer to an Arduino Uno
over a serial connection and reproduces it using PWM output.

The project explores audio playback on an Arduino Uno without dedicated
audio hardware, DACs, or amplifier modules.

## Features

-   Serial audio streaming from a PC
-   MP3, WAV, OGG and FLAC support
-   Automatic Arduino port detection
-   Stereo to mono conversion
-   8 kHz resampling
-   Bridge mode output
-   Dual bridge mode support

## Requirements

### Hardware

-   Arduino Uno
-   One or two speaker drivers
-   USB cable
-   Computer running Python

### Software

-   Python 3.10+
-   pyserial
-   miniaudio
-   numpy

Install dependencies:

``` bash
pip install pyserial miniaudio numpy
```

## Usage

Upload one of the Arduino sketches.

Run:

``` bash
python play.py song.mp3 COM3
```

or

``` bash
python play.py song.mp3
```

## Wiring

### Bridge Mode

``` text
Speaker terminal 1 -> Pin 9
Speaker terminal 2 -> Pin 10
```

Do not connect the speaker to GND.

### Dual Bridge Mode

dual bridge is only meant for experimental purposes use it for less then two 3 inch or >4 OHM drivers if not then it can cause stress to IO pins leading to damage of it 

``` text
Speaker 1:
Pin 9  <-> Speaker <-> Pin 10

Speaker 2:
Pin 3  <-> Speaker <-> Pin 11
```

Neither speaker should be connected to GND.

## Technical Notes

Audio is decoded on the host computer, converted to unsigned 8-bit PCM,
and streamed to the Arduino over a serial connection. The Arduino
reproduces the samples using high-frequency PWM.

This project is intended as an experiment and learning exercise rather
than a replacement for dedicated audio hardware.

## Limitations

-   Mono playback
-   Limited bass response
-   Audible distortion at higher volumes
-   Quality depends on speaker characteristics
-   Constrained by serial bandwidth and PWM output

## Future Improvements

-   Buffered playback
-   Higher quality resampling
-   SD card playback
-   Better filtering
-   Stereo playback

## License

Released for educational and experimental use.

## Developer note 
feel free to use this and if you some how improve the audio quality i would love to hear it , at the end this was made for only fun i know there are better ways to play audio using arduino but how cool is arduino streaming music over the serial.
