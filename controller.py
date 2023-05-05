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
        hand_inserted = False
        while not hand_inserted:
            self.view.show("Please choose a valid position to insert the hand at.")
            insertpos, rotations = self.view.get_insert_state()

            hand = self.model.hand
            hand.orientation += rotations

            match insertpos:
                case (0|6, 1|3|5) | (1|3|5, 0|6) if insertpos != self.model.get_slideout_position():
                    hand_inserted = True

                    self.model.board.slide_tile(insertpos, hand)
                    self.view.show_tile_slide(insertpos, hand)
            
            if not hand_inserted:
                self.view.show("Insert position was invalid.")

    def collect_treasure(self):
        active_pawn = self.model.get_active_player()
        _, active_tile = self.model.get_pawn_container(active_pawn)

        if active_pawn.objectives[0] == active_tile.treasure:
            active_pawn.objectives.pop(0)
            self.view.show_treasure_collect()
            #active_tile.treasure = None ????????
    
    def check_win_state(self):
        active_pawn = self.model.get_active_player()

        if len(active_pawn.objectives) == 0:
            self.game_active = False
            self.winner = active_pawn
    
    def rotate_players(self):
        self.model.advance_queue()
        self.view.show_turn_rotation()

    def turn(self):
        self.insert_hand()
        self.move_pawn()
        self.collect_treasure()
        self.check_win_state()
        self.rotate_players()

        self.view.signal_end_turn()
    
    def start_game(self):
        self.game_active = True
        self.view.show_game_start()
        
        while self.game_active:
            self.turn()
        
        self.view.show_congratulations(self.winner)