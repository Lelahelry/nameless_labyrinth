import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class Game_window():
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Labyrinth - the aMAZEing game")
        self.root.geometry("1000x600")
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
        self.welcome = ctk.CTkLabel(root, height = 110, text = "Welcome to the aMAZEing Labyrinth - Software version !", text_color = "DodgerBlue4", font = ('Calibri', 28, 'bold'))
        self.welcome.pack(side = tk.TOP)

        self.label = ctk.CTkLabel(root, height = 40, text = "Choose the number of players and enter their names :", font = ('Calibri', 20))
        self.label.pack(side = tk.TOP)

        # player number
        self.player_number = tk.IntVar()
        self.scale = ctk.CTkSlider(root, height = 30, width = 455, progress_color = "goldenrod", fg_color = "DodgerBlue4",  button_corner_radius = 5, button_color = "goldenrod", button_hover_color = "DodgerBlue4", from_ = 2, to = 4, number_of_steps = 2, orientation = "horizontal", variable = self.player_number)

        self.scale.pack(pady = 20, anchor = ctk.CENTER)
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
                entry.pack(padx = 10, pady = 6, anchor = ctk.CENTER)
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
            self.f_graph.geometry("1000x600")
            
            #bouton "mon tour est fini"?
            self.button_done = ctk.CTkButton(self.f_graph, text = "My turn is over.", corner_radius = 8, height = 30, width = 15, fg_color = "goldenrod", hover_color = "DodgerBlue4", font = ('Calibri', 20))
            #self.button_done.bind('<Button-1>', self.turn_over())
            self.button_done.pack(side = ctk.BOTTOM, fill = 'x')
            
            self.canvas_for_board()
           
            self.slide_tiles_buttons()
            
            self.canvas_for_objective() 
            
            self.text_area()
            
            self.canvas_for_hand()

            #self.images()

            self.turn_tile_buttons()
            
            self.validate_buttons()

            
            

    def canvas_for_board(self):
        """creates the canva for the board with the background
        no input
        no output"""
        
        self.f_graph.canvas_board = tk.Canvas(self.f_graph, width = 1100, height = 1100)
        
        self.background = tk.PhotoImage(file = self.folder + '\\zoomed_board.png')
        self.item = self.f_graph.canvas_board.create_image(550, 550, image = self.background)
        self.f_graph.canvas_board.lower(self.item)
        
        self.f_graph.canvas_board.pack(side = tk.LEFT, padx=40, pady=40)

    def slide_tiles_buttons(self):
        """creates the buttons around the board allowing to choose where to insert the tile
        no input
        no output"""
        #sliding option buttons
        #bind them to slide tile with a parameter(to be chosen)
        #validate button 
        #bind it to controller somehow

    def canvas_for_objective(self):
        """creates canvas to display the objective of the player"""
        self.f_graph.canvas_card = tk.Canvas(self.f_graph, bg = "magenta", width = 550, height = 800)
        self.objective_image()
        #self.f_graph.canvas_card.pack(side = tk.TOP, anchor='e', expand = True)

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
        self.f_graph.canvas_tile = tk.Canvas(self.f_graph, bg = "grey", width = 500, height = 500)

        
       
        self.hand_image(self.f_graph.canvas_tile)
        self.f_graph.canvas_tile.pack(side = tk.BOTTOM, anchor = 'w', padx=50, expand = True)

    def turn_tile_buttons(self):
        """creates the buttons next to the hand allowing to turn the orientation of the hand tile
        no input
        no output"""
        #turning buttons
        
    def validate_buttons(self):
        """creates the button under the hand to validate the chosen orientation and insertion
        no input
        no output"""    
        #validate button 
        #bind it to controller somehow

    def images(self):
        """creates the board objects and binds them all
        no input
        no output"""
        self.image_library()

        self.objective_image()
        
        self.hand_image()
           
        #self.grid_images()    

        #self.place_pawns()

    def objective_image(self):
        self.f_graph.canvas_card.pack(side = tk.TOP, anchor='e', expand = True)

        
    def image_library(self, filepath):
        """loads and sizes all PNG files (not arrows)
        no input
        no output"""
        pass
        #load the 3 tile images and resize them
        self.tile_c = tk.PhotoImage(file = self.folder + '\\tile_corner.png')
        self.tile_t = tk.PhotoImage(file = self.folder + '\\tile_t.png')
        self.tile_s = tk.PhotoImage(file = self.folder + '\\tile_straight.png')
        
        #load the 24 treas images and resize them for display
        #wel not opti i think
        

    def hand_image(self, canvas):
        """displays the hand in its canvas and binds it to the rotation
        no input
        no output"""
        
        #filepath_t = self.controller.hand.filepath à la place de filepath_t = ...
        filepath_ti="\\tile_corner.png"
        #filepath_tr = self.Controller.hand.treasure.filepath
        filepath_tr = "\\tr_bat.png"
        self.tile_h = tk.PhotoImage(file = self.folder + filepath_ti)
        self.tile_h_resized = self.tile_h.zoom(3,3)
        self.bg = canvas.create_image(250, 250, image = self.tile_h_resized)
        canvas.lower(self.bg)

        self.tile_t = tk.PhotoImage(file = self.folder + filepath_tr)
        self.tile_t_resized = self.tile_t.zoom(3,3)
        self.fg = canvas.create_image(250, 250, image = self.tile_t_resized)
        canvas.lift(self.fg)
        
        #self.f_graph.canvas_tile.pack(side = tk.BOTTOM, anchor = 'w', padx=50, expand = True) 
        
        
        
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
        pass
        #use the grid to create all the other tiles
            #choose the tile
            #place the treasure on it
            #place the image on its spot
        #bind method de rotation 
        #stock the tile in a dict



        
        self.tile_c = tk.PhotoImage(file = self.folder + '\\tile_corner.png')
        self.item2 = self.f_graph.canvas_board.create_image(100, 100, image = self.tile_c)
        self.treas1 =  tk.PhotoImage(file = self.folder + '\\tr_bat.png')
        self.item21 = self.f_graph.canvas_board.create_image(100, 100, image = self.treas1)


        
        self.f_graph.canvas_board.lift(self.item2)
        self.f_graph.canvas_board.lift(self.item21)
        self.item3 = self.f_graph.canvas_board.create_image(246, 100, image = self.tile_c)
        self.f_graph.canvas_board.lift(self.item3)
        self.item4 = self.f_graph.canvas_board.create_image(100, 246, image = self.tile_c)
        self.f_graph.canvas_board.lift(self.item4)

    def anim_silde_tile(self):
        """pour slider les tiles à l'écran"""
        pass
        #effacer bout
        # animer translation des 6 d'avant
        # ajouter la première
        
    def place_pawns(self):
        """place circles for the pawn"""
        pass
        #place pawns and bind them to moving animation
    """
    def turn_over(self, event):
        validates that the player is done with his turn and communicates the changes of player back and forth with the controller
        no input
        output

        
               
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
    



        
if __name__ == "__main__":
    app = Game_window()
    app.root.mainloop()