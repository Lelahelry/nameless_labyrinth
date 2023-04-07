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
    treasure: Treasure | None = None
    pawn: Pawn | None = None

@dataclass
class FixedTile(Tile):
    """These tiles are the ones that are fixed to the board and cannot move."""
    fixed_position: tuple[int, int] | None = None

@dataclass
class MovingTile(Tile):
    """Tiles that can be moved by sliding and rotating."""
    
    def rotate_cw(self):
        """Rotates the tile clockwise."""
        self.orientation = (self.orientation+1)%(4)
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
        Pushes the tiles in the direcrtion of the inserted tile
        """
        pass
    
    def get_pawn_position(self, pawn) -> tuple[int, int]:
        for pos, tile in self.grid.items():
            pass

@dataclass
class Message:
    """communicates with the graphics file"""
    choosentile: tuple[int,int] | None
    insertpos : tuple[int, int] | None
    newpos : tuple[int,int] | None
    foundtreasure : 

@dataclass
class Game:
    """Encapsulates all data related to an individual game's state and manages game flow."""
    queue: list[Pawn] # Rotating queue for playing order
    board: Board
    hand: MovingTile # Tile that last slid out of the board, returned by Board.slide_tile method
    message : Message

    def __init__(self, datapath: str, playernames: list[str]):
        '''initialize the game'''
        the_ftiles=set()
        the_mtiles=set()
        #get the treasures
        with open("./treasures.json" , 'r', encoding ='itf-8') as treasures:
            data_treas = json.load(treasures)
            the_treasures = dict()
            for name, fpath in data_treas:
                t = Treasure(fpath, name)
                the_treasures[name]=t
            #à voir parce que je dois pouvoir les appeler et distribuer mais peut etre pas besoin d'avoir un objet direct
            
        #get the tiles
        with open("./tiles.json" , 'r', encoding ='itf-8') as tiles:
            data_tiles = json.load(tiles)

        for section, the_dict in data_tiles.items():
            #get fixed tiles
            if section == "fixed": 
                for filep, sides, treasure, pawns, position in the_dict:
                    new_tile = FixedTile(filep, sides, 0, the_treasures[treasure], pawns, position)
                    the_ftiles.add(new_tile)

            else:
                for filep, sides, treasure, pawn in the_dict:
                    treas = 
                    new_tile = MovingTile(filepath, sides, 0, treas, pawn)
                    the_tiles.append(new_tile)
             
        pass
        
        self.queue=list()
        #get players
        for i in range in len(playernames):
            objectives=list()
            for p in range(6):
                ind = randint(len(the_treasures)-1)
                objectives.append(the_treasures.pop(ind))
            new_p = Pawn(colors[i], playernames[i], objectives)   
            self.queue.append(new_p)
        #board creation
        self.board = Board(the_ftiles, the_mtiles)
        self.hand = the_mtiles.pop()
        #place pawns
        positions=[(0,0), (6,6), (0,6), (6,0)]
        for i in range(len(self.queue)):
            placement = position[i]
            strat_tile=self.board.grid[placement]
            start_tile.pawn = queue[i]

    
    def move_pawn(self, pawn, newpos):
        startpos = self.board.get_pawn_position()
        

    def start(self):
        pass

    def turn(self, player, choosentile):
        pass
        '''return player and boolean'''
        choosentile = Message.choosentile
        Board.slide_tile(Message.insertpos, Tile)
        self.move_pawn(self.queue[0], Message.newpos)
        if Pawn.objectives == Tile.treasure

        #check a treasure was found
            #check the player has won choosentile


