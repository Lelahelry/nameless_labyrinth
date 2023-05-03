import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class Game_window():
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Labyrinth - the aMAZEing game")
        self.root.geometry("300x350")
        # management of the communication with the game class
            
        ########################################
        # Graphic window settings
        ########################################
        # graphical elements
        self.folder = "./textures" # adresse 
        # canva size
        self.f_graph_height = 2000
        self.f_graph_width = 2000

        # display window setting
        self.f_graph = None
        # test parameters
        self.playernames_e = list()
        self.playernames = list()
        # widgets creation
        self.widgets_creation(self.root)

    def widgets_creation(self, root):
        # text
        self.welcome = ctk.CTkLabel(root, height = 160, text = "Welcome to the aMAZEing Labyrinth - Software version !", text_color = "DodgerBlue4", font = ('Calibri', 28, 'bold'))
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
        for i in range(len(self.playernames_e)):
            name = str(self.playernames_e[i].get())
            if name == "":
                    name = "Player" + str(i+1)
                    self.playernames.append(name)
        # init the game through message
        # creation of the graphic window
        if (self.f_graph == None) :
            self.f_graph = ctk.CTkToplevel(self.root)
            self.f_graph.width = self.f_graph_width
            self.f_graph.height = self.f_graph_height
            # canvas for the board
            self.f_graph.canvas_board = tk.Canvas(self.f_graph, height = self.f_graph.height, width = self.f_graph.width - 800)
            self.background = tk.PhotoImage(file = self.folder + '\\board.png')
            self.item = self.f_graph.canvas_board.create_image(500, 300, image = self.background, anchor = 'c')
            """self.item.resize((1000,1000))"""
            self.f_graph.canvas_board.lower(self.item)
            self.f_graph.canvas_board.pack(side = tk.LEFT)
            # canvas for the card of the current objective
            self.f_graph.canvas_card = tk.Canvas(self.f_graph, height = self.f_graph.height/2, width = 800, bg = "magenta")
            self.f_graph.canvas_card.pack(side = tk.RIGHT)
        # self.place_objects()
        
    """ def place_objects():
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