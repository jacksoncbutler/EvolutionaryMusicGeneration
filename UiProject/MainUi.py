"""

Jackson Butler
"""
from ProjectUiParent import ProjectUi
from tkinter import *
from customtkinter import *
import os

""" Include error checking for os.abspath stuff """

class App(CTk):
    APP_BORDER = "#222233"
    BG_COLOUR = "#444455"
    SCROLL_COLOUR = "gray45"
    BUTTON_HOVER = "#325882"
    
    def __init__(self, workingDir=os.path.abspath("versions"), dataFolder="data", descriptionFileName="description.txt"):
        super().__init__()
        
        self.title("Evolutionary GUI")
        self.geometry("500x400")
        # self.bg = self.BG_COLOUR
        
        self.workingDir = workingDir
        self.dataFolder = dataFolder
        self.descriptionFileName = descriptionFileName
        
        
        master = CTkFrame(self)
        master.pack(side = "top", fill = "both", expand = True)
        master.grid_rowconfigure(0, weight = 1)
        master.grid_columnconfigure(0, weight = 1)
        
        self.homeFrame = ProjectSelection(master, self)
        self.show_frame('first', self.homeFrame)
        
    def show_frame(self, oldPage, page,):
        if oldPage != 'first':
            oldPage.pack_forget()
            oldPage.grid_forget()

        page.tkraise()
        page.pack(side = "top", fill = "both", expand = True)
        page.grid(row = 0, column = 0, sticky ="nsew")
        

class ProjectSelection(CTkFrame):

    def __init__(self, master, root):
        super().__init__(master)
        self.__master = master
        self.__root = root
        self.selected = None
        self.scroll_hover = False
        self.text_hover = False

        self.grid()
        rowWeights = (1,1,0)
        colWeights = (0,0,1)

        for rows in range(len(rowWeights)):
            Grid.rowconfigure(self, rows, weight=rowWeights[rows])
        for cols in range(len(colWeights)):
            Grid.grid_columnconfigure(self, cols, weight=colWeights[cols])

        self.create_widgets()

    def create_widgets(self):

        # Button Frame Instantiation
        self.buttonFrame = CTkScrollableFrame(self, corner_radius=1)
        
        # Inserting a button for each file in projectDir into buttonFrame
        for line in sorted(os.listdir(projectDir)):
            CTkButton(self.buttonFrame, text=line, 
                      command= lambda x=line : self.on_click(x), 
                      corner_radius=1, 
                      anchor=W, 
                      border_spacing=5
                    ).pack(anchor=W, fill=X)
        # Places buttonFrame into grid
        self.buttonFrame.update()
        self.buttonFrame.grid(row=0, column=0, rowspan=3, sticky=N+S+E+W)
        
        # Scroll Hover State Bindings
        self.buttonFrame._parent_canvas.bind("<Enter>", self.on_scroll_hover)
        self.buttonFrame._parent_canvas.bind("<Leave>", self.on_scroll_hover_leave)
        # self.buttonFrame._scrollbar.bind("<Enter>", self.on_scroll_hover)
        # self.buttonFrame._scrollbar.bind("<Leave>", self.on_scroll_hover_leave)

        # Linux Scrollwheel Bindings 
        # Causes all scrollable interfaces to move
        # self.buttonFrame._scrollbar._canvas.bind_all("<Button-4>", lambda e: self.on_button_scroll(1))
        # self.buttonFrame._scrollbar._canvas.bind_all("<Button-5>", lambda e: self.on_button_scroll(-1))
    
        # Description Box Instantiation
        self.descriptionBox = CTkTextbox(self)
        self.descriptionBox.configure(state='disabled')
        self.descriptionBox.grid(row=0, column=2, rowspan=2, sticky=N+S+E+W)

        # Description Box Hover State Bindings
        self.descriptionBox.bind("<Enter>", self.on_text_hover)
        self.descriptionBox.bind("<Leave>", self.on_text_hover_leave)
        self.descriptionBox._y_scrollbar._canvas.bind("<Enter>", self.on_text_hover)
        self.descriptionBox._y_scrollbar._canvas.bind("<Leave>", self.on_text_hover_leave)
        # self.descriptionBox._y_scrollbar._canvas.bind("<Button-4>", lambda e: self.on_text_scroll(1))
        # self.descriptionBox._y_scrollbar._canvas.bind("<Button-5>", lambda e: self.on_text_scroll(-1))
        # self.descriptionBox.bind("<Enter>", self.on_text_hover)
        # self.descriptionBox.bind("<Leave>", self.on_text_hover_leave)
        

        # Open Button Instantiation
        self.open = CTkButton(self, text="Open", command=lambda : self.on_open(), corner_radius=1, height=10)
        self.open.grid(row=2, column=2, sticky=N+S+E+W)


    def on_click(self, project):
        self.selected = project

        self.descriptionBox.configure(state='normal')
        self.descriptionBox.delete("0.0", END)
        
        # self.descriptionBox = CTkTextbox(self)
        with open(f"{self.__root.workingDir}/{self.selected}/{self.__root.dataFolder}/{self.__root.descriptionFileName}", 'r') as file:
            description = file.readlines()
            for index in range(len(description)-1, -1, -1):
                line = description[index]
                self.descriptionBox.insert("0.0", line)

            self.descriptionBox.configure(state='disabled')
            # self.descriptionBox.grid(row=0, column=2, rowspan=2, sticky=N+S+E+W)

        
    def on_open(self):
        print(f"Open {self.selected}")
        self.__root.show_frame(self, ProjectUi(self.__master, self.__root, self.selected))


    
    def on_scroll_hover(self, e):
        self.scroll_hover = True
        self.buttonFrame.configure(scrollbar_button_color=self.__root.SCROLL_COLOUR)
    
    def on_scroll_hover_leave(self, e):
        self.scroll_hover = False
        self.buttonFrame.configure(scrollbar_button_color=self.__root.APP_BORDER)

    def on_text_hover(self, e):
        self.text_hover = True
        self.descriptionBox.configure(scrollbar_button_color=self.__root.SCROLL_COLOUR)
    
    def on_text_hover_leave(self, e):
        self.text_hover = False
        self.descriptionBox.configure(scrollbar_button_color=self.__root.BG_COLOUR)

    # def on_button_scroll(self, scroll):
    #     self._delta = scroll
    #     if self.scroll_hover and not self.text_hover:
    #         self.descriptionBox._y_scrollbar._mouse_scroll_event(self)

    # def on_text_scroll(self,scroll):
    #     self._delta = scroll
    #     if self.text_hover and not self.scroll_hover:
    #         self.buttonFrame._scrollbar._mouse_scroll_event(self)

    @property
    def delta(self):
        return self._delta
        

if __name__ == '__main__':
    # print()
    customTheme = "deep-blue"
    projectDir = "versions"
    projectDir = os.path.abspath(projectDir)

    set_default_color_theme(os.path.abspath(f"UiProject/custom-themes/{customTheme}.json"))
    app = App(workingDir=projectDir)

    app.mainloop()

    