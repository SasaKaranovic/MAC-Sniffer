import time
import board
import digitalio
import terminalio
import displayio
import adafruit_miniqr
from fourwire import FourWire
from adafruit_display_text import label
from adafruit_st7789 import ST7789

class SKDisplay:
    def __init__(self, spi):
        self.display_width = 280
        self.display_height = 240
        self.display_rotation = 90
        
        # Setup backlight
        self.pin_bl = digitalio.DigitalInOut(board.GP28)
        self.pin_bl.direction = digitalio.Direction.OUTPUT
        self.pin_bl.value = False
        
        displayio.release_displays()

        self.spi = spi
        tft_cs = board.GP22
        tft_dc = board.GP26
        tft_reset = board.GP27
        
        self.display_bus = FourWire(self.spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset)
        self.display = ST7789(self.display_bus, width=self.display_width, height=self.display_height, rowstart=20, rotation=90)
        
        # Display resources
        self.splash = displayio.Group()
        self.display.root_group = self.splash

    def clear(self, color=0x000000):
        try:
            for i in range(0, 10):
                self.splash.pop(i)
        except:
            pass
        color_bitmap = displayio.Bitmap(self.display_width, self.display_height, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = color

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        self.splash.append(bg_sprite)
    
    def show_text(self, x, y, text, scale=2, color=0xFFFF00):
        # Draw a label
        text_group = displayio.Group(scale=2, x=x, y=y)
        text_area = label.Label(terminalio.FONT, text=text, color=color)
        text_group.append(text_area)  # Subgroup for text scaling
        self.splash.append(text_group)
    
    def backlight(self, enable):
        self.pin_bl.value = enable

    def test(self):
        # Make the display context
        splash = displayio.Group()
        self.display.root_group = splash
        color_bitmap = displayio.Bitmap(self.display_width, 240, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0x00FF00  # Bright Green

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)

        # Draw a smaller inner rectangle
        inner_bitmap = displayio.Bitmap(240, 200, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0xAA0088  # Purple
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
        splash.append(inner_sprite)

        # Draw a label
        text_group = displayio.Group(scale=2, x=37, y=120)
        text = "f4:12:fa:27:6c:60"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
        text_group.append(text_area)  # Subgroup for text scaling
        splash.append(text_group)

    def show_qr_and_text(self, data):
        # generate the 1-pixel-per-bit bitmap
        qr_bitmap = self.qr_to_bitmap(data)
        # We'll draw with a classic black/white palette
        palette = displayio.Palette(2)
        palette[0] = 0xFFFFFF
        palette[1] = 0x000000

        # scale = 3
        scale = min(
            self.display.width // qr_bitmap.width, (self.display.height - 50) // qr_bitmap.height
        )

        # QR at the bottom
        pos_x = int(((self.display.width / scale) - qr_bitmap.width) / 2)
        pos_y = int(((self.display.height / scale) - qr_bitmap.height))
        qr_img = displayio.TileGrid(qr_bitmap, pixel_shader=palette, x=pos_x, y=pos_y)

        qr_group = displayio.Group(scale=scale)
        qr_group.append(qr_img)
        self.splash.append(qr_group)

        # Add text
        # Draw a label
        text_area = label.Label(terminalio.FONT, text=data, color=0xFFFF00)
        text_scale = 2
        text_width = text_area.width * text_scale
        text_height = text_area.height * text_scale
        pos_x = int((self.display.width - text_width) /2 )
        pos_y = 20
        text_group = displayio.Group(scale=text_scale, x=pos_x, y=pos_y)
        text_group.append(text_area)  # Subgroup for text scaling
        self.splash.append(text_group)


    def show_qr(self, data):
        # generate the 1-pixel-per-bit bitmap
        qr_bitmap = self.qr_to_bitmap(data)
        # We'll draw with a classic black/white palette
        palette = displayio.Palette(2)
        palette[0] = 0xFFFFFF
        palette[1] = 0x000000

        # scale = 3
        scale = min(
            self.display.width // qr_bitmap.width, self.display.height // qr_bitmap.height
        )

        # then center it!
        pos_x = int(((self.display.width / scale) - qr_bitmap.width) / 2)
        pos_y = int(((self.display.height / scale) - qr_bitmap.height) / 2)
        qr_img = displayio.TileGrid(qr_bitmap, pixel_shader=palette, x=pos_x, y=pos_y)

        qr_group = displayio.Group(scale=scale)
        qr_group.append(qr_img)
        self.splash.append(qr_group)



    def qr_to_bitmap(self, data):
        qr = adafruit_miniqr.QRCode()
        qr.add_data(data)
        qr.make()

        # monochome (2 color) palette
        BORDER_PIXELS = 2

        # bitmap the size of the screen, monochrome (2 colors)
        bitmap = displayio.Bitmap(
            qr.matrix.width + 2 * BORDER_PIXELS, qr.matrix.height + 2 * BORDER_PIXELS, 2
        )
        # raster the QR code
        for y in range(qr.matrix.height):  # each scanline in the height
            for x in range(qr.matrix.width):
                if qr.matrix[x, y]:
                    bitmap[x + BORDER_PIXELS, y + BORDER_PIXELS] = 1
                else:
                    bitmap[x + BORDER_PIXELS, y + BORDER_PIXELS] = 0
        return bitmap
