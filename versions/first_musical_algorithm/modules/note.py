

class Note:

    def __init__(self, note:int=0, octave:int=4, octaveRange:tuple=(0,8)):
        self.pitch = note  # Can be any int between 0 and 11 inclusive
        
        self.octave = octave
        self.octaveRange = octaveRange

    def flat(self, num:int=1):
        for _ in range(num):
            if self.pitch == 0:
                if (self.octave - 1) in [i for i in range(*self.octaveRange)]:
                    self.octave -= 1
            self.pitch = (self.pitch - 1) % 12
            
    
    def sharp(self, num:int=1):
        for _ in range(num):
            if self.pitch == 11:
                if (self.octave + 1) in [i for i in range(*self.octaveRange)]:
                    self.octave += 1
            self.pitch = (self.pitch + 1) % 12
            

    def as_midi(self):
        return self.pitch + (self.octave *12)

    def __str__(self):
        return f'{self.pitch}'
    

if __name__ == '__main__':
    x = Note(0)
    print(x)
    print(x.as_midi())
    x.sharp()
    print(x.as_midi())
    x.sharp()
    print(x.as_midi())
    x.sharp()
    print(x.as_midi())
    x.sharp()
    print(x.as_midi())
    x.sharp()
    print(x.as_midi())
    x.sharp()
    print(x.as_midi())
    x.sharp()
    print(x.as_midi())
    x.sharp()
    print(x.as_midi())
    x.sharp()
    print(x.as_midi())
    x.sharp()
    print(x.as_midi())
    x.sharp()
    print(x.as_midi())
            



