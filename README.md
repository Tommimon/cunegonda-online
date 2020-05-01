# Cunegonda-online
"Cunegonda" is an online strategic card game for 4 players. The main reason for his success is his clever and planned nature, nobody is safe and a small mistake can cause huge losses.

'Cunegonda' is an individual game but, as for everything, teaming is natural, if you are winning expect 3 other players against you, if you are losing you have plenty of chances to climb back up if you play your cards correctly. Everybody can overturn the standings, you can pass from first to last and back again to first in a matter of few rounds, the game is over only when the 10th round finishes.

*Habet etiam mala fortuna levitatem. Fortasse erit, fortasse non erit*

# Installation
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

# Setup
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



# _Rules_

## Introduction
A match is 10 rounds long.
The player with the highest score at the end of the 10th round wins.

## Pre-game
At the beginning of the round each player has 13 cards.
Before the start of the round each player has to select 3 cards from his deck that will be passed to the player on his right.

## Round developement
The first player choses a card to play, the game develops in a clockwise turn. Whoever wins the hand will start the next round.

All the players must play a card of the same suit as the card played (i.e. if the first played card is a diamond everyone must play a diamond).
If a playes does not have a card of the same suit as the first he can play whichever card he wants.

The first cards commands the suit, whoever played the highest card in that suit wins the hand.

The round ends when each player plays his last card (each round has 13 hands).

## Scoring
Each hand won adds 10 points to the winner's total regardless of the cards he gets.

-Hearts- are the point-removing suit, if a player wins a hand with some hearts he has to subtract to the 10 points for winning the hand the corresponding value of the card.
(i.e. K = -13 points, J = -11 points, 7 = -7 points,...)

The Queen of Spades is a special card since his value is -26 points (negative 26)

BUT if a player manages to have ALL the hearts and the Queen of Spades at the end of the round he will get +60 points and all of the other players will get -20 points for that round.


