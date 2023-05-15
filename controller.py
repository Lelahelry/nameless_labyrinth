# -*- coding: utf-8 -*-

from dataclasses import dataclass
from model import GameData
from graphics import GameWindow
from utils import bfs_walk


@dataclass
class GameController:
    view: GameWindow
    model: GameData
    game_active: bool

    def __init__(self):
        self.view = GameWindow(self)
        self.game_active = False
    
    def insert_hand(self):
        """Checks that the insertion position chosen by the player is valid (i.e. not where the hand just came from).
        Then shifts all the tiles of the chosen row or column by one position.
        A different tile is thus pushed out of the board and becomes the new hand.
        ----------
        No input
        No output"""
        hand_inserted = False
        while not hand_inserted:
            insertpos = self.view.get_insert_state()

            hand = self.model.hand

            match insertpos:
                case (0|6, 1|3|5) | (1|3|5, 0|6) if insertpos != self.model.get_slideout_position():
                    hand_inserted = True

                    self.model.hand = self.model.board.slide_tile(insertpos, hand)
                    self.view.anim_tiles_slide()
            
            if not hand_inserted:
                self.view.show_warning("Insert position was invalid.")
        

    def validate_move(self, newpos):
        pawn = self.model.get_active_player()
        startpos, start_tile = self.model.get_pawn_container(pawn)
        path_found = False

        steps = []
        paths = (path for path in bfs_walk(startpos, self.model.get_adjacency_fn()) if not path_found)
        for path in paths:
            

            endpos = path[-1]
            if endpos == newpos:
                path_found = True
                steps = path

        return path_found, steps

    def move_pawn(self, newpos):
        """Moves a player's pawn from its current position on the board to the desired position, if this new position can be reached.
        ----------
        Input : newpos (tuple)
        No output"""
        pawn = self.model.get_active_player()
        startpos, start_tile = self.model.get_pawn_container(pawn)
        dest_pawns = self.model.get_pawns_at_pos(newpos)

        start_tile.pawns.remove(pawn)
        dest_pawns.append(pawn)
        self.view.anim_pawn_displacement()

    def end_turn(self):
        self.collect_treasure()
        self.check_win_state()
        self.rotate_players()
        self.view.turn_over()
    
    def collect_treasure(self):
        """Checks that the treasure reached by a player corresponds to its current objective.
        Removes the collected treasure from the player's list of objectives.
        ----------
        No input
        No output"""
        active_pawn = self.model.get_active_player()
        _, active_tile = self.model.get_pawn_container(active_pawn)

        if active_pawn.objectives[0] == active_tile.treasure:
            found = active_pawn.objectives.pop(0)
            self.view.messagebox(f"You found the {found.name}. \n You still have {len(active_pawn.objectives)} treasures to find.")
    
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

    def give_queue(self):
        """We use this function to get the players queue.
        ----------
        No input
        Output : info_dict (dictionary)"""
        info_dict = {}
        for pawn in self.model.queue:
            info_dict[pawn.color] = {'color' : pawn.color, 'name' : pawn.name, 'objectives' : [obj.filepath for obj in pawn.objectives]}
        return info_dict
    
    def give_player_color(self):
        """Gives the active player's color
        ----------
        No input
        Output : str (color)"""
        return self.model.get_active_player().color

    def give_player_name(self):
        """Gives the active player's name
        ----------
        No input
        Output : str (name)"""
        return self.model.get_active_player().name
    def give_objective(self):
        """Gives the player's current objective
        ----------
        No input
        Output : str (filepath)"""
        return self.model.get_active_player().objectives[0].filepath
    
    def give_hand(self):
        """Gives the info on the current hand
        ----------
        No input
        Output :  2 str (filepath)"""
        if self.model.hand.treasure == None:
            filepath_treas = None
        else:
            filepath_treas = self.model.hand.treasure.filepath
        return self.model.hand.filepath, filepath_treas, self.model.hand.orientation
    
    def give_grid(self):
        """Gives a simplified version of the grid to view
        ----------
        No input
        Output : dict (the grid)"""
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
        """Gives the coordinates of the position the tile in hand was ejected from.
        ----------
        No input
        Output : tuple (slideout_position)"""
        return self.model.get_slideout_position()

    def rotate_hand_clockwise(self):
        self.model.hand.rotate_cw()

    def rotate_hand_counterclockwise(self):
        self.model.hand.rotate_ccw()
    
    def start_game(self, playernames: list[str]):
        """Launches the game and every turn until someone won.
        ----------
        No input
        No output"""
        self.model = GameData("", playernames)
        self.game_active = True
        self.view.display_game()
    
    def launch(self):
        """Launches the game.
        ----------
        No input
        No output"""
        self.view.app_start()

    def done(self):
        return self.game_active 