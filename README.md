# point-to-point

A simple game for two that can test your typing speed

![image](https://github.com/user-attachments/assets/0d714291-afa8-4699-952f-27fe1c5dee9f) | ![image](https://github.com/user-attachments/assets/81b15c5b-f0e9-400c-96c4-74988c90d87a)
:----------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------:

## ✨ Features

- Server and client interaction
- Constant stable connection
- Saving text for typing

## 🎲 How to play

There are two players: a server and a client.

The server presses the "Server" and "Open connection" buttons.
Under the buttons in the server menu there are host and port values.
The server must give these two parameters to the client.
The server has the ability to choose what text will be typed during the game.
To do this, the server presses the "Settings" button and writes the text in a special window.
The text is automatically saved when the "Back" button is pressed.

The client presses the "Client" button and writes the host and port received from the server in the available edit lines.
Then the client presses the "Connect" button.

After a successful connection, both can press the "Play" button to start playing.

## 🚀 Launch

### Windows

Download zip archive and unzip it. Run .exe (antivirus may complain).

### Linux

Run these commands

    git clone git@github.com:FSK-idk/point-to-point.git
    cd point-to-point
    ./scripts/build.sh
    ./scripts/run.sh

