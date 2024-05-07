'''
Jackson Butler
Pledged
Contains useful helper functions for use in genetic algorithms
'''

import copy
import random
import os
from midiutil import MIDIFile
import pygame



def crossover(genotype1:list, genotype2:list):

    for section in range(len(genotype1)):
        diff = len(genotype1[section]) - len(genotype2[section])
        # print('section',genotype1[section])
       
        if diff > 0:
            crossingPoint = random.randrange(len(genotype2))
            tempGeno = copy.deepcopy(genotype1)
            diff = abs(diff)

            
            genotype1[section] = [*(tempGeno[section][:crossingPoint+diff]), *(genotype2[section][crossingPoint:])]
            genotype2[section] = [*(genotype2[section][:crossingPoint]), *(tempGeno[section][crossingPoint+diff:])]


        elif diff < 0:
            crossingPoint = random.randrange(len(genotype1))
            tempGeno = copy.deepcopy(genotype1)
            diff = abs(diff)


            genotype1[section] = [*(tempGeno[section][:crossingPoint]), *(genotype2[section][crossingPoint+diff:])]
            genotype2[section] = [*(genotype2[section][:crossingPoint+diff]), *(tempGeno[section][crossingPoint:])]

        else:
            crossingPoint = random.randrange(len(genotype1))
            tempGeno = copy.deepcopy(genotype1)

            genotype1[section] = [*(tempGeno[section][:crossingPoint]), *(genotype2[section][crossingPoint:])]
            genotype2[section] = [*(genotype2[section][:crossingPoint]), *(tempGeno[section][crossingPoint:])]

    
    return genotype1, genotype2


def get_translations():
    return {'R':'R', 'P':'P', 'L':'L', 'H':'PLR', 'S':'LPRP', 'N':'RLP', 'F':'PL', 'M':'RL'}

def generate_genotype(length:int, timeRange:tuple) -> list:
    return [random_transformations_list(length), random_float_list(length, timeRange)]


def random_integer_list(length:int, base:int=9) -> list:
    # random.seed(42)
    return [random.randrange(0,base) for _ in range(length)]

def random_float_list(length:int, timeRange:tuple) -> list:
    # random.seed(42)
    return [round(random.randrange(*timeRange) / 100, 2) for _ in range(length)]

def random_transformations_list(length:int) -> list:
    # random.seed(42)
    keys = list(get_translations().keys())
    return [random.choice(keys) for _ in range(length)]


def normalize(number:int, total): 
    return float(number/(total))


def output_to_midi(chords, midiFile, apregiate=False):
    # degrees  = [60, 62, 64, 65, 67, 69, 71, 72] # MIDI note number
    track    = 0
    channel  = 0
    time     = 0   # In beats
    # duration = .5   # In beats
    tempo    = 60  # In BPM
    volume   = 100 # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                        # automatically created)
    MyMIDI.addTempo(track,time, tempo)
    for chord, duration in chords: # assumes len(genotype[0]) == len(genotype[1])
        for note in chord:
            # print(note, end=", ")
            MyMIDI.addNote(track, channel, note, time, duration, volume)
            # time += duration
        time += duration
        # print()

    with open(midiFile, "wb") as output_file:
        MyMIDI.writeFile(output_file)

def play_midi(midiFile):
    freq = 44100                               # audio CD quality
    bitsize = -16                              # unsigned 16 bit
    channels = 2                               # 1 is mono, 2 is stereo
    buffer = 1024                              # number of samples
    clock = pygame.time.Clock()
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.set_volume(0.8)         # volume 0 to 1.0

    pygame.mixer.music.load(midiFile)         # read the midi file
    pygame.mixer.music.play()                  # play the music
    while pygame.mixer.music.get_busy():       # check if playback has finished
        clock.tick(100)


if __name__ == '__main__':
    print(get_translations()['N'])
    print(random_transformations_list(4))
    print(random_integer_list(4, 10))
    output_to_midi("foo", "major-scale.mid")
    play_midi("major-scale.mid")
    


    