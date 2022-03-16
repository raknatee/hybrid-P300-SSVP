
# [Paper](./Paper/index.md)

# [About EEG](./eeg/index.md)

# [Application Protocol](./application-protopol/index.md)

# [ML-server API](./ml-server/index.md)

# [Database Model](./database-model/index.md)

# [Data Collection](./data-collection/index.md)

# [Stack Talk](./stacktalk/index.md) 

# Daily

## 2021-12-17
- A20S01

## 2021-12-15
All was failed

- A17S01: 6 9 11 13 Hz 1cell/grid
- A18S01: 6 9 11 13 Hz all cells/grid
- A19S01: 6 9 11 13 Hz all cells/grid


## 2021-11-11
Zero padding for FFT in SSVEP

## 2021-11-09
- leave only 1 grid
- A15S01 A15S02 A16S01 failed

## 2021-11-08
- Add grid line
- A12S01
- A13S01
- A14S01
    
    However, the result was not good.
- Plan A15

## 2021-11-04
Okay, used PreImage Black White for rendering. And it can improve the browser performance. Ref: StackOverflow

PulseWave = Sin(y) > 0 ? black : white      

[Acceptable and Better Result For A10S01]()

Moreover, I had tried to use all of Alp (so we had all grid and all alps). Then tried A11S01 but result was not good but we got something. The result showed that Participant saw all of the signals. He/She could not focus on only one grid field. So, I decided to draw a line between each grid.

## 2021-11-03
- Fixed bugs: Please be careful about GUI Rendering. IF you GUI cannot Flash the signal (black and white) clearly. SSVP would not be working.
- Change Black and White from RBG to string value.
- Upgrade Sin to Pulse Wave (Sin(t)> 0.5 ? 1 : 0)
- [Acceptable Result]()

- After, I came back to home. I decided to remove SinWave mode and used only Pulse Wave = Sin(t) > 0 ? 1 : 0. Therefore, Pulse Wave would have freq and phare same as original SinWave.

However, Im curious that would it work or not. Let me test it tmr.

## 2021-10-28

Attempt8
Result: not okay
## 2021-10-27
Fixed: SSVEP uses FFT not the real (time domain) EEG data.
used Chaky's SSVP dataset for testing

## 2021-10-26
- Today, I fixed the SSVEP blinking

- Change API from Date.now() to performance.now() click here for stackoverflow
- Timing for SSVP must be blinking at the started time of - each round (not the REAL time).
- There was a problem about blinking because SinWave can be [-1, 1] so the -255 color can be White so USER can see double of real frequency.
 - Ex: 1Hz but User saw 2Hz (Black 2 times)
 - Fixed by reduce it to one half.
- Data collection (did it again because I changed Frontend)

    - A06S01
    - A07S01

## 2021-10-25

A03S01
A04S01
A03S02
A04S02
A05S01

## 2021-10-23

- Plan data collection: attempt 4 attempt 3

- Fixed: Canvas would stop when exit FullScreen

- Fixed: Online mode with corrent configuration

- Fixed: Online mode: need to change from guess_index to guess_index_order

## 2021-10-21
- Done Model Series 002

- Checkerboard randoms white and black

- GUI has many config like FullHYPS, SSVP only, etc.

## 2021-10-20
SSVP method okay

## 2021-10-18
series002 CNN2D Series 002

## 2021-10-17
data collection: Attemp 2 Participant A02S01

## 2021-10-14
Frontend added Cooldown for sleep function

Change default of experiment click here

## 2021-10-13
Frontend Upgrade from Vue2 To Vue3 with Typescript

## 2021-10-12
- Add get SSVP dataset and notch+bypass filter

- GUI supports Sleep for Offline but I need to test it more

## 2021-10-11
Add selected channel feature in DataExtractor class.

## 2021-10-10
Model Series001 Series 001
## 2021-10-09
- Start new branch ml-session
- data processing: Notch filter and bypass filter
- create a P300 dataset with those filter and padding to make all sizes are equal.
## 2021-10-07
Finally, I changed /eeg_offline and /eeg_online to WS

## 2021-10-05
- Collected EEG from A01 S02 S03

- Add Database viewer both GUI and ML-server

## 2021-10-04
- Checkerboard

##2021-10-03
- refactoring database name and add ML-server API for naming Mongo collection

- sync GUI and eeg-client

- edit db-script which matchs with new Database name

## 2021-09-30
- Experiment can configurate on Frontend

- collect data S01

## 2021-09-29
- set up and plan a EEG headset data collection attempt 1

- create export db-script (only export not import)

- Refactor Frontend and overlap time is implemented. Checkerboard hasnt been implemented.

## 2021-09-28
- I had spent almost 2 days to fix the spam problem on EEG-client (read on My Stack Task For more details)

- Update Doc

## 2021-09-25
- implement GUI on offline mode and change status to okay click me (API Doc)
## 2021-09-24
implement GUI on online mode and change status to okay click me (API Doc)
## 2021-09-23
plan the offline and online mode click me (Experiment API Doc)
coding dummy server and change status to okay