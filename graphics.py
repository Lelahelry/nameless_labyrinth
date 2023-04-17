import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class Game_window():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Labyrinth - the aMAZEing game")
        self.root.geometry("600x400")
        #management of the communication with the game class
            
        ########################################
        # Graphic window settings
        ########################################
        #graphical elements
        folder = "C:\\Users\\cleme\\Documents\\INSA\\cours\\2A\\algo\\nameless_labyrinth\\textures"#adresse 
        # canva size
        self.f_graph_height = 650
        self.f_graph_width = 650

        # display window setting
        self.f_graph = None
        
        # widgets creation
        self.widgets_creation(self.root)

    def widgets_creation(self):
        #player number
        #player names
        #launch game
        self.button_launch = tk.Button(root, text = "Start game", height = 1, width = 15)
        self.button_launch.bind('<Button-1>', self.game_launch)
        self.button_launch.pack(side = tk.BOTTOM, fill='x')
        #quit
    #launch callback
    def game_launch(self, message):
        """creation of the window"""
        #init game through message
        #create the graphic window
        if (self.f_graph == None) :
            self.f_graph = tk.Toplevel(self.racine)
            self.f_graph.width = self.f_graph_width
            self.f_graph.height = self.f_graph_height
            self.f_graph.canvas = tk.Canvas(self.f_graph, height = self.f_graph.height+150, width = self.f_graph.width+150)
            self.backgroundImage=root.PhotoImage(file = folder+"//board.png")
            self.f_graph.canevas.pack()
        self.place_objects()
        
    def place_objects():
        grid = #board read through message
        for position, tile in grid.items():
            #get the type of tile and orientation
            self.background = PhotoImage(file='C:/Users/cleme/Pictures/meduse.png')
            self.item = self.f_graph.canvas.create_image(100, 100, image=self.background, anchor='c')
            self.f_graph.canvas.lower(self.item)
        #read the current player, display his name and his objective
    #graphic window
        #initialize
        #set background
        #read grid to fill the graphic grid + read the treasure and pawn to draw them...
        #read the hand and display it
        #read the current player, display his name and his objective






"""récupération des positions de clic"""
def affiche_info_ville(self,event):
        self.text_area.delete("1.0", "end")
        mouseX = event.x
        mouseY = event.y
        ident = self.f_graph.canevas.find_withtag("current")[0]
        item_clicked = self.dicoSommetsGraphiques[ident]
        self.text_area.insert(tk.INSERT,item_clicked)