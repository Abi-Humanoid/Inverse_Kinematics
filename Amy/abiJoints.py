# Constants file containing the Dynamixel ID numbers for each of Abi's joints
# Includes lists of each limb and body area
# Amy Zuell

# MISSING
# 14, 15, 16
# front/back torso


NECK        = 1

# TORSO
LOWER_TORSO = 17
UPPER_TORSO = 18

# LEFT ARM
L_COLLAR    = 19
L_SHOULDER  = 20
L_ELBOW     = 24

# RIGHT ARM
R_COLLAR    = 21
R_SHOULDER  = 22
R_ELBOW     = 23

# LEFT LEG
L_INNER_HIP = 2
L_UPPER_HIP = 3
L_LOWER_HIP = 4
L_KNEE      = 5
L_ANKLE     = 6
L_FOOT      = 7

# RIGHT LEG
R_INNER_HIP = 8
R_UPPER_HIP = 9
R_LOWER_HIP = 10
R_KNEE      = 11
R_ANKLE     = 12
R_FOOT      = 13

# FULL BODY
COLLAR      = [L_COLLAR, R_COLLAR]
SHOULDER    = [L_SHOULDER, R_SHOULDER]
ELBOW       = [L_ELBOW, R_ELBOW]
L_ARM       = [L_COLLAR, L_SHOULDER, L_ELBOW]
R_ARM       = [R_COLLAR, R_SHOULDER, R_ELBOW]
ARMS        = L_ARM + R_ARM

INNER_HIP   = [L_INNER_HIP, R_INNER_HIP]
UPPER_HIP   = [L_UPPER_HIP, R_UPPER_HIP] 
LOWER_HIP   = [L_LOWER_HIP, R_LOWER_HIP] 
KNEE        = [L_KNEE, R_KNEE] 
ANKLE       = [L_ANKLE, R_ANKLE] 
FOOT        = [L_FOOT, R_FOOT] 
L_LEG       = [L_INNER_HIP, L_UPPER_HIP, L_LOWER_HIP, L_KNEE, L_ANKLE, L_FOOT]
R_LEG       = [R_INNER_HIP, R_UPPER_HIP, R_LOWER_HIP, R_KNEE, R_ANKLE, R_FOOT]
LEGS        = L_LEG + R_LEG

TORSO       = [LOWER_TORSO, UPPER_TORSO]

UPPER_BODY  = TORSO + ARMS
LOWER_BODY  = LEGS

ABI         = UPPER_BODY + LOWER_BODY

ID_TO_STR_DICT = {NECK: "Neck", LOWER_TORSO: "Lower Torso", UPPER_TORSO: "Upper Torso",
                  L_COLLAR: "Left Collar", L_SHOULDER: "Left Shoulder", L_ELBOW: "Left Elbow",
                  L_INNER_HIP: "Left Inner Hip", L_UPPER_HIP: "Left Upper Hip", 
                  L_LOWER_HIP: "Left Lower Hip", L_KNEE: "Left Knee", L_ANKLE: "Left Ankle", 
                  L_FOOT: "Left Foot",
                  R_COLLAR: "Right Collar", R_SHOULDER: "Right Shoulder", R_ELBOW: "Right Elbow",
                  R_INNER_HIP: "Right Inner Hip", R_UPPER_HIP: "Right Upper Hip", 
                  R_LOWER_HIP: "Right Lower Hip", R_KNEE: "Right Knee", R_ANKLE: "Right Ankle", 
                  R_FOOT: "Right Foot"}

# CONTROL TABLE
ADDR_TORQUE_ENABLE       = 24
ADDR_LED                 = 25
ADDR_GOAL_POSITION       = 30
ADDR_MOVING_SPEED        = 32
ADDR_PRESENT_POSITION    = 36
ADDR_PRESENT_SPEED       = 38
ADDR_PRESENT_LOAD        = 40
ADDR_PRESENT_VOLTAGE     = 42
ADDR_PRESENT_TEMPERATURE = 43
ADDR_MOVING              = 46

# Data Byte Length
LEN_GOAL_POSITION        = 4
LEN_MOVING_SPEED         = 4
LEN_PRESENT_POSITION     = 4
LEN_PRESENT_SPEED        = 4
LEN_PRESENT_LOAD         = 4
LEN_PRESENT_VOLTAGE      = 1
LEN_PRESENT_TEMPERATURE  = 1
LEN_MOVING               = 1

