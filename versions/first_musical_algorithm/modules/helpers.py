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

def generate_chord_genotype(length:int, timeRange:tuple) -> list:
    return [random_transformations_list(length), random_float_list(length, timeRange)]

def generate_melody_genotype(totalLength:int, length:int,timeRange:tuple) -> list:
    return [[random_transformations_list(length) for _ in range(totalLength)], [random_float_list(length, timeRange) for _ in range(totalLength)]]

def random_integer_list(length:int, base:int=9) -> list:
    # random.seed(42)
    return [random.randrange(0,base) for _ in range(length)]

def random_float_list(length:int, timeRange:tuple) -> list:
    # random.seed(42)
    print(timeRange)
    return [round(random.randrange(*timeRange) / 100, 2) for _ in range(length)]

def random_transformations_list(length:int) -> list:
    # random.seed(42)
    keys = list(get_translations().keys())
    return [random.choice(keys) for _ in range(length)]


def normalize(number:int, total): 
    return float(number/(total))


def output_to_midi(chords, melodies, midiFile, apregiate=False):
    # degrees  = [60, 62, 64, 65, 67, 69, 71, 72] # MIDI note number
    # print(chords[:4])
    # print(melodies[:4])



    track      = 0
    channel    = 0
    chordTime  = 0   # In beats
    melodyTime = 0

    allChordsIndex = 0
    indexCount     = 0

    tempo      = 90  # In BPM
    volume     = 100 # 0-127, as per the MIDI standard  

    MyMIDI = MIDIFile(2) # One track, defaults to format 1 (tempo track
                        # automatically created)

    MyMIDI.addTempo(0, chordTime, tempo) 


    for index in range(len(chords)):
        indexedChords   = chords[index]
        indexedMelody   = melodies[index]
        currentIndexChordDuration = 0

        # print('indexedChords',indexedChords)
        for chordInfo in indexedChords:
            chordDuration = chordInfo[1]
            for note in chordInfo[0]:
                MyMIDI.addNote(track, channel, note, chordTime, chordDuration, volume)
                pass
            # print(melodyTime)
            # print(chordTime)

            chordTime += chordDuration
            currentIndexChordDuration += chordDuration
        
        # print('indexedMelody',melody)
        # print (melody)
        chordDuration
        melodyDurationSum = sum([dur[1] for dur in indexedMelody])
        for melodyInfo in indexedMelody:
            melodyDuration = melodyInfo[1]
            normalizedMelodyDuration = normalize(melodyDuration, melodyDurationSum) * currentIndexChordDuration
            # print('melodyDuration', melodyDuration, normalizedMelodyDuration, )
            for note in melodyInfo[0]:
            # note = melodyInfo[0][0]
                MyMIDI.addNote(track, channel, note, melodyTime, 0.05+normalizedMelodyDuration/3, volume)

                melodyTime += normalizedMelodyDuration/3
        
        # indexCount += 1
        # print(allChords)
        # print('indexed chords',allChords[allChordsIndex])
        # if indexCount % len(allChords[allChordsIndex].transforms) == 0:
            
        #     indexCount = 0

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
    


    