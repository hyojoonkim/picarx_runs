# Code Snippets For Running The PiCarX 

## Reference code from SunFounder
- Main examples: [https://github.com/sunfounder/picar-x/tree/v2.0](https://github.com/sunfounder/picar-x/tree/v2.0)
- Backend code: [https://github.com/sunfounder/robot-hat](https://github.com/sunfounder/robot-hat)

## How to run
1. At the server that will **send** commands, start a server instance. The server instance will listen to TCP port 9999.
    ```
    $ git clone https://github.com/hyojoonkim/picarx_runs.git
    $ cd picarx_run
    $ python3 server-command.py
    ```    
1. At the PiCarX that will **receive** commands, start the client. The client will make a TCP connection to the given IP address, default port 9999. In this example, the server IP address is 10.250.250.10
    ```
    $ git clone https://github.com/hyojoonkim/picarx_runs.git
    $ cd picarx_run
    $ python3 client-car.py 10.250.250.10
    ```
1. At the server, you will see that a client has connected. For example,
    ```
    Got a connection from ('10.250.254.236', 42780)
    Enter command (f <duration>, b <duration>, speed <amount>, linetrack):
    ```
    Now you can start entering commands.
    
## Commands
- Forward for X seconds: `f X`
    - Default X is 0, meaning never stop.
- Backward for X seconds: `b X`
    - Default X is 0, meaning never stop. 
- Set speed to power X: `speed X`
    - Default X is 10. 
- Start black linetracking for X seconds : `linetrack X`
    - Default X is 0, meaning never stop **until** the car detects an end of black line. 
