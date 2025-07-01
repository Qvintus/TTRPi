# TTRPi
Twitch To Rasperry Pi Integration
Made for Streamer.bot, for now

# Instructions - Rasperry Pi OS
1. Have python3 along with python3-dev, python3-setuptools and python3-pip installed
2. Get the python dependencies: pip install -r requirements.txt from the git
3. The streamer.bot C# code need to be configured<br/>
   IP should be set to your local LAN ip of the Raspberry Pi.<br/>
   Alternatively if you're running it non-locally (Not recommended), it should still work if there has been proper port forwarding.
5. Install C# code in streamer bot<br/>
   Example:<br/>
     Actions > TTRPi Integration<br/>
     Trigger > Core > Streamer.bot Started<br/>
     Sub-Actions > Core > C# > Execute C# Code
   ![image](https://github.com/user-attachments/assets/04a2da8f-6d3c-40bb-b349-ef2cbf8360c7)

   Make sure its Settings tab has "Precompile on Application Start"
   ![image](https://github.com/user-attachments/assets/f69046eb-1feb-473a-828f-1e451fcb2845)

7. There is an example Method for enable pin 1 inside the Code, do add or change as needed.
8. Add an Action and trigger that has sub-action Execute C# Method, select the C# method you wish to execute.
![image](https://github.com/user-attachments/assets/e31b85e8-9fa2-4b60-ac9e-6c313b461c9e)
