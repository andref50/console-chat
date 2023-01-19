# console-chat 0.3.0

### Usage:

1) You need to install the pyfiglet module in order to run **run_server.py** script:  
<code>pip install pyfiglet</code>


2) To start the server:  
<code>python run_server.py xxx.xxx.xxx.xxx yyyy</code>, where:  
   <code>xxx.xxx.xxx.xxx</code>: host IP\
   <code>YYYY</code>: host port (integer).
   

### Tasks to-do:

- [x] Separate class responsabilities:
    - [x] detach update ui function of server class
- [ ] Divide classes into individual modules:
    - [x] UI
    - [ ] app.py (?)
- [ ] Implement communication between objects (app.py??)
- [ ] Implement client functionalities:
   - [ ] UI
- [ ] Implement interactive functionalities for the console (modules to test):
   - [ ] _cmd_ module
   - [ ] _ctypes_ module for terminal manipulation (cursor position, etc)
