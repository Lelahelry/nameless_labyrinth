from dataclasses import dataclass
from labyrinth import GameData
from graphics import GameWindow
from utils import bfs_walk


@dataclass
class GameController:
    model: GameData
    view: GameWindow

    def __post_init__(self):
        self.view.set_controller(self)
        self.game_active = False
    
    def move_pawn(self):
        """Enables moving a player's pawn to the tile they chose, given that this tile can indeed be reached.
        Otherwise, the player's pawn goes back to where it was.
        ----------
         No input
         No output"""
        pawn_moved = False
        pawn = self.model.get_active_player()
        startpos, start_tile = self.model.get_pawn_container(pawn)

        while not pawn_moved:
            self.view.show("Please choose a valid position to move your pawn to.")

            newpos = self.view.get_move_pos()
            for pos in bfs_walk(startpos, self.model.get_adjacency_fn()):
                if pos == newpos:
                    pawn_moved = True
                    dest_pawns = self.model.get_pawns_at_pos(newpos)

                    start_tile.pawns.remove(pawn)
                    dest_pawns.append(pawn)
                    
                    self.view.show_pawn_move(startpos, newpos)
            
            if not pawn_moved:
                self.view.show("Pawn didn't have an open path to the given tile.")
    
    def insert_hand(self):
        """Checks that the insertion position chosen by the player is valid (i.e. not where the hand just came from).
         Then shifts all the tiles of the chosen row or column by one position.
         A different tile is thus pushed out of the board and becomes the new hand.
         ----------
         No input
         No output"""
        hand_inserted = False
        while not hand_inserted:
            self.view.show("Please choose a valid position to insert the hand at.")
            insertpos, rotations = self.view.get_insert_state()

            hand = self.model.hand
            hand.orientation += rotations

            match insertpos:
                case (0|6, 1|3|5) | (1|3|5, 0|6) if insertpos != self.model.get_slideout_position():
                    hand_inserted = True

                    self.model.hand = self.model.board.slide_tile(insertpos, hand)
                    self.view.show_tile_slide(insertpos, hand)
            
            if not hand_inserted:
                self.view.show("Insert position was invalid.")

    def collect_treasure(self):
        """Checks that the treasure reached by a player corresponds to its current objective.
        Removes the collected treasure from the player's list of objectives.
        ----------
        No input
        No output"""
        active_pawn = self.model.get_active_player()
        _, active_tile = self.model.get_pawn_container(active_pawn)

        if active_pawn.objectives[0] == active_tile.treasure:
            active_pawn.objectives.pop(0)
            self.view.show_treasure_collect()
            #active_tile.treasure = None ????????
    
    def check_win_state(self):
        """Checks whether a player won (i.e. collected all their objectives).
        Ends the game if that's the case.
        ----------
        No input
        No output"""
        active_pawn = self.model.get_active_player()

        if len(active_pawn.objectives) == 0:
            self.game_active = False
            self.winner = active_pawn
    
    def rotate_players(self):
        """Once a player's turn is over, moves on to the next player in the queue.
        ----------
        No input
        No output"""
        self.model.advance_queue()
        self.view.show_turn_rotation()

    def turn(self):
        """Calls all necessary functions for a player to complete their turn.
        ----------
        No input
        No output"""
        self.insert_hand()
        self.move_pawn()
        self.collect_treasure()
        self.check_win_state()
        self.rotate_players()

        self.view.signal_end_turn()
    
    def start_game(self):
        """Launches the game and every turn until someone won.
        ----------
        No input
        No output"""
        self.game_active = True
        self.view.show_game_start()
        
        while self.game_active:
            self.turn()
        
        self.view.show_congratulations(self.winner)

    def give_objective(self):
        """gives the player's current objective
        output: str (filepath)"""
        return self.model.get_active_player().objectives[0].filepath
    
    def give_hand(self):
        """gives the hand
        output:  2 str (filepath)"""
        if self.model.hand.treasure == None:
            filepath_treas = None
        else:
            filepath_treas = self.model.hand.treasure.filepath
        return self.model.hand.filepath, filepath_treas
    
    def give_grid(self):
        """gives simplified version of the grid to view
        output : dict"""
        graphics_dict = {}
        for position , tile in self.model.board.grid.items():
            if tile.treasure != None:
                pawns = [p.color for p in tile.pawns]
                graphics_dict[position] = {"filepath_ti" : tile.filepath,"filepath_treas" : tile.treasure.filepath, "orientation" : tile.orientation, "pawns" : pawns}
            else:
                pawns = [p.color for p in tile.pawns]
                graphics_dict[position] = {"filepath_ti" : tile.filepath, "filepath_treas" : None, "orientation" : tile.orientation, "pawns" : pawns}
        return graphics_dict
    
    def give_outpos(self):
        return self.model.get_slideout_position()