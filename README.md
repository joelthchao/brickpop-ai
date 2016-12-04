# brickpop-ai

Solver for Brick Pop game (Gamee) in FB messenger

------------------

##Usage

Define input as a text file. Use single digit number to represent different color block and 0 for empty block. Notice that line in file is actually column in game.


In python console:
```python
>>> from ai import play
>>> map_file = 'maps/map_easy.txt'
>>> play(map_file)
```
Output will suggest next step (`Step 1`) for you, the other future steps are for reference. Press enter to continue.
```
Loading map from maps/map_easy.txt and construct 10 x 10 map
0 0 0 0 0 0 0 0 3 3
0 0 0 0 3 0 0 4 3 4
3 0 6 0 3 0 0 1 3 4
3 3 6 0 4 3 1 4 1 4
3 1 1 0 3 3 1 4 1 4
2 2 2 2 4 4 5 3 5 6
2 2 2 4 1 4 6 3 6 6
6 2 2 1 4 1 6 3 5 6
6 6 6 6 6 6 1 1 5 6
1 2 2 3 6 6 6 6 5 5
--------------------
Best paths:
Step 1: (0, 1), loss: 7, score: 110.0
Step 2: (4, 3), loss: 6, score: 116.0
Step 3: (3, 1), loss: 5, score: 118.0
Step 4: (3, 1), loss: 4, score: 148.0
Step 5: (0, 1), loss: 3, score: 258.0
continue? n to exit.
```

------------------

# Algorithm

Here we implement an greedy search algorithm to generate moves. The loss is defined as "number of isolated block", also, we introduce game over penalty to prevent dead move. To earn more score, we add second priority loss "-score" for tie breaking.

------------------

# Configuration

In `config.py`, we define the params, `SEARCH_WIDTH` and `SEARCH_DEPTH`, to configure how algorithm perform search. Larger `SEARCH_WIDTH` will allow the algorithm more choices of move, and larger `SEARCH_DEPTH` help the algorithm to explore more steps forward. The two params heavily influence compute time, and default setting is good enough to win all the game.