# cunegonda-online
"Cunegonda" is an online strategic card game for 4 players. The main reason for his success is his clever and planned nature, nobody is safe and a small mistake can cause huge losses.

'Cunegonda' is an individual game but, as for everything, teaming is natural, if you are winning expect 3 other players against you, if you are losing you have plenty of chances to climb back up if you play your cards correctly. Everybody can overturn the standings, you can pass from first to last and back again to first in a matter of few rounds, the game is over only when the 10th round finishes.

*Habet etiam mala fortuna levitatem. Fortasse erit, fortasse non erit*

## Installation
### windows or linux
Download the right version for your OS from the release section, extract the files where ever you want and you're good to go.

To join a match run the ``launcher`` executable.
To host a match run the ``host`` executable.

### mac OS
Currently, we don't provide any mac one file executable so installation for mac is a bit trickier.

First install [Python](https://www.python.org/downloads/) on your computer.

Then you need to install pygame and varname:

```sh
pip3 install pygame
pip3 install varname
```

Now download the raw_client_code or raw_server_code from the release section and extract the files somewhere.
To join a match run the module ``launcher.py``
To host a match run the module ``host.py``
You can run the python modules by navigating to the directory where you extracted the files and executing the command:
```sh
python3 -m launcher.py
```
or
```sh
python3 -m host.py
```

## Setup
All you need to play this game is:
- one machine with public IP address running the ``host`` process
- 4 players running the ``launcher`` program

### Server setup
In ``server_settings.txt``:
Edit the server IP address (you may need the LAN address) and the port you wish to open the host process on

### Client setup
In ``client_settings.txt``:
Edit the server IP address (has to be the public address) and the public port you are connecting to

You can change other settings about the GUI in this file
