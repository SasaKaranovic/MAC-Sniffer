import board
from skdisplay import SKDisplay
from sketh import SKEthernet

print("------")
print("MAC Sniffer v0.1")
print("https://github.com/SasaKaranovic/MAC-Sniffer")
print("------")

# Setup SPI bus
spi_bus = board.SPI()

display = SKDisplay(spi_bus)
display.clear()
display.show_text(37, 120, "Setting up...", scale=1)
display.backlight(True)
eth = SKEthernet(spi_bus)

state = 0

while True:
    eth_state = eth.tick()
    
    if eth_state != state:
        if eth_state == -1:
            display.clear()
            display.show_text(37, 120, "Waiting for eth...", scale=1)

        elif eth_state == 0:
            if state != 1:
                display.clear()
                display.show_text(37, 120, "Listening...")

        elif eth_state == 1:
            if state != 1:
                mac = eth.get_last_mac()
                display.clear()
                display.show_qr_and_text(mac)
       
        state = eth_state
