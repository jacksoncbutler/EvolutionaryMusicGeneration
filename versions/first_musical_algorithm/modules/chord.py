from note import Note
from helpers import get_translations

class Chord:

    num_to_chord = ['_', 'C', 'D','E','F','G','A','B']
    tonics       = [(1, 'natural'), (3, 'flat'), (5, 'flat'), (6, 'natural')]
    subDominant  = [(2, 'natural'), (4, 'natural'), (6, 'flat'), (7, 'natural')]
    dominant     = [(2, 'flat'), (3, 'natural'), (6, 'natural'), (7, 'flat')]

    def __init__(self, notes:tuple=(1,3,5), flats:tuple=('natural', 'natural', 'natural'), mod:str='M'):

        self.operations = []
        self.notes      = [Note(notes[0], flats[0]), Note(notes[1], flats[1]), Note(notes[2], flats[2])]
        self.mod        = mod

    def fill_operations(self, transitions:list):
        # print(transitions)
        for item in transitions:
            # print(item)
            self.operations.append([i for i in get_translations()[item]])

    def test_fill(self, transitions:list):
        return [[i for i in get_translations()[item]] for item in transitions]
    
    def perform_operations(self):
        # print('anything')
        # print(self.operations)
        while len(self.operations) > 0:
            operations = self.operations.pop()
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
                if num == 2:
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
        return True if (self.notes[0].value, self.notes[0].mod) in Chord.tonics else False

    @property
    def is_subDominant(self):
        return True if (self.notes[0].value, self.notes[0].mod) in Chord.subDominant else False
    
    @property
    def is_dominant(self):
        return True if (self.notes[0].value, self.notes[0].mod) in Chord.dominant else False

    def chord_string(self):
        return f'{Chord.num_to_chord[self.notes[0].value]}{self.mod}'
    
    def as_midi(self):
        return [note.as_midi() for note in self.notes]


    def __str__(self):
        return f'{[str(note) for note in self.notes]}, {self.mod}, Chord: {self.chord_string()}'



if __name__ == '__main__':
    chord = Chord()
    # chord.fill_operations(['L','P', 'R'])
    print(chord)

    chord.fill_operations(['P','L'])

    for _ in chord.perform_operations():
        print(_)

    # print(chord)


