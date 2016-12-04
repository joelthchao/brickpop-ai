# brickpop-ai

Solver for Brick Pop game (Gamee) in FB messenger

------------------

##Usage

Define input as a text file. Use single digit number to represent different color block and 0 for empty block. Notice that line in file is actually column in game.


```
# map_easy.txt
1662233300
2622213000
2622216600
3614200000
6641434330
6614433000
6166511000
6133344140
5556511333
5666644443
```

```python
from ai import play
map_file = 'maps/map_easy.txt'
play(map_file)
```

------------------

# Algorithm

Here we implement an greedy search algorithm to generate moves. The loss is defined as "number of isolated block", also, we introduce game over penalty to prevent dead move. To earn more score, we add second priority loss "-score" for tie breaking.

------------------

# Configuration

In `config.py`, we define the params, `SEARCH_WIDTH` and `SEARCH_DEPTH`, to configure how algorithm perform search. Larger `SEARCH_WIDTH` will allow the algorithm more choices of move, and larger `SEARCH_DEPTH` help the algorithm to explore more steps forward. The two params heavily influence compute time, and default setting is good enough to win all the game.