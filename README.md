# point-to-point

A simple game for two that can test your typing speed

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

Run this commands

    ./scripts/build.sh
    ./scripts/run.sh

