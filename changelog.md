# Changelog


## [0.1.0]
###### 2023-01-17

- implements basic connection and message exchange functionalities
- implements server and client objects on server side
- implements basic UI functions


## [0.2.0]
###### 2023-01-18

- fixed server **"lost connection"** message
- added client **"can't reach host error"** message
- fixed minor bugs on both server and client side
- added UI module, now works on both client and server
- added
  utils/utils.py module, for functions used by UI module (separator)
  

## [0.3.0]
###### 2023-01-19

- new gui.py is the former ui.py module
- fixed modules paths
- added Logger class
- implemented logger object to log management on server side
- client/server now send JSON data


## [0.4.1]
###### 2023-01-20

- improved and simplified Logger class
- all information sent/received now are treated as and event by Logger class
- improved DataProtocol class, methods now works in a clearer way
- DataProtocol is now sftp (Simple Data Transfer Protocol)
- added types annotation and start docstringing

## [0.4.2]
###### 2023-01-21

- minor changes in annotation
- moved global variables and initializations to inside "if __main__" function
- added time to data structure

## [0.5.0]
###### 2023-01-28

- added an event handler model, now server can post an event, and event handler  
object take care of log, broadcast and ui update (so far).
- classes are now divided by responsabilities, follow the Model, View, Controller principle.