using System;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;

public class CPHInline
{
    private string RPi_IP 		 = "127.0.0.1"; // Set this as Raspberry  Pi IP | dont forget ;
    private int RPi_PORT 		 = 3000; //Set this as Raspberry Pi Port | dont forget ;
    
    
    public enum GPIO {
		LOW = 1,
		HIGH = 2,
		BOARD = 1,
		BCM = 2
    }
    
    public void RPi_GPIO_CALL(GPIO mode, int pin, GPIO power, bool isOutput) {
		try {
        	
        	using (UdpClient client = new UdpClient()) {
        		
        		var payload  = new {
					mode 	 = (int)mode,
					pin		 = pin,
					power 	 = (int)power,
					isOutput = (bool)isOutput
        		};
        		
        		string json = JsonSerializer.Serialize(payload);
        		byte[] sendBytes = Encoding.UTF8.GetBytes(json);
				
				int bytesSent = client.Send(sendBytes, sendBytes.Length, RPi_IP, RPi_PORT);
			}
		} catch (Exception e) {
			Console.WriteLine($"Error sending UDP packet: {e.Message}");
		}
	}
    
    public bool RPi_GPIO_Example_Pin1() {
		RPi_GPIO_CALL(GPIO.BOARD, 1, GPIO.HIGH, true);
        return true;
    }

}