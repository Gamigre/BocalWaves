# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests the audacity pipe.
Keep pipe_test.py short!!
You can make more complicated longer tests to test other functionality
or to generate screenshots etc in other scripts.
Make sure Audacity is running first and that mod-script-pipe is enabled
before running this script.
Requires Python 2.7 or later. Python 3 is strongly recommended.
"""

import os
import sys
import sox
import numpy as np
from ffmpy import FFmpeg
import pipeclient
import time

client = pipeclient.PipeClient()
print(os.getcwd())  # Prints the current working directory

"""sox -r 44100 --endian little -e mu-law -t raw --ignore-length CNV000005.bmp CNV000005bis.wav remix -"""

"""
if sys.platform == 'win32':
    print("pipe-test.py, running on windows")
    TONAME = '\\\\.\\pipe\\ToSrvPipe'
    FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
    EOL = '\r\n\0'
else:
    print("pipe-test.py, running on linux or mac")
    TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
    FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
    EOL = '\n'

print("Write to  \"" + TONAME +"\"")
if not os.path.exists(TONAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("Read from \"" + FROMNAME +"\"")
if not os.path.exists(FROMNAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("-- Both pipes exist.  Good.")

TOFILE = open(TONAME, 'w')
print("-- File to write to has been opened")
FROMFILE = open(FROMNAME, 'rt')
print("-- File to read from has now been opened too\r\n")
"""


def send_command(command):
    """Send a single command."""
    print("Send: >>> \n" + command)
    TOFILE.write(command + EOL)
    TOFILE.flush()


def get_response():
    """Return the command response."""
    result = ''
    line = ''
    while line != '\n':
        result += line
        line = FROMFILE.readline()
        # print(" I read line:["+line+"]")
    return result


"""
def do_command(command):

    send_command(command)
    response = get_response()
    print("Rcvd: <<< \n" + response)
    return response
"""


def do_command(command):
    client.write(command, timer=True)
    response = client.read()
    print("rcvd\n" + response)
    return response

def importAndSliceHeader(file):
    do_command('import2: Filename="input\\{}"'.format(file))
    do_command('SelectTracks:Mode="Set" Track="0" TrackCount="1"')
    do_command('SelectTime:Start="0.1" End="999" RelativeTo="ProjectStart" ')

def exportFile(parameters, folder):
    do_command('SelectAll')
    name = str(parameters[0]).replace(",", "p").replace(".", "p").replace("-", "m")
    newFileName = '{:s}bocal_{:s}.raw '.format(folder, name)
    do_command('Export2:Filename=' + newFileName + 'NumChannels=1')
    fileNamesList.append(newFileName)
    do_command("SelectAll")
    do_command("RemoveTracks")

def VideoToBMPConv():
    import subprocess
    from subprocess import Popen, PIPE
    process = subprocess.call("ffmpeg -i inputMP4\input.mp4 ExportedBMP\image_%5d.bmp")

def BMPtoWAV():
    import subprocess
    from subprocess import Popen, PIPE
    process = subprocess.call("FOR %I IN (ExportedBMP\*.bmp) DO sox -r 44100 --endian little -e mu-law -t raw --ignore-length %I input\\%~nI.wav remix -", shell=True)

def commandSetBuild(file, parameters, folder, type_question):
    importAndSliceHeader(file)
    if type_question == 1:
        do_command('Amplify: Ratio=' + str(float(parameters[1])) + ' AllowClipping=True')

    elif type_question == 3:
        do_command('BassAndTreble: Bass='+ str(float(parameters[1]))+' Treble='+ str(float(parameters[2]))+' Link Sliders=True')
    elif type_question == 4:
        do_command('ChangePitch: Percentage=' + str(float(parameters[1])) +' SBSMS=False')
    elif type_question == 5:
        do_command('ChangePitch: Percentage=' + str(float(parameters[1])) +'')
    elif type_question == 6:
        do_command('ChangeTempo: Percentage=' + str(float(parameters[1])) + '+ SBSMS=False')
    elif type_question == 8:
        do_command('Compressor: Treshold=' + str(float(parameters[1])) + ' NoiseFloor=' + str(float(parameters[2])) + ' Ratio=' + str(float(parameters[3])) + ' AttackTime=' + str(float(parameters[4])) + ' ReleaseTime=' + str(float(parameters[5])) + '+ Normalize=False UsePeak=False')
    elif type_question == 10:
        do_command('Echo: Delay='+ str(float(parameters[1]))+' Decay='+ str(float(parameters[2]))+'')
    elif type_question == 13:
        do_command('FilterCurve: f0='+ str(int(parameters[1]))+' v0='+ str(int(parameters[2]))+'')
    elif type_question == 18:
        do_command('Paulstretch: Stretch Factor='+ str(float(parameters[1]))+' Time Resolution='+ str(float(parameters[2]))+'')
    elif type_question == 19:
        do_command('Phaser: Stages='+ str(int(parameters[1]))+' Freq='+ str(float(parameters[2]))+' Feedback='+ str(int(parameters[3]))+'')
    elif type_question == 22:
        do_command('Reverb: RoomSize='+ str(float(parameters[1]))+' Delay='+ str(float(parameters[2]))+' Reverberance='+ str(int(parameters[3]))+' HfDamping='+ str(float(parameters[4]))+' ToneLow='+ str(float(parameters[5]))+' ToneHigh='+ str(float(parameters[6]))+' WetGain='+ str(float(parameters[7]))+' DryGain='+ str(float(parameters[8]))+' StereoWidth='+ str(float(parameters[9]))+' ')
    elif type_question == 27:
        do_command('Wahwah: Freq=' + str(float(parameters[1])) + ' Phase=0 Depth=' + str(int(parameters[2])) + ' Resonance=' + str(float(parameters[3])) + ' Offset=' + str(int(parameters[4])) + ' Gain=-6')
        #do_command('ChangeSpeed:	Percentage='+ str(float(parameters[1]))+''.format(parameters[0], parameters[2]))
        # do_command(string)



    exportFile(parameters, folder)



def conversionRawJpeg(inputName):
    ff = FFmpeg(inputs={inputName + '.raw': None},
                outputs={inputName + '.jpeg': None}
                )
    print(ff.cmd)
    ff.run()


global fileNamesList
fileNamesList = []
inputFile = os.listdir('input') #Audacity MUST BE opened from a .aup audacity project file placed at the root of your work folder, along with your input and output folders, else, Au won't find your file

print(inputFile)
outputFolder = "output\\"
print("BOCALWAVES v0.9")
print("0=Exporting your files 1= Amplify, 3=Bass&Treble, 4=ChangePitch, 5=ChangeSpeed, 6=ChangeTempo, 8=Compressor, 10=Echo, 13=FrequenceCurbe, 18=Paulstretch, 19= Phaser, 22=Reverb, 27=Wahwah, more to come")
Type_Question = int(input("Select an effect to apply : "))

if(Type_Question==1):
    print("Effect: Amplify")
    nbIterations = int(input("Number of outputs ?"))  # number of outputs
    nbRangeRatioMin = int(input("Ratio min (-50dB to 50dB) ?"))
    nbRangeRatioMax = int(input("Ratio min (-50dB to 50dB) ?"))

    if (len(inputFile) == 1):
        inputFile = inputFile * nbIterations

    IterationList = np.linspace(start=0, stop=nbIterations, num=nbIterations,
                                dtype=int).tolist()  # Range of the effect
    RatioList = np.linspace(start=nbRangeRatioMin, stop=nbRangeRatioMax, num=nbIterations,
                            dtype=int).tolist()  # Range of the effect

    parametersList = []
    for i in range(nbIterations):
        parametersList.append([IterationList[i], RatioList[i]])
        print(parametersList)
    for parametersSet, i in zip(parametersList, range(nbIterations)):
        print("Envoi avec paramètres Ratio%: {:f} SBSMS = False ".format(parametersSet[1]))
        print(i, inputFile[i], range(nbIterations))
        commandSetBuild(inputFile[i], parametersSet, outputFolder, type_question=Type_Question)
        print(fileNamesList)
    for image in fileNamesList:
        #time.sleep(1)
        #conversionRawJpeg(os.path.splitext(image)[0])
        time.sleep(0.1)

elif (Type_Question == 0):
    print("Conversion mp4 to BMP sequence; WARNING make sure your video in /inputMP4 folder is named input.mp4 !")
    VideoToBMPConv()
    BMPtoWAV()

elif(Type_Question==2):
    print("Effect: AutoDuck: , not added yet")

elif (Type_Question == 3):
    print("Effect: BassAndTreble")
    nbIterations = int(input("Number of outputs ?"))  # number of outputs
    nbRangeBassMin = float(input("Amount of bass minimum (-30 to 30) ?"))
    nbRangeBassMax = float(input("Amount of bass maximum (-30 to 30) ?"))
    nbRangeTrebleMin = float(input("Amount of Treble minimum (-30 to 30) ?"))
    nbRangeTrebleMax = float(input("Amount of Treble maximum (-30 to 30) ?"))


    if (len(inputFile) == 1):
        inputFile = inputFile * nbIterations

    IterationList = np.linspace(start=0, stop=nbIterations, num=nbIterations,
                                dtype=int).tolist()  # Range of the effect
    BassList = np.linspace(start=nbRangeBassMin, stop=nbRangeBassMax, num=nbIterations,
                           dtype=float).tolist()  # Range of the effect

    TrebleList = np.linspace(start=nbRangeTrebleMin, stop=nbRangeTrebleMax, num=nbIterations,
                               dtype=float).tolist()  # Range of the effect

    parametersList = []
    for i in range(nbIterations):
        """paramètres : Bass, Treble (volume is indexed on the bass and treble settings)"""
        parametersList.append([IterationList[i], BassList[i], TrebleList[i]])
        print(parametersList)
    for parametersSet, i in zip(parametersList, range(nbIterations)):
        print("Envoi avec paramètres Bass: {:f} Treble: {:f} ".format(parametersSet[1], parametersSet[2]))
        print(i, inputFile[i], range(nbIterations))
        commandSetBuild(inputFile[i], parametersSet, outputFolder, type_question=Type_Question)
        print(fileNamesList)
    for image in fileNamesList:
        time.sleep(1)
        conversionRawJpeg(os.path.splitext(image)[0])
        time.sleep(0.1)

elif (Type_Question == 4):
    print("Effect: Change Pitch")
    nbIterations = int(input("Number of outputs ?"))  # number of outputs
    nbRangePitchMin = float(input("% of Pitch min (-99 to 400) ?"))
    nbRangePitchMax = float(input("% of Pitch max (-99 to 400) ?"))

    if (len(inputFile) == 1):
        inputFile = inputFile * nbIterations

    IterationList = np.linspace(start=0, stop=nbIterations, num=nbIterations,
                                dtype=int).tolist()  # Range of the effect
    PitchList = np.linspace(start=nbRangePitchMin, stop=nbRangePitchMax, num=nbIterations,
                           dtype=float).tolist()  # Range of the effect

    parametersList = []
    for i in range(nbIterations):
        parametersList.append([IterationList[i], PitchList[i]])
        print(parametersList)
    for parametersSet, i in zip(parametersList, range(nbIterations)):
        print("Envoi avec paramètres Pitch%: {:f} SBSMS = False ".format(parametersSet[1]))
        print(i, inputFile[i], range(nbIterations))
        commandSetBuild(inputFile[i], parametersSet, outputFolder, type_question=Type_Question)
        print(fileNamesList)
    for image in fileNamesList:
        #time.sleep(1)
        #conversionRawJpeg(os.path.splitext(image)[0])
        time.sleep(0.1)

elif (Type_Question == 5):
    print("Effect: Change Speed")
    nbIterations = int(input("Number of outputs ?"))  # number of outputs
    nbRangeSpeedMin = float(input("% of Speed min (-99 to 400) ?"))
    nbRangeSpeedMax = float(input("% of Speed max (-99 to 400) ?"))

    if (len(inputFile) == 1):
        inputFile = inputFile * nbIterations

    IterationList = np.linspace(start=0, stop=nbIterations, num=nbIterations,
                                dtype=int).tolist()  # Range of the effect
    SpeedList = np.linspace(start=nbRangeSpeedMin, stop=nbRangeSpeedMax, num=nbIterations,
                           dtype=float).tolist()  # Range of the effect

    parametersList = []
    for i in range(nbIterations):
        """paramètres : Bass, Treble (volume is indexed on the bass and treble settings)"""
        parametersList.append([IterationList[i], SpeedList[i]])
        print(parametersList)
    for parametersSet, i in zip(parametersList, range(nbIterations)):
        print("Envoi avec paramètres Speed%: {:f} ".format(parametersSet[1]))
        print(i, inputFile[i], range(nbIterations))
        commandSetBuild(inputFile[i], parametersSet, outputFolder, type_question=Type_Question)
        print(fileNamesList)
    for image in fileNamesList:
        #time.sleep(1)
        conversionRawJpeg(os.path.splitext(image)[0])
        time.sleep(0.1)

elif (Type_Question == 6):
    print("Effect: Change Tempo, doesn't seems to do anything")
    nbIterations = int(input("Number of outputs ?"))  # number of outputs
    nbRangeTempoMin = float(input("% of Tempo min (-99 to 400) ?"))
    nbRangeTempoMax = float(input("% of Tempo max (-99 to 400) ?"))

    if (len(inputFile) == 1):
        inputFile = inputFile * nbIterations

    IterationList = np.linspace(start=0, stop=nbIterations, num=nbIterations,
                                dtype=int).tolist()  # Range of the effect
    TempoList = np.linspace(start=nbRangeTempoMin, stop=nbRangeTempoMax, num=nbIterations,
                           dtype=float).tolist()  # Range of the effect

    parametersList = []
    for i in range(nbIterations):
        parametersList.append([IterationList[i], TempoList[i]])
        print(parametersList)
    for parametersSet, i in zip(parametersList, range(nbIterations)):
        print("Envoi avec paramètres Tempo%: {:f} SBSMS = False ".format(parametersSet[1]))
        print(i, inputFile[i], range(nbIterations))
        commandSetBuild(inputFile[i], parametersSet, outputFolder, type_question=Type_Question)
        print(fileNamesList)
    for image in fileNamesList:
        time.sleep(1)
        conversionRawJpeg(os.path.splitext(image)[0])
        time.sleep(0.1)


elif (Type_Question == 7):
    print("Effect: ClickRemoval: , not added yet")

elif (Type_Question == 8):
    print("Effect: Compressor, doesn't seems to do a lot :(")
    nbIterations = int(input("Number of outputs ?"))  # number of outputs
    nbRangeTresholdMin = float(input("Treshold Range minimum in dB (-60 to -1) ?"))
    nbRangeTresholdMax = float(input("Treshold Range maximum in dB (-60 to -1) ?"))
    nbRangeNoiseFloorMin = float(input("NoiseFloor Range minimum in dB  (-80 to -20) ?"))
    nbRangeNoiseFloorMax = float(input("NoiseFloor Range maximum in dB  (-80 to -20) ?"))
    nbRangeRatioMin = float(input("Ratio Range minimum (1.1 to 10) ?"))
    nbRangeRatioMax = float(input("Ratio Range maximum (1.1 to 10) ?"))
    nbRangeAttackTimeMin = float(input("AttackTime Range minimum (0.1s to 5s) ?"))
    nbRangeAttackTimeMax = float(input("AttackTime Range maximum (0.1s to 5s) ?"))
    nbRangeReleaseTimeMin = float(input("ReleaseTime Range minimum (1s to 30s) ?"))
    nbRangeReleaseTimeMax = float(input("ReleaseTime Range maximum (1s to 30s) ?"))

    if (len(inputFile) == 1):
        inputFile = inputFile * nbIterations

    IterationList = np.linspace(start=0, stop=nbIterations, num=nbIterations,
                                dtype=int).tolist()  # Range of the effect
    TresholdList = np.linspace(start=nbRangeTresholdMin, stop=nbRangeTresholdMax, num=nbIterations,
                           dtype=float).tolist()  # Range of the effect

    NoiseFloorList = np.linspace(start=nbRangeNoiseFloorMin, stop=nbRangeNoiseFloorMax, num=nbIterations,
                               dtype=float).tolist()  # Range of the effect
    RatioList = np.linspace(start=nbRangeRatioMin, stop=nbRangeRatioMax, num=nbIterations,
                               dtype=float).tolist()  # Range of the effect
    AttackTimeList = np.linspace(start=nbRangeAttackTimeMin, stop=nbRangeAttackTimeMax, num=nbIterations,
                               dtype=float).tolist()  # Range of the effect
    ReleaseTimeList = np.linspace(start=nbRangeReleaseTimeMin, stop=nbRangeReleaseTimeMax, num=nbIterations,
                               dtype=float).tolist()  # Range of the effect

    parametersList = []
    for i in range(nbIterations):
        parametersList.append([IterationList[i], TresholdList[i], NoiseFloorList[i], RatioList[i], AttackTimeList[i], ReleaseTimeList[i]])
        print(parametersList)
    for parametersSet, i in zip(parametersList, range(nbIterations)):
        print("Envoi avec parametres Treshold: {:f} NoiseFloor: {:f} Ratio: {:f} AttackTime: {:f} ReleaseTime: {:f}  ".format(parametersSet[1],parametersSet[2], parametersSet[3], parametersSet[4], parametersSet[5]))
        print(i, inputFile[i], range(nbIterations))
        commandSetBuild(inputFile[i], parametersSet, outputFolder, type_question=Type_Question)
        print(fileNamesList)
    # for image in fileNamesList:
    # conversionRawJpeg(os.path.splitext(image)[0])
    # time.sleep(0.1)

elif (Type_Question == 9):
    print("Effect: Distortion: , not added yet")

elif (Type_Question == 10):
    print("Effect: Echo")
    nbIterations = int(input("Number of outputs ?"))  # number of outputs
    nbRangeDelayMin = float(input("Amount of Delay minimum (length of the echo in seconds) ?"))
    nbRangeDelayMax = float(input("Amount of Delay maximum (length of the echo in seconds) ?"))
    nbRangeDecayMin = float(input("Amount of Decay minimum (usually between 0 and 1 but can be higher) ?"))
    nbRangeDecayMax = float(input("Amount of Decay maximum (usually between 0 and 1 but can be higher) ?"))


    if (len(inputFile) == 1):
        inputFile = inputFile * nbIterations

    IterationList = np.linspace(start=0, stop=nbIterations, num=nbIterations,
                                dtype=int).tolist()  # Range of the effect
    DelayList = np.linspace(start=nbRangeDelayMin, stop=nbRangeDelayMax, num=nbIterations,
                           dtype=float).tolist()  # Range of the effect

    DecayList = np.linspace(start=nbRangeDecayMin, stop=nbRangeDecayMax, num=nbIterations,
                               dtype=float).tolist()  # Range of the effect

    parametersList = []
    for i in range(nbIterations):
        """paramètres : Delay, Decay (volume is indexed on the Delay and Decay settings)"""
        parametersList.append([IterationList[i], DelayList[i], DecayList[i]])
        print(parametersList)
    for parametersSet, i in zip(parametersList, range(nbIterations)):
        print("Envoi avec paramètres Delay: {:f} Decay: {:f} ".format(parametersSet[1], parametersSet[2]))
        print(i, inputFile[i], range(nbIterations))
        commandSetBuild(inputFile[i], parametersSet, outputFolder, type_question=Type_Question)
        print(fileNamesList)
    """for image in fileNamesList:
        time.sleep(1)
        conversionRawJpeg(os.path.splitext(image)[0])
        time.sleep(0.1)"""

elif (Type_Question == 11):
    print("Effect: FadeIn: , not added yet")

elif (Type_Question == 12):
    print("Effect: FadeOut: , not added yet")

elif (Type_Question == 13):
    print("Effect: FilterCurve: mysterious but somehow works, not very interesting")
    nbIterations = int(input("Number of outputs ?"))  # number of outputs
    nbRangeF0Min = int(input("F0 value min ? "))
    nbRangeF0Max = int(input("f0 value max ? "))
    nbRangeV0Min = int(input("V0 value min ? "))
    nbRangeV0Max = int(input("V0 value max ? "))

    if (len(inputFile) == 1):
        inputFile = inputFile * nbIterations

    IterationList = np.linspace(start=0, stop=nbIterations, num=nbIterations,
                                dtype=int).tolist()  # Range of the effect
    RangeF0List = np.linspace(start=nbRangeF0Min, stop=nbRangeF0Max, num=nbIterations,
                           dtype=float).tolist()  # Range of the effect
    RangeV0List = np.linspace(start=nbRangeV0Min, stop=nbRangeV0Max, num=nbIterations,
                           dtype=float).tolist()  # Range of the effect

    parametersList = []
    for i in range(nbIterations):
        parametersList.append([IterationList[i], RangeF0List[i], RangeV0List[i]])
        print(parametersList)
    for parametersSet, i in zip(parametersList, range(nbIterations)):
        print(i, inputFile[i], range(nbIterations))
        commandSetBuild(inputFile[i], parametersSet, outputFolder, type_question=Type_Question)
        print(fileNamesList)
    for image in fileNamesList:
        time.sleep(1)
        #conversionRawJpeg(os.path.splitext(image)[0])
        #time.sleep(0.1)

elif (Type_Question == 14):
    print("Effect: GraphicEq: , not added yet")

elif (Type_Question == 15):
    print("Effect: LoudnessNormalization: , not added yet")

elif (Type_Question == 16):
    print("Effect: NoiseReduction: , not added yet")

elif (Type_Question == 17):
    print("Effect: Normalize: , not added yet")

elif (Type_Question == 18):
    print("Effect: Paulstretch, WARNING: Usually mangle your input file and outputs only static noise, and takes its time to do that")
    nbIterations = int(input("Number of outputs ?"))  # number of outputs
    nbRangeFacStretchMin = float(input("Factor of stretching minimum, by default 10 makes it 10 times longer (0 to 10000000000000000,0, restrain yourself !) ?"))
    nbRangeFacStretchMax = float(input("Factor of stretching maximum, by default 10 makes it 10 times (0 to 10000000000000000,0, restrain yourself !) ?"))
    nbRangeTimeResMin = float(input("Time Resolution minimum by default at 0.25 (0 to billions of billions, but keep it low !) ?"))
    nbRangeTimeResMax = float(input("Time Resolution minimum by default at 0.25 (0 to billions of billions, but keep it low !) ?"))


    if (len(inputFile) == 1):
        inputFile = inputFile * nbIterations

    IterationList = np.linspace(start=0, stop=nbIterations, num=nbIterations,
                                dtype=int).tolist()  # Range of the effect
    FacStretchList = np.linspace(start=nbRangeFacStretchMin, stop=nbRangeFacStretchMax, num=nbIterations,
                           dtype=float).tolist()  # Range of the effect

    TimeResList = np.linspace(start=nbRangeTimeResMin, stop=nbRangeTimeResMax, num=nbIterations,
                               dtype=float).tolist()  # Range of the effect

    parametersList = []
    for i in range(nbIterations):
        """paramètres : Stretch Factor, Time Resolution"""
        parametersList.append([IterationList[i], FacStretchList[i], TimeResList[i]])
        print(parametersList)
    for parametersSet, i in zip(parametersList, range(nbIterations)):
        print("Envoi avec paramètres Factor of stretching: {:f} Time Resolution: {:f} ".format(parametersSet[1], parametersSet[2]))
        print(i, inputFile[i], range(nbIterations))
        commandSetBuild(inputFile[i], parametersSet, outputFolder, type_question=Type_Question)
        print(fileNamesList)
    for image in fileNamesList:
        conversionRawJpeg(os.path.splitext(image)[0])
        time.sleep(0.1)


elif (Type_Question == 19):
    print("Effect: Phaser")
    nbIterations = int(input("Number of outputs ?"))  # number of outputs
    nbStages = float(input("Number of stages (2 to 24) ?"))
    nbRangeFreqMin = float(input("Frequency Range minimum (0.001 to 4) ?"))
    nbRangeFreqMax = float(input("Frequency Range maximum (0.001 to 4) ?"))
    nbRangeFeedbackMin = float(input("Feedback Range minimum (-100 to 100 (enter -99 to 99 for better results)) ?"))
    nbRangeFeedbackMax = float(input("Feedback Range maximum (-100 to 100 (enter -99 to 99 for better results)) ?"))

    if (len(inputFile) == 1):
        inputFile = inputFile * nbIterations

    IterationList = np.linspace(start=0, stop=nbIterations, num=nbIterations,
                                dtype=int).tolist()  # Range of the effect
    FreqList = np.linspace(start=nbRangeFreqMin, stop=nbRangeFreqMax, num=nbIterations,
                           dtype=float).tolist()  # Range of the effect

    FeedbackList = np.linspace(start=nbRangeFeedbackMin, stop=nbRangeFeedbackMax, num=nbIterations,
                               dtype=float).tolist()  # Range of the effect

    parametersList = []
    for i in range(nbIterations):
        """paramètres : Stages, Frequency, Feedback"""
        parametersList.append([IterationList[i], nbStages, FreqList[i], FeedbackList[i]])
        print(parametersList)
    for parametersSet, i in zip(parametersList, range(nbIterations)):
        print("Envoi avec parametres Stages: {:f} Frequency: {:f} Feedback: {:f}  ".format(parametersSet[1], parametersSet[2], parametersSet[3]))
        print(i, inputFile[i], range(nbIterations))
        commandSetBuild(inputFile[i], parametersSet, outputFolder, type_question=Type_Question)
        print(fileNamesList)
    #for image in fileNamesList:
        #conversionRawJpeg(os.path.splitext(image)[0])
        #time.sleep(0.1)

elif (Type_Question == 20):
    print("Effect: Repair: , not added yet")

elif (Type_Question == 21):
    print("Effect: Repeat: , not added yet")

elif (Type_Question == 22):
    print("Effect: Reverb:")
    nbIterations = int(input("Number of outputs ?"))  # number of outputs
    nbRangeRoomSizeMin = float(input("RoomSize min (0 to 100) ?"))
    nbRangeRoomSizeMax = float(input("RoomSize max (0 to 100) ?"))
    nbRangeDelayMin = float(input("Delay minimum (0 to 200) ?"))
    nbRangeDelayMax = float(input("Delay maximum (0 to 200) ?"))
    nbRangeReverbMin = float(input("Reverb min (0 to 100) ?"))
    nbRangeReverbMax = float(input("Reverb max (0 to 100) ?"))
    nbRangeHfDampingMin = 50 #float(input("HfDamping min (0 to 100) ?")) removed because unnoticeable results
    nbRangeHfDampingMax = 50 #float(input("HfDamping min (0 to 100) ?"))
    nbRangeToneLowMin = float(input("ToneLow min (0 to 100) ?"))
    nbRangeToneLowMax = float(input("ToneLow max (0 to 100) ?"))
    nbRangeToneHighMin = float(input("ToneHigh min (0 to 100) ?"))
    nbRangeToneHighMax = float(input("ToneHigh max (0 to 100) ?"))
    nbRangeWetGainMin = float(input("WetGain min (-20 to 10) ?"))
    nbRangeWetGainMax = float(input("WetGain max (-20 to 10) ?"))
    nbRangeDryGainMin = float(input("DryGain min (-20 to 10) ?"))
    nbRangeDryGainMax = float(input("DryGain max (-20 to 10) ?"))
    nbRangeStereoWidthMin = 100 #float(input("StereoWidth min (0 to 100) ?")) removed because no known effect
    nbRangeStereoWidthMax = 100 #float(input("StereoWidth min (0 to 100) ?"))

    if (len(inputFile) == 1):
        inputFile = inputFile * nbIterations

    IterationList = np.linspace(start=0, stop=nbIterations, num=nbIterations,
                                dtype=int).tolist()  # Range of the effect
    RoomSizeList = np.linspace(start=nbRangeRoomSizeMin, stop=nbRangeRoomSizeMax, num=nbIterations,
                           dtype=float).tolist()  # Range of the effect

    DelayList = np.linspace(start=nbRangeDelayMin, stop=nbRangeDelayMax, num=nbIterations,
                               dtype=float).tolist()  # Range of the effect
    ReverbList = np.linspace(start=nbRangeReverbMin, stop=nbRangeReverbMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect
    HfDampingList = np.linspace(start=nbRangeHfDampingMin, stop=nbRangeHfDampingMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect
    ToneLowList = np.linspace(start=nbRangeToneLowMin, stop=nbRangeToneLowMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect
    ToneHighList = np.linspace(start=nbRangeToneHighMin, stop=nbRangeToneHighMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect
    WetGainList = np.linspace(start=nbRangeWetGainMin, stop=nbRangeWetGainMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect
    DryGainList = np.linspace(start=nbRangeDryGainMin, stop=nbRangeDryGainMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect
    StereoWidthList = np.linspace(start=nbRangeStereoWidthMin, stop=nbRangeStereoWidthMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect

    parametersList = []
    for i in range(nbIterations):
        """paramètres : Stages, Frequency, Feedback"""
        parametersList.append([IterationList[i], RoomSizeList[i], DelayList[i], ReverbList[i], HfDampingList[i], ToneLowList[i], ToneHighList[i],
                               WetGainList[i], DryGainList[i], StereoWidthList[i]])
        print(parametersList)
    for parametersSet, i in zip(parametersList, range(nbIterations)):
        print("Envoi avec parametres RoomSize: {:f} Delay: {:f} Reverberance:  {:f} HfDamping: {:f} ToneLow: {:f} ToneHigh: {:f} WetGain: {:f} DryGain: {:f} StereoWidth: {:f} ".format(parametersSet[1], parametersSet[2], parametersSet[3], parametersSet[4], parametersSet[5], parametersSet[6], parametersSet[7], parametersSet[8], parametersSet[9]))
        print(i, inputFile[i], range(nbIterations))
        commandSetBuild(inputFile[i], parametersSet, outputFolder, type_question=Type_Question)
        print(fileNamesList)
    #for image in fileNamesList:
        #conversionRawJpeg(os.path.splitext(image)[0])
        time.sleep(0.1)


elif (Type_Question == 23):
    print("Effect: Reverse: , not added yet")


elif (Type_Question == 24):
    print("Effect: SlidingStretch:")
    nbIterations = int(input("Number of outputs ?"))  # number of outputs
    nbRangeRoomSizeMin = float(input("RoomSize min (0 to 100) ?"))
    nbRangeRoomSizeMax = float(input("RoomSize max (0 to 100) ?"))
    nbRangeDelayMin = float(input("Delay minimum (0 to 200) ?"))
    nbRangeDelayMax = float(input("Delay maximum (0 to 200) ?"))
    nbRangeReverbMin = float(input("Reverb min (0 to 100) ?"))
    nbRangeReverbMax = float(input("Reverb max (0 to 100) ?"))
    nbRangeHfDampingMin = 50 #float(input("HfDamping min (0 to 100) ?")) removed because unnoticeable results
    nbRangeHfDampingMax = 50 #float(input("HfDamping min (0 to 100) ?"))
    nbRangeToneLowMin = float(input("ToneLow min (0 to 100) ?"))
    nbRangeToneLowMax = float(input("ToneLow max (0 to 100) ?"))
    nbRangeToneHighMin = float(input("ToneHigh min (0 to 100) ?"))
    nbRangeToneHighMax = float(input("ToneHigh max (0 to 100) ?"))
    nbRangeWetGainMin = float(input("WetGain min (-20 to 10) ?"))
    nbRangeWetGainMax = float(input("WetGain max (-20 to 10) ?"))
    nbRangeDryGainMin = float(input("DryGain min (-20 to 10) ?"))
    nbRangeDryGainMax = float(input("DryGain max (-20 to 10) ?"))
    nbRangeStereoWidthMin = 100 #float(input("StereoWidth min (0 to 100) ?")) removed because no known effect
    nbRangeStereoWidthMax = 100 #float(input("StereoWidth min (0 to 100) ?"))

    if (len(inputFile) == 1):
        inputFile = inputFile * nbIterations

    IterationList = np.linspace(start=0, stop=nbIterations, num=nbIterations,
                                dtype=int).tolist()  # Range of the effect
    RoomSizeList = np.linspace(start=nbRangeRoomSizeMin, stop=nbRangeRoomSizeMax, num=nbIterations,
                           dtype=float).tolist()  # Range of the effect

    DelayList = np.linspace(start=nbRangeDelayMin, stop=nbRangeDelayMax, num=nbIterations,
                               dtype=float).tolist()  # Range of the effect
    ReverbList = np.linspace(start=nbRangeReverbMin, stop=nbRangeReverbMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect
    HfDampingList = np.linspace(start=nbRangeHfDampingMin, stop=nbRangeHfDampingMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect
    ToneLowList = np.linspace(start=nbRangeToneLowMin, stop=nbRangeToneLowMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect
    ToneHighList = np.linspace(start=nbRangeToneHighMin, stop=nbRangeToneHighMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect
    WetGainList = np.linspace(start=nbRangeWetGainMin, stop=nbRangeWetGainMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect
    DryGainList = np.linspace(start=nbRangeDryGainMin, stop=nbRangeDryGainMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect
    StereoWidthList = np.linspace(start=nbRangeStereoWidthMin, stop=nbRangeStereoWidthMax, num=nbIterations,
                            dtype=float).tolist()  # Range of the effect

    parametersList = []
    for i in range(nbIterations):
        """paramètres : Stages, Frequency, Feedback"""
        parametersList.append([IterationList[i], RoomSizeList[i], DelayList[i], ReverbList[i], HfDampingList[i], ToneLowList[i], ToneHighList[i],
                               WetGainList[i], DryGainList[i], StereoWidthList[i]])
        print(parametersList)
    for parametersSet, i in zip(parametersList, range(nbIterations)):
        print("Envoi avec parametres RoomSize: {:f} Delay: {:f} Reverberance:  {:f} HfDamping: {:f} ToneLow: {:f} ToneHigh: {:f} WetGain: {:f} DryGain: {:f} StereoWidth: {:f} ".format(parametersSet[1], parametersSet[2], parametersSet[3], parametersSet[4], parametersSet[5], parametersSet[6], parametersSet[7], parametersSet[8], parametersSet[9]))
        print(i, inputFile[i], range(nbIterations))
        commandSetBuild(inputFile[i], parametersSet, outputFolder, type_question=Type_Question)
        print(fileNamesList)
    #for image in fileNamesList:
        #conversionRawJpeg(os.path.splitext(image)[0])
        time.sleep(0.1)

elif (Type_Question == 25):
    print("Effect: TruncateSilence: , not added yet")

elif (Type_Question == 26):
    print("Effect: Effect: , not added yet")

elif (Type_Question == 27):
    print("Effect: Wahwah")
    nbIterations = int(input("Number of outputs ?"))  # number of outputs
    nbRangeFreqMin = float(input("Freq Range minimum (0.1 to 4.0) ?"))
    nbRangeFreqMax = float(input("Freq Range maximum (0.1 to 4.0)  ?"))
    nbRangeDepthMin = int(input("% of Depth Range minimum (0 to 100) ?"))
    nbRangeDepthMax = int(input("% of Depth Range maximum (0 to 100) ?"))
    nbRangeResonanceMin = float(input("% of Resonance Range minimum (0.1 to 10) ?"))
    nbRangeResonanceMax = float(input("% of Resonance Range maximum (0.1 to 10) ?"))
    nbRangeOffsetMin = int(input("% of Offset Range minimum (0 to 100) ?"))
    nbRangeOffsetMax = int(input("% of Offset Range maximum (0 to 100) ?"))

    if (len(inputFile) == 1):
        inputFile = inputFile * nbIterations
    #print(inputFile)
    IterationList = np.linspace(start=0, stop=nbIterations, num=nbIterations,
                                dtype=int).tolist()  # Range of the effect
    FreqList = np.linspace(start=nbRangeFreqMin, stop=nbRangeFreqMax, num=nbIterations,
                           dtype=float).tolist()  # Range of the effect
    
    DepthList = np.linspace(start=nbRangeDepthMin, stop=nbRangeDepthMax, num=nbIterations,
                             dtype=int).tolist()  # Range of the effect

    ResonanceList = np.linspace(start=nbRangeResonanceMin, stop=nbRangeResonanceMax, num=nbIterations,
                             dtype=float).tolist()  # Range of the effect

    OffsetList = np.linspace(start=nbRangeOffsetMin, stop=nbRangeOffsetMax, num=nbIterations,
                             dtype=int).tolist()  # Range of the effect

    parametersList = []
    for i in range(nbIterations):
        """paramètres : Frequency, Feedback"""
        parametersList.append([IterationList[i], FreqList[i], DepthList[i], ResonanceList[i], OffsetList[i]])  # define the parameter[0], [1], [2], etc
        print(parametersList)
    for parametersSet, i in zip(parametersList, range(nbIterations)):
        print("Envoi avec parametres Frequency: {:f} Depth: {:f} Resonance: {:f} Offset: {:f} ".format(parametersSet[1], parametersSet[2], parametersSet[3], parametersSet[4]))
        print(i, inputFile[i], range(nbIterations))
        commandSetBuild(inputFile[i], parametersSet, outputFolder, type_question=Type_Question)
        print(fileNamesList)
    for image in fileNamesList:
        #conversionRawJpeg(os.path.splitext(image)[0])
        time.sleep(0.1)


elif (Type_Question == 28):
    print("Effect: , not added yet")

elif (Type_Question == 29):
    print("Effect: , not added yet")



else:
        print("mode absent")
        #return(null)



#else:
    #print('effect not found, check for spelling mistakes')





