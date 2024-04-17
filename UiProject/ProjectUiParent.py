"""

Jackson Butler
"""

from tkinter import ttk
from turtle import bgcolor
from customtkinter import *
from tkinter import *
import threading
import json
import sys
import os

class ProjectUi(CTkFrame):
    
    def __init__(self, master, root, project):
        super().__init__(master)
        self.__master = master
        self.__root = root
        
        self.workingDir = f"{self.__root.workingDir}/{project}"
        self.infoFileDir = f"{self.workingDir}/{self.__root.dataFolder}/info.json"
        self.loadFileDir = f"{self.workingDir}/{self.__root.dataFolder}/saved_population.json"
        self.saveFileDir = f"{self.workingDir}/{self.__root.dataFolder}/saved_population.json"
        
        sys.path.append(self.workingDir)
        import main
        
        self._project = main.Main()
        self._running = False
        self._active = False
        self._params = {}
        self._paramEntries = []
        
        self.grid()
        rowWeights = (1,1,1,1,1,0)
        colWeights = (1,1,1,0)

        for rows in range(len(rowWeights)):
            Grid.rowconfigure(self, rows, weight=rowWeights[rows])
        for cols in range(len(colWeights)):
            Grid.grid_columnconfigure(self, cols, weight=colWeights[cols])
            
        self.create_widgets()
        
    def create_widgets(self):
        # Main Output Box
        self._outputBox = CTkTextbox(self, corner_radius=5, wrap=NONE)
        self._outputBox.configure(state='disabled')
        self._outputBox.grid(row=0, column=0, rowspan=5, columnspan=3, padx=20, pady=20,sticky=N+S+E+W)
        self._outputBox.bind("<Enter>", self._on_text_box_hover)
        self._outputBox.bind("<Leave>", self._on_text_box_hover_leave)
        
        # Switch Main Output Box for a Table
        # self._outputTableContainer = CTkFrame(self)
        # self._paramContainer.configure(fg_color="#FFFFFF", corner_radius=5)
        # self._paramContainer.grid(row = 0, column = 3, rowspan=5, padx=20,pady=20, sticky=N+E+S+W)
        # self._paramContainer.grid_columnconfigure(0, weight=1)
        # self._paramContainer.grid_rowconfigure(0, weight=1)
        # self._outputTable = ttk.Treeview(self)
        # self._outputTable.grid(row=0, column=0, rowspan=5, columnspan=3, padx=20,pady=20,sticky=N+E+S+W)
        
        # Visualize Params
        self._paramContainer = CTkFrame(self)
        self._paramContainer.configure(corner_radius=5)
        self._paramContainer.grid(row = 0, column = 3, rowspan=5, padx=20,pady=20, sticky=N+E+S+W)
        # _paramContainer.pack(side=TOP, fill=BOTH, expand = True)
        self._paramContainer.grid_columnconfigure(0, weight=0)
        self._paramContainer.grid_columnconfigure(1, weight=0)
        
        self._params = self._project.get_params()
        count = 0
        for key,value in self._params.items():
            self._paramContainer.grid_rowconfigure(count, weight=0)
            
            label = CTkLabel(self._paramContainer, text=key+":")
            label.grid(row=count, column=0, sticky=N+S+E)
            
            entry = CTkEntry(self._paramContainer, placeholder_text=value)
            entry.insert('0', value)
            entry.grid(row=count, column=1, sticky=N+S+E)
            self._paramEntries.append(entry)

            count+=1
            
        # Run Save File Path
        # self._paramContainer.grid_rowconfigure(count, weight=0)

        # self.runBoxLabel = CTkLabel(self._paramContainer, text="Save Run Stats")
        # self.runBoxLabel.grid(row=count, column=0, sticky=N+S+E)
        # self.saveRun = StringVar(value=ON)
        # self.saveRunBox = CTkCheckBox(self._paramContainer, text='', command=self._save_run_check(),
        #                              variable=self.saveRun, onvalue=ON, offvalue=OFF)
        # self.saveRunBox.grid(row=count, column=1, sticky=N+S+E)
        # count +=1
        
        # Load Population
        self.loadButton = CTkButton(self, text="Load", command=lambda : self._load_population_from_file(), corner_radius=1, height=10)
        self.loadButton.grid(row=5, column=0, sticky=E+W, pady=10)
        
        # Save Population
        self.saveButton = CTkButton(self, text="Save", command=lambda : self._project.save_population_to_file(self._params, self.saveFileDir), corner_radius=1, height=10)
        self.saveButton.grid(row=5, column=1, sticky=E+W, pady=10)
        
        # Update Simulation
        self._updateButton = CTkButton(self, text="Update", command=lambda : self._update_project_params(), corner_radius=1, height=10)
        self._updateButton.grid(row=5, column=2, sticky=E+W, pady=10)
        
        # Run/Pause Simulation
        self._stopButton = CTkButton(self, text="Stop", command=lambda : self._run_toggle(), corner_radius=1, height=10)
        self._stopButton.grid(row=5, column=3, sticky=E+W, pady=10)
        self._stopButton.grid_forget()
        self._runButton = CTkButton(self, text="Run", command=lambda : self._run_toggle(), corner_radius=1, height=10)
        self._runButton.grid(row=5, column=3, sticky=E+W, pady=10)
        
    def _save_run_check(self):
        print("checkbox toggled, current value:", self.saveRun.get())
    
    def _load_population_from_file(self):
        print('load')
        self._project.load_population_from_file(self.loadFileDir)
        print(self._project.get_params())
        self._update_entries()
            
    def _update_entries(self):
        count = 0
        self._params = self._project.get_params()
        tempParams = []
        for value in self._params.values():
            entry = self._paramEntries[count]
            
            entry.delete("0", END)
            entry.insert('0', value)

            tempParams.append(entry)

            count+=1
        self._paramEntries = tempParams
        
    def _update_project_params(self):
        count = 0
        for key,value in self._params.items():
            entry = self._paramEntries[count].get()
            print(key,entry)
            if isinstance(value, int):
                entry = int(entry)
            elif isinstance(value, float):
                entry = float(entry)
            elif isinstance(value, bool):
                entry = bool(entry)
            elif isinstance(value, str):
                entry = str(entry)
            self._params[key] = entry
            count+= 1
        self._project.update_params(self._params)
        
    def _run_toggle(self):
        if self._running:
            print("Stop")
            self._running = False
            self._runButton.grid_forget()
            self._stopButton.grid(row=5, column=3, sticky=E+W)
        else:
            print("start")
            self._running = True
            threading.Thread(self.run()).start()
            self._stopButton.grid_forget()
            self._runButton.grid(row=5, column=3, sticky=E+W)
        
    def run(self):
        self._outputBox.configure(state='normal')
        for gen_info in self._project.run():
            print(gen_info)
            self._outputBox.insert("0.0", f"| {self._project.curGeneration} {gen_info}\n")
            if not self._running:
                break
        self._outputBox.insert("0.0", self._project.stringHeader)
        self._outputBox.configure(state='disabled')
        
        if self._running:
            self._run_toggle()
    
    def _on_text_box_hover(self, e):
        self._outputBox.configure(scrollbar_button_color=self.__root.SCROLL_COLOUR)

    def _on_text_box_hover_leave(self, e):
        self._outputBox.configure(scrollbar_button_color=self.__root.BG_COLOUR)

    
if __name__ == "__main__":
    pass

