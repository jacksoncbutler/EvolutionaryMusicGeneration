

class Note:

    translate = {'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G':5, 'A': 6, 'B': 7}

    def __init__(self, note:int|str=1, mod:str='natural', octave:int=4, octaveRange:tuple=(0,8)):
        self.mod = mod.lower()  # Can be 'natural' or 'flat'

        if isinstance(note, int):
            self.value = note  # Can be any int between 1 and 7 inclusive
        elif isinstance(note, str):
            self.value = Note.translate[note]  # Can be any str between A and F inclusive
        else:
            raise ValueError("bad note value")
        
        self.octave = octave
        self.octaveRange = octaveRange

    def flat(self, num:int=1):
        for _ in range(num):
            if self.value == 1:
                self.value = 7
                if (self.octave - 1) in [i for i in range(*self.octaveRange)]:
                    self.octave -= 1
            elif self.value == 4:
                self.value -= 1
            elif self.mod == 'flat':
                self.value -= 1
                self.mod = 'natural'
            else:
                self.mod = 'flat'
    
    def sharp(self, num:int=1):
        for _ in range(num):
            if self.value == 7:
                self.value = 1
                if (self.octave + 1) in [i for i in range(*self.octaveRange)]:
                    self.octave += 1
            elif self.value == 3 and self.mod == 'natural':
                self.value += 1
            elif self.mod == 'natural':
                self.value += 1
                self.mod = 'flat'
            else:
                self.mod = 'natural'

    def __str__(self):
        return f'{self.value}, {self.mod}'



if __name__ == '__main__':
    x = Note(1)

    x.sharp()
    print(x)
    x.flat()
    print(x)
    x.sharp(2)
    print(x)
            



