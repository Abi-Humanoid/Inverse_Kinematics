Inverse Kinematics [Dynamixel Motors] 
================
All code for testing, calibrating, and controlling the Dynamixel motors used by Abi. 

## WHAT TO DO 🧐

Use the **template.py** file to write/add your code for Abi's Dynamixel motors (note. may need to change the control table values depending on the motors you are using). 

The (obviously) main script in this repo is **main.py**. This script currently include functions that allow you to enable/disable the torque on a specific motor, and actuate a motor to a specific position. 

How to run the script:
```bash 
python3 main.py
```

## Laura (Folder)
All scripts written by Laura Harman prior to 20th May 2022. 

## Amy (Folder)

**abiJoints.py** contains definitions for each of Abi's motors, lists of motors defining limbs, as well as control table constants
**movingAbi.py** is an all in one file for reading/writing/setting Abi's Dyanmixel motors

How to run the script:
```bash 
python movingAbi.py
```
This script is interactive and instructions are fully contained within.