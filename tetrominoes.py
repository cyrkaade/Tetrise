from __future__ import print_function
from collections import namedtuple

X, O = 'X', None
Tetromino = namedtuple("Tetrimino", "name color shape")

list_of_tetrominoes = [
    Tetromino(name="long",
              color="blue",
              shape=((O,O,O,O),
                     (X,X,X,X),
                     (O,O,O,O),
                     (O,O,O,O))),
    Tetromino(name="square",
              color="yellow",
              shape=((X,X),
                     (X,X))),
    Tetromino(name="hat",
              color="pink",
              shape=((O,X,O),
                     (X,X,X),
                     (O,O,O))),
    Tetromino(name="right_snake",
              color="green",
              shape=((O,X,X),
                     (X,X,O),
                     (O,O,O))),
    Tetromino(name="left_snake",
              color="red",
              shape=((X,X,O),
                     (O,X,X),
                     (O,O,O))),
    Tetromino(name="left_gun",
              color="cyan",
              shape=((X,O,O),
                     (X,X,X),
                     (O,O,O))),
    Tetromino(name="right_gun",
              color="orange",
              shape=((O,O,X),
                     (X,X,X),
                     (O,O,O)))
    ]

def rotate(shape, times=1):
    return shape if times == 0 else rotate(tuple(zip(*shape[::-1])), times-1)


def shape_str(shape):
    return '\n'.join(''.join(map({'X': 'X', None: 'O'}.get, line))
                     for line in shape)

def shape(shape):
    print(shape_str(shape))
