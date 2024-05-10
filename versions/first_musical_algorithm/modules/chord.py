from note import Note
from helpers import get_translations

class Chord:

    tonics       = [0, 3, 4, 6, 9]
    subDominant  = [2, 5, 8, 11]
    dominant     = [1, 5, 10]
                    

    def __init__(self, notes:tuple=(0,4,7), mod:str='M'):

        self.operations = []
        self.notes      = [Note(notes[0]), Note(notes[1]), Note(notes[2])]
        self.mod        = mod

    def fill_operations(self, transitions:list, ismelody:bool):
        # print(transitions)
        temp = []
        # if ismelody:
        #     for actualTransistions in transitions:
        #         temp = [get_translations()[item] for item in actualTransistions]
        #         print(temp)
        #         # self.operations.append([i for i in ])
        # else:
        for item in transitions:
            self.operations.append([i for i in get_translations()[item]])

    def test_fill(self, transitions:list, ismelody:bool):
        # print(ismelody)
        # if ismelody:
        #     returnChar = []
        #     print(transitions)
        #     for actualTransitions in transitions:
        #         print(actualTransitions)
        #         # returnChar.append()
        #         returnChar = [[i for i in get_translations()[item]] for item in actualTransitions]
        # else:
        returnChar = [[i for i in get_translations()[item]] for item in transitions]
        
        return returnChar
    
    def perform_operations(self, ismelody):
        # print('anything')
        # print(self.operations)
        while len(self.operations) > 0:
            operations = self.operations.pop(0)
            # print(operations)

            for item in operations:
                if item == 'R':
                    self.R()
                elif item == 'P':
                    self.P()
                elif item == 'L':
                    self.L()
                    # print('l')
                else:
                    print(item)
                    raise ValueError("Invalid tranformation in class Chord")
                # print(item, self)
            yield self
            
    def shift(self, direction:int):
        """
        direction == -1 for 0->1 | 1 for 0->2
        """

        holdVar = None
        if direction > 0:
            for num in range(0, len(self.notes), 1):
                if num == 0:
                    holdVar = self.notes[num]
                index = num + direction
                if index != len(self.notes):
                    self.notes[num] = self.notes[index]
                else:
                    self.notes[num] = holdVar
        else:
            for num in range(len(self.notes)-1, -1, -1):
                if num == len(self.notes)-1:
                    holdVar = self.notes[num]
                index = num + direction
                if num != 0:
                    self.notes[num] = self.notes[index]
                else:
                    self.notes[num] = holdVar
    
    def L(self):
        if self.mod == 'M':
            self.notes[0].flat(1)
            self.shift(1)
            self.mod = 'm'
        else:
            self.notes[2].sharp(1)
            self.shift(-1)
            self.mod = 'M'

    def R(self):
        if self.mod == 'M':
            self.notes[2].sharp(2)
            self.shift(-1)
            self.mod = 'm'
        else:
            self.notes[0].flat(2)
            self.shift(1)
            self.mod = 'M'

    def P(self):
        if self.mod == 'M':
            self.notes[1].flat(1)
            self.mod = 'm'
        else:
            self.notes[1].sharp(1)
            self.mod = 'M'

    @property
    def is_tonic(self):
        return True if self.notes[0].pitch in Chord.tonics else False

    @property
    def is_subDominant(self):
        return True if self.notes[0].pitch in Chord.subDominant else False
    
    @property
    def is_dominant(self):
        return True if self.notes[0].pitch in Chord.dominant else False
    
    def as_midi(self):
        return [note.as_midi() for note in self.notes]

    def __str__(self):
        return f'{[str(note) for note in self.notes]}, {self.mod}'


if __name__ == '__main__':
    chord = Chord()
    # chord.fill_operations(['L','P', 'R'])
    print(chord)

    chord.fill_operations(['P','L'])

    for _ in chord.perform_operations():
        print(_)

    # print(chord)


