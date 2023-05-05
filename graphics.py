import tkinter as tk
import customtkinter as ctk

from PIL import Image, ImageTk

ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class GameWindow():
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Labyrinth - the aMAZEing game")
        self.root.iconbitmap('tr_chest.ico')
        self.root.geometry("1200x700")
        # management of the communication with the game class
            
        ########################################
        # Graphic window settings
        ########################################
        # graphical elements
        self.folder = "./textures" # adresse 

        # display window setting
        self.f_graph = None
        # test parameters
        self.playernames_e = list()
        self.playernames = list()
        # widgets creation
        self.widgets_creation(self.root)

    def widgets_creation(self, root):
        # text
        self.welcome = ctk.CTkLabel(root, height = 120, text = "Welcome to the aMAZEing Labyrinth - Software version !", text_color = "DodgerBlue4", font = ('Calibri', 28, 'bold'))
        self.welcome.pack(side = tk.TOP)

        self.label = ctk.CTkLabel(root, height = 50, text = "Choose the number of players and enter their names :", font = ('Calibri', 20))
        self.label.pack(side = tk.TOP)

        # player number
        self.player_number = tk.IntVar()
        self.scale = ctk.CTkSlider(root, height = 30, width = 455, progress_color = "goldenrod", fg_color = "DodgerBlue4",  button_corner_radius = 5, button_color = "goldenrod", button_hover_color = "DodgerBlue4", from_ = 2, to = 4, number_of_steps = 2, orientation = "horizontal", variable = self.player_number)

        self.scale.pack(pady = 30, anchor = ctk.CENTER)
        self.scale.bind('<ButtonRelease-1>', self.add_playernames)

        self.scale.set(2)
        self.add_playernames(None)

        # quit
        self.bouton_2 = ctk.CTkButton(root, text = "Quit", corner_radius = 8, height = 40, width = 15, fg_color = "red4", hover_color = "DodgerBlue4", font = ('Calibri', 20), command = self.root.destroy)
        self.bouton_2.pack(fill = 'x', side = tk.BOTTOM)
        
        # launch game
        self.button_launch = ctk.CTkButton(self.root, text = "Start game", corner_radius = 8, height = 60, width = 15, fg_color = "goldenrod", hover_color = "DodgerBlue4", font = ('Calibri', 20))
        self.button_launch.bind('<Button-1>', self.game_launch)
        self.button_launch.pack(side = ctk.BOTTOM, fill = 'x')
 
    def add_playernames(self, event):
        """adds entry bars to get player names"""
        length = self.player_number.get()

        if length > len(self.playernames_e):
            # add new player name entries
  
            for i in range(1, length - len(self.playernames_e) + 1):
                name = "Player" + str(len(self.playernames_e) +1)
                entry = ctk.CTkEntry(self.root,text_color = "DodgerBlue4", placeholder_text = name,  height = 50, width = 200, font = ('Calibri', 16))
                entry.pack(padx = 10, pady = 10, anchor = ctk.CENTER)
                self.playernames_e.append(entry)
        elif length<len(self.playernames_e): 

            diff = len(self.playernames_e) - length
            # empty player names and change entries
            for i in range(diff):
                self.playernames_e.pop().pack_forget()
           
    def game_launch(self, message):
        """creation of the window"""
        # find the player name
        self.get_playernames()
        
        # init the game through controller
        #self.controller.init_control()

        # creation of the graphic window
        self.graphic_window() 
        
    #callback
    def get_playernames(self):
        """recovers the player's name
        no input
        no output"""
        for i in range(len(self.playernames_e)):
            name = str(self.playernames_e[i].get())
            if name == "":
                name = "Player" + str(i+1)
            self.playernames.append(name)
    
    def graphic_window(self):
        """creates graphic window for current game display
        no input
        no output"""
        if (self.f_graph == None) :
            self.f_graph = ctk.CTkToplevel(self.root)
            self.f_graph.title('Labyrinth - Current game')
            #self.f_graph.iconbitmap('tr_chest.ico')      celiu-ci n'a pas l'air de fonctionner...
            self.f_graph.geometry("1200x700")      
            
            #bouton "mon tour est fini"?
            self.button_done = ctk.CTkButton(self.f_graph, text = "My turn is over.", corner_radius = 8, height = 30, width = 15, fg_color = "goldenrod", hover_color = "DodgerBlue4", font = ('Calibri', 20))
            #self.button_done.bind('<Button-1>', self.turn_over())
            self.button_done.pack(side = ctk.BOTTOM, fill = 'x')
            
            
            self.image_dict = {}#stock all 50 tiles as (bg, fg, pawn) in grid size

            self.canvas_for_board()
           
            self.slide_tiles_buttons()
            
            self.canvas_for_objective() 
            
            self.text_area()
            
            self.canvas_for_hand()

            self.turn_tile_buttons()
            
            self.validate_button()

    def canvas_for_board(self):
        """creates the canva for the board with the background
        no input
        no output"""
        
        self.canvas_board = tk.Canvas(self.f_graph, width = 752, height = 752)
        
        self.grid_images() 

        self.place_pawns()

        self.background = tk.PhotoImage(file = self.folder + '\\zoomed_board.png')
        self.item = self.canvas_board.create_image(370, 370, image = self.background)
        self.canvas_board.lower(self.item)

        self.canvas_board.pack(side = tk.LEFT, padx=40, pady=40)

    def slide_tiles_buttons(self):
        """creates the buttons around the board allowing to choose where to insert the tile
        no input
        no output"""

        # Bind it to controller somehow so as to disable the button where it's not allowed to insert the tile
        self.selected_button = None
        
        self.bouton01 = ctk.CTkButton(self.f_graph, text = "▼", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton01.bind('<Button-1>', lambda event: self.select_insertion_button((0,1), self.bouton01))
        self.bouton01.place(x = 155, y = 0)

        self.bouton03 = ctk.CTkButton(self.f_graph, text = "▼", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton03.bind('<Button-1>', lambda event:  self.select_insertion_button( (0,3), self.bouton03))
        self.bouton03.place(x = 312, y = 0)

        self.bouton05 = ctk.CTkButton(self.f_graph, text = "▼", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton05.bind('<Button-1>', lambda event: self.select_insertion_button( (0,5), self.bouton05))
        self.bouton05.place(x = 468, y = 0)

        self.bouton10 = ctk.CTkButton(self.f_graph, text = "►", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton10.bind('<Button-1>', lambda event: self.select_insertion_button( (1,0), self.bouton10))
        self.bouton10.place(x = 0, y = 155)

        self.bouton30 = ctk.CTkButton(self.f_graph, text = "►", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton30.bind('<Button-1>',  lambda event: self.select_insertion_button((3,0), self.bouton30))
        self.bouton30.place(x = 0, y = 312)

        self.bouton50 = ctk.CTkButton(self.f_graph, text = "►", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton50.bind('<Button-1>', lambda event: self.select_insertion_button((5,0), self.bouton50))
        self.bouton50.place(x = 0, y = 468)

        self.bouton71 = ctk.CTkButton(self.f_graph, text = "▲", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton71.bind('<Button-1>',  lambda event: self.select_insertion_button((7,1), self.bouton71))
        self.bouton71.place(x = 155, y = 630)

        self.bouton73 = ctk.CTkButton(self.f_graph, text = "▲", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton73.bind('<Button-1>', lambda event: self.select_insertion_button((7,3), self.bouton73))
        self.bouton73.place(x = 312, y = 630)

        self.bouton75 = ctk.CTkButton(self.f_graph, text = "▲", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton75.bind('<Button-1>', lambda event: self.select_insertion_button((7,5), self.bouton75))
        self.bouton75.place(x = 468, y = 630)

        self.bouton17 = ctk.CTkButton(self.f_graph, text = "◄", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton17.bind('<Button-1>', lambda event: self.select_insertion_button((1,7), self.bouton17))
        self.bouton17.place(x = 630, y = 155)

        self.bouton37 = ctk.CTkButton(self.f_graph, text = "◄", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton37.bind('<Button-1>', lambda event: self.select_insertion_button((3,7), self.bouton37))
        self.bouton37.place(x = 630, y = 312)
        
        
        self.bouton57 = ctk.CTkButton(self.f_graph, text = "◄", font = ('Calibri', 20), width = 33, height = 33, fg_color = "goldenrod", hover_color = "red4")
        self.bouton57.bind('<Button-1>', lambda event: self.select_insertion_button((5,7), self.bouton57))
        self.bouton57.place(x = 630, y = 468)
    
    def select_insertion_button(self,  pos, button):
        """changes the color of the selected button and gets its position"""
        # change color : when clicked, becomes red4 and stays that way unless a different insertion button was selected
        # find button clicked
        button.configure(fg_color= "red4")
        if self.selected_button != None:
            self.selected_button.configure(fg_color = "goldenrod")
        self.selected_button = button
        # get button position and call anim_slide_tile
        self.chosen_pos = pos
        print(self.chosen_pos)

    def canvas_for_objective(self):
        """creates canvas to display the objective of the player"""
        self.canvas_card = tk.Canvas(self.f_graph, width = 360, height = 420)
        self.objective_background()
        self.objective_image()
        self.canvas_card.pack(side = tk.TOP, anchor = 'ne')



    def text_area(self):
        """creates text area where the controller sends event messages
        no input
        no output"""
        #text area for commmunication through controller
        #bind it to messagerie method

    def canvas_for_hand(self):
        """creates canvas area for the hand
        no input
        no output"""
        self.canvas_tile = tk.Canvas(self.f_graph, bg = "grey", width = 400, height = 400)
        self.hand_image()
        self.canvas_tile.pack(side = tk.TOP, anchor = 'e')

    def turn_tile_buttons(self):
        """creates the buttons next to the hand allowing to turn the orientation of the hand tile
        no input
        no output"""
        #turning buttons
        
    def validate_button(self):
        """creates the button under the hand to validate the chosen orientation and insertion
        no input
        no output"""    
        self.button_valid = ctk.CTkButton(self.f_graph, text = "✔", font = ('Calibri', 30, 'bold'), width = 50, height = 50, fg_color = 'green3', hover_color = "green4")
        self.button_valid.bind('<Button-1>', self.anim_slide_tiles)
        self.button_valid.place(x = 1100, y = 600)
        # bind it to controller somehow

    def objective_background(self):
        self.canvas_card.original_background = tk.PhotoImage(file = self.folder + '\\card.png')
        self.canvas_card.background = self.canvas_card.original_background.zoom(6, 6)
        self.canvas_card.item = self.canvas_card.create_image(160, 212, image = self.canvas_card.background)
        self.canvas_card.lower(self.item)

    def objective_image(self):
        """displays the right treasure in the objective card
        no input
        no output"""
        # filepath_tr = self.controller.hand
        filepath_tr = "\\tr_spider.png"
        self.treas_c = tk.PhotoImage(file = self.folder + filepath_tr)
        self.treas_c_resized = self.treas_c.zoom(3,3)
        self.fg_c = self.canvas_card.create_image(160, 212, image = self.treas_c_resized)
        self.canvas_card.lift(self.fg_c)
        
        #display the treasure using the controller
                # select treasure index 0 in the list of the player's objectives
     
    def image_library(self):
        """loads and sizes all PNG files (not arrows)
        no input
        no output"""
        self.image_dict = {}
        #load the 3 tile images and resize them
        self.tile_c = tk.PhotoImage(file = self.folder + '\\tile_corner.png')
        self.tile_t = tk.PhotoImage(file = self.folder + '\\tile_t.png')
        self.tile_s = tk.PhotoImage(file = self.folder + '\\tile_straight.png')

    def image_library_i(self):
        """loads and sizes all PNG files (not arrows)
        no input
        no output"""
        self.image_dict = {}
        #load the 3 tile images and resize them
        self.tile_c = Image.open(self.folder + '\\tile_corner.png')
        self.tile_t = Image.open(self.folder + '\\tile_t.png')
        self.tile_s = Image.open(self.folder + '\\tile_straight.png')
        
    def hand_image(self):
        """displays the hand in its canvas and binds it to the rotation
        no input
        no output"""
        
        #filepath_t, filepath_tr = self.controller.hand: #hand should be reduced to (filepathTile, filepathTreas|None)
        filepath_ti="\\tile_corner.png"
        filepath_tr = "\\tr_bat.png"
        self.tile_h = tk.PhotoImage(file = self.folder + filepath_ti)
        self.tile_h_resized = self.tile_h.zoom(3,3)
        self.bg_h = self.canvas_tile.create_image(200, 200, image = self.tile_h_resized)
        self.canvas_tile.lower(self.bg_h)
        if filepath_tr != None:
            self.treas_h = tk.PhotoImage(file = self.folder + filepath_tr)
            self.treas_h_resized = self.treas_h.zoom(3,3)
            self.fg_h = self.canvas_tile.create_image(205, 195, image = self.treas_h_resized)
            self.canvas_tile.lift(self.fg_h)
            self.image_dict[(self.tile_h, self.treas_h, None)]=(7,7)  
        else:
            self.image_dict[(self.tile_h, None, None)]=(7,7)  
        
        #display the hand using the controller
                #choose the tile
                #place the treasure on it
                #place the image on its spot
            #bind method de rotation 
            #stock the tile in a dict


    def grid_images(self):
        """displays the tiles on the board in its canvas and binds it to the sliding
        beforehand associates tiles and treasures+stock them 
        
        no input
        no output"""
        graphics_dict = {(0, 0): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 1, 'pawns': ['blue']}, (0, 6): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': ['red']}, (6, 6): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, (6, 0): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': ['green']}, (0, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_helmet.png', 'orientation': 0, 'pawns': []}, (0, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_candelabrum.png', 'orientation': 0, 'pawns': []}, (2, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_chest.png', 'orientation': 0, 'pawns': []}, (2, 0): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_sword.png', 'orientation': 3, 'pawns': []}, (4, 0): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_skull.png', 'orientation': 3, 'pawns': []}, (2, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_emerald.png', 'orientation': 3, 'pawns': []}, (2, 6): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_ring.png', 'orientation': 1, 'pawns': []}, (4, 6): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_map.png', 'orientation': 1, 'pawns': []}, (4, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_crown.png', 'orientation': 1, 'pawns': []}, (4, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_keys.png', 'orientation': 2, 'pawns': []}, (6, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_purse.png', 'orientation': 1, 'pawns': []}, (6, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_grimoire.png', 'orientation': 2, 'pawns': []}, (0, 1): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, (0, 3): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (0, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_rat.png', 'orientation': 2, 'pawns': []}, (1, 0): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_ghost.png', 'orientation': 3, 'pawns': []}, (1, 1): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, (1, 2): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_owl.png', 'orientation': 0, 'pawns': []}, (1, 3): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, (1, 4): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, (1, 5): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, (1, 6): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (2, 1): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_scarab.png', 'orientation': 0, 'pawns': []}, (2, 3): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, (2, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 1, 'pawns': []}, (3, 0): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (3, 1): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_gnome.png', 'orientation': 2, 'pawns': []}, (3, 2): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_salamander.png', 'orientation': 1, 'pawns': []}, (3, 3): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, (3, 4): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (3, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_moth.png', 'orientation': 2, 'pawns': []}, (3, 6): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_dragon.png', 'orientation': 3, 'pawns': []}, (4, 1): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_genie.png', 'orientation': 2, 'pawns': []}, (4, 3): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (4, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (5, 0): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (5, 1): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (5, 2): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (5, 3): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_bat.png', 'orientation': 3, 'pawns': []}, (5, 4): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, (5, 5): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, (5, 6): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 1, 'pawns': []}, (6, 1): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, (6, 3): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_sorceress.png', 'orientation': 0, 'pawns': []}, (6, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}}
        self.image_library_i()
        #get grid
        #for position, tile in self.controller.grid: #grid should be reduced to (positionTuple)={filepathTile, filepathTreas|None, list of colors or empty list]
        i = 0
        self.treasures ={}
        self.tiles = {}
        for position, tile in graphics_dict.items():
            i += 1
            #position
            x0 = position[0]
            y0 = position[1]
            x = 70 + x0*100
            y = 70 + y0*100
            #treasure display
            if tile["filepathTreas"]!=None:
                #create and position treasure
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
                
            #init
            if tile["filepathTile"] == './tile_corner.png':
                self.new_tile = self.tile_c
            elif tile["filepathTile"] == './tile_t.png':
                self.new_tile = self.tile_t
            else:
                self.new_tile = self.tile_s

            #orientate
            self.tiles[i] = rotate_image(self.new_tile, tile["orientation"])
            
            #display
            new_bg = self.canvas_board.create_image(y, x, image = self.tiles[i])
            self.canvas_board.lower(new_bg)
            

            

            self.image_dict[new_bg] = (x,y)

                
                
                
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


    def anim_silde_tile(self, event, pos):
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
        #place pawns and bind them to moving animation
        graphics_dict = {(0, 0): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 1, 'pawns': ['blue']}, (0, 6): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': ['red']}, (6, 6): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, (6, 0): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': ['green']}, (0, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_helmet.png', 'orientation': 0, 'pawns': []}, (0, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_candelabrum.png', 'orientation': 0, 'pawns': []}, (2, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_chest.png', 'orientation': 0, 'pawns': []}, (2, 0): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_sword.png', 'orientation': 3, 'pawns': []}, (4, 0): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_skull.png', 'orientation': 3, 'pawns': []}, (2, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_emerald.png', 'orientation': 3, 'pawns': []}, (2, 6): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_ring.png', 'orientation': 1, 'pawns': []}, (4, 6): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_map.png', 'orientation': 1, 'pawns': []}, (4, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_crown.png', 'orientation': 1, 'pawns': []}, (4, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_keys.png', 'orientation': 2, 'pawns': []}, (6, 2): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_purse.png', 'orientation': 1, 'pawns': []}, (6, 4): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_grimoire.png', 'orientation': 2, 'pawns': []}, (0, 1): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, (0, 3): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (0, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_rat.png', 'orientation': 2, 'pawns': []}, (1, 0): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_ghost.png', 'orientation': 3, 'pawns': []}, (1, 1): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, (1, 2): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_owl.png', 'orientation': 0, 'pawns': []}, (1, 3): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, (1, 4): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, (1, 5): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, (1, 6): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (2, 1): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_scarab.png', 'orientation': 0, 'pawns': []}, (2, 3): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, (2, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 1, 'pawns': []}, (3, 0): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (3, 1): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_gnome.png', 'orientation': 2, 'pawns': []}, (3, 2): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_salamander.png', 'orientation': 1, 'pawns': []}, (3, 3): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, (3, 4): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (3, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': './tr_moth.png', 'orientation': 2, 'pawns': []}, (3, 6): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_dragon.png', 'orientation': 3, 'pawns': []}, (4, 1): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_genie.png', 'orientation': 2, 'pawns': []}, (4, 3): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (4, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (5, 0): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (5, 1): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (5, 2): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 2, 'pawns': []}, (5, 3): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_bat.png', 'orientation': 3, 'pawns': []}, (5, 4): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, (5, 5): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}, (5, 6): {'filepathTile': './tile_straight.png', 'filepathTreas': None, 'orientation': 1, 'pawns': []}, (6, 1): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 3, 'pawns': []}, (6, 3): {'filepathTile': './tile_t.png', 'filepathTreas': './tr_sorceress.png', 'orientation': 0, 'pawns': []}, (6, 5): {'filepathTile': './tile_corner.png', 'filepathTreas': None, 'orientation': 0, 'pawns': []}}
        
        #pawn display
        for position, tile in graphics_dict.items():
            if tile["pawns"]!=None:
                #position
                x0 = position[0]
        y0 = position[1]
        x = 70 + x0*100
        y = 70 + y0*100
        #create circles on the tile
        for color in tile["pawns"]:
            if color == "blue": 
                new_pawn = self.canvas_board.create_oval(x-20, y+10, x, y+10, fill = color  )
            elif color == "red": 
                new_pawn =self.canvas_board.create_oval(x-20, y-10, x, y-10, fill = color  ) 
            elif color == "green": 
                new_pawn =self.canvas_board.create_oval(x+20, y+10, x, y+10, fill = color  )      
            else:
                new_pawn =self.canvas_board.create_oval(x+20, y-10, x, y-10, fill = color  )  
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
