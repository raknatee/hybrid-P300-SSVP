﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v3.1.1),
    on Thu May  9 17:56:55 2019
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '3.1.1'
expName = 'untitled.py'
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='newJoystickComponent.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation
from psychopy.hardware import joystick as joysticklib  # joystick/gamepad accsss
from psychopy.experiment.components.joystick import virtualJoystick as virtualjoysticklib

# Setup the Window
win = visual.Window(
    size=(1024, 768), fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "trial"
trialClock = core.Clock()
x, y = [None, None]
joystick = type('', (), {})() # Create an object to use as a name space
joystick.device = None
joystick.device_number = 0
joystick.joystickClock = core.Clock()
joystick.xFactor = 1
joystick.yFactor = 1

try:
    numJoysticks = joysticklib.getNumJoysticks()
    if numJoysticks > 0:
        try:
            joystickCache
        except NameError:
            joystickCache={}
        if not 0 in joystickCache:
            joystickCache[0] = joysticklib.Joystick(0)
        joystick.device = joystickCache[0]
        if win.units == 'height':
            joystick.xFactor = 0.5 * win.size[0]/win.size[1]
            joystick.yFactor = 0.5
    else:
        joystick.device = virtualjoysticklib.VirtualJoystick(0)
        logging.warning("joystick_{}: Using keyboard+mouse emulation 'ctrl' + 'Alt' + digit.".format(joystick.device_number))
except Exception:
    pass
    
if not joystick.device:
    logging.error('No joystick/gamepad device found.')
    core.quit()

joystick.status = None
joystick.clock = core.Clock()
joystick.numButtons = joystick.device.getNumButtons()
joystick.getNumButtons = joystick.device.getNumButtons
joystick.getAllButtons = joystick.device.getAllButtons
joystick.getX = lambda: joystick.xFactor * joystick.device.getX()
joystick.getY = lambda: joystick.yFactor * joystick.device.getY()


# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "trial"-------
t = 0
trialClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
joystick.oldButtonState = joystick.device.getAllButtons()[:]
joystick.activeButtons=[i for i in range(joystick.numButtons)]
# setup some python lists for storing info about the joystick
gotValidClick = False  # until a click is received
# keep track of which components have finished
trialComponents = [joystick]
for thisComponent in trialComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "trial"-------
while continueRoutine:
    # get current time
    t = trialClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # *joystick* updates
    if t >= 0.0 and joystick.status == NOT_STARTED:
        # keep track of start time/frame for later
        joystick.tStart = t  # not accounting for scr refresh
        joystick.frameNStart = frameN  # exact frame index
        win.timeOnFlip(joystick, 'tStartRefresh')  # time at next scr refresh
        joystick.status = STARTED
        joystick.joystickClock.reset()
    if joystick.status == STARTED:  # only update if started and not finished!
        joystick.newButtonState = joystick.getAllButtons()[:]
        if joystick.newButtonState != joystick.oldButtonState: # New button press
            joystick.pressedButtons = [i for i in range(joystick.numButtons) if joystick.newButtonState[i] and not joystick.oldButtonState[i]]
            joystick.releasedButtons = [i for i in range(joystick.numButtons) if not joystick.newButtonState[i] and joystick.oldButtonState[i]]
            joystick.newPressedButtons = [i for i in joystick.activeButtons if i in joystick.pressedButtons]
            joystick.oldButtonState = joystick.newButtonState
            joystick.buttons = joystick.newPressedButtons
            [logging.data("joystick_{}_button: {}, pos=({:1.4f},{:1.4f})".format(joystick.device_number, i, joystick.getX(), joystick.getY())) for i in joystick.pressedButtons]
            if len(joystick.buttons) > 0:  # state changed to a new click
                # abort routine on response
                continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or keyboard.Keyboard().getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "trial"-------
for thisComponent in trialComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# store data for thisExp (ExperimentHandler)
# store data for thisExp (ExperimentHandler)
x, y = joystick.getX(), joystick.getY()
joystick.newButtonState = joystick.getAllButtons()[:]
joystick.pressedState = [joystick.newButtonState[i] for i in range(joystick.numButtons)]
joystick.time = joystick.joystickClock.getTime()
thisExp.addData('joystick.x', x)
thisExp.addData('joystick.y', y)
[thisExp.addData('joystick.button_{0}'.format(i), int(joystick.pressedState[i])) for i in joystick.activeButtons]
thisExp.addData('joystick.time', joystick.time)
thisExp.addData('joystick.started', joystick.tStart)
thisExp.addData('joystick.stopped', joystick.tStop)
thisExp.nextEntry()
# the Routine "trial" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
