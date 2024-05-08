# Minimax Algorithm with alpha-beta pruning implementation for the game of Gomoku 

This project implements an AI player to play Gomoku on a reduced size board (10 x 10). 

## About Gomoku
Gomoku is similar in principle to the games Connect-Four or Tic-Tac-Toe. Besides the number of checkers required to form a line to win, the differences between Gomoku and the Connect-Four is that you can place your checker anywhere on the Gomoku board instead of stacking them. Compared to Tic-Tac-Toe, Gomoku has a larger board size and you need to make a line of 5 checkers instead of 3 to win.

## Algorithm

This project contains four python scripts: gomoku.py, process.py, main.py and run.py. The first two scripts handle the actual gameplay, either against another human player (initialized as an object of the Player class) or against a dummy (RandomPlayer class). The main.py implements the AIPlayer class and the core algorithm; an implementation of the minimax algorithm with alpha beta pruning. The penalty and reward policy is custom, and can be improved. The last script is just used to run the game, by initializing the 2 players needed.

More information about the minimax algorithm can be found [here](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning).

## Run Example

### 1) Intialize two players:

```
>>>joe = Player('X')
>>>dummy = AIPlayer('O')
```
  
### 2) Start the game:

```
>>>gomoku(joe, dummy)
```

```
Welcome to Gomoku!

| | | | | | | | | | | 0
| | | | | | | | | | | 1
| | | | | | | | | | | 2
| | | | | | | | | | | 3
| | | | | | | | | | | 4
| | | | | | | | | | | 5
| | | | | | | | | | | 6
| | | | | | | | | | | 7
| | | | | | | | | | | 8
| | | | | | | | | | | 9
-----------------------
 0 1 2 3 4 5 6 7 8 9

Player: X's turn
Enter a position: 
```

### 3) Joe inputs the coordinates of first move: 4 5 (input row and column is separated by whitespace.)
Dummy puts its checker "O" randomly at 6 5

```
Enter a position: 4 5

| | | | | | | | | | | 0
| | | | | | | | | | | 1
| | | | | | | | | | | 2
| | | | | | | | | | | 3
| | | | | |X| | | | | 4
| | | | | | | | | | | 5
| | | | | | | | | | | 6
| | | | | | | | | | | 7
| | | | | | | | | | | 8
| | | | | | | | | | | 9
-----------------------
 0 1 2 3 4 5 6 7 8 9
```

```
Player: O's turn

| | | | | | | | | | | 0
| | | | | | | | | | | 1
| | | | | | | | | | | 2
| | | | | | | | | | | 3
| | | | | |X| | | | | 4
| | | | | | | | | | | 5
| | | | | |O| | | | | 6
| | | | | | | | | | | 7
| | | | | | | | | | | 8
| | | | | | | | | | | 9
-----------------------
 0 1 2 3 4 5 6 7 8 9

```

```
Player: X's turn

Enter a position: 
```

### 4) Joe and Dummy place their checkers until there is a winner or the board is full (tie).

Example of end of game:  

```
Player: X wins in 5 moves.
Congratulations!
| | | | | | | | | | | 0
| | | | | | |O| | | | 1
| | | | | | | | | | | 2
| | | | | | | | | | | 3
| | | |X|X|X|X|X| | | 4
| | | | | | |O| | | | 5
| | | | | |O| | | | | 6
| | | |O| | | | | | | 7
| | | | | | | | | | | 8
| | | | | | | | | | | 9
-----------------------
 0 1 2 3 4 5 6 7 8 9
 ```
