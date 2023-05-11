import random
import tkinter as tk
import customtkinter as ctk
import time
from PIL import Image, ImageTk

ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class GameWindow():
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Labyrinth - the aMAZEing game") # Title of the window
        self.root.configure(bg='#103A86')
        self.root.iconbitmap('tr_chest.ico') # Icon of the window
        self.root.geometry("1200x700") # Initial dimensions of the window
        # management of the communication with the game class
            
        ########################################
        # Graphic window settings
        ########################################

        # Graphical elements
        self.folder = "./textures" # address 

        # Display window setting
        self.f_graph = None

        # Test parameters
        self.playernames_e = list()
        self.playernames = list()

        # Widgets creation
        self.widgets_creation(self.root)

    def widgets_creation(self, root):
        """Creates all necessary widgets for the welcome window"""
        # Text : game title
        self.welcome = ctk.CTkLabel(root, height = 120, text = "Welcome to the aMAZEing Labyrinth - Software version !", text_color = "DodgerBlue4", font = ('Calibri', 28, 'bold'))
        self.welcome.pack(side = tk.TOP)

        # Instructions
        self.label = ctk.CTkLabel(root, height = 50, text = "Choose the number of players and enter their names :", font = ('Calibri', 20))
        self.label.pack(side = tk.TOP)

        # Number of players
        self.player_number = tk.IntVar()
        self.scale = ctk.CTkSlider(root, height = 30, width = 455, progress_color = "goldenrod", fg_color = "DodgerBlue4", button_corner_radius = 5, button_color = "goldenrod", button_hover_color = "DodgerBlue4", from_ = 2, to = 4, number_of_steps = 2, orientation = "horizontal", variable = self.player_number)
        self.scale.pack(pady = 30, anchor = ctk.CENTER)
        self.scale.bind('<ButtonRelease-1>', self.add_playernames)
        self.scale.set(2)
        self.add_playernames(None)

        # Quit app button
        self.button_quit = ctk.CTkButton(root, text = "Quit", corner_radius = 8, height = 40, width = 15, fg_color = "red4", hover_color = "DodgerBlue4", font = ('Calibri', 20), command = self.root.destroy)
        self.button_quit.pack(fill = 'x', side = tk.BOTTOM)
        
        # launch game
        self.button_launch = ctk.CTkButton(self.root, text = "Start game", corner_radius = 8, height = 60, width = 15, fg_color = "goldenrod", hover_color = "DodgerBlue4", font = ('Calibri', 20))
        self.button_launch.bind('<Button-1>', self.game_launch)
        self.button_launch.pack(side = ctk.BOTTOM, fill = 'x')
 
    def add_playernames(self, event):
        """Adds entry bars for players to enter custom names (optional)"""
        length = self.player_number.get()

        if length > len(self.playernames_e):
            # Add new player name entries
            for i in range(1, length - len(self.playernames_e) + 1):
                name = "Player" + str(len(self.playernames_e) +1)
                entry = ctk.CTkEntry(self.root,text_color = "DodgerBlue4", placeholder_text = name,  height = 50, width = 200, font = ('Calibri', 16))
                entry.pack(padx = 10, pady = 10, anchor = ctk.CENTER)
                self.playernames_e.append(entry)

        elif length < len(self.playernames_e): 
            diff = len(self.playernames_e) - length
            # Empty player names and change entries
            for i in range(diff):
                self.playernames_e.pop().pack_forget()
           
    def game_launch(self, message):
        """Creation of the actual game window"""
        # Find the names of the players
        self.get_playernames()
        
        # Initialize the game through the controller
        #self.controller.init_control() CONTROLLER

        # Creation of the graphic window
        self.graphic_window() 
        
    # Callback functions
    def get_playernames(self):
        """Recovers each player's name
        Default names are provided in case players don't add names
        No input
        No output"""
        for i in range(len(self.playernames_e)):
            name = str(self.playernames_e[i].get()) # Names the players chose for themselves
            if name == "":
                name = "Player" + str(i+1) # Default name
            self.playernames.append(name) #SEND THIS TO CONTROLLER
    
    def graphic_window(self):
        """Creates the graphic window for current game display
        No input
        No output"""
        self.running = False
        self.running_pawn = False
        self.timer_id = None
        self.timer_id_pawn = None
        self.pawn_motion = False

        if (self.f_graph == None) :
            self.f_graph = tk.Toplevel(self.root)
            self.f_graph.title('Labyrinth - Current game')
            self.f_graph.iconbitmap('tr_chest.ico')      
            self.f_graph.geometry("1500x875") 
            self.f_graph.config(background = '#EFEFE1')
            
            # Button for players to indicate they finished their turn
            self.button_done = ctk.CTkButton(self.f_graph, text = "My turn is over.", corner_radius = 8, height = 30, width = 15, fg_color = "goldenrod", hover_color = "DodgerBlue4", font = ('Calibri', 20))
            self.button_done.bind('<Button-1>', self.turn_over)
            self.button_done.pack(side = ctk.BOTTOM, fill = 'x')
            
            self.image_dict = {} # Dict that stocks all 50 tiles as (bg, fg, pawn) in grid size

            # Functions calls
            self.canvas_for_board()
            self.slide_tiles_buttons()
            self.canvas_for_objective() 
            #self.text_area()
            self.canvas_for_hand()
            self.turn_tile_buttons()
            self.validate_button()

        # Reset state of f_graph so that it can be opened again once closed (without rerunning the whole program)
        #self.f_graph = None 
        

    def canvas_for_board(self):
        """Creates the canvas for the board with the background
        No input
        No output"""        
        self.canvas_board = tk.Canvas(self.f_graph, width = 752, height = 752, bg = "#EFEFE1")

        self.grid_images() 
        self.place_pawns()

        # Set the background image of the canvas
        self.background = tk.PhotoImage(file = self.folder + '\\board.png')
        self.item = self.canvas_board.create_image(378, 378, image = self.background)
        self.canvas_board.lower(self.item)

        self.canvas_board.pack(side = tk.LEFT, padx = 40, pady = 32)

    def slide_tiles_buttons(self):
        """Creates the buttons around the board allowing to choose where to insert the tile in hand
        Each button is named according to the grid position it points to (row number, column number)
        No input
        No output"""

        # Bind it to controller somehow so as to disable the button where it's not allowed to insert the tile
        self.selected_button = None
        
        # Top side buttons
        self.bouton01 = ctk.CTkButton(self.f_graph, text = "▼", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton01.bind('<Button-1>', lambda event: self.select_insertion_button((0,1), self.bouton01, self.bouton61))
        self.bouton01.place(x = 161, y = 1)

        self.bouton03 = ctk.CTkButton(self.f_graph, text = "▼", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton03.bind('<Button-1>', lambda event:  self.select_insertion_button( (0,3), self.bouton03, self.bouton63))
        self.bouton03.place(x = 318, y = 1)

        self.bouton05 = ctk.CTkButton(self.f_graph, text = "▼", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton05.bind('<Button-1>', lambda event: self.select_insertion_button( (0,5), self.bouton05, self.bouton65))
        self.bouton05.place(x = 475, y = 1)

        # Left side buttons
        self.bouton10 = ctk.CTkButton(self.f_graph, text = "►", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton10.bind('<Button-1>', lambda event: self.select_insertion_button( (1,0), self.bouton10, self.bouton16))
        self.bouton10.place(x = 1, y = 161)

        self.bouton30 = ctk.CTkButton(self.f_graph, text = "►", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton30.bind('<Button-1>',  lambda event: self.select_insertion_button((3,0), self.bouton30, self.bouton36))
        self.bouton30.place(x = 1, y = 318)

        self.bouton50 = ctk.CTkButton(self.f_graph, text = "►", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton50.bind('<Button-1>', lambda event: self.select_insertion_button((5,0), self.bouton50, self.bouton56))
        self.bouton50.place(x = 1, y = 475)

        # Bottom side buttons
        self.bouton61 = ctk.CTkButton(self.f_graph, text = "▲", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton61.bind('<Button-1>',  lambda event: self.select_insertion_button((6,1), self.bouton61, self.bouton01))
        self.bouton61.place(x = 161, y = 635)

        self.bouton63 = ctk.CTkButton(self.f_graph, text = "▲", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton63.bind('<Button-1>', lambda event: self.select_insertion_button((6,3), self.bouton63, self.bouton03))
        self.bouton63.place(x = 318, y = 635)

        self.bouton65 = ctk.CTkButton(self.f_graph, text = "▲", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton65.bind('<Button-1>', lambda event: self.select_insertion_button((6,5), self.bouton65, self.bouton05))
        self.bouton65.place(x = 475, y = 635)

        # Right side buttons
        self.bouton16 = ctk.CTkButton(self.f_graph, text = "◄", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton16.bind('<Button-1>', lambda event: self.select_insertion_button((1,6), self.bouton16, self.bouton10))
        self.bouton16.place(x = 635, y = 161)

        self.bouton36 = ctk.CTkButton(self.f_graph, text = "◄", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton36.bind('<Button-1>', lambda event: self.select_insertion_button((3,6), self.bouton36, self.bouton30))
        self.bouton36.place(x = 635, y = 318)
        
        self.bouton56 = ctk.CTkButton(self.f_graph, text = "◄", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton56.bind('<Button-1>', lambda event: self.select_insertion_button((5,6), self.bouton56, self.bouton50))
        self.bouton56.place(x = 635, y = 475)

        self.opposite_button_old = None

    
    def select_insertion_button(self, pos, button_in, button_out):
        """Changes the color of the selected button and gets its position"""
        # Change color : when clicked, becomes red4 and stays that way unless a different insertion button was selected
        # Find button selected by the player
        if button_in.cget("state") != "disabled":
            button_in.configure(fg_color = "red4")
            #deselect the previous button
            if self.selected_button != None:
                self.selected_button.configure(fg_color = "goldenrod")

            if self.selected_button == button_in: #case you deselected the line/row after all
                self.selected_button = None
                self.opposite_button = None
                self.chosen_pos = None
            else:
                self.selected_button = button_in
                self.opposite_button = button_out
                # Get button position
                self.chosen_pos = pos
        

    def canvas_for_objective(self):
        """Creates the canvas to display the current objective of the player"""
        self.canvas_card = tk.Canvas(self.f_graph, width = 360, height = 420, bg = '#EFEFE1')

        self.objective_background()
        self.objective_image()

        self.canvas_card.pack(side = tk.TOP, anchor = 'ne')

    def objective_background(self):
        """Sets the image of the empty treasure card, which is the current objective of the player
        No input
        No output"""
        # Background image settings
        self.canvas_card.original_background = tk.PhotoImage(file = self.folder + '\\card.png')
        self.canvas_card.background = self.canvas_card.original_background.zoom(6, 6)
        self.canvas_card.item = self.canvas_card.create_image(160, 212, image = self.canvas_card.background)

        self.canvas_card.lower(self.item)

    def objective_image(self):
        """Displays the right treasure in the objective card
        No input
        No output"""
        #filepath_tr = self.controller.hand CONTROLLER
        filepath_tr = "\\tr_crown.png" # address
        # Treasure image settings
        self.treas_c = tk.PhotoImage(file = self.folder + filepath_tr)
        self.treas_c_resized = self.treas_c.zoom(3, 3)
        self.fg_c = self.canvas_card.create_image(160, 212, image = self.treas_c_resized)

        self.canvas_card.lift(self.fg_c)
        
        #display the treasure using the controller CONTROLLER
            #select treasure index 0 in the list of the player's objectives

    #def text_area(self):
        """creates text area where the controller sends event messages
        no input
        no output"""
        #text area for commmunication through controller
        #bind it to messagerie method

    def canvas_for_hand(self):
        """Creates the canvas for the tile in hand
        No input
        No output"""
        self.canvas_tile = tk.Canvas(self.f_graph, bg = "#EFEFE1", width = 400, height = 400)
        self.hand_image()
        self.canvas_tile.pack(side = tk.TOP, anchor = 'e')

    def hand_image(self):
        """Displays the tile in hand in its canvas and binds it to the rotation function
        No input
        No output"""
        #filepath_t, filepath_tr = self.controller.hand: #hand should be reduced to (filepathTile, filepathTreas|None) CONTROLLER
        filepath_ti = "\\tile_corner.png" # address
        filepath_tr = "\\tr_spider.png" # address
        # Set the image of the tile in hand
        self.tile_h = tk.PhotoImage(file = self.folder + filepath_ti)
        self.tile_h_resized = self.tile_h.zoom(3, 3)
        self.bg_h = self.canvas_tile.create_image(200, 175, image = self.tile_h_resized)
        self.canvas_tile.lower(self.bg_h)

        # Set the image of the treasure of the tile (if any) FUNCTION TO CREATE
        if filepath_tr != None:
            self.treas_h = tk.PhotoImage(file = self.folder + filepath_tr)
            self.treas_h_resized = self.treas_h.zoom(3, 3)
            self.fg_h = self.canvas_tile.create_image(205, 175, image = self.treas_h_resized)
            self.canvas_tile.lift(self.fg_h)
              
        # Useful for the rotation display
        self.orientation_h = 1 
        self.dict_r ={}
        

    def turn_tile_buttons(self):
        """Creates the buttons next to the hand allowing to change the orientation of the tile in hand
        No input
        No output"""
        # Turning buttons
        self.button_counterclockwise = ctk.CTkButton(self.f_graph, text = "⤹", font = ('Calibri', 30, 'bold'), width = 33, height = 33, bg_color = "#EFEFE1", fg_color = "goldenrod", hover_color = "red4")
        self.button_clockwise = ctk.CTkButton(self.f_graph, text = "⤸", font = ('Calibri', 30, 'bold'), width = 33, height = 33, bg_color = "#EFEFE1", fg_color = "goldenrod", hover_color = "red4")
        self.button_counterclockwise.place(x = 980, y = 610)
        self.button_clockwise.place(x = 1068, y = 610)
        self.button_counterclockwise.bind('<Button-1>', lambda event: self.turn_hand_tile(-1))
        self.button_clockwise.bind('<Button-1>', lambda event: self.turn_hand_tile(1))
        

    def turn_hand_tile(self, sens):
        """Rotates the tile in hand
        input = sens, the direction of the rotation
        no output"""
        tilec = './tile_t.png' #CONTROLLER
        #set new orientation
        self.orientation_h += sens
        #prepare the image tile
        self.image_library_i()#displace that in a larger theme maybe
        if tilec == './tile_corner.png':
            self.c_tile = self.tile_c
        elif tilec == './tile_t.png':
            self.c_tile = self.tile_t
        else:
            self.c_tile = self.tile_s
        
        self.rotatedc_tile=rotate_image_h(self.c_tile, self.orientation_h)
        self.dict_r[1]=self.rotatedc_tile  
        #replace self.bg_h with the rotated image
        self.canvas_tile.delete(self.bg_h) #delete the old image
        self.bg_h = self.canvas_tile.create_image(200, 175, image = self.dict_r[1]) #create the new image
        self.canvas_tile.lower(self.bg_h)

        
    def validate_button(self):
        """Creates the button under the hand to validate the chosen orientation and insertion
        No input
        No output"""    
        self.button_valid = ctk.CTkButton(self.f_graph, text = "✔", font = ('Calibri', 30, 'bold'), width = 50, height = 50, bg_color = '#E8E4CC', fg_color = '#009900', hover_color = "green4")
        self.button_valid.bind('<Button-1>', self.check_insertion)
        self.button_valid.place(x = 1015, y = 605)
        
    
    def check_insertion(self, event):
        """Verify that the player did select where to insert the tile in hand
        No input
        No output"""
        if self.selected_button == None:
            self.selection_error_messagebox()
        else:
            self.anim_slide_tiles()
    
    def selection_error_messagebox(self):
        """Opens a messagebox reminding the player that they didn't choose where to insert the tile although it is mandatory
        No input
        No output"""
        self.msg_error = tk.messagebox.showwarning("Selection error", "You need to select an insertion button.\nPlease choose where you want to insert the tile.")
     
    def image_library(self):
        """Loads and sizes all PNG files
        No input
        No output"""
        self.image_dict = {}
        # Load the 3 tile images and resize them
        self.tile_c = tk.PhotoImage(file = self.folder + '\\tile_corner.png')
        self.tile_t = tk.PhotoImage(file = self.folder + '\\tile_t.png')
        self.tile_s = tk.PhotoImage(file = self.folder + '\\tile_straight.png')

    def image_library_i(self):
        """Loads and sizes all PNG files as Images (this object type can be rotated)
        No input
        No output"""
        self.image_dict = {}
        # Load the 3 tile images and resize them
        self.tile_c = Image.open(self.folder + '\\tile_corner.png')
        self.tile_t = Image.open(self.folder + '\\tile_t.png')
        self.tile_s = Image.open(self.folder + '\\tile_straight.png')
        self.target_pic = tk.PhotoImage(file = self.folder + '\\target.png')

    def grid_images(self):
        """Associates tiles to treasures and stocks them 
        Displays the tiles on the board in its canvas and binds it to the sliding
        No input
        No output"""
        graphics_dict = {(0, 0): {'filepathTile' : './tile_corner.png', 'filepathTreas': None, 'orientation': 1, 'pawns': ['blue']}, 
                         (0, 1): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []},
                         (0, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_helmet.png', 'orientation': 0, 'pawns': []}, 
                         (0, 3): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (0, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_candelabrum.png', 'orientation': 0, 'pawns': []},
                         (0, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_rat.png', 'orientation': 2, 'pawns': []},
                         (0, 6): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': ['red']}, 
                         (1, 0): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_ghost.png', 'orientation': 3, 'pawns': []}, 
                         (1, 1): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, 
                         (1, 2): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_owl.png', 'orientation': 0, 'pawns': []}, 
                         (1, 3): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, 
                         (1, 4): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, 
                         (1, 5): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, 
                         (1, 6): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (2, 0): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_sword.png', 'orientation': 3, 'pawns': []}, 
                         (2, 1): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_scarab.png', 'orientation': 0, 'pawns': []}, 
                         (2, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_emerald.png', 'orientation': 3, 'pawns': []}, 
                         (2, 3): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []},
                         (2, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_chest.png', 'orientation': 0, 'pawns': []}, 
                         (2, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 1, 'pawns': []}, 
                         (2, 6): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_ring.png', 'orientation': 1, 'pawns': []}, 
                         (3, 0): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (3, 1): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_gnome.png', 'orientation': 2, 'pawns': []}, 
                         (3, 2): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_salamander.png', 'orientation': 1, 'pawns': []}, 
                         (3, 3): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, 
                         (3, 4): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (3, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_moth.png', 'orientation': 2, 'pawns': []}, 
                         (3, 6): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_dragon.png', 'orientation': 3, 'pawns': []},
                         (4, 0): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_skull.png', 'orientation': 3, 'pawns': []}, 
                         (4, 1): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_genie.png', 'orientation': 2, 'pawns': []}, 
                         (4, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_keys.png', 'orientation': 2, 'pawns': []},
                         (4, 3): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (4, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_crown.png', 'orientation': 1, 'pawns': []}, 
                         (4, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (4, 6): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_map.png', 'orientation': 1, 'pawns': []}, 
                         (5, 0): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (5, 1): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (5, 2): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (5, 3): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_bat.png', 'orientation': 3, 'pawns': []}, 
                         (5, 4): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, 
                         (5, 5): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, 
                         (5, 6): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 1, 'pawns': []},       
                         (6, 0): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': ['green']}, 
                         (6, 1): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, 
                         (6, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_purse.png', 'orientation': 2, 'pawns': []}, 
                         (6, 3): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_sorceress.png', 'orientation': 0, 'pawns': []}, 
                         (6, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_grimoire.png', 'orientation': 2, 'pawns': []},                          
                         (6, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []},
                         (6, 6): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}} #CONTROLLER
        self.image_library_i()#move that to higher function
        # Get grid
        # For position, tile in self.controller.grid: #grid should be reduced to (positionTuple)={filepathTile, filepathTreas|None, list of colors or empty list]
        i = 0
        self.treasures = {}
        self.tiles = {}
        self.tile_dict  = {}
        self.treasure_dict = { }
        for position, tile in graphics_dict.items():
            i += 1
            #position
            co0 = position[1]
            li0 = position[0]
            co = 75 + co0*100
            li = 75 + li0*100
            #treasure display
            if tile["filepathTreas"]!=None:
                #create and position treasure
                self.treasures[i] = tk.PhotoImage(file = self.folder + tile["filepathTreas"])
                
                new_fg = self.canvas_board.create_image(co, li, image = self.treasures[i])
                
                self.canvas_board.lift(new_fg)
                self.canvas_board.tag_bind(new_fg, '<Button-1>', self.click_tile)
                
            else:
                new_fg = None
                
            # Initialisation
            if tile["filepathTile"] == './tile_corner.png':
                self.new_tile = self.tile_c
            elif tile["filepathTile"] == './tile_t.png':
                self.new_tile = self.tile_t
            else:
                self.new_tile = self.tile_s

            # Orientate
            self.tiles[i] = rotate_image(self.new_tile, tile["orientation"])
            
            # Display
            new_bg = self.canvas_board.create_image(co, li, image = self.tiles[i])
            self.canvas_board.lower(new_bg)
            self.canvas_board.tag_bind(new_bg, '<Button-1>', self.click_tile)
            

            self.tile_dict[(li0,co0)] = new_bg
            self.treasure_dict[(li0, co0)] = new_fg
    

    def anim_slide_tiles(self):
        """pour slider les tiles à l'écran
        input : tuple   """
        #Get which row/column moves
        ##If it is a line
        if self.chosen_pos[1]==0 :
            init_pos = (self.chosen_pos[0], -1)
            out_pos = (self.chosen_pos[0], 6)
            self.slider = "lin_r"
        elif self.chosen_pos[1]==6:
            init_pos = (self.chosen_pos[0], 7)
            out_pos = (self.chosen_pos[0], 0)
            self.slider ='lin_l'
        ##If it s a column
        elif self.chosen_pos[0]==0:
            init_pos = (-1, self.chosen_pos[1])
            out_pos = (6, self.chosen_pos[1])
            self.slider = 'col_d'
        elif self.chosen_pos[0]==6:
            init_pos = (7, self.chosen_pos[1])
            out_pos = (0, self.chosen_pos[1])
            self.slider = 'col_u'
        
        #Add the new tile at the beginning of the row/column TO BE CHANGED FOR CONTROLLER
        treasure = None
        treasure_filepath = None
        hand_filepath = './tile_corner.png'
        hand_orientation = 2
        
        # Initialisation of position
        co0 = init_pos[1]
        li0 = init_pos[0]
        co = 75 + co0*100
        li = 75 + li0*100

        # New treasure
        # place_a_treasure FUNCTION TO CREATE
        #if self.controller.hand.tile.treasure != None: CONTROLLER
        if treasure != None:
                #create and position treasure
                if self.treasures.get(init_pos) == None:
                    self.treasures[init_pos] = []
                self.treasures[init_pos].append(tk.PhotoImage(file = self.folder + treasure_filepath))#CONTROLLER
                
                #self.treasures[init_pos] = tk.PhotoImage(file = self.folder + self.controller.hand.tile.treasure.filepath) CONTROLLER
                #display
                new_fg = self.canvas_board.create_image(co, li, image = self.treasures[init_pos][len(self.treasures[init_pos])-1])
                self.canvas_board.lift(new_fg)
                self.canvas_board.tag_bind(new_fg, '<Button-1>', self.click_tile)
        else:
            new_fg = None     

        # New tile
        #plae_a_tile FUNCTION TO CREATE
        #if self.controller.hand.filepath == './tile_corner.png':
        if hand_filepath == './tile_corner.png':
            self.new_tile = self.tile_c
        #elif self.controller.hand.filepath == './tile_t.png':
        elif hand_filepath == './tile_t.png':
            self.new_tile = self.tile_t
        else:
            self.new_tile = self.tile_s

        # Orientate
        
        if self.tiles.get(init_pos) == None:
            self.tiles[init_pos] = []
        self.tiles[init_pos].append(rotate_image(self.new_tile,random.randint(0,3)))#CONTROLLER
        # Display
        new_bg = self.canvas_board.create_image(co, li, image = self.tiles[init_pos][len(self.tiles[init_pos])-1])
        self.canvas_board.lift(new_bg)
        self.canvas_board.tag_bind(new_bg, '<Button-1>', self.click_tile)
        
        # Storage
        self.tile_dict[init_pos] = new_bg
        self.treasure_dict[init_pos] = new_fg
        self.pawn_dict[init_pos] = None

        # Storage update
        # Delete the tiles+treasures pushed out of the board
        #self.controller.hand = self.tile_dict[out_pos] CONTROLLER
        self.canvas_board.delete(self.tile_dict[out_pos])
        #self.controller.hand.treas = self.treasure_dict[out_pos] CONTROLLER
        self.canvas_board.delete(self.treasure_dict[out_pos])
        
        # Move the pawns pushed out of the board
        if self.pawn_dict[out_pos] != None:
            for pawn in self.pawn_dict[out_pos]:

                # place_a_pawn FUNCTION TO  CREATE
                co = 75 + 100*init_pos[1]
                li = 75 + 100*init_pos[0]
                
                # Find the color of the circle pawn and move in consequence
                
                
                color = self.canvas_board.itemcget(pawn,  "fill")
                
                if color == "blue": 
                    self.canvas_board.coords(pawn, co-20, li+20, co, li  )
                    
                elif color == "red": 
                    self.canvas_board.coords(pawn, co, li, co+20, li-20 ) 
                    
                elif color == "green": 
                    self.canvas_board.coords(pawn, co-20, li, co, li-20  )
                    
                else:
                    self.canvas_board.coords(pawn, co, li+20, co+20, li )
                #m Mve it in storage
                self.canvas_board.lift(pawn)
                if self.pawn_dict[init_pos] == None:
                    self.pawn_dict[init_pos] = []
                self.pawn_dict[init_pos].append(self.pawn_dict[out_pos].pop(0))

        # Change the position tuples of the tiles and treasures and pawns moved
        if self.slider == "col_u" or self.slider == "lin_l":
            r = (0, 7, 1)
        else:
            r = (6, -1, -1)
        for i in range(r[0], r[1], r[2]):
            if 'col' in self.slider:
                self.tile_dict[(i, self.chosen_pos[1])] = self.tile_dict[i+r[2], self.chosen_pos[1]]
                self.treasure_dict[(i, self.chosen_pos[1])] = self.treasure_dict[i+r[2], self.chosen_pos[1]]
                self.pawn_dict[(i, self.chosen_pos[1])] = self.pawn_dict[i+r[2], self.chosen_pos[1]]
            else:
                self.tile_dict[(self.chosen_pos[0], i)] = self.tile_dict[(self.chosen_pos[0], i+r[2])]
                self.treasure_dict[(self.chosen_pos[0], i)] = self.treasure_dict[(self.chosen_pos[0], i+r[2])]
                self.pawn_dict[(self.chosen_pos[0], i)] = self.pawn_dict[(self.chosen_pos[0], i+r[2])]
        self.tile_dict[init_pos]= None
        self.treasure_dict[init_pos]= None
        
        #start the animation
        self.lancer()

        #comunicate the motuon to the controller
        #self.controller.insert_hand() CONTROLLER

        # Handle buttons
        if self.opposite_button_old != None:
            self.opposite_button_old.configure(fg_color = "goldenrod", state="normal")
        self.opposite_button.configure(fg_color = "grey", state="disabled")
        self.selected_button.configure(fg_color = "goldenrod")
        # Handle turn unrolling
        self.pawn_motion = True
        self.cross = False

        
    


    def lancer(self):
        """
        Lancement de la boucle du timer si elle n'est pas déjà active
        """
        self.i = 0
        if not(self.running) :
            self.timer_loop()
        self.running = True
        
        


    def stop(self):
        """
        Arrêt de la boucle du timer si elle est active
        """        
        if self.running :
            self.f_graph.after_cancel(self.timer_id) 
        self.running = False
        
        #self.tile_dict[init_pos]= None


    def timer_loop(self):
        """
        Boucle gérée par le timer : déplacement et affichage de l'image
        """
        if self.slider == "col_d" or self.slider == "lin_r":
            r = (0, 7, 1)
        else:
            r = (6, -1, -1)
        
        for i in range(r[0],r[1],r[2]):
            if "col" in self.slider:
                self.canvas_board.move(self.tile_dict[(i,self.chosen_pos[1])], 0, r[2] * 10)
                
                if self.treasure_dict[(i,self.chosen_pos[1])] != None:
                    self.canvas_board.move(self.treasure_dict[(i,self.chosen_pos[1])], 0, r[2]*10)
                    self.canvas_board.lift(self.treasure_dict[(i,self.chosen_pos[1])])
                    
                if self.pawn_dict[(i,self.chosen_pos[1])] != None:
                    for pawn in self.pawn_dict[(i,self.chosen_pos[1])]:
                        self.canvas_board.move(pawn, 0, r[2]*10)
                        self.canvas_board.lift(pawn)
            else:
                self.canvas_board.move(self.tile_dict[(self.chosen_pos[0], i)], r[2] *10, 0)
                
                if self.treasure_dict[(self.chosen_pos[0], i)] != None:  
                    self.canvas_board.move(self.treasure_dict[(self.chosen_pos[0], i)], r[2]* 10, 0)
                    self.canvas_board.lift(self.treasure_dict[(self.chosen_pos[0], i)])
                    
                if self.pawn_dict[(self.chosen_pos[0], i)] != None:
                    for pawn in self.pawn_dict[(self.chosen_pos[0], i)]:
                        self.canvas_board.move(pawn, r[2]*10, 0)
                        self.canvas_board.lift(pawn)
                    
        self.i += 1
        if self.i == 10:
           self.stop()
        else:
            self.timer_id = self.f_graph.after(100, self.timer_loop)

        
    def place_pawns(self):
        """place circles for the pawn"""
        # Place pawns and bind them to moving animation
        graphics_dict = {(0, 0): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 1, 'pawns': ['blue']}, 
                         (0, 6): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': ['red']}, 
                         (6, 6): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, 
                         (6, 0): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': ['green']}, 
                         (0, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_helmet.png', 'orientation': 0, 'pawns': []}, 
                         (0, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_candelabrum.png', 'orientation': 0, 'pawns': []}, 
                         (2, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_chest.png', 'orientation': 0, 'pawns': []}, 
                         (2, 0): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_sword.png', 'orientation': 3, 'pawns': []}, 
                         (4, 0): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_skull.png', 'orientation': 3, 'pawns': []}, 
                         (2, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_emerald.png', 'orientation': 3, 'pawns': []}, 
                         (2, 6): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_ring.png', 'orientation': 1, 'pawns': []}, 
                         (4, 6): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_map.png', 'orientation': 1, 'pawns': []}, 
                         (4, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_crown.png', 'orientation': 1, 'pawns': []}, 
                         (4, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_keys.png', 'orientation': 2, 'pawns': []}, 
                         (6, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_purse.png', 'orientation': 1, 'pawns': []}, 
                         (6, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_grimoire.png', 'orientation': 2, 'pawns': []}, 
                         (0, 1): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, 
                         (0, 3): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (0, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_rat.png', 'orientation': 2, 'pawns': []}, 
                         (1, 0): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_ghost.png', 'orientation': 3, 'pawns': []}, 
                         (1, 1): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, 
                         (1, 2): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_owl.png', 'orientation': 0, 'pawns': []}, 
                         (1, 3): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, 
                         (1, 4): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, 
                         (1, 5): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, 
                         (1, 6): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (2, 1): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_scarab.png', 'orientation': 0, 'pawns': []}, 
                         (2, 3): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, 
                         (2, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 1, 'pawns': []}, 
                         (3, 0): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (3, 1): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_gnome.png', 'orientation': 2, 'pawns': []}, 
                         (3, 2): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_salamander.png', 'orientation': 1, 'pawns': []}, 
                         (3, 3): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, 
                         (3, 4): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (3, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_moth.png', 'orientation': 2, 'pawns': []}, 
                         (3, 6): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_dragon.png', 'orientation': 3, 'pawns': []}, 
                         (4, 1): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_genie.png', 'orientation': 2, 'pawns': []}, 
                         (4, 3): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (4, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (5, 0): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (5, 1): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (5, 2): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, 
                         (5, 3): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_bat.png', 'orientation': 3, 'pawns': ['yellow']}, 
                         (5, 4): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, 
                         (5, 5): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, 
                         (5, 6): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 1, 'pawns': []}, 
                         (6, 1): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, 
                         (6, 3): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_sorceress.png', 'orientation': 0, 'pawns': []}, 
                         (6, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}}
        # Pawn storage
        self.pawn_dict ={}
        # Pawn display
        for position, tile in graphics_dict.items():
            if tile["pawns"]!=None:
                #position
                li0 = position[0]
                co0 = position[1]
                li = 75 + li0*100
                co = 75 + co0*100
                #create circles on the tile
                new_pawns = []
                for color in tile["pawns"]:
                    if color == "blue": 
                        new_pawn = self.canvas_board.create_oval(co-20, li+20, co, li, fill = color  )
                        
                    elif color == "red": 
                        new_pawn =self.canvas_board.create_oval(co, li, co+20, li-20, fill = color  ) 
                        
                    elif color == "green": 
                        new_pawn =self.canvas_board.create_oval(co-20, li, co, li-20, fill = color  )
                        
                    else:
                        new_pawn =self.canvas_board.create_oval(co, li+20, co+20, li, fill = color  )

                    self.canvas_board.lift(new_pawn)
                    new_pawns.append(new_pawn)
                self.pawn_dict[position] = new_pawns

    
    def turn_over(self, event):
        #validates that the player is done with his turn and communicates the changes of player back and forth with the controller
        #no input
        #output
        #throw animation to move pawn when checked it is possible
        #slide buttons preparation
        #this will gather the information necessary for move pawn animation
        self.dict_anim = {"path": [(0,5),(1,5),(2,5), (2,4)], "pawn": self.pawn_dict[(0,0)][0], "previous_step": (0,0)}
        
        self.anim_move_pawn()
        #useful for turn over
        self.opposite_button_old = self.opposite_button
        self.opposite_button = None
        self.pawn_motion = False

    def anim_move_pawn(self):
        """animates the movement of the pawn to the destination"""
        
        if not(self.running_pawn):
            self.timer_loop_pawn()
        self.running_pawn = True       

    
    def timer_loop_pawn(self):
        """moves the pawn one step at a time"""

        path = self.dict_anim["path"]
        pawn = self.dict_anim["pawn"]
        previous_step = self.dict_anim["previous_step"]

        obj = path.pop(0)
        step_x = (obj[1]-previous_step[1])*100
        step_y = (obj[0]-previous_step[0])*100
        print(step_x, step_y)
        self.canvas_board.move(pawn, step_x, step_y)
        self.canvas_board.lift(pawn)

        self.pawn_dict[previous_step].remove(pawn)
        self.pawn_dict[obj].append(pawn)
        self.dict_anim["previous_step"] = obj  
        if path != []:
            self.timer_id_pawn = self.f_graph.after(2000, self.timer_loop_pawn)  
        else:
            self.stop_pawn()

    def stop_pawn(self):
        """stops the animation of the pawn"""
        if self.running_pawn :
            self.f_graph.after_cancel(self.timer_id_pawn) 
        self.running_pawn = False
        print("stop_pawn")
        
    def click_tile(self, event):
        """places a cross where the player wants to place the pawn and registers the grid coordinates"""
        #si j ai le droit de bouger un pion:
        if self.pawn_motion:
            pos = self.canvas_board.coords(self.canvas_board.find_withtag('current')[0])# get tile position with coords
            
            #if there is a cross
            if self.cross:
                self.canvas_board.delete(self.target)
            self.target = self.canvas_board.create_image(pos[0], pos[1], image = self.target_pic)
            self.cross = True
            self.canvas_board.lift(self.target)
             
            # take note of the objective coordinates
            self.destination_co = (pos[0]-75)/100
            self.destination_li = (pos[1]-75)/100    
        else:
            self.msg_error2 = tk.messagebox.showwarning("Selection error", "You can't choose a displacement now.\nPlease insert your tile first.")
     


    """   
     
    def process_click(self, event):
        
        Gestion du clic éventuel sur l'image en mouvement

        
        if self.running :
            self.stop(None)
            self. id_boom = self.canevas.create_image((self.x,self.y), anchor = "nw", image = self.boom)
            self.count += 1
            messagebox.showinfo("Gagné !", f"Nombre de points : {self.count}")
            self.lancer(None)
               
    #inspi
    def place_objects():
            grid = #board read through message
            for position, tile in grid.items():
                #get the type of tile and orientation
                self.background = PhotoImage(file='C:/Users/cleme/Pictures/meduse.png')
                self.item = self.f_graph.canvas.create_image(100, 100, image=self.background, anchor='c')
                self.f_graph.canvas.lower(self.item)
                #ajouter la taille au dico avec son ident
            #read the current player, display his name and his objective
            #ajouter boutons pour tourner la tuile et placer  
        #graphic window
            #initialize
            #set background
            #read grid to fill the graphic grid + read the treasure and pawn to draw them...
            #read the hand and display it
            #read the current player, display his name and his objective


    récupération des positions de clic
    def affiche_info_ville(self,event):
            self.text_area.delete("1.0", "end")
            mouseX = event.x
            mouseY = event.y
            ident = self.f_graph.canevas.find_withtag("current")[0]
            item_clicked = self.dicoSommetsGraphiques[ident]
            self.text_area.insert(tk.INSERT,item_clicked)
            
            
            
            
             def supprime_oval(self, event):
        mouseX = event.x
        mouseY = event.y
        # find the circle closest to the mouse click
        # and remove it from the canvas
        x = self.fen_graphique.canevas.canvasx(mouseX)
        y = self.fen_graphique.canevas.canvasy(mouseY)
        item = self.fen_graphique.canevas.find_closest(x, y, halo=None, start=None)
        self.fen_graphique.canevas.delete(item)
        """
    
def rotate_image(img, orientation):
    img = img.rotate(orientation* -90)
    return (ImageTk.PhotoImage(img))
def rotate_image_h(img, orientation):
    w,h = img.size
    img = img.resize((3*w,3*h))
    img_f = rotate_image(img, orientation)
    return (img_f)
    


        
        
if __name__ == "__main__":
    app = GameWindow()
    app.root.mainloop()