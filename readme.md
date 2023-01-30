# console-chat 0.5.0

Console chat is a chat app that runs on terminal. The app has 2 scripts: the run_server.py, which hosts the chat room, and the run_client.py script (that runs on a different terminal instance), which join the chat room and allow sending and receive text messages.  
<br>
The server can hold an unlimited number of clients, and have a basic UI to monitor events.  
Clients can send and receive simple text messages, with a basic UI that will be improved.

### Usage:
To start the server:  
    <code>python run_server.py xxx.xxx.xxx.xxx yyyy</code> or  
    <code>python run_client.py xxx.xxx.xxx.xxx yyyy</code>, where:  
    <code>xxx.xxx.xxx.xxx</code>: host IP,     <code>YYYY</code>: host port (integer).


### Tasks to-do:
- Implement interactive functionalities for the console (modules to test):
   - _cmd_ module
   - _ctypes_ module for terminal manipulation (cursor position, etc)
