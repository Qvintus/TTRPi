import configparser
import socket
import time
import json
import RPi.GPIO as GPIO

#Config parser
config = configparser.ConfigParser()
config.read('config.ini')

#Socket
SERVER_IP       = config.get('Socket', 'ip')
SERVER_PORT     = int(config.get('Socket', 'port'))

SOCKET_TIMEOUT  = 1.0 #Seconds float - to allow for application interrupt


class TTRPi:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP based socket
    
    
    # Setup UDP SOCKET Server
    def init_udp_server(self):
        print("TTRPi: Starting listening server...")
        try:
            self.socket.bind((SERVER_IP, SERVER_PORT))
            self.socket.settimeout(SOCKET_TIMEOUT)
            
            print("TTRPi: success running at: ", SERVER_IP, ":", SERVER_PORT)
        except Exception as e:
            print("ERROR: [init_udp_server]: ", e)
    
    # Handle packages from bot as JSON objects
    def handle_UDP_package(self, data):
        try:
            payload = json.loads(data.decode())
            print("JSON payload from Bot: ", payload)
            
            # Validate required keys
            for key in ('mode', 'pin', 'power', 'isOutput'):
                if key not in payload:
                    print(f"ERROR: Missing key '{key}' in payload")
                    return
            
            # Otherwise setup variables from JSON
            mode     = payload["mode"]
            pin      = payload["pin"]
            power    = payload["power"]
            isOutput = payload["isOutput"]
            
            #Set GPIO Mode
            if mode == 1:
                GPIO.setmode(GPIO.BOARD)
            elif mode == 2:
                GPIO.setmode(GPIO.BCM)
            else:
                print("ERROR: [handle_UDP_package]: Invalid GPIO MODE: ", mode, " Excepted 1 or 2 ~ BOARD or BCM")
                return
            
            #Set GPIO pin/channel as either Output or Input
            if isOutput:
                GPIO.setup(pin, GPIO.OUT)
                
                #Set GPIO pin power
                if power == 1:
                    GPIO.output(pin, GPIO.LOW)
                elif power == 2:
                    GPIO.output(pin, GPIO.HIGH)
                    
            elif not isOutput:
                GPIO.setup(pin, GPIO.IN)

            print("TTRPi running - CTRL + C to kill")
        except json.JSONDecodeError:
            print("ERROR: [handle_UDP_package]: Invalid JSON received")
        except Exception as e:
            print("ERROR: [handle_UDP_package]: ", e)
    
    # We waiting for a package from Bot
    def wait_for_package(self):
        try:
            data, addr = self.socket.recvfrom(1024)
            self.handle_UDP_package(data)
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print("ERROR: [check_for_package]: ", e)
    
    # Close socket binding correctly
    def close(self):
        try:
            self.socket.close()
            print("TTRPi: Server closed...") 
        except Exception as e:
            print("ERROR: [close]: ", e)
    
    #Start TTRPi
    def start(self):
        try:
            self.init_udp_server()
            print("TTRPi: Running...")
        except Exception as e:
            print("ERROR: ", e)
        

def run():
    server = TTRPi()
    server.start()
    
    #Keep server running until interrupted
    try:
        print("TTRPi running - CTRL + C to kill")
        while True:
            server.wait_for_package()
            time.sleep(1)
    except KeyboardInterrupt:
        print("TTRPi: Closing...") 
    finally:
        server.close()
    
if __name__ == "__main__":
    run()

