import tkinter as tk
import customtkinter as ctk # "upgrade" for tkinter with better esthetics

from PIL import Image, ImageTk # Librairy to manage images

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
        #self.controller.init_control()

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
            self.playernames.append(name)
    
    def graphic_window(self):
        """Creates the graphic window for current game display
        No input
        No output"""
        if (self.f_graph == None) :
            self.f_graph = tk.Toplevel(self.root)
            self.f_graph.title('Labyrinth - Current game')
            self.f_graph.iconbitmap('tr_chest.ico')      
            self.f_graph.geometry("1500x875") 
            self.f_graph.config(background = '#EFEFE1')
            
            # Button for players to indicate they finished their turn
            self.button_done = ctk.CTkButton(self.f_graph, text = "My turn is over.", corner_radius = 8, height = 30, width = 15, fg_color = "goldenrod", hover_color = "DodgerBlue4", font = ('Calibri', 20))
            #self.button_done.bind('<Button-1>', self.turn_over())
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
        self.f_graph = None 

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
        self.bouton01.bind('<Button-1>', lambda event: self.select_insertion_button((0,1), self.bouton01))
        self.bouton01.place(x = 161, y = 1)

        self.bouton03 = ctk.CTkButton(self.f_graph, text = "▼", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton03.bind('<Button-1>', lambda event:  self.select_insertion_button( (0,3), self.bouton03))
        self.bouton03.place(x = 318, y = 1)

        self.bouton05 = ctk.CTkButton(self.f_graph, text = "▼", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton05.bind('<Button-1>', lambda event: self.select_insertion_button( (0,5), self.bouton05))
        self.bouton05.place(x = 475, y = 1)

        # Left side buttons
        self.bouton10 = ctk.CTkButton(self.f_graph, text = "►", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton10.bind('<Button-1>', lambda event: self.select_insertion_button( (1,0), self.bouton10))
        self.bouton10.place(x = 1, y = 161)

        self.bouton30 = ctk.CTkButton(self.f_graph, text = "►", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton30.bind('<Button-1>',  lambda event: self.select_insertion_button((3,0), self.bouton30))
        self.bouton30.place(x = 1, y = 318)

        self.bouton50 = ctk.CTkButton(self.f_graph, text = "►", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton50.bind('<Button-1>', lambda event: self.select_insertion_button((5,0), self.bouton50))
        self.bouton50.place(x = 1, y = 475)

        # Bottom side buttons
        self.bouton61 = ctk.CTkButton(self.f_graph, text = "▲", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton61.bind('<Button-1>',  lambda event: self.select_insertion_button((6,1), self.bouton61))
        self.bouton61.place(x = 161, y = 635)

        self.bouton63 = ctk.CTkButton(self.f_graph, text = "▲", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton63.bind('<Button-1>', lambda event: self.select_insertion_button((6,3), self.bouton63))
        self.bouton63.place(x = 318, y = 635)

        self.bouton65 = ctk.CTkButton(self.f_graph, text = "▲", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton65.bind('<Button-1>', lambda event: self.select_insertion_button((6,5), self.bouton65))
        self.bouton65.place(x = 475, y = 635)

        # Right side buttons
        self.bouton16 = ctk.CTkButton(self.f_graph, text = "◄", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton16.bind('<Button-1>', lambda event: self.select_insertion_button((1,6), self.bouton16))
        self.bouton16.place(x = 635, y = 161)

        self.bouton36 = ctk.CTkButton(self.f_graph, text = "◄", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton36.bind('<Button-1>', lambda event: self.select_insertion_button((3,6), self.bouton36))
        self.bouton36.place(x = 635, y = 318)
        
        self.bouton56 = ctk.CTkButton(self.f_graph, text = "◄", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton56.bind('<Button-1>', lambda event: self.select_insertion_button((5,6), self.bouton56))
        self.bouton56.place(x = 635, y = 475)
    
    def select_insertion_button(self, pos, button):
        """Changes the color of the selected button and gets its position"""
        # Change color : when clicked, becomes red4 and stays that way unless a different insertion button was selected
        # Find button selected by the player
        button.configure(fg_color = "red4")
        if self.selected_button != None:
            self.selected_button.configure(fg_color = "goldenrod")
        self.selected_button = button
        # Get button position and call anim_slide_tile
        self.chosen_pos = pos
        print(self.chosen_pos)

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
        #filepath_tr = self.controller.hand
        filepath_tr = "\\tr_crown.png" # address
        # Treasure image settings
        self.treas_c = tk.PhotoImage(file = self.folder + filepath_tr)
        self.treas_c_resized = self.treas_c.zoom(3, 3)
        self.fg_c = self.canvas_card.create_image(160, 212, image = self.treas_c_resized)

        self.canvas_card.lift(self.fg_c)
        
        #display the treasure using the controller
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
        #filepath_t, filepath_tr = self.controller.hand: #hand should be reduced to (filepathTile, filepathTreas|None)
        filepath_ti = "\\tile_corner.png" # address
        filepath_tr = "\\tr_spider.png" # address
        # Set the image of the tile in hand
        self.tile_h = tk.PhotoImage(file = self.folder + filepath_ti)
        self.tile_h_resized = self.tile_h.zoom(3, 3)
        self.bg_h = self.canvas_tile.create_image(200, 175, image = self.tile_h_resized)
        self.canvas_tile.lower(self.bg_h)

        # Set the image of the treasure of the tile (if any)
        if filepath_tr != None:
            self.treas_h = tk.PhotoImage(file = self.folder + filepath_tr)
            self.treas_h_resized = self.treas_h.zoom(3, 3)
            self.fg_h = self.canvas_tile.create_image(205, 175, image = self.treas_h_resized)
            self.canvas_tile.lift(self.fg_h)
            self.image_dict[(self.tile_h, self.treas_h, None)] = (7, 7)  
        # In case there is no treasure on the current tile in hand
        else:
            self.image_dict[(self.tile_h, None, None)]=(7,7)  
        
        #display the hand using the controller
                #choose the tile
                #place the treasure on it
                #place the image on its spot
            #bind method de rotation 
            #stock the tile in a dict

    def turn_tile_buttons(self):
        """Creates the buttons next to the hand allowing to change the orientation of the tile in hand
        No input
        No output"""
        # Turning buttons
        self.button_counterclockwise = ctk.CTkButton(self.f_graph, text = "⤹", font = ('Calibri', 30, 'bold'), width = 33, height = 33, bg_color = "#EFEFE1", fg_color = "goldenrod", hover_color = "red4")
        self.button_clockwise = ctk.CTkButton(self.f_graph, text = "⤸", font = ('Calibri', 30, 'bold'), width = 33, height = 33, bg_color = "#EFEFE1", fg_color = "goldenrod", hover_color = "red4")
        self.button_counterclockwise.place(x = 980, y = 610)
        self.button_clockwise.place(x = 1068, y = 610)
        self.button_counterclockwise.bind('<Button-1>', lambda event: self.turn_counterclockwise())
        
    def turn_counterclockwise(self):
        tile = "\\tile_corner.png" # Controller
        self.image_library_i()
        if tile == './tile_corner.png':
            self.new_tile = self.tile_c
        elif tile == './tile_t.png':
            self.new_tile = self.tile_t
        else:
            self.new_tile = self.tile_s
        self.rotatedcc_tile = rotate_image(self.new_tile, -1)
        #self.rotatedcc_tile = tk.PhotoImage(self.rotatedcc_tile)
        self.tile_cc_resized = (tk.PhotoImage(self.rotatedcc_tile)).zoom(3, 3)
        self.canvas_tile.delete(self.bg_h)
        self.bg_cc = self.canvas_tile.create_image(200, 175, image = self.tile_cc_resized)
        self.canvas_tile.lift(self.bg_cc)
        
    def validate_button(self):
        """Creates the button under the hand to validate the chosen orientation and insertion
        No input
        No output"""    
        self.button_valid = ctk.CTkButton(self.f_graph, text = "✔", font = ('Calibri', 30, 'bold'), width = 50, height = 50, bg_color = '#E8E4CC', fg_color = '#009900', hover_color = "green4")
        self.button_valid.bind('<Button-1>', self.check_insertion)
        self.button_valid.place(x = 1015, y = 605)
        # bind it to controller somehow
    
    def check_insertion(self, event, selected_button):
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
        tk.messagebox.showwarning("Selection error", "You need to select an insertion button.\nPlease choose where you want to insert the tile.")
     
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
                         (6, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_purse.png', 'orientation': 1, 'pawns': []}, 
                         (6, 3): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_sorceress.png', 'orientation': 0, 'pawns': []}, 
                         (6, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_grimoire.png', 'orientation': 2, 'pawns': []},                          
                         (6, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []},
                         (6, 6): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}} 
        self.image_library_i()
        # Get grid
        # For position, tile in self.controller.grid: #grid should be reduced to (positionTuple)={filepathTile, filepathTreas|None, list of colors or empty list]
        i = 0
        self.treasures = {}
        self.tiles = {}
        for position, tile in graphics_dict.items():
            i += 1
            # Position
            x0 = position[0]
            y0 = position[1]
            x = 78 + x0*100
            y = 78 + y0*100
            # Treasure display
            if tile["filepathTreas"] != None:
                # Create and position treasure
                self.treasures[i] = tk.PhotoImage(file = self.folder + tile["filepathTreas"])
                #print('1')
                new_fg = self.canvas_board.create_image(y, x, image = self.treasures[i])
                #print('2')
                self.canvas_board.lift(new_fg)
                #orientate
                #self.new_treas = Image.open(self.folder + tile['filepathTreas'])
                #self.treasures[i] = rotate_image(self.new_tile, tile["orientation"])
                
                #display
                #new_fg = self.canvas_board.create_image(y, x, image = self.treasures[i])
                #self.canvas_board.lift(new_fg)
            else:
                treas = None
                
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
            new_bg = self.canvas_board.create_image(y, x, image = self.tiles[i])
            self.canvas_board.lower(new_bg)            

            self.image_dict[new_bg] = (x, y)
                

        #use the grid to create all the other tiles
            #choose the tile
            #place the treasure on it
            #place the image on its spot
        #bind method de rotation 
        #stock the tile in a dict
               

        #self.tile_c = tk.PhotoImage(file = self.folder + '\\tile_corner.png')
        #self.item2 = self.f_graph.canvas_board.create_image(100, 100, image = self.tile_c)
        #self.treas1 =  tk.PhotoImage(file = self.folder + '\\tr_bat.png')
        #self.item21 = self.f_graph.canvas_board.create_image(100, 100, image = self.treas1)
        


        #self.f_graph.canvas_board.lift(self.item2)
        #self.f_graph.canvas_board.lift(self.item21)
        #self.item3 = self.f_graph.canvas_board.create_image(246, 100, image = self.tile_c)
        #self.f_graph.canvas_board.lift(self.item3)
        #self.item4 = self.f_graph.canvas_board.create_image(100, 246, image = self.tile_c)
        #self.f_graph.canvas_board.lift(self.item4)


    def anim_silde_tiles(self, event, pos):
        """pour slider les tiles à l'écran
        input : tuple"""
    def anim_slide_tiles(self):
        """pour slider les tiles à l'écran"""
        pass
        #effacer bout
        # animer translation des 6 d'avant
        # ajouter la première
        
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
                         (5, 3): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_bat.png', 'orientation': 3, 'pawns': []}, 
                         (5, 4): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, 
                         (5, 5): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, 
                         (5, 6): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 1, 'pawns': []}, 
                         (6, 1): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, 
                         (6, 3): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_sorceress.png', 'orientation': 0, 'pawns': []}, 
                         (6, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}}
        
        # Pawn display
        for position, tile in graphics_dict.items():
            if tile["pawns"] != None:
                # Position
                x0 = position[0]
        y0 = position[1]
        x = 70 + x0*100
        y = 70 + y0*100
        # Create circles on the tile
        for color in tile["pawns"]:
            if color == "blue": 
                new_pawn = self.canvas_board.create_oval(x-20, y+10, x, y+10, fill = color)
            elif color == "red": 
                new_pawn =self.canvas_board.create_oval(x-20, y-10, x, y-10, fill = color) 
            elif color == "green": 
                new_pawn = self.canvas_board.create_oval(x+20, y+10, x, y+10, fill = color)      
            else:
                new_pawn = self.canvas_board.create_oval(x+20, y-10, x, y-10, fill = color)  
            self.canvas_board.lift(new_pawn)

    """
    def turn_over(self, event):
        #validates that the player is done with his turn and communicates the changes of player back and forth with the controller
        #no input
        #output

        
               
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
            self.text_area.insert(tk.INSERT,item_clicked)"""
    
def rotate_image(img, orientation):
    img = img.rotate(orientation* -90)
    return (ImageTk.PhotoImage(img))


        
        
if __name__ == "__main__":
    app = GameWindow()
    app.root.mainloop()