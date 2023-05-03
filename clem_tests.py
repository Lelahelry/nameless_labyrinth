from dataclasses import dataclass
import json
import random
from labyrinth import Pawn, Treasure, Tile, MovingTile, FixedTile, Board



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
        treasures = {name: Treasure(fpath, name) for name, fpath in data_treasures[0].items()}


        #get players
        self.queue = list()
        random_treasures = list(treasures.values())
        random.shuffle(random_treasures)
        for name, color in zip(playernames, COLORS):
            objectives = list()
            for _ in range(int(24/len(playernames))):
                objectives.append(random_treasures.pop())
            #test
            print(name+f" you will look for:")
            for thing in objectives:
                print(f'{thing.name }')
            print("you are "+ color)
            print("")
            self.queue.append(Pawn(color, name, objectives))
            #test
            print("pawn created")
            print("")
            
        #get the tiles
        with open("./tiles.json" , 'r', encoding ='utf-8') as tiles:
            data_tiles = json.load(tiles)
        #test
        print("I loaded the tiles")
        print(data_tiles)
        print("")
            

        ftiles = list()
        for tile_dict in data_tiles["fixed"]:
            if tile_dict["treasure"]==None:
                tile = FixedTile(filepath = tile_dict["filepath"], sides = tile_dict["sides"], orientation = tile_dict["orientation"], fixed_position = tuple(tile_dict["position"]))
            else:
                tile = FixedTile(filepath = tile_dict["filepath"], sides =  tile_dict["sides"], orientation = tile_dict["orientation"],treasure =  treasures[tile_dict["treasure"]], fixed_position=tuple(tile_dict["position"]))
            
            ftiles.append(tile)
            print(tile)
            print("")
            
        #test
        print("fixed tiles are done")
        print("")
            
        mtiles = list()
        for tile_dict in data_tiles["moving"]:
            if tile_dict["treasure"]==None:
                tile = MovingTile(filepath = tile_dict["filepath"], 
                            sides = tile_dict["sides"])
            else:
                tile = MovingTile(filepath = tile_dict["filepath"], 
                           sides = tile_dict["sides"], 
                            treasure = treasures[tile_dict["treasure"]])
            mtiles.append(tile)
            print(tile)
            print("")
        #test
        print("moving tiles are done")
        print("")
            
        #board creation
        self.board = Board(ftiles, mtiles)
        self.hand = mtiles.pop()
        #test
        print("The board is ready")
        print(self.board.grid)
        print("we begin with this tile:")
        print(self.hand)
        #place pawns
        for pawn, pos in zip(self.queue, STARTING_POSITIONS):
            start_tile = self.board[pos].pawns.append(pawn)
            
                
t1=Treasure("1","a")
t2=Treasure("1","b")
t3=Treasure("1","c")
t4=Treasure("1","d")
t5=Treasure("1","e")

p1=Pawn("blue","léa",[t1,t2,t3])
p2=Pawn("red","clem",[t4,t5])


print(p1.__repr__(), p2.__repr__())

print(p1.current_objective())

p1.collect()

p2.collect()
p2.collect()
print(p1.__repr__())
print(p2.__repr__())

ti_1=MovingTile("bcjced", [True, False, False, False] )
ti_1.rotate_cw()
print(ti_1.orientation)
ti_1.rotate_cw()
print(ti_1.orientation)
ti_1.rotate_ccw()
print(ti_1.orientation)
ti_1.rotate_cw()
print(ti_1.orientation)

gamer = Game("jkscnj", ["léa","clem","marine"])


graphics_dict ={}
##grid should be reduced to (positionTuple)={filepathTile, filepathTreas|None, list of colors or empty list]
for position , tile in gamer.board.grid.items():
    if tile.treasure != None:
        pawns=[p.color for p in tile.pawns]
        graphics_dict[position]= {"filepathTile" : tile.filepath,"filepathTreas" : tile.treasure.filepath,"orientation":tile.orientation, "pawns" : pawns}
    else:
        pawns=[p.color for p in tile.pawns]
        graphics_dict[position]= {"filepathTile" : tile.filepath, "filepathTreas" : None, "orientation":tile.orientation, "pawns" : pawns}


print("")
print("")
print(graphics_dict)

t1 = FixedTile(filepath="",sides=[True])
t2 = MovingTile(filepath="", sides=[False])
b=Board([t1],[t2])
print(b)

