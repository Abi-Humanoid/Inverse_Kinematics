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




# Main script

print("**************** MOVING ABI ****************")
       
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
print("[Modes]\n 1: Arms\n 2: Legs\n 3: Full Body")
abiMode = input("Enter Abi mode: ")
motors = ABI_MODE[abiMode]
addParamater(motors)
setTorque(motors, TORQUE_DISABLE)
    
print("Press any key to continue\n") 

# Loop
while 1:

    # Escape key to exit
    if getch() == chr(0x1b):
        break

    # Set mode
    print("Choose mode or ESC to exit")
    print("[Modes]\n 1: Read current position\n 2: Store current position\n 3: Print stored position\n 4: Set stored position\n 5: Enable torque\n 6: Disable torque")
    mode = input("Enter mode: ")

    # Apply action
    if mode == '1':
        print("- Reading Abi's %s current position" % ABI_MODE_TO_STR[abiMode])
        readPosition(motors)

    if mode == '2':
        print("- Storing Abi's %s current position" % ABI_MODE_TO_STR[abiMode])
        storePosition(motors)

    if mode == '3':
        print("- Printing Abi's %s stored position" % ABI_MODE_TO_STR[abiMode])
        printStoredPosition(motors, motors_position)

    if mode == '4':
        print("- Setting Abi's %s position" % ABI_MODE_TO_STR[abiMode])
        setPosition(motors, motors_position)

    if mode == '5':
        print("- Enabling torque")
        setTorque(motors, TORQUE_ENABLE)

    if mode == '6':
        print("- Disabling torque")
        setTorque(motors, TORQUE_DISABLE)


    print("Press any key to continue\n")

print("Disconnecting and turning off")
groupBulkRead.clearParam()          # Clear bulkread parameter storage
setTorque(motors, TORQUE_DISABLE)   # Disable torque
portHandler.closePort()             # Close port
print("Successfully disconnected")