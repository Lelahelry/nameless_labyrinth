from dataclasses import dataclass
from typing import Iterator
from utils import pairwise, bfs_walk
import random
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

    def current_objective(self) -> Treasure:
        return self.objectives[0]

    def collect(self) -> Treasure:
        return self.objectives.pop(0)
    
    def __str__(self) -> str:
        return f"{self.color.upper()}/{self.name!r}"

@dataclass
class Tile:
    """Represents the tiles that compose the labyrinth."""
    filepath: str # Path to .json file with init data.
    sides: list[bool] # Represents the open/closed nature of the four sides.
    orientation: int = 0
    treasure: Treasure | None = None
    pawns: list[Pawn] = []

@dataclass
class FixedTile(Tile):
    """These tiles are the ones that are fixed to the board and cannot move."""
    fixed_position: tuple[int, int] = (-1, -1)

@dataclass
class MovingTile(Tile):
    """Tiles that can be moved by sliding and rotating."""
    
    def rotate_cw(self) -> None:
        """Rotates the tile clockwise."""
        self.orientation = (self.orientation+1)%(4)
    
    def rotate_ccw(self) -> None:
        """Rotates the tile counterclockwise."""
        self.orientation = (self.orientation-1)%(4)

@dataclass
class Board:
    """Represents the game board containing all tiles."""
    grid: dict[tuple[int, int], Tile]
    slideout_position: tuple[int, int] | None

    def __init__(self, fixed_tiles: set[FixedTile], moving_tiles: set[MovingTile]):
        """
        Initializes the grid, then places base tiles according to their fixed positions, then randomly fills the rest of the grid with the moving tiles.
        """
        for ftile in fixed_tiles:
            self.grid[ftile.fixed_position] = ftile
        
        for i in range(7):
            for j in range(7):
                if (i, j) in self.grid: continue
                else:
                    tile = moving_tiles.pop()
                    for _ in range(random.randint(0, 3)):
                        tile.rotate_cw()
                    self.grid[(i, j)] = tile
    
    def __getitem__(self, pos: tuple[int, int]) -> Tile:
        return self.grid[pos]
    
    def __setitem__(self, pos: tuple[int, int], tile: Tile) -> None:
        if isinstance(self.grid[pos], FixedTile):
            raise ValueError("You can't move fixed tiles!")
        elif pos == self.slideout_position:
            raise ValueError("You can't insert your tile at the same place it came from!")
        else:
            self.grid[pos] = tile
    
    def slide_tile(self, insertpos: tuple[int, int], tile: Tile) -> Tile:
        """
        Applies the desired slide (if valid), and returns the tile that slid out.
        """
        match insertpos:

            case self.slideout_position:
                raise ValueError("Can't cancel previous move.")

            case ((0 | 6) as row, (1 | 2 | 5) as col):
                first, last = row, 6 if row == 0 else 0
                r = range(last, first)

                self.slideout_position = (last, col)
                slideout_tile = self.grid.pop(self.slideout_position)
                for i_current, i_next in pairwise(r):
                    self.grid[(i_current, col)] = self.grid.pop((i_next, col))
                self.grid[(first, col)] = tile
            
            case ((1 | 2 | 5) as row, (0 | 6) as col):
                first, last = col, 6 if col == 0 else 0
                r = range(last, first)

                self.slideout_position = (row, last)
                slideout_tile = self.grid.pop(self.slideout_position)
                for j_current, j_next in pairwise(r):
                    self.grid[(row, j_current)] = self.grid.pop((row, j_next))
                self.grid[(row, first)] = tile

            case (a, b) if (a is int) and (b is int):
                raise ValueError("Invalid insert position")
            
            case _:
                raise ValueError("Invalid insertpos type passed.")
        
        return slideout_tile
    
    def get_pawn_position(self, pawn: Pawn) -> tuple[int, int]:
        for pos, tile in self.grid.items():
            if pawn in tile.pawns:
                return pos
        
        raise ValueError(f"{pawn} doesn't exist on the board.")
    
    def connected_tiles(self, origin_pos: tuple[int, int]) -> Iterator[tuple[int, int]]:
        i, j = origin_pos
        origin = self.grid[origin_pos]
        neighbors_pos = [(i-1, j), (i, j+1), (i+1, j), (i, j-1)]

        for side in enumerate(origin.sides):
            match side:

                case (idx, True):
                    neighb_pos = neighbors_pos[idx]
                    neighb = self.grid.get(neighb_pos)
                    if neighb is None: continue

                    opp = (idx+2)%4
                    if not neighb.sides[opp]: continue
                    
                    yield neighb_pos
                
                case _:
                    continue

@dataclass
class Message:
    """communicates with the graphics file"""
    choosentile: tuple[int,int] | None
    insertpos : tuple[int, int] | None
    newpos : tuple[int,int] | None
    foundtreasure : Treasure | None
    current_grid : dict
    playernames : list[str]

@dataclass
class Game:
    """Encapsulates all data related to an individual game's state and manages game flow."""
    queue: list[Pawn] # Rotating queue for playing order
    board: Board
    hand: MovingTile # Tile that last slid out of the board, returned by Board.slide_tile method

    def __init__(self, datapath: str, playernames: list[str]):
        '''initialize the game'''
        COLORS = ['blue', 'red', 'green', 'yellow']
        STARTING_POSITIONS = [(0, 0), (0, 6), (6, 0), (6, 6)]

        #get the treasures
        with open("./treasures.json" , 'r', encoding ='utf-8') as treasures_file:
            data_treasures = json.load(treasures_file)
        treasures = {name: Treasure(fpath, name) for name, fpath in data_treasures}

        #get players
        self.queue = list()
        random_treasures = list(treasures.values())
        random.shuffle(random_treasures)
        for name, color in zip(playernames, COLORS):
            objectives = list()
            for _ in range(6):
                objectives.append(random_treasures.pop())
            
            self.queue.append(Pawn(color, name, objectives))
        
        #get the tiles
        with open("./tiles.json" , 'r', encoding ='utf-8') as tiles:
            data_tiles = json.load(tiles)

        ftiles = set()
        for tiles in data_tiles["fixed"]:
            for tile_dict in tiles:
                tile = FixedTile(tile_dict["filepath"], 
                                 tile_dict["sides"], 
                                 tile_dict["orientation"], 
                                 treasures[tile_dict["treasure"]], 
                                 tile_dict["pawns"], 
                                 tuple(tile_dict["position"]))
                ftiles.add(tile)

        mtiles = set()
        for tiles in data_tiles["moving"]:
            for tile_dict in tiles:
                tile = MovingTile(tile_dict["filepath"], 
                                  tile_dict["sides"], 
                                  tile_dict["orientation"], 
                                  treasures[tile_dict["treasure"]], 
                                  tile_dict["pawns"])
                mtiles.add(tile)
        
        #board creation
        self.board = Board(ftiles, mtiles)
        self.hand = mtiles.pop()
        
        #place pawns
        for pawn, pos in zip(self.queue, STARTING_POSITIONS):
            start_tile = self.board[pos].pawns.append(pawn)
    
    
    def move_pawn(self, pawn: Pawn, newpos: tuple[int, int]) -> tuple[int, int]:
        """return destination tile"""
        startpos = self.board.get_pawn_position(pawn)
        for pos in bfs_walk(startpos, self.board.connected_tiles):
            if pos == newpos:
                self.board[startpos].pawns.remove(pawn)
                self.board[newpos].pawns.append(pawn)

                return newpos
        
        raise ValueError("Pawn doesn't have an open path to given tile.")

    def start(self):
        game_won = False
        while not game_won:
            if self.turn():
                self.queue[0].treasures.pop(0)
                if self.queue[0].treasures == []:
                    game_won = True
            self.queue = self.queue.append(self.queue.pop(0))

    def turn(self):
        pass
        '''return boolean'''
        self.board.slide_tile(Message.insertpos, Tile)
        destination = self.move_pawn(self.queue[0], Message.newpos)
        return self.queue[0].objectives[0] == destination.treasure