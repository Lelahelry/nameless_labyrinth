import random
import tkinter as tk
import customtkinter as ctk
import time
from PIL import Image, ImageTk

ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class GameWindow():
    def __init__(self, controller):
        from controller import GameController

        self.controller: GameController = controller

        self.root = ctk.CTk()
        self.root.title("Labyrinth - the aMAZEing game") # Title of the window
        self.root.configure(bg='#103A86')
        self.root.iconbitmap('tr_chest.ico') # Icon of the window
        self.root.geometry("1200x700") # Initial dimensions of the window
            
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

        # Controller creation
        self.move_ok = False
        self.insert_ok = False

    def widgets_creation(self, root):
        """Creates all necessary widgets for the welcome window.
        ----------
        Input : root
        No output"""
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
        
        # Launch game
        self.button_launch = ctk.CTkButton(self.root, text = "Start game", corner_radius = 8, height = 60, width = 15, fg_color = "goldenrod", hover_color = "DodgerBlue4", font = ('Calibri', 20))
        self.button_launch.bind('<Button-1>', self.game_launch)
        self.button_launch.pack(side = ctk.BOTTOM, fill = 'x')

        # Rules display
        self.rules_button = ctk.CTkButton(self.root, text = "?", font = ("Calibri", 20), corner_radius = 15, height = 30, width = 10, fg_color = "lightgrey", hover_color = "darkgrey")
        self.rules_button.bind('<Button-1>', self.show_rules)
        self.rules_button.bind('<Enter>', self.show_tip)
        self.rules_button.bind('<Leave>', self.hide_tip)
        self.rules_button.place(x = 10, y = 10)

    def show_rules(self, event):
        """Displays the game rules in a Messagebox when the "?" rules_button is clicked.
        ----------
        Input : right click from the mouse
        No output"""
        tk.messagebox.showinfo("Labyrinth - Rules", "Goal : Navigate the labyrinth to collect your assigned treasures.\n\nHow to play ?\nYour current objective is displayed in the top right corner of the game window. In the bottom left corner is the tile in your hand.\n\nDuring your turn :\n1 - Insert the tile on the board.\n• Select an insertion position (yellow arrow buttons).\n• Rotate the tile in your hand (yellow rounded arrow buttons).\n• Validate to slide the tiles on the board (green check button).\n2 - Move your pawn on the board (optional) :\n• Click on the tile you wish to go to.\n• Click on 'My turn is over'.\n\nGood luck !")

    def show_tip(self, event):
        """Shows a "Rules" label when hovering the mouse over the "?" rules_button.
        ----------
        Input : mouse hovering above the rules_button
        No output"""
        self.tip = ctk.CTkLabel(self.root, text = "Rules", font = ("Calibri", 12), bg_color = "gainsboro", width = 50)
        self.tip.place(x = 55, y = 11)
    
    def hide_tip(self, event):
        """Hides the "Rules" label when the mouse is not over the "?" rules_button anymore.
        ----------
        Input : mouse left the rules_button area
        No output"""
        self.tip.destroy()
 
    def add_playernames(self, event):
        """Adds entry bars for players to enter custom names (optional).
        ----------
        Input : Slider is released at a position (i.e. a new number of players)
        No output"""
        length = self.player_number.get()

        if length > len(self.playernames_e):
            # Add new player name entries
            for i in range(1, length - len(self.playernames_e) + 1):
                name = "Player" + str(len(self.playernames_e) + 1)
                entry = ctk.CTkEntry(self.root,text_color = "DodgerBlue4", placeholder_text = name,  height = 50, width = 200, font = ('Calibri', 16))
                entry.pack(padx = 10, pady = 10, anchor = ctk.CENTER)
                self.playernames_e.append(entry)

        elif length < len(self.playernames_e): 
            diff = len(self.playernames_e) - length
            # Empty player names and change entries
            for i in range(diff):
                self.playernames_e.pop().pack_forget()
           
    def game_launch(self, message):
        """Creation of the current game window.
        ----------
        Input : message (str)
        No output"""
        # Find the names of the players
        self.get_playernames()
        
        # Start game (and init model) through the controller
        self.controller.start_game(self.playernames)
        
    # Callback functions
    def get_playernames(self):
        """Recovers each player's name.
        Default names are provided in case players don't add names.
        ----------
        No input
        No output"""
        for i in range(len(self.playernames_e)):
            name = str(self.playernames_e[i].get()) # Names the players chose for themselves
            if name == "":
                name = "Player" + str(i+1) # Default name
            self.playernames.append(name) #SEND THIS TO CONTROLLER
    
    def display_game(self):
        """Creates the graphic window for current game display.
        ----------
        No input
        No output"""
        # Initialization of the game variables
        self.running = False
        self.running_pawn = False
        self.timer_id = None
        self.timer_id_pawn = None
        self.pawn_motion = False
        self.slid = False
        self.bg_h = None
        self.fg_h = None
        self.index = 0

        if (self.f_graph == None) :
            self.f_graph = tk.Toplevel(self.root)
            self.f_graph.title('Labyrinth - Current game')
            self.f_graph.iconbitmap('tr_chest.ico')      
            self.f_graph.geometry("1500x875") 
            self.f_graph.config(background = '#EFEFE1')
            
            # Button for players to indicate they finished their turn
            self.button_done = ctk.CTkButton(self.f_graph, text = "Validate displacement.", corner_radius = 8, height = 30, width = 15, fg_color = "grey", hover_color = "DodgerBlue4", font = ('Calibri', 20), state = "disabled")
            self.button_done.bind('<Button-1>', self.move)
            self.button_done.pack(side = ctk.BOTTOM, fill = 'x')
            
            self.image_dict = {} # Dict that stocks all 50 tiles as (bg, fg, pawn) in grid size

            # Functions calls
            self.image_library_i()

            self.frame_left = tk.Frame(self.f_graph, bg = '#EFEFE1')
            self.frame_left.pack(side = tk.LEFT, fill = 'y' )

            
            self.slide_tiles_buttons()
            self.canvas_for_board()
            
            self.frame_right = tk.Frame(self.f_graph, bg = '#EFEFE1')
            self.frame_right.pack(side = tk.RIGHT, fill = 'y' )

            self.canvas_for_objective() 
            self.canvas_for_hand()
            self.turn_tile_buttons()
            self.validate_button()
            self.queue_display()

    def queue_display(self):
        """Queue (playing order) displayed with labels containing : player's name written in color, number of remaining objectives.
        ----------
        No input
        No output"""
        self.current = ctk.CTkLabel(self.f_graph, text = "CURRENT :", font = ("Calibri", 16, "bold"), text_color = "black")
        self.current.pack(side = tk.TOP)
        i = 0
        queue = self.controller.get_queue().values()
        for pawn in queue : 
            i += 1
            obj = len(pawn["objectives"])
            self.name_label = ctk.CTkLabel(self.f_graph, text = pawn["name"], font = ("Calibri", 16, "bold"), text_color = pawn["color"])
            self.name_label.pack(side = tk.TOP)
            self.tr_label = ctk.CTkLabel(self.f_graph, text = f"Treasures left : {obj}", font = ("Calibri", 16), text_color = pawn["color"])
            self.tr_label.pack(side = tk.TOP)
            if i != len(queue):
                self.next = ctk.CTkLabel(self.f_graph, text = "NEXT :", font = ("Calibri", 16, "bold"), text_color = "black")
                self.next.pack(side = tk.TOP)

    def canvas_for_board(self):
        """Creates the canvas for the board with the background.
        ----------
        No input
        No output"""        
        self.canvas_board = tk.Canvas(self.frame_left, width = 752, height = 752, bg = "#EFEFE1")
        
        self.grid_images() 
        self.place_pawns()

        # Set the background image of the canvas
        self.background = tk.PhotoImage(file = self.folder + '\\board.png')
        self.item = self.canvas_board.create_image(378, 378, image = self.background)
        self.canvas_board.lower(self.item)

        self.canvas_board.pack()

    def slide_tiles_buttons(self):
        """Creates the buttons around the board allowing to choose where to insert the tile in hand.
        Each button is named according to the grid position it points to (row number, column number).
        ----------
        No input
        No output"""

        # Initialisation of state of selected_button variable
        self.selected_button = None
        
        # Top side buttons
        self.frame_left_topbar = tk.Frame(self.frame_left, bg = '#EFEFE1')
        self.frame_left_topbar.pack(side = tk.TOP, fill = 'x', pady = 1, padx= 175)

        self.bouton01 = ctk.CTkButton(self.frame_left_topbar, text = "▼", font = ('Calibri', 20), width = 52, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton01.bind('<Button-1>', lambda event: self.select_insertion_button((0,1), self.bouton01, self.bouton61))
        #self.bouton01.place(x = 161, y = 1)
        self.bouton01.pack(side = tk.LEFT, padx = 20)
        

        self.bouton05 = ctk.CTkButton(self.frame_left_topbar, text = "▼", font = ('Calibri', 20), width = 52, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton05.bind('<Button-1>', lambda event: self.select_insertion_button( (0,5), self.bouton05, self.bouton65))
        #self.bouton05.place(x = 475, y = 1)
        self.bouton05.pack(side = tk.RIGHT, padx = 20)

        self.bouton03 = ctk.CTkButton(self.frame_left_topbar, text = "▼", font = ('Calibri', 20), width = 52, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton03.bind('<Button-1>', lambda event:  self.select_insertion_button( (0,3), self.bouton03, self.bouton63))
        #self.bouton03.place(x = 318, y = 1)
        self.bouton03.pack(padx =10)

        # Bottom side buttons
        self.frame_left_bottombar = tk.Frame(self.frame_left, bg = '#EFEFE1')
        self.frame_left_bottombar.pack(side = tk.BOTTOM, fill = 'x', pady = 1, padx = 175)

        self.bouton61 = ctk.CTkButton(self.frame_left_bottombar, text = "▲", font = ('Calibri', 20), width = 52, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton61.bind('<Button-1>',  lambda event: self.select_insertion_button((6,1), self.bouton61, self.bouton01))
        #self.bouton61.place(x = 161, y = 635)
        self.bouton61.pack(side = tk.LEFT, padx = 20)


        self.bouton65 = ctk.CTkButton(self.frame_left_bottombar, text = "▲", font = ('Calibri', 20), width = 52, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton65.bind('<Button-1>', lambda event: self.select_insertion_button((6,5), self.bouton65, self.bouton05))
        #self.bouton65.place(x = 475, y = 635)
        self.bouton65.pack(side = tk.RIGHT, padx = 20)

        self.bouton63 = ctk.CTkButton(self.frame_left_bottombar, text = "▲", font = ('Calibri', 20), width = 52, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton63.bind('<Button-1>', lambda event: self.select_insertion_button((6,3), self.bouton63, self.bouton03))
        #self.bouton63.place(x = 318, y = 635)
        self.bouton63.pack(padx = 10)


        # Left side buttons
        self.frame_left_leftbar = tk.Frame(self.frame_left, bg = '#EFEFE1')
        self.frame_left_leftbar.pack(side = tk.LEFT, padx = 3, pady = 10)

        self.bouton10 = ctk.CTkButton(self.frame_left_leftbar, text = "►", font = ('Calibri', 20), width = 33, height = 52, fg_color = "goldenrod", hover_color = "red4")
        self.bouton10.bind('<Button-1>', lambda event: self.select_insertion_button( (1,0), self.bouton10, self.bouton16))
        #self.bouton10.place(x = 1, y = 161)
        self.bouton10.pack(side = tk.TOP, pady = 55)

        

        self.bouton50 = ctk.CTkButton(self.frame_left_leftbar, text = "►", font = ('Calibri', 20), width = 33, height = 52, fg_color = "goldenrod", hover_color = "red4")
        self.bouton50.bind('<Button-1>', lambda event: self.select_insertion_button((5,0), self.bouton50, self.bouton56))
        #self.bouton50.place(x = 1, y = 475)
        self.bouton50.pack(side = tk.BOTTOM, pady = 55)

        self.bouton30 = ctk.CTkButton(self.frame_left_leftbar, text = "►", font = ('Calibri', 20), width = 33, height = 52, fg_color = "goldenrod", hover_color = "red4")
        self.bouton30.bind('<Button-1>',  lambda event: self.select_insertion_button((3,0), self.bouton30, self.bouton36))
        #self.bouton30.place(x = 1, y = 318)
        self.bouton30.pack( pady = 55)

        # Right side buttons
        self.frame_left_rightbar = tk.Frame(self.frame_left, bg = '#EFEFE1')
        self.frame_left_rightbar.pack(side = tk.RIGHT, padx = 3, pady = 10)

        self.bouton16 = ctk.CTkButton(self.frame_left_rightbar, text = "◄", font = ('Calibri', 20), width = 33, height = 52, fg_color = "goldenrod", hover_color = "red4")
        self.bouton16.bind('<Button-1>', lambda event: self.select_insertion_button((1,6), self.bouton16, self.bouton10))
        #self.bouton16.place(x = 635, y = 161)
        self.bouton16.pack(side = tk.TOP, pady = 55)

        

        self.bouton56 = ctk.CTkButton(self.frame_left_rightbar, text = "◄", font = ('Calibri', 20), width = 33, height = 52, fg_color = "goldenrod", hover_color = "red4")
        self.bouton56.bind('<Button-1>', lambda event: self.select_insertion_button((5,6), self.bouton56, self.bouton50))
        #self.bouton56.place(x = 635, y = 475)
        self.bouton56.pack(side = tk.BOTTOM, pady = 55)

        self.bouton36 = ctk.CTkButton(self.frame_left_rightbar, text = "◄", font = ('Calibri', 20), width = 33, height = 52, fg_color = "goldenrod", hover_color = "red4")
        self.bouton36.bind('<Button-1>', lambda event: self.select_insertion_button((3,6), self.bouton36, self.bouton30))
        #self.bouton36.place(x = 635, y = 318)
        self.bouton36.pack( pady =55)

        self.opposite_button_old = None
    
    def select_insertion_button(self, pos, button_in, button_out):
        """Changes the color of the selected button and gets its position.
        ----------
        Input : tuple (pos), 2 widgets (button_in, button_out)
        No output"""
        # Change color : when clicked, becomes red4 and stays that way unless a different insertion button was selected
        # Find button selected by the player
        if button_in.cget("state") != "disabled" and not self.slid:
            button_in.configure(fg_color = "red4")
            #deselect the previous button
            if self.selected_button != None:
                self.selected_button.configure(fg_color = "goldenrod")
                
            if self.selected_button == button_in: # Case you deselected the line/row after all
                self.selected_button = None
                self.opposite_button = None
                self.chosen_pos = None
            else:
                self.selected_button = button_in
                self.opposite_button = button_out
                # Get button position
                self.chosen_pos = pos
            print(self.selected_button, self.opposite_button, self.chosen_pos)

    def canvas_for_objective(self):
        """Creates the canvas to display the current objective of the player.
        ----------
        No input
        No output"""
        self.canvas_card = tk.Canvas(self.frame_right, width = 360, height = 420, bg = '#EFEFE1')
        self.objective_background()
        self.objective_image()
        self.canvas_card.pack(side = tk.TOP, anchor = 'n')

    def objective_background(self):
        """Sets the image of the empty treasure card, which is the current objective of the player.
        ----------
        No input
        No output"""
        # Background image settings
        self.canvas_card.original_background = tk.PhotoImage(file = self.folder + '\\card.png')
        self.canvas_card.background = self.canvas_card.original_background.zoom(6, 6)
        self.canvas_card.item = self.canvas_card.create_image(160, 212, image = self.canvas_card.background)

        self.canvas_card.lower(self.item)

    def objective_image(self):
        """Displays the right treasure in the objective card.
        ----------
        No input
        No output"""
        filepath_tr = self.controller.get_objective_filepath()
        # Treasure image settings
        self.treas_c = tk.PhotoImage(file = self.folder + filepath_tr)
        self.treas_c_resized = self.treas_c.zoom(3, 3)
        self.fg_c = self.canvas_card.create_image(160, 212, image = self.treas_c_resized)
        self.canvas_card.lift(self.fg_c)
        
    def canvas_for_hand(self):
        """Creates the canvas for the tile in hand.
        ----------
        No input
        No output"""
        self.canvas_tile = tk.Canvas(self.frame_right, bg = "#EFEFE1", width = 380, height = 380)
        self.hand_image()
        self.canvas_tile.pack(side = tk.TOP, anchor = 'e')

    def hand_image(self):
        """Displays the tile in hand in its canvas and binds it to the rotation function.
        ----------
        No input
        No output"""
        self.filepath_ti_h, self.filepath_tr_h = self.controller.get_hand_filepath() #address of the tile and treasure images
        # Set the image of the tile in hand
        self.hand_tile()

        # Set the image of the treasure of the tile (if any)
        self.hand_treasure()
              
        # Useful for the rotation display
        self.orientation_h = 0 
        self.dict_r ={}

    def hand_tile(self):
        """Displays the tile in hand.
        ----------
        No input
        No output"""
        if self.bg_h != None:
            self.canvas_tile.delete(self.bg_h)
        self.tile_h = tk.PhotoImage(file = self.folder + self.filepath_ti_h)
        self.tile_h_resized = self.tile_h.zoom(3, 3)
        self.bg_h = self.canvas_tile.create_image(200, 175, image = self.tile_h_resized)
        self.canvas_tile.lower(self.bg_h)

    def hand_treasure(self):
        """Displays the treasure of the tile in hand.
        ----------
        No input
        No output"""
        if self.fg_h != None:
            self.canvas_tile.delete(self.fg_h)
        # Set the image of the treasure of the tile (if any) 
        if self.filepath_tr_h is not None:
            self.treas_h = tk.PhotoImage(file = self.folder + self.filepath_tr_h)
            self.treas_h_resized = self.treas_h.zoom(3, 3)
            self.fg_h = self.canvas_tile.create_image(205, 175, image = self.treas_h_resized)
            self.canvas_tile.lift(self.fg_h)

    def turn_tile_buttons(self):
        """Creates the buttons next to the hand allowing to change the orientation of the tile in hand.
        ----------
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
        """Rotates the tile in hand.
        ----------
        Input = integer (sens, i.e., the direction of the rotation)
        No output"""
        # Set new orientation
        self.orientation_h += sens
        # Prepare the image tile
        if self.filepath_ti_h == './tile_corner.png':
            self.ti_h = self.tile_c
        elif self.filepath_ti_h == './tile_t.png':
            self.ti_h = self.tile_t
        else:
            self.ti_h = self.tile_s
        
        self.rotatedc_tile = rotate_image_h(self.ti_h, self.orientation_h)
        self.dict_r[1] = self.rotatedc_tile  
        # Replace self.bg_h with the rotated image
        self.canvas_tile.delete(self.bg_h) # Delete the old image
        self.bg_h = self.canvas_tile.create_image(200, 175, image = self.dict_r[1]) # Create the new image
        self.canvas_tile.lower(self.bg_h)
        
    def validate_button(self):
        """Creates the button under the hand to validate the chosen orientation and insertion.
        ----------
        No input
        No output"""    
        self.button_valid = ctk.CTkButton(self.f_graph, text = "✔", font = ('Calibri', 30, 'bold'), width = 50, height = 50, bg_color = '#E8E4CC', fg_color = '#009900', hover_color = "green4")
        self.button_valid.bind('<Button-1>', self.check_insertion)
        self.button_valid.place(x = 1015, y = 605)
        
    def check_insertion(self, event):
        """Verify that the player did select where to insert the tile in hand.
        ----------
        Input : right click from the mouse on validate_button
        No output"""
        if self.selected_button == None:
            self.selection_error_messagebox()
        elif self.button_valid.cget('state') == 'disabled':
            self.show_warning("You already inserted a tile this turn.\nPlease end your turn.")
        else:
            self.controller.insert_hand()
    
    def selection_error_messagebox(self):
        """Opens a messagebox reminding the player that they didn't choose where to insert the tile although it is mandatory.
        ----------
        No input
        No output"""
        self.msg_error = tk.messagebox.showwarning("Selection error", "You need to select an insertion button.\nPlease choose where you want to insert the tile.")

    def show_warning(self, text):
        """Opens a messagebox with a custom text.
        ----------
        Input : str (text)
        No output"""
        self.msg_error2 = tk.messagebox.showwarning("Warning", text)

    def messagebox(self, text):
        """Opens a messagebox with a custom text.
        ----------
        Input : str (text)
        No output"""
        self.msg = tk.messagebox.showinfo("Message", text)

    def image_library_i(self):
        """Loads and sizes all PNG files as Images (this object type can be rotated).
        ----------
        No input
        No output"""
        self.image_dict = {}
        # Load the 3 tile images and resize them
        self.tile_c = Image.open(self.folder + '\\tile_corner.png')
        self.tile_t = Image.open(self.folder + '\\tile_t.png')
        self.tile_s = Image.open(self.folder + '\\tile_straight.png')
        self.target_pic_o = tk.PhotoImage(file = self.folder + '\\target_ok.png')
        self.target_pic_n = tk.PhotoImage(file = self.folder + '\\target_no.png')

    def grid_images(self):
        """Associates tiles to treasures and stocks them.
        Displays the tiles on the board in its canvas and binds it to the sliding.
        ----------
        No input
        No output"""
        # Get grid
        self.graphics_dict = self.controller.get_display_grid()        
        # Initialisation of storage
        self.treasures = {}
        self.tiles = {}
        self.tile_dict = {}
        self.treasure_dict = {}

        for position, tile in self.graphics_dict.items():
            self.index += 1
            # Position
            li, co = grid_position(position)
            # Tile display
            new_bg = self.grid_tile(tile["filepath_ti"], tile["orientation"], co, li)    
            # Treasure display
            if tile["filepath_treas"] != None:
                #create and position treasure
                new_fg = self.grid_treasure(tile["filepath_treas"], co, li)
            else:
                new_fg = None
            # Save
            self.tile_dict[position] = new_bg
            self.treasure_dict[position] = new_fg
    
    def grid_treasure(self, filepath, co, li):
        """Places the treasures on the board.
        ----------
        Input : str, int, int
        Output : PhotoImage on canvas"""
        # Create and position treasure
        self.treasures[self.index] = tk.PhotoImage(file = self.folder + filepath)
        new_fg = self.canvas_board.create_image(co, li, image = self.treasures[self.index])
        self.canvas_board.lift(new_fg)
        self.canvas_board.tag_bind(new_fg, '<Button-1>', self.click_tile)
        return new_fg
    
    def grid_tile(self, filepath, orientation, co, li):
        """Places the tiles on the board.
        ----------
        Input : str, int, int, int
        Output : PhotoImage on canvas"""
        # Initialisation
        self.get_image(filepath)
        # Orientate
        self.tiles[self.index] = rotate_image(self.new_tile, orientation)
        # Display
        new_bg = self.canvas_board.create_image(co, li, image = self.tiles[self.index])
        self.canvas_board.lift(new_bg)
        self.canvas_board.tag_bind(new_bg, '<Button-1>', self.click_tile)
        return new_bg

    def get_image(self, filepath):
        """Get image from filepath.
        ----------
        Input : str
        Output : Image"""
        if filepath == './tile_corner.png':
                self.new_tile = self.tile_c
        elif filepath == './tile_t.png':
            self.new_tile = self.tile_t
        else:
            self.new_tile = self.tile_s
        
    def get_insert_state(self):
        """Sends position and tile orientation to controller.
        ----------
        No input
        Output : tuple, int"""
        self.orientation_h = self.orientation_h%(4)
        self.insert_ok = False
        return self.chosen_pos, self.orientation_h

    def anim_tiles_slide(self):
        """Slides the tile on the screen using a timer.
        ----------
        No input
        No output"""
        # Get which row/column moves
        self.index += 1
        out_pos = self.controller.get_slideout_pos()
        ## If it is a line
        if self.chosen_pos[1] == 0:
            init_pos = (self.chosen_pos[0], -1)
            #out_pos = (self.chosen_pos[0], 6)
            self.slider = "lin_r"
        elif self.chosen_pos[1] == 6:
            init_pos = (self.chosen_pos[0], 7)
            #out_pos = (self.chosen_pos[0], 0)
            self.slider ='lin_l'
        ## If it s a column
        elif self.chosen_pos[0]==0:
            init_pos = (-1, self.chosen_pos[1])
            #out_pos = (6, self.chosen_pos[1])
            self.slider = 'col_d'
        elif self.chosen_pos[0]==6:
            init_pos = (7, self.chosen_pos[1])
            #out_pos = (0, self.chosen_pos[1])
            self.slider = 'col_u'
        # Add the new tile at the beginning of the row/column 
        treasure_filepath = self.filepath_tr_h
        hand_filepath = self.filepath_ti_h
        hand_orientation = self.orientation_h
        # Initialisation of position
        li, co = grid_position(init_pos)
        # New treasure
        if treasure_filepath != None:
            # Create and position treasure
            new_fg = self.grid_treasure(treasure_filepath, co, li)
        else:
            new_fg = None     
        # New tile
        new_bg = self.grid_tile(hand_filepath, hand_orientation, co, li)
        # Storage
        self.tile_dict[init_pos] = new_bg
        self.treasure_dict[init_pos] = new_fg
        self.pawn_dict[init_pos] = None
        # Storage update
        self.storage_update(init_pos, out_pos, li, co)
        # Start the animation
        self.lancer()
        # Handle buttons
        if self.opposite_button_old != None:
            self.opposite_button_old.configure(fg_color = "goldenrod", state = "normal")
        self.opposite_button.configure(fg_color = "grey", state = "disabled")
        self.selected_button.configure(fg_color = "goldenrod")
        self.button_valid.configure(state = "disabled", fg_color = "grey")
        # Handle turn unrolling
        self.pawn_motion = True
        self.cross = False
        self.slid = True
        
    def storage_update(self, init_pos, out_pos, li, co):
        """Updates the dictionnaries of the grid display.
        ----------
        Input : 2 tuples, 2 integers
        No output"""
        # Delete the tiles+treasures pushed out of the board
        self.canvas_board.delete(self.tile_dict[out_pos])
        self.canvas_board.delete(self.treasure_dict[out_pos])
        # Move the pawns pushed out of the board
        if self.pawn_dict[out_pos] != None:
            for pawn in self.pawn_dict[out_pos]:
                # Find the color of the circle pawn and move in consequence
                color = self.canvas_board.itemcget(pawn, "fill")
                if color == "blue": 
                    self.canvas_board.coords(pawn, co-20, li+20, co, li)
                elif color == "red": 
                    self.canvas_board.coords(pawn, co, li, co+20, li-20) 
                elif color == "green": 
                    self.canvas_board.coords(pawn, co-20, li, co, li-20)
                else:
                    self.canvas_board.coords(pawn, co, li+20, co+20, li)
                # Move it in storage
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
                self.tile_dict[(i, self.chosen_pos[1])] = self.tile_dict[i + r[2], self.chosen_pos[1]]
                self.treasure_dict[(i, self.chosen_pos[1])] = self.treasure_dict[i + r[2], self.chosen_pos[1]]
                self.pawn_dict[(i, self.chosen_pos[1])] = self.pawn_dict[i + r[2], self.chosen_pos[1]]
            else:
                self.tile_dict[(self.chosen_pos[0], i)] = self.tile_dict[(self.chosen_pos[0], i + r[2])]
                self.treasure_dict[(self.chosen_pos[0], i)] = self.treasure_dict[(self.chosen_pos[0], i + r[2])]
                self.pawn_dict[(self.chosen_pos[0], i)] = self.pawn_dict[(self.chosen_pos[0], i + r[2])]
        self.tile_dict[init_pos] = None
        self.treasure_dict[init_pos] = None

    def lancer(self):
        """Launches the timer loop if it's not already running.
        ----------
        No input
        No output"""
        self.i = 0
        if not(self.running):
            self.timer_loop()
        self.running = True
        
    def stop(self):
        """Stops the timer loop if it is running.
        ----------
        No input
        No output"""        
        if self.running :
            self.f_graph.after_cancel(self.timer_id) 
        self.running = False
        #self.tile_dict[init_pos] = None

    def timer_loop(self):
        """Defines the loop that is handled by the timer : allows image displacement and display.
        ----------
        No input
        No output"""
        if self.slider == "col_d" or self.slider == "lin_r":
            r = (0, 7, 1)
        else:
            r = (6, -1, -1)
        for i in range(r[0],r[1],r[2]):
            if "col" in self.slider:
                self.canvas_board.move(self.tile_dict[(i,self.chosen_pos[1])], 0, r[2] * 10)
                if self.treasure_dict[(i,self.chosen_pos[1])] != None:
                    self.canvas_board.move(self.treasure_dict[(i,self.chosen_pos[1])], 0, r[2] * 10)
                    self.canvas_board.lift(self.treasure_dict[(i,self.chosen_pos[1])])
                if self.pawn_dict[(i,self.chosen_pos[1])] != None:
                    for pawn in self.pawn_dict[(i,self.chosen_pos[1])]:
                        self.canvas_board.move(pawn, 0, r[2]*10)
                        self.canvas_board.lift(pawn)
            else:
                self.canvas_board.move(self.tile_dict[(self.chosen_pos[0], i)], r[2] * 10, 0)
                if self.treasure_dict[(self.chosen_pos[0], i)] != None:  
                    self.canvas_board.move(self.treasure_dict[(self.chosen_pos[0], i)], r[2] * 10, 0)
                    self.canvas_board.lift(self.treasure_dict[(self.chosen_pos[0], i)])
                if self.pawn_dict[(self.chosen_pos[0], i)] != None:
                    for pawn in self.pawn_dict[(self.chosen_pos[0], i)]:
                        self.canvas_board.move(pawn, r[2] * 10, 0)
                        self.canvas_board.lift(pawn)
        self.i += 1
        if self.i == 10:
           self.stop()
        else:
            self.timer_id = self.f_graph.after(100, self.timer_loop)
        
    def place_pawns(self):
        """Places circles for the pawns on the boards.
        ----------
        No input
        No output"""
        # Initialisation of pawn storage
        self.pawn_dict = {}
        # Pawn display
        for position, tile in self.graphics_dict.items():
            if tile["pawns"] != None:
                # Position
                li, co = grid_position(position)
                # Create circles on the tiles
                new_pawns = []
                for color in tile["pawns"]:
                    if color == "blue": 
                        new_pawn = self.canvas_board.create_oval(co-20, li+20, co, li, fill = color)
                    elif color == "red": 
                        new_pawn =self.canvas_board.create_oval(co, li, co+20, li-20, fill = color) 
                    elif color == "green": 
                        new_pawn = self.canvas_board.create_oval(co-20, li, co, li-20, fill = color)
                    else:
                        new_pawn = self.canvas_board.create_oval(co, li+20, co+20, li, fill = color)
                    self.canvas_board.lift(new_pawn)
                    new_pawns.append(new_pawn)
                self.pawn_dict[position] = new_pawns
    
    def turn_over(self, event):
        """Validates that the player is done with their turn and communicates the changes of player back and forth with the controller.
        ----------
        Input : event
        No output"""
        self.queue_display()
        self.objective_image()
        self.hand_image()
        #throw animation to move pawn when checked it is possible
        #slide buttons preparation
        #this will gather the information necessary for move pawn animation
        #self.anim_move_pawn()
        #useful for turn over
        self.opposite_button_old = self.opposite_button
        self.opposite_button = None
        self.pawn_motion = False
        self.slid = False
        self.insert_ok = False
        self.move_ok = False
        self.button_done.config(fg_color = 'grey', state = 'disabled')
        self.button_valid.configure(state = 'normal', fg_color = 'green')

    def anim_move_pawn(self):
        """Animates the movement of the pawn to the chosen destination.
        ----------
        No input
        No output"""
        if not(self.running_pawn):
            self.timer_loop_pawn()
        self.running_pawn = True       
    
    def timer_loop_pawn(self):
        """Moves the pawn one step at a time on the board.
        ----------
        No input
        No output"""
        path = self.dict_anim["path"]
        pawn = self.dict_anim["pawn"]
        previous_step = self.dict_anim["previous_step"]
        obj = path.pop(0)
        step_x = (obj[1] - previous_step[1]) * 100
        step_y = (obj[0] - previous_step[0]) * 100
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
        """Stops the animation of the pawn.
        ----------
        No input
        No output"""
        if self.running_pawn :
            self.f_graph.after_cancel(self.timer_id_pawn) 
        self.running_pawn = False
        print("stop_pawn")
        
    def click_tile(self, event):
        """Places a cross where the player wants to move their pawn and registers the grid coordinates.
        ----------
        Input : right click from the mouse on a tile of the board
        No output"""
        # If the pawn can be moved
        if self.pawn_motion:
            pos = self.canvas_board.coords(self.canvas_board.find_withtag('current')[0]) # Get tile position with coords
            # Take note of the objective coordinates
            self.destination_co = int((pos[0] - 75) / 100)
            self.destination_li = int((pos[1] - 75) / 100)
            self.accessible, self.displacement = self.controller.validate_move((self.destination_li, self.destination_co))
            # If there is a cross
            if self.cross:
                self.canvas_board.delete(self.target)
            if self.accessible:
                self.target = self.canvas_board.create_image(pos[0], pos[1], image = self.target_pic_o)
                self.button_done.configure(fg_color = "goldenrod", state = "normal")
            else:
                self.target = self.canvas_board.create_image(pos[0], pos[1], image = self.target_pic_n)
                self.button_done.configure(fg_color = "grey", state = "disabled")
            self.cross = True
            self.canvas_board.lift(self.target)
        # If its not the right time to move the pawn
        else:
            self.msg_error2 = tk.messagebox.showwarning("Selection error", "You can't choose a displacement now.\nPlease insert your tile first.")

    def move(self, event):
        """Moves the player's pawn.
        ----------
        Input : right click from the mouse on the "validate displacement" button
        No output"""
        if self.button_done.cget("state") != "disabled":
            self.controller.move_pawn((self.destination_li, self.destination_co))
            depart = self.displacement.pop(0)
            color = self.controller.get_player_color()
            pawn = self.find_ident(color, depart)
            self.dict_anim = {"path": self.displacement, "pawn": pawn, "previous_step": depart}
            self.anim_move_pawn()
            self.controller.end_turn()

    def find_ident(self, color, pos):
        """Identifies a pawn and communicates the info to the controller.
        ----------
        Input : str, tuple
        Output : pawn"""
        found = None
        for pawn in self.pawn_dict[pos]:
            if pawn.cget("fill") == color:
                found = pawn
        return pawn

    def get_move_pos(self):
        """Returns the coordinates of the tile where the player wants to move the pawn.
        ----------
        No input
        Output : 2 intergers"""
        self.move_ok = False
        return self.destination_li, self.destination_co
 
    def app_start(self):
        self.root.mainloop()


# General functions    
def rotate_image(img, orientation):
    """Rotates an image to the given orientation.
    ----------
    Input : image, int
    Output : PhotoImage"""
    img = img.rotate(orientation* - 90)
    return (ImageTk.PhotoImage(img))

def rotate_image_h(img, orientation):
    """Rotates and enlarges by 3 an image.
    ----------
    Input : image, int
    Output : PhotoImage"""
    w,h = img.size
    img = img.resize((3*w, 3*h))
    img_f = rotate_image(img, orientation)
    return img_f
    
def grid_position(pos):
    """Converts the grid into canvas coordinates.
    ----------
    Input : tuple (line, column)
    Output : tuple (line, column)"""
    co0 = pos[1]
    li0 = pos[0]
    co = 75 + co0*100
    li = 75 + li0*100
    return(li, co)