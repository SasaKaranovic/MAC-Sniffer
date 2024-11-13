import board
import busio
import digitalio
import adafruit_connection_manager
import adafruit_requests
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K, SNMR_UDP

class SKEthernet:
    def __init__(self, spi_bus):
        print("Setting up ethernet...")
        cs = digitalio.DigitalInOut(board.GP17)
        self.spi_bus = spi_bus
        self.socket = None
        self.last_mac = ""
        self.mac_waiting = False
        
        self.DHCP_SERVER_PORT = 67
        self.MAC_START = 36
        self.MAC_END = 42

        # Setup your network configuration below
        self.IP_ADDRESS = (192, 168, 0, 1)
        self.SUBNET_MASK = (255, 255, 0, 0)
        self.GATEWAY_ADDRESS = (192, 168, 0, 1)
        self.DNS_SERVER = (8, 8, 8, 8)

        # Initialize ethernet interface with DHCP
        self.eth = WIZNET5K(self.spi_bus, cs, is_dhcp=False)

        # Set network configuration
        self.eth.ifconfig = (self.IP_ADDRESS, self.SUBNET_MASK, self.GATEWAY_ADDRESS, self.DNS_SERVER)

        print("Chip Version:", self.eth.chip)
        print("MAC Address:", [hex(i) for i in self.eth.mac_address])
        print("My IP address is:", self.eth.pretty_ip(self.eth.ip_address))
    
    def get_last_mac(self):
        return self.last_mac
    
    def mark_as_read(self):
        self.mac_waiting = False
    
    def reset_socket(self):
        try:
            self.eth.socket_close(self.socket)
            self.socket = None
        except:
            pass

    def setup_socket(self):
        try:
            if self.socket is None:
                self.socket = self.eth.get_socket()
                self.eth.socket_listen(self.socket, self.DHCP_SERVER_PORT, SNMR_UDP)
                print("Listening for DHCP request on UDP port:", self.DHCP_SERVER_PORT)
            return True
        except:
            self.reset_socket()
            return False
    
    def tick(self):
        # Check if ETH is connected
        if not self.eth.link_status:
            # Ethernet is down, close socket
            self.reset_socket()
            return -1
        
        # Setup socket if necessary
        if not self.setup_socket():
            print("Failed to open socket")
            return -2
        
        # Check if socket has data
        len = self.eth.socket_available(self.socket)
        if len > 0:
            len, data = self.eth.socket_read(self.socket, len)
            self.last_mac = ":".join("%02X" % b for b in data[self.MAC_START:self.MAC_END])
            print("Device MAC:", self.last_mac)
            self.mac_waiting = True
            return 1
        return 0
