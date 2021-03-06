import os
import time


if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
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
ADDR_MX_TORQUE_ENABLE       = 24               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION       = 30
ADDR_MX_PRESENT_POSITION    = 36
ADDR_MX_MOVING              = 46
ADDR_DXL_GOAL_SPEED         = 32
ADDR_DXL_PRESENT_SPEED		= 38

# Data Byte Length
LEN_MX_GOAL_POSITION        = 4
LEN_MX_PRESENT_POSITION     = 4
LEN_MX_MOVING               = 1

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

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
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/tty.usbserial-FT62AHPC'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 10           # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 4000            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold


index = 0
      # Goal position

#positions_array = [1032, 3598, 2632, 2199, 1623, 3639, 2491, 2591, 2339, 2405, 3178, 3607]

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

def moving_components(dynamixels,positions_array): 
#while 1:
    #print("Press any key to continue! (or press ESC to quit!)")
    """
    if getch() == chr(0x1b):
        break
    """
    index=0
    # Write Dynamixel#1 goal position
    for dynamixel in dynamixels:
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ADDR_DXL_GOAL_SPEED, 10)
        if (dxl_comm_result != COMM_SUCCESS):
            print("%s\n", packetHandler.getTxRxResult(dxl_comm_result))
        elif (dxl_error != 0):
            print("%s\n", packetHandler.getRxPacketError(dxl_error))
        
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ADDR_MX_GOAL_POSITION, positions_array[index])
        print('dynamixel',dynamixel)
        print('position',positions_array[index])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        index+=1
        #while 1:
        #    dxl1_present_position = groupBulkRead.getData(dynamixel, ADDR_MX_PRESENT_POSITION, LEN_MX_PRESENT_POSITION)
        #    if not (abs(positions[index] - dxl1_present_position) > DXL_MOVING_STATUS_THRESHOLD):
        #        break
        # Write goal velocity

def Run_Dynamixels(positions_array):
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
    # Write Dynamixel#1 goal position
    for dynamixel in Dynamixels:
        # Add parameter storage for Dynamixel#1 moving position
        dxl_addparam_result = groupBulkRead.addParam(
            dynamixel, ADDR_MX_MOVING, LEN_MX_MOVING)
        print('Connected')
        if dxl_addparam_result != True:
            print("[ID:%03d] groupBulkRead addparam failed first" % dynamixel)
            quit()
        dxl_comm_result = groupBulkRead.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        dxl_getdata_result = groupBulkRead.isAvailable(dynamixel, ADDR_MX_MOVING, LEN_MX_MOVING)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupBulkRead getdata failed" % dynamixel)
            quit()
    
    #call function for each of the positions
    moving_components(Dynamixels,positions_array)
    print("Moved!")
    time.sleep(10)
    #disconnect
    # Clear bulkread parameter storage
    groupBulkRead.clearParam()
    #DXL2_ID, DXL3_ID, DXL4_ID, DXL5_ID, DXL6_ID, DXL7_ID, 
    """
    Dynamixels = [DXL4_ID, DXL5_ID, DXL6_ID, DXL7_ID, DXL10_ID, DXL11_ID, DXL12_ID, DXL13_ID]
    for dynamixel in Dynamixels:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
            portHandler, dynamixel, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
    """
    # Close port
    #portHandler.closePort()
    

#Run_Dynamixels(positions_array)