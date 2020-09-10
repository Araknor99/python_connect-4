# A simple connect 4

#### DISCLAIMER: This program might not work with different Python versions!
####             It has been tested in Python 3.8.2 on Ubuntu Linux.


![The game](/game.png)
_The game. The green circles indicate where the player can drop a stone._

This is a simple python connect 4 I made for an assignment in school.
The graphical user interface is done with the turtle, because my resources were limited.
Two players can play this game remotely, as long as they are in the same network.

---

That aside, this game was put together hastily and as such does have flaws in ux design and maybe even functionality.
Flaws:
 - UI is in german!
 - The GUI uses the turtle.
 - Input and Output (e.g. for connecting to another player) use the terminal.
 - The netcode is not async-proof: If one client desyncs then the game is effectively ruined.
   - This could be improved by improving the feedback given by the other client.
 - The program cannot handle a deconnect of the other client and will crash on the next turn.
 - The color assignment is hardcoded; instead the starting player is assigned randomly.
 - Also the programs exits instead of re-looping if it cannot connect.

---

 #### I might improve this program, I might not.
 Alas, nothing is guaranteed.
