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
 - the code was split into 5 separate python files:
   - model: this code has all the declarations of classes useful for the game and the game class in itself
   - view: this code handles all the aspects of the graphic display
   - controller: this code is used as a communication medium linking the view to its model
   - utils: this code contains all the functions useful for the unrolling of the game algorithm but directly manipulating the objects
   - main : this code is the one initialising the game. It is the code that should be executed to start our program.

## Description of model.py
- The model creates all the objects used in the labyrinth game and the game object in itself, which stores the state of the game.
```python
@dataclass(frozen = True)
class Treasure:
    """Represents the treasures and treasure objectives of the game.
    ----------
    Input : str, str
    No output"""
    filepath: str # Path to .png texture file of the treasure.
    name: str

@dataclass
class Pawn:
    """Represents the pawns (assigned to players) and contains their lists of objectives.
    ----------
    Input : str, str, list[Treasure]
    No output"""
    color: str
    name: str
    objectives: list[Treasure]

    def current_objective(self) -> Treasure:
        """Returns the current objective of the pawn.
        ----------
        Input : None
        Output : Treasure"""

    def collect(self) -> Treasure:
        """Removes the current objective from the list and returns it.
        ----------
        Input : None
        Output : Treasure"""
    
    def __str__(self) -> str:
        """Returns a string representation of the pawn.
        Input : None
        Output : str"""

@dataclass
class Tile:
    """Represents the tiles that compose the labyrinth.
    ----------
    Input : str, list[bool], int, Treasure, list[Pawn]
    No output"""
    filepath: str # Path to .json file with init data.
    sides: list[bool] # Represents the open/closed nature of the four sides.
    orientation: int = 0
    treasure: Treasure | None = None
    pawns: list[Pawn] = field(default_factory=list)

@dataclass
class FixedTile(Tile):
    """These tiles are the ones that are fixed to the board and cannot move.
    ----------
    Input : str, list[bool], int, Treasure, tuple[int, int]
    No output"""
    fixed_position: tuple[int, int] = (-1, -1)

@dataclass
class MovingTile(Tile):
    """Tiles that can be moved by sliding and rotating.
    ----------
    Input : str, list[bool], int, Treasure
    No output"""
    
    def rotate_cw(self) -> None:
        """Rotates the tile clockwise.
        ----------
        Input : None
        Output : None"""
    
    def rotate_ccw(self) -> None:
        """Rotates the tile counterclockwise.
        ----------
        Input : None
        Output : None"""

@dataclass
class Board:
    """Represents the game board containing all tiles.
    ----------
    Input : list[FixedTile], list[MovingTile]
    No output"""
    grid: dict[tuple[int, int], Tile] 
    slideout_position: tuple[int, int] | None = None

    def __init__(self, fixed_tiles: list[FixedTile], moving_tiles: list[MovingTile]):
        """
        Initializes the grid, then places base tiles according to their fixed positions, then randomly fills the rest of the grid with the moving tiles.
        ----------
        Input : list[FixedTile], list[MovingTile]
        Output : None"""
            
    def __getitem__(self, pos: tuple[int, int]) -> Tile:
        """Returns the tile at the given position.
        ----------
        Input : tuple[int, int]
        Output : Tile"""
    
    def __setitem__(self, pos: tuple[int, int], tile: Tile) -> None:
        """Sets the tile at the given position.
        ----------
        Input : tuple[int, int], Tile
        Output : None"""
            
    def slide_tile(self, insertpos: tuple[int, int], tile: MovingTile) -> MovingTile:
        """
        Applies the desired slide (if valid), and returns the tile that slid out.
        ----------
        Input : tuple[int, int], MovingTile
        Output : MovingTile
        """
        
    def connected_tiles(self, origin_pos: tuple[int, int]) -> Iterator[tuple[int, int]]:
        """Returns an iterator over the positions of the tiles adjacent to the given one.
        ----------
        Input : tuple[int, int]
        Output : Iterator[tuple[int, int]]"""

@dataclass
class GameData:
    """Encapsulates all data related to an individual game's state and can provide insight into it to external callers.
    Input : str, list[str]
    No output"""
    queue: list[Pawn] # Rotating queue for playing order
    board: Board
    hand: MovingTile # Tile that last slid out of the board, returned by Board.slide_tile method

    def __init__(self, datapath: str, playernames: list[str]):
        '''Initializes the game objects.
        ----------
        Input : str, list[str]
        Output : None'''
        
    def get_pawn_container(self, pawn: Pawn) -> tuple[tuple[int, int], Tile]:
        """Returns the position and tile of the given pawn.
        ----------
        Input : Pawn
        Output : tuple[tuple[int, int], Tile]"""
    
    def get_adjacency_fn(self) -> Callable[[tuple[int, int]], Iterator[tuple[int, int]]]:
        """Returns a function that can be used to get the adjacent tiles to a given position.
        ----------
        Input : None
        Output : Callable[[tuple[int, int]], Iterator[tuple[int, int]]]"""

    def get_slideout_position(self) -> tuple[int, int] | None:
        """Returns the position from which the last tile slid out.
        ----------
        Input : None
        Output : tuple[int, int] | None"""

    def get_active_player(self) -> Pawn:
        """Returns the active player.
        ----------
        Input : None
        Output : Pawn"""
    
    def get_pawns_at_pos(self, pos: tuple[int, int]):
        """Returns the pawns at the given position on the board.
        ----------
        Input : tuple[int, int]
        Output : list[Pawn]"""

    def advance_queue(self):
        """Update the queue to place the first player at the end of the queue.
        ----------
        Input : None
        Output : None"""

```

## Description of view.py
- The view is all about the graphic interface elements. There are 2 main windows: the window to prepare the game and the one that represents the current game.
``` python
class GameWindow():
    def __init__(self, controller):
        """Creates the welcome window and some game variables.
        Input : GameController
        No output"""
        

    def widgets_creation(self, root):
        """Creates all necessary widgets and variables for the welcome window.
        ----------
        Input : root
        No output"""  
           
    def game_launch(self, message):
        """Creation of the current game window.
        ----------
        Input : message (str)
        No output"""
                
    # Callback methods
    def show_rules(self, event):
        """Displays the game rules in a Messagebox when the "?" rules_button is clicked.
        ----------
        Input : right click from the mouse
        No output"""
        
    def show_tip(self, event):
        """Shows a "Rules" label when hovering the mouse over the "?" rules_button.
        ----------
        Input : mouse hovering above the rules_button
        No output"""
    
    def hide_tip(self, event):
        """Hides the "Rules" label when the mouse is not over the "?" rules_button anymore.
        ----------
        Input : mouse left the rules_button area
        No output"""
 
    def add_playernames(self, event):
        """Adds or removes entry bars for players to enter custom names (optional).
        ----------
        Input : Slider is released at a position (i.e. a new number of players)
        No output"""

    def get_playernames(self):
        """Recovers each player's name.
        Default names are provided in case players don't add names.
        ----------
        No input
        No output"""
    
    def display_game(self):
        """Creates the graphic window for current game display.
        ----------
        No input
        No output"""
        
    # Display material methods
    def image_library_i(self):
        """Loads and sizes all PNG files as Images (this object type can be rotated).
        ----------
        No input
        No output"""
            
    def get_image(self, filepath):
        """Get image from filepath.
        ----------
        Input : str
        Output : Image"""

    # Messageboxes calls    
    def show_warning(self, text):
        """Opens a messagebox with a custom text.
        ----------
        Input : str (text)
        No output"""
        
    def messagebox(self, text):
        """Opens a messagebox with a custom text.
        ----------
        Input : str (text)
        No output"""

    # Display window methods
    def queue_display(self):
        """Queue (playing order) displayed with labels containing : player's name written in color, number of remaining objectives.
        ----------
        No input
        No output"""
        
    def canvas_for_board(self):
        """Creates the canvas for the board with the background and the foreground.
        ----------
        No input
        No output""" 

    def slide_tiles_buttons(self):
        """Creates the buttons around the board allowing to choose where to insert the tile in hand.
        Each button is named according to the grid position it points to (row number, column number).
        ----------
        No input
        No output"""

    def canvas_for_objective(self):
        """Creates the canvas to display the current objective of the player filles it with the background and foreground.
        ----------
        No input
        No output """
        

    def objective_background(self):
        """Sets the image of the empty treasure card, which is the current objective of the player.
        ----------
        No input
        No output"""
        

    def objective_image(self):
        """Displays the right treasure in the objective card.
        ----------
        No input
        No output"""
                
    def canvas_for_hand(self):
        """Creates the canvas for the tile in hand with the background and foreground.
        ----------
        No input
        No output"""
        

    def hand_image(self):
        """Displays the tile in hand in its canvas.
        ----------
        No input
        No output"""

    def hand_treasure(self):
        """Displays the treasure of the tile in hand.
        ----------
        No input
        No output"""

    def hand_tile(self):
        """Displays the tile in hand (background).
        ----------
        No input
        No output"""

    def turn_tile_buttons(self):
        """Creates the buttons next to the hand allowing to change the orientation of the tile in hand and binds them to the image update.
        ----------
        No input
        No output"""
        
    def validate_button(self):
        """Creates the button under the hand to validate the chosen orientation and insertion.
        ----------
        No input
        No output"""    
        
    def grid_images(self):
        """Displays the tiles on the board in its canvas and binds it to the sliding.
        Same actions for the treasures. All images are stocked as images and as elements of the canvas.
        ----------
        No input
        No output"""
    
    def grid_treasure(self, filepath, co, li):
        """Places the treasures on the board.
        ----------
        Input : str, int, int
        Output : PhotoImage on canvas"""
    
    def grid_tile(self, filepath, orientation, co, li):
        """Places the tiles on the board.
        ----------
        Input : str, int, int, int
        Output : PhotoImage on canvas"""

    def place_pawns(self):
        """Places circles for the pawns on the boards.
        ----------
        No input
        No output"""
        
    # Buttons methods
    def select_insertion_button(self, pos, button_in, button_out):
        """Changes the color of the selected button to mark it as chosen and gets its position.
        ----------
        Input : tuple (pos), 2 widgets (button_in, button_out)
        No output""" 

    def turn_hand_tile(self, sens):
        """Rotates the tile in hand and redoes its background display.
        ----------
        Input = integer (sens, i.e., the direction of the rotation)
        No output"""

    def check_insertion(self, event):
        """Verify that the player did select a valid place to insert the tile in hand.
        ----------
        Input : right click from the mouse on validate_button
        No output"""

    def click_tile(self, event):
        """Places a cross where the player wants to move their pawn. The cross color depends on whether the tile is accessible or not.
        Controller verfies accessiblity and gives a possible path if so. The destination coordinates on the grid are registered.
        ----------
        Input : right click from the mouse on a tile of the board
        No output"""
        
    def move(self, event):
        """Moves the player's pawn in the model(through controller) and the view.
        ----------
        Input : right click from the mouse on the "validate displacement" button
        No output"""

    def click_tile(self, event):
        """Places a cross where the player wants to move their pawn and registers the grid coordinates.
        ----------
        Input : right click from the mouse on a tile of the board
        No output"""
        
        
    # Controller communication methods
    def app_start(self):
        """Starts the interface
        No input
        No output"""
    
    def anim_tiles_slide(self):
        """Slides the tile on the screen using a timer. Prepares the animation by changing the displayed tiles. Updates the sorage of every graphical object and manages the turn unrolling by enabling the pawn movement features and disabling the tile insertion features.
        ----------
        No input
        No output"""

    def get_move_pos(self):
        """Returns the coordinates of the tile where the player wants to move the pawn.
        ----------
        No input
        Output : 2 intergers"""
            
    def anim_pawn_displacement(self):     
        """Prepares the required information for the animation of the pawn. And begins the animation of the pawn
        ----------
        No input
        No output"""   

    def turn_over(self):
        """Verifies if the game is over and if not, prepares the next turn.
        ----------
        No input 
        No output"""
   
    # Animation things
    ## Animation of tiles
           
    def storage_update(self, init_pos, out_pos, li, co):
        """Updates the dictionnaries of the grid display.
        ----------
        Input : 2 tuples, 2 integers
        No output"""
    
    def lancer(self):
        """Launches the timer loop if it's not already running for the tile animation.
        ----------
        No input
        No output"""
        
    def stop(self):
        """Stops the timer loop if it is running for the tile animation.
        ----------
        No input
        No output"""        

    def timer_loop(self):
        """Defines the loop that is handled by the timer : allows image displacement and display fror the tile animation.
        ----------
        No input
        No output"""        
             
    ## Animation of pawns 
    def anim_move_pawn(self):
        """Launches the timer loop if it's not already running for the pawn animation.
        ----------
        No input
        No output"""     
    
    def timer_loop_pawn(self):
        """Defines the loop that is handled by the timer : allows image displacement and display fror the pawn animation.
        ----------
        No input
        No output"""

    def stop_pawn(self):
        """Stops the timer loop if it is running for the pawn animation.
        ----------
        No input
        No output"""
    # Usefulmethod for animation
    def find_ident(self, color, pos):
        """Identifies a pawn circle on the canvas using its position tile and its color.
        ----------
        Input : str, tuple
        Output : Int (identifier of the canvas object)"""
        
# General functions    
def rotate_image(img, orientation):
    """Rotates an image to the given orientation.
    ----------
    Input : Image, int
    Output : PhotoImage"""

def rotate_image_h(img, orientation):
    """Rotates and enlarges by 3 an image.
    ----------
    Input : Image, int
    Output : PhotoImage"""
    
def grid_position(pos):
    """Converts the grid into canvas coordinates.
    ----------
    Input : tuple (line, column)
    Output : tuple (line, column)"""
```

## Descrition of controller.py
- The controller establishes communication between the model and the view. It is able to communicate with both and is responsible for both their creation.

## Description of main
- Main executed and creates the controller which is in charge of distributing the tasks to view and model.

## Description of utils
 - Funcitions contained: 

