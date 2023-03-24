from dataclasses import dataclass
import json

@dataclass(frozen=True)
class Treasure:
    """Represents the treasures and treasure objectives of the game."""
    filepath: str # Path to .png texture file of the treasure.
    name: str

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

@dataclass
class Tile:
    """Represents the tiles that compose the labyrinth."""
    filepath: str # Path to .json file with init data.
    sides: list[bool] # Represents the open/closed nature of the four sides.
    orientation: int = 0

@dataclass
class FixedTile(Tile):
    """These tiles are the ones that are fixed to the board and cannot move."""
    fixed_position: tuple[int, int]
    treasure: Treasure | None = None
    pawn: Pawn | None = None

@dataclass
class MovingTile(Tile):
    """Tiles that can be moved by sliding and rotating."""
    treasure: Treasure | None = None
    pawn: Pawn | None = None

    def rotate_cw(self):
        """Rotates the tile clockwise."""
        self.orientation = (self.orientation+1)%(4)
        self.sides = self.sides[2:] + self.sides[:2]

        pass
    
    def rotate_ccw(self):
        """Rotates the tile counterclockwise."""
        self.orientation = (self.orientation-1)%(4)
        self.sides = self.sides[-2:] + self.sides[:-2]
        pass

@dataclass
class Board:
    """Represents the game board containing all tiles."""
    grid: dict[tuple[int, int], Tile]
    slideout_position: tuple[int, int] | None

    def __init__(self, fixed_tiles, moving_tiles):
        """
        Initializes the grid, then places base tiles according to their fixed positions, then randomly fills the rest of the grid with the moving tiles.
        """
        pass
    
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
        Initializes the grid, then places base tiles according to their fixed positions, then randomly fills the rest of the grid with the moving tiles.
        """
        pass
    
    def get_pawn_position(self, pawn) -> tuple[int, int]:
        pass

@dataclass
class Game:
    """Encapsulates all data related to an individual game's state and manages game flow."""
    queue: list[Pawn] # Rotating queue for playing order
    board: Board
    hand: MovingTile # Tile that last slid out of the board, returned by Board.slide_tile method

    def __init__(self, datapath: str, playernames: list[str]):
        '''initialize the game'''
        #get the treasures
        with open("./treasures.json" , 'r', encoding ='itf-8') as treasures:
            data_list = json.load(treasures)
            for my_treasure in data_list:
                

        #load treasures+declaration
        #load tiles+declaration
        #board creation
        #place pawns and give them names
        #distribute treasures
    
    def move_pawn(self, pawn, newpos):
        pass

    def start(self):
        pass
