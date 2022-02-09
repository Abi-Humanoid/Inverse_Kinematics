
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

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
# Control table address is different in Dynamixel model
ADDR_MX_TORQUE_ENABLE = 24
ADDR_MX_GOAL_POSITION = 30
ADDR_MX_PRESENT_POSITION = 36
ADDR_MX_MOVING = 46

# Data Byte Length
LEN_MX_GOAL_POSITION = 4
LEN_MX_PRESENT_POSITION = 4
LEN_MX_MOVING = 1

# Protocol version
# See which protocol version is used in the Dynamixel
PROTOCOL_VERSION = 1.0

# Default setting


DXL2_ID = 2                 # Dynamixel#1 ID : 1
DXL3_ID = 3                 # Dynamixel#1 ID : 2
DXL4_ID = 4
DXL5_ID = 5
DXL6_ID = 6
DXL7_ID = 7

DXL8_ID = 8
DXL9_ID = 9            
DXL10_ID = 10
DXL11_ID = 11
DXL12_ID = 12
DXL13_ID = 13
BAUDRATE = 57600             # Dynamixel default baudrate : 57600
# Check which port is being used on your controller
DEVICENAME = '/dev/tty.usbserial-FT62AHPC'
                                              # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE = 1                 # Value for enabling the torque
TORQUE_DISABLE = 0                 # Value for disabling the torque
# Dynamixel will rotate between this value
DXL_MINIMUM_POSITION_VALUE = 10
# and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MAXIMUM_POSITION_VALUE = 4000
# Dynamixel moving status threshold
DXL_MOVING_STATUS_THRESHOLD = 20

index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE,
                     DXL_MAXIMUM_POSITION_VALUE]        # Goal position

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Initialize GroupBulkRead instace for Present Position
groupBulkRead = GroupBulkRead(portHandler, packetHandler)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

#DXL2_ID, DXL3_ID, DXL4_ID, DXL5_ID, DXL6_ID, DXL7_ID, 

Dynamixels = [DXL2_ID, DXL3_ID, DXL4_ID, DXL5_ID, DXL6_ID, DXL7_ID, DXL8_ID, DXL9_ID, DXL10_ID, DXL11_ID, DXL12_ID, DXL13_ID]
# Enable Dynamixel#2-7 Torque
for dynamixel in Dynamixels:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, dynamixel, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)

    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel#%d has been successfully connected" % dynamixel)


for dynamixel in Dynamixels:
    # Add parameter storage for Dynamixel#1 present position
    dxl_addparam_result = groupBulkRead.addParam(
        dynamixel, ADDR_MX_PRESENT_POSITION, LEN_MX_PRESENT_POSITION)
    print('Connected')
    if dxl_addparam_result != True:
        print("[ID:%03d] groupBulkRead addparam failed first" % dynamixel)
        quit()

"""
# Add parameter storage for Dynamixel#2 moving value
for dynamixel in Dynamixels:
    dxl_addparam_result = groupBulkRead.addParam(
        dynamixel, ADDR_MX_MOVING, LEN_MX_MOVING)
    print('2nd: Connected')
    if dxl_addparam_result != True:
        print("[ID:%03d] groupBulkRead addparam failed" % dynamixel)
        quit()
"""

while 1:
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break

    # Write Dynamixel#1 goal position
    #dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_MX_GOAL_POSITION, dxl_goal_position[index])
    # if dxl_comm_result != COMM_SUCCESS:
    #    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    # elif dxl_error != 0:
    #    print("%s" % packetHandler.getRxPacketError(dxl_error))

    # Write Dynamixel#2 goal position
    """
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, DXL2_ID, ADDR_MX_GOAL_POSITION, dxl_goal_position[index])
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    """

    # Bulkread present position and moving status
    dxl_comm_result = groupBulkRead.txRxPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    for dynamixel in Dynamixels:
        # Check if groupbulkread data of Dynamixel#1 is available
        dxl_getdata_result = groupBulkRead.isAvailable(
            dynamixel, ADDR_MX_PRESENT_POSITION, LEN_MX_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupBulkRead getdata failed" % dynamixel)
            quit()
    """
    for dynamixel in Dynamixels:
        # Check if groupbulkread data of Dynamixel#2 is available
        dxl_getdata_result = groupBulkRead.isAvailable(dynamixel, ADDR_MX_MOVING, LEN_MX_MOVING)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupBulkRead getdata failed" % dynamixel)
            quit()
    """
    dxl1_present_position=[]
    index1=0

    for dynamixel in Dynamixels:
        # Get Dynamixel#1 present position value
        dxl1_present_position.append( groupBulkRead.getData(
            dynamixel, ADDR_MX_PRESENT_POSITION, LEN_MX_PRESENT_POSITION))
        #dxl2_moving_value = groupBulkRead.getData(dynamixel, ADDR_MX_MOVING, LEN_MX_MOVING)
        #print("[ID:%03d] Present Position : %d \t " %
                #(dynamixel, dxl1_present_position))
        if not (abs(dxl_goal_position[index] - dxl1_present_position[index1]) > DXL_MOVING_STATUS_THRESHOLD):
            break
        index1 +=1

    print("Final pos: ")
    
    print(dxl1_present_position)



    
    # Change goal position
    """
    if index == 0:
        index = 1
    else:
        index = 0
    """

# Clear bulkread parameter storage
groupBulkRead.clearParam()

# Disable Dynamixel#1 Torque

Dynamixels = [DXL4_ID, DXL5_ID, DXL6_ID, DXL7_ID, DXL10_ID, DXL11_ID, DXL12_ID, DXL13_ID]
for dynamixel in Dynamixels:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, dynamixel, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()
