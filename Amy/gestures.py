# Experimenting with an all-in-one reading/setting file for controlling Abis movements
# Amy Zuell

# Initialise operating systems
import os
if os.name == 'nt':
    import msvcrt

    def getch():
        return msvcrt.getch().decode()
else:
    import sys
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# Import Dynamixel SDK library and Abi Joint definitions
from dynamixel_sdk import * 
import abiJoints as ID

# Protocol version
PROTOCOL_VERSION = 1.0

# Device
BAUDRATE   = 57600

# Torque constants
TORQUE_ENABLE  = 1
TORQUE_DISABLE = 0                

DXL_MINIMUM_POSITION_VALUE = 10     # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE = 4000   # and this value (note that the Dynamixel would not move when the position value is out of movable range.
DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold

# Motors and their positions
motors          = []
motors_position = []

# Open port and set baudrate
def openPort():
    ## Open port
    print(" # Opening port")
    if portHandler.openPort():
        print(" # Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()

    # Set port baudrate
    print(" # Setting baudrate")
    if portHandler.setBaudRate(BAUDRATE):
        print(" # Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()

# Function to set the torque
def setTorque(motors, enable):
    print("Setting torque %s" % ("on" if enable else "off"))
    for dynamixel in motors:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dynamixel, ID.ADDR_TORQUE_ENABLE, enable)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print(" # {}: torque {}".format(ID.ID_TO_STR_DICT[dynamixel].ljust(18), ("on" if enable else "off")))

# Initialise the group bulk read parameters
def addParamater(motors):
    print("Initialising")
    for dynamixel in motors:
        dxl_addparam_result = groupBulkRead.addParam(dynamixel, ID.ADDR_PRESENT_POSITION, ID.LEN_PRESENT_POSITION)
        #dxl_addparam_result = groupBulkRead.addParam(dynamixel, ID.ADDR_MOVING, ID.LEN_MOVING)
        print(' # %s Connected' % ID.ID_TO_STR_DICT[dynamixel].ljust(18))
        if dxl_addparam_result != True:
            print("[%s] groupBulkRead addparam failed first" % ID.ID_TO_STR_DICT[dynamixel])
            quit()

# Read and print the position of the motors 
def readPosition(motors):
    # Bulkread present position and moving status
    dxl_comm_result = groupBulkRead.txRxPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    
    for dynamixel in motors:
        # Check if groupbulkread data is available
        dxl_getdata_result = groupBulkRead.isAvailable(dynamixel, ID.ADDR_PRESENT_POSITION, ID.LEN_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[%s] groupBulkRead getdata failed" % ID.ID_TO_STR_DICT[dynamixel])
            quit()
        dxl_present_position = groupBulkRead.getData(dynamixel, ID.ADDR_PRESENT_POSITION, ID.LEN_PRESENT_POSITION)
        print(" # {} : {}".format(ID.ID_TO_STR_DICT[dynamixel].ljust(18), dxl_present_position))

# Store the current position of the motors
def storePosition(motors):
    # Bulkread present position and moving status
    dxl_comm_result = groupBulkRead.txRxPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    
    num_motor = 0
    for dynamixel in motors:
        # Check if groupbulkread data is available
        dxl_getdata_result = groupBulkRead.isAvailable(dynamixel, ID.ADDR_PRESENT_POSITION, ID.LEN_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[%s] groupBulkRead getdata failed" % ID.ID_TO_STR_DICT[dynamixel])
            quit()

        dxl_present_position = groupBulkRead.getData(dynamixel, ID.ADDR_PRESENT_POSITION, ID.LEN_PRESENT_POSITION)
        motors_position.insert(num_motor, dxl_present_position)
        print(" # {} Stored {}".format(ID.ID_TO_STR_DICT[dynamixel].ljust(18), dxl_present_position))
        num_motor += 1

# Print the currently stored position
def printStoredPosition(motors, motors_position):
    num_motor = 0
    for dynamixel in motors:
        print(" # {} : {}".format(ID.ID_TO_STR_DICT[dynamixel].ljust(18), motors_position[num_motor]))
        num_motor += 1

# Make Abi move into the stored position
def setPosition(motors, motors_position):
    num_motor = 0
    for dynamixel in motors:
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ID.ADDR_GOAL_POSITION, motors_position[num_motor])
        num_motor += 1

def setSpeed(motors, motors_speed):
    num_motor = 0
    for dynamixel in motors:
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ID.ADDR_MOVING_SPEED, motors_speed[num_motor])
        num_motor += 1

def actionArmBySide(motors):
    goal = [2010, 2030, 1997, 1586, 1035, 2074]

    SPEED_SHOULDER  = 85
    SPEED_ELBOW     = 95
    SPEED_COLLAR    = 100

    num_motor = 0
    for dynamixel in motors:
        if dynamixel in ID.SHOULDER:
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ID.ADDR_MOVING_SPEED, SPEED_SHOULDER)
        if dynamixel in ID.ELBOW:
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ID.ADDR_MOVING_SPEED, SPEED_ELBOW)
        if dynamixel in ID.COLLAR:
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ID.ADDR_MOVING_SPEED, SPEED_COLLAR)

        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ID.ADDR_GOAL_POSITION, goal[num_motor])
        num_motor += 1



def actionHug(motors):
    goal = [746, 2316, 2413, 2795, 771, 1525]

    SPEED_SHOULDER  = 85
    SPEED_ELBOW     = 95
    SPEED_COLLAR    = 100

    num_motor = 0
    for dynamixel in motors:
        if dynamixel in ID.SHOULDER:
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ID.ADDR_MOVING_SPEED, SPEED_SHOULDER)
        if dynamixel in ID.ELBOW:
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ID.ADDR_MOVING_SPEED, SPEED_ELBOW)
        if dynamixel in ID.COLLAR:
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ID.ADDR_MOVING_SPEED, SPEED_COLLAR)

        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ID.ADDR_GOAL_POSITION, goal[num_motor])
        num_motor += 1

#def actionWave(motors):
    #motors_speed = [80 for dynamixel in motors]

    #setSpeed(motors, motors_speed)
    #print("first move")
    #setPosition(motors, [1910, 2153, 1990, 1669, 4034, 1074])
    #time.sleep(2)
    #print("second move")
    #setPosition(motors, [1922, 2154, 1990, 3570, 3821, 1350])
    #time.sleep(2)
    #print("third move")
    #setPosition(motors, [1923, 2153, 1991, 3570, 3824, 656])
    #time.sleep(1)
    #setPosition(motors, [2004, 2102, 1948, 3616, 4032, 868])
    #time.sleep(1)
    #setPosition(motors, [2006, 2155, 1948, 3511, 4086, 1568])

def actionHandshake(motors):
    motors_speed = [90 for dynamixel in motors]

    pos_down = [2152, 2062, 2002, 2314, 808, 1726]
    pos_up = [2152, 2063, 2002, 2582, 897, 1804]

    setSpeed(motors, motors_speed)
    setPosition(motors, pos_down)
    time.sleep(1.5)
    setPosition(motors, pos_up)
    time.sleep(0.5)
    setPosition(motors, pos_down)
    time.sleep(0.5)
    setPosition(motors, pos_up)
    time.sleep(0.5)
    setPosition(motors, pos_down)
    time.sleep(0.5)
    setPosition(motors, pos_up)
    

# Main script

print("**************** GESTURING ABI ****************")
       
# Initialize PortHandler and open ports
print("Establishing connection to Abi via serial communication")
print("Example [Windows: COM1   Linux: /dev/ttyUSB0 Mac: /dev/tty.usbserial-*]")
DEVICENAME = input("Enter port name: ")
portHandler = PortHandler(DEVICENAME)
openPort()
print("\n")

# Initialize PacketHandler and GroupBulkRead
packetHandler = PacketHandler(PROTOCOL_VERSION)
groupBulkRead = GroupBulkRead(portHandler, packetHandler)

# Set limbs
ABI_MODE = {'1': ID.ARMS, '2': ID.LEGS, '3': ID.ABI}
ABI_MODE_TO_STR = {'1': "Arms", '2': "Legs", '3': 'Full Body'}
print("[Modes]\n 1: Arms")
#\n 2: Legs\n 3: Full Body")
abiMode = input("Enter Abi mode: ")
motors = ABI_MODE[abiMode]
setTorque(motors, TORQUE_DISABLE)
addParamater(motors)
    
print("Press any key to continue\n") 

# Loop
while 1:

    # Escape key to exit
    if getch() == chr(0x1b):
        break

    # Set mode
    print("Choose gesture or ESC to exit")
    print("[Modes]\n 1: Reset\n 2: Hug\n 3: Wave\n 4: Handshake")
    mode = input("Enter gesture: ")

    ## Apply action
    if mode == '1':
        print('- Reset')
        actionArmBySide(motors)
        
    if mode == '2':
        print("- Hug")
        actionHug(motors)

    if mode == '3':
        print("- Wave")
        actionWave(motors)

    if mode == '4':
        print("- Handshake")
        actionHandshake(motors)
        


    time.sleep(2)

    print("Press any key to continue\n")

print("Reset position")
actionArmBySide(motors)
time.sleep(2)
print("Disconnecting and turning off")
groupBulkRead.clearParam()          # Clear bulkread parameter storage
setTorque(motors, TORQUE_DISABLE)   # Disable torque
portHandler.closePort()             # Close port
print("Successfully disconnected")


# initialise, open port etc
# enable torque
# add parameter storage
# set speed
# set goal pos
