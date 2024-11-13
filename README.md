# MAC Sniffer

## What is this project about?

[![MAC Sniffer](http://img.youtube.com/vi/tu_N1xqSLxA/0.jpg)](http://www.youtube.com/watch?v=tu_N1xqSLxA "MAC Sniffer")


In the above video you will learn what is a MAC Sniffer, why I built it and how you can build your own.

If you are looking for a TL;DR version: It is a simple stand-alone tool used to read network equipment MAC address and display it on screen as text and a QR code. And it can also work with devices that don't even have an OS installed.

If you find this video/project useful, I would really love to hear from you.
<br/><br/>

## Can I buy one?

No. But you can easily build your own. :)
<br/><br/>

## Can I build my own?

Yes! It is super simple and uses only off-the-shelf parts.

You will need

- [Wiznet W5500-EVB-Pico](https://docs.wiznet.io/Product/iEthernet/W5500/w5500-evb-pico) development board
- 1.69" 240x280 ST7789V2 Display Module ([Seeed Studio](https://www.seeedstudio.com/1-69inch-240-280-Resolution-IPS-LCD-Display-Module-p-5755.html),  [Waveshare](https://www.waveshare.com/1.69inch-lcd-module.htm))
<br/><br/>

### 1. Prepare the development board (Install Circuit Python)

1. Place the development board into bootloader mode (hold `BOOTSEL` button and then connect USB cable.
2. Pico2040 will report as a new USB drive
3. Copy `adafruit-circuitpython-wiznet_w5500_evb_pico-en_US-9.1.4.uf2` file from the firmware folder to the Pico2040
4. The board will reload and new `CIRCUITPY` drive will appear


### 2. Setup Python code

1. Copy all files from `pico_content` folder to root of your `CIRCUITPY` drive
2. Power cycle the board


### 3. Wire the display

Follow the below table to connect your display to the Pico2040

| Display       | Pico2040      |
| ------------- | ------------- |
| VCC           | 3V3           |
| GND           | GND           |
| DIN           | GP19          |
| CLK           | GP18          |
| CS            | GP22          |
| DC            | GP26          |
| RST           | GP27          |
| BL            | GP28          |


<br><br>

## Useful links

Blog page: https://sasakaranovic.com/projects/mac-sniffer/

YouTube video: http://www.youtube.com/watch?v=tu_N1xqSLxA


<br/><br/>

#### Sasa Karanovic

<a href="https://sasakaranovic.com/" target="_blank" title="Sasa Karanovic Home Page"><img src="https://raw.githubusercontent.com/SasaKaranovic/common/master/assets/img_home.png" width="16"> Home Page</a> &nbsp;&middot;&nbsp;
<a href="https://youtube.com/c/sasakaranovic" target="_blank" title="Sasa Karanovic on YouTube"><img src="https://raw.githubusercontent.com/SasaKaranovic/common/master/assets/img_youtube.png" width="16"> YouTube</a> &nbsp;&middot;&nbsp;
<a href="https://github.com/sasakaranovic" target="_blank" title="Sasa Karanovic on GitHub"><img src="https://raw.githubusercontent.com/SasaKaranovic/common/master/assets/img_github.png" width="16"> GitHub</a> &nbsp;&middot;&nbsp;
<a href="https://twitter.com/_sasakaranovic_" target="_blank" title="Sasa Karanovic on Twitter"><img src="https://raw.githubusercontent.com/SasaKaranovic/common/master/assets/img_twitter.png" width="16"> Twitter</a> &nbsp;&middot;&nbsp;
<a href="https://instagram.com/_sasakaranovic_" target="_blank" title="Sasa Karanovic on Instagram"><img src="https://raw.githubusercontent.com/SasaKaranovic/common/master/assets/img_instagram.png" width="16"> Instagram</a> &nbsp;&middot;&nbsp;
<a href="https://github.com/sponsors/SasaKaranovic" target="_blank" title="Sponsor on GitHub"><img src="https://raw.githubusercontent.com/SasaKaranovic/common/master/assets/img_github.png" width="16"> Sponsor on GitHub</a>
