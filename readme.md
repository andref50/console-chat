# console-chat 0.4.2

Console chat is a chat app that runs on terminal (as the name implies). The app is divided in 2 parts: a server script, a script that hosts the chat room, and a client script (to run on different terminal instance) to join and interact with the server and other clients.  
<br>
At the moment the server can hold an unlimited number of clients, and have a basic UI to monitor activity: a list of clients with their names, IP and port, and a event log and message log area.  
Clients can send and receive simple text messages, with a basic UI that will be improved.

### Usage:

1) You need to install the pyfiglet module in order to run **run_server.py** script:  
<code>pip install pyfiglet</code>


2) To start the server:  
    <code>python run_server.py xxx.xxx.xxx.xxx yyyy</code> or  
    <code>python run_client.py xxx.xxx.xxx.xxx yyyy</code>, where:  
    <code>xxx.xxx.xxx.xxx</code>: host IP  
    <code>YYYY</code>: host port (integer).
   

### Tasks to-do:

- [ ] Implement client functionalities:
   - [ ] UI
- [ ] Implement interactive functionalities for the console (modules to test):
   - [ ] _cmd_ module
   - [ ] _ctypes_ module for terminal manipulation (cursor position, etc)
