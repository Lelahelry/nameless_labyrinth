# Functional breakdown

## Program logic

- Players choose starting parameters
- Intitialisation of game state and objects
- Run game mainloop
  - orient tile
  - insert tile (and verify that move is allowed)
  - move pawn (and check validity)
  - check objectives completion and win conditions
  - give control to next player or end game
- Congratulate winner

## Data structures

### Treasure class

```py
@dataclass(frozen=True)
class Treasure:
    """Represents the treasures which the objectives of the players."""
    filepath: str # Path to .png texture file of the treasure.
    name: str
```

### Pawn class

```py
@dataclass
class Pawn:
    """Represents the pawns (assigned to players) and contains their lists of objectives."""
    color: str
    name: str
    objectives: list[Treasure]

    def current_objective(self):
        return self.objectives[0]

    def collect(self):
        self.objectives.pop(0)
```

### Tile class

```py
@dataclass
class Tile:
    """Represents the tiles that compose the labyrinth."""
    filepath: str # Path to .json file with init data.
    sides: list[bool] # Represents the open/closed nature of the four sides.
```

### FixedTile class

```py
@dataclass
class FixedTile(Tile):
    """These tiles are the ones that are fixed to the board and cannot move."""
    fixed_position: tuple[int, int]
    treasure: Treasure | None = None
    pawn: Pawn | None = None
```

### MovingTile class

```py
@dataclass
class MovingTile(Tile):
    """Tiles that can be moved by sliding and rotating."""
    treasure: Treasure | None = None
    pawn: Pawn | None = None

    def rotate_cw(self):
        """Rotates the tile clockwise."""
        pass
    
    def rotate_ccw(self):
        """Rotates the tile counterclockwise."""
        pass
```

### Board class

```py
@dataclass
class Board:
    """Represents the game board containing all tiles."""
    grid: dict[tuple[int, int], Tile] #(line, column)
    slideout_position: tuple[int, int] | None

    def __init__(self, fixed_tiles, moving_tiles):
        """
        Initializes the grid, then places base tiles according to their fixed positions, then randomly fills the rest of the grid with the moving tiles.
        """
        pass
        #create the empty grid
        #place fixed tiles (seperate method)
        #place random tiles (seperate method)
    
    def __getitem__(self, pos: tuple[int, int]):
        return self.grid[pos]
    
    def __setitem__(self, pos: tuple[int, int], tile: Tile):
        if isinstance(self.grid[pos], FixedTile):
            raise KeyError("You can't move fixed tiles!")
        elif pos == self.slideout_position:
            raise KeyError("You can't insert your tile at the same place it came from!")
        else:
            self.grid[pos] = tile
    
    def slide_tile(self, insertpos: tuple[int, int], tile: Tile) -> Tile:
        """
        Updates the grid according to the line or column pushed by the player. 
        inputs: tuple(position of new tile) and new tile 
        returns: tile pushed out
        """
        pass
    
    def get_pawn_position(self, pawn) -> tuple[int, int]:
        pass
```

### Game class
```py
@dataclass
class Game:
    """Encapsulates all data related to an individual game's state and manages game flow."""
    queue: list[Pawn] # Rotating queue for playing order
    board: Board
    hand: MovingTile # Tile that last slid out of the board, returned by Board.slide_tile method

    def __init__(self, datapath: str, playernames: list[str]):
        pass
        #load treasures+declaration
        #load tiles+declaration
        #board creation
        #place pawns and give them names
        #distribute treasures
    
    def move_pawn(self, pawn, newpos):
        '''return updated grid+boolean on managed motion'''
        pass
        #get_pawn_position
        #check destination is reached
        #update pawn position or display error message or else 

    def turn(self, player):
        pass
        '''return player and boolean'''
        #tile choice
        #slide_tile
        #move_pawn
        #check a treasure was found
            #check the player has won 
    def start(self):
        #while player didn't win won
            #change player
            #turn
            

```

## GUI

- Start menu & game init
- Game board display
- Game state display
- Game control interface

## Test sets
- rotation
- slide tiles
- get pawn position