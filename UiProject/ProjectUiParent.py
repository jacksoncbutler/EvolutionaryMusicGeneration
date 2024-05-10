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
        self.loadPopulationFileDir = f"{self.workingDir}/{self.__root.dataFolder}/saved_population.json"
        self.savePopulationFileDir = f"{self.workingDir}/{self.__root.dataFolder}/saved_population.json"
        self.loadParamsFileDir = f"{self.workingDir}/{self.__root.dataFolder}/saved_parameters.json"
        self.saveParamsFileDir = f"{self.workingDir}/{self.__root.dataFolder}/saved_parameters.json"
        
        sys.path.append(self.workingDir)
        import main
        from modules.helpers import play_midi, output_to_midi

        self.play_midi = play_midi
        self.output_to_midi = output_to_midi
        self._playing = False
        self.musicFileDir = f"midi_file.mid"
        self.exampleMidiDir = f"{self.workingDir}/{self.__root.dataFolder}/midi_file.mid"

        self._project = main.Main()
        self._running = False
        self._active = False
        self._params = {}
        self._paramEntries = {}
        
        self.grid()
        rowWeights = (0,1,1,1,1,1,0)
        colWeights = (1,1,1,1,1,0)

        for rows in range(len(rowWeights)):
            Grid.rowconfigure(self, rows, weight=rowWeights[rows])
        for cols in range(len(colWeights)):
            Grid.grid_columnconfigure(self, cols, weight=colWeights[cols])
            
        self.create_widgets()
        
    def create_widgets(self):
        # Main Output Box
        self._outputBox = CTkTextbox(self, corner_radius=5, wrap=NONE)
        self._outputBox.configure(state='disabled')
        self._outputBox.grid(row=1, column=0, rowspan=5, columnspan=5, padx=20, pady=20,sticky=N+S+E+W)
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
        self._paramContainer.grid(row = 1, column = 5, rowspan=4, padx=20,pady=20, sticky=N+E+S+W)
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
            self._paramEntries[key] = entry

            count+=1
        
        self._musicPlayerContainer = CTkFrame(self)
        self._musicPlayerContainer.configure(corner_radius=5)
        self._musicPlayerContainer.grid(row = 5, column = 5, sticky=N+E+S+W)
        self._musicPlayerContainer.grid_rowconfigure(1, weight=1)
        self._musicPlayerContainer.grid_columnconfigure(1, weight=1)
        self._musicPlayerContainer.grid_columnconfigure(2, weight=1)
        self._musicPlayerContainer.grid_columnconfigure(3, weight=1)

        self._playMusic = CTkButton(self._musicPlayerContainer, text="Play", command=lambda : self.play_midi(self.musicFileDir), corner_radius=1, height=15)
        self._playMusic.grid(row=0, column=2, sticky=N+E+S+W, pady=0)

        # Run Save File Path
        # self._paramContainer.grid_rowconfigure(count, weight=0)

        # self.runBoxLabel = CTkLabel(self._paramContainer, text="Save Run Stats")
        # self.runBoxLabel.grid(row=count, column=0, sticky=N+S+E)
        # self.saveRun = StringVar(value=ON)
        # self.saveRunBox = CTkCheckBox(self._paramContainer, text='', command=self._save_run_check(),
        #                              variable=self.saveRun, onvalue=ON, offvalue=OFF)
        # self.saveRunBox.grid(row=count, column=1, sticky=N+S+E)
        # count +=1
        
        # Clear Output
        self.clearOuputButton = CTkButton(self, text="Clear", command=lambda : self._clearOutput(), corner_radius=1, height=8)
        self.clearOuputButton.grid(row=1, column=0, sticky=N+E+W, pady=0)

        # Clear Output
        self.outputCurGenButton = CTkButton(self, text="Current Gen", command=lambda : self._outputCurGen(), corner_radius=1, height=8)
        self.outputCurGenButton.grid(row=1, column=1, sticky=N+E+W, pady=0)

        # Load Population
        self.loadPopulationButton = CTkButton(self, text="Load Pop", command=lambda : self._load_population_from_file(), corner_radius=1, height=10)
        self.loadPopulationButton.grid(row=6, column=0, sticky=E+W, pady=10)
        
        # Save Population
        self.savePopulationButton = CTkButton(self, text="Save Pop", command=lambda : self._project.save_population_to_file(self.savePopulationFileDir), corner_radius=1, height=10)
        self.savePopulationButton.grid(row=6, column=2, sticky=E+W, pady=10)

        # Load Params
        self.loadParamsButton = CTkButton(self, text="Load Params", command=lambda : self._load_params_from_file(), corner_radius=1, height=10)
        self.loadParamsButton.grid(row=6, column=1, sticky=E+W, pady=10)

        # Save Params}
        self.saveParamsButton = CTkButton(self, text="Save Params", command=lambda : self._project.save_params_to_file(self._params, self.saveParamsFileDir), corner_radius=1, height=10)
        self.saveParamsButton.grid(row=6, column=3, sticky=E+W, pady=10)
        
        # Update Simulation
        self._updateButton = CTkButton(self, text="Update", command=lambda : self._update_project_params(), corner_radius=1, height=10)
        self._updateButton.grid(row=6, column=4, sticky=E+W, pady=10)
        
        # Run/Pause Simulation
        self._stopButton = CTkButton(self, text="Stop", command=lambda : self._run_toggle(), corner_radius=1, height=10)
        self._stopButton.grid(row=6, column=5, sticky=E+W, pady=10)
        self._stopButton.grid_forget()
        self._runButton = CTkButton(self, text="Run", command=lambda : self._run_toggle(), corner_radius=1, height=10)
        self._runButton.grid(row=6, column=5, sticky=E+W, pady=10)

    def _save_run_check(self):
        print("checkbox toggled, current value:", self.saveRun.get())
    
    def _load_population_from_file(self):
        print('load')
        self._project.load_population_from_file(self.loadPopulationFileDir)
        print(self._project.get_params())
        self._update_entries()

    def _load_params_from_file(self):
        print('load')
        self._project.load_params_from_file(self.loadParamsFileDir)
        print(self._project.get_params())
        self._update_entries()
            
    def _update_entries(self):
        self._params = self._project.get_params()
        tempParams = {}
        for key,value in self._params.items():
            entry = self._paramEntries[key]
            
            entry.delete("0", END)
            entry.insert('0', value)

            tempParams[key] = entry

        self._paramEntries = tempParams
        del tempParams

    def _update_entry(self, target):
        value = eval(f'self._project.{target}')
        # print("VALUE", value)
        entry = self._paramEntries[target]
        entry.delete("0", END)
        entry.insert('0', value)
        self._paramEntries[target] = entry
        self._params[target] = value
        
    def _update_project_params(self):
        count = 0
        for key,value in self._params.items():
            entry = self._paramEntries[key].get()
            # print(key,entry)
            if isinstance(value, int):
                entry = int(entry)
            elif isinstance(value, float):
                entry = float(entry)
            elif isinstance(value, bool):
                entry = bool(entry)
            elif isinstance(value, str):
                entry = str(entry)
            elif isinstance(value, list):
                print(value)
                entry = str(value).strip(' ').split(',')
            elif isinstance(value, tuple):
                print(value)
                entry = str(value).strip(' ').split(',')
            self._params[key] = entry
            count+= 1
        self._project.update_params(self._params)

    def _clearOutput(self):
        self._outputBox.configure(state='normal')
        self._outputBox.delete("0.0", END)
        self._outputBox.configure(state='disabled')

    def _outputCurGen(self):
        self._outputBox.configure(state='normal')
        self._outputBox.insert("0.0", f"| {self._project.curGeneration} {self._project._curPopulation} |\n")
        self._outputBox.configure(state='disabled')
        
    def _run_toggle(self):
        if self._running:
            print("Stop")
            self._running = False
            self._runButton.grid_forget()
            self._stopButton.grid(row=6, column=5, sticky=E+W)
        else:
            print("start")
            self._running = True
            threading.Thread(self.run()).start()
            self._stopButton.grid_forget()
            self._runButton.grid(row=6, column=5, sticky=E+W)
        
    def run(self):
        self._outputBox.configure(state='normal')
        for gen_info in self._project.run():

            print(gen_info)
            self._outputBox.insert("0.0", f"| {self._project.curGeneration} {gen_info}\n")
            self._update_entry('curGeneration')
            self._update_entry('curRun')

            if not self._running:
                break
        self._outputBox.insert("0.0", self._project.stringHeader)
        self._outputBox.configure(state='disabled')
        
        if self._running:
            self._run_toggle()
        
        self.output_to_midi(gen_info._midiChords, gen_info._midiChords, self.musicFileDir)
        
    
    def _on_text_box_hover(self, e):
        self._outputBox.configure(scrollbar_button_color=self.__root.SCROLL_COLOUR)

    def _on_text_box_hover_leave(self, e):
        self._outputBox.configure(scrollbar_button_color=self.__root.BG_COLOUR)

    
if __name__ == "__main__":
    pass

