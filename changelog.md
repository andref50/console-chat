# Changelog


## [0.1.0]
######2023-01-17

- implements basic connection and message exchange functionalities
- implements server and client objects on server side
- implements basic UI functions


## [0.2.0]
######2023-01-18

- fixed server **"lost connection"** message
- added client **"can't reach host error"** message
- fixed minor bugs on both server and client side
- added UI module, now works on both client and server
- added
  utils/utils.py module, for functions used by UI module (separator)
  

## [0.3.0]
######2023-01-19

- new gui.py is the former ui.py module
- fixed modules paths
- added Logger class
- implemented logger object to log management on server side
- client/server now send JSON data