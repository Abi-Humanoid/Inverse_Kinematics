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
"""
DXL2_ID = 2                 # Dynamixel#1 ID : 1
DXL3_ID = 3                 # Dynamixel#1 ID : 2
DXL4_ID = 4
DXL5_ID = 5
DXL6_ID = 6
DXL7_ID = 7
"""
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

Sitting_position = [2674, 2596, 119, 2961, 3034, 3586]
Left_leg_1 = [2675, 2602, 119, 2862, 3031, 3587]
Left_leg_2 = [2675, 2603, 119, 2734, 3037, 3587]
Left_leg_3 = [2675, 2604, 119, 2649, 3060, 3587]
Left_leg_4 = [2675, 2605, 119, 2624, 3063, 3587]
Left_leg_5 = [2675, 2608, 119, 2570, 3072, 3587]
Left_leg_6 = [2674, 2604, 119, 2543, 3074, 3587]
Left_leg_7 = [2675, 2608, 119, 2511, 3075, 3587]
Left_leg_8 = [2675, 2595, 119, 2448, 3082, 3587]
Left_leg_9 = [2725, 2599, 94, 1870, 3101, 3538]

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


def moving_components(dynamixels,positions): 
#while 1:
    #print("Press any key to continue! (or press ESC to quit!)")
    """
    if getch() == chr(0x1b):
        break
    """
    index=0
    # Write Dynamixel#1 goal position
    for dynamixel in dynamixels:
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ADDR_DXL_GOAL_SPEED, 30)
        if (dxl_comm_result != COMM_SUCCESS):
            print("%s\n", packetHandler.getTxRxResult(dxl_comm_result))
        elif (dxl_error != 0):
            print("%s\n", packetHandler.getRxPacketError(dxl_error))
        
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ADDR_MX_GOAL_POSITION, positions[index])
        print('dynamixel',dynamixel)
        print('position',positions[index])
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
        
    



def main():
    #DXL2_ID, DXL3_ID, DXL4_ID, DXL5_ID, DXL6_ID, DXL7_ID, 
    Dynamixels = [DXL8_ID, DXL9_ID, DXL10_ID, DXL11_ID, DXL12_ID, DXL13_ID]
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
    moving_components(Dynamixels,Sitting_position)
    print("Sitting_position")
    
    moving_components(Dynamixels,Left_leg_9)
    print("Left_leg_9")
    time.sleep(8)
    moving_components(Dynamixels,Sitting_position)
    print("Sitting_position")
    time.sleep(8)
    #disconnect
    # Clear bulkread parameter storage
    groupBulkRead.clearParam()
    #DXL2_ID, DXL3_ID, DXL4_ID, DXL5_ID, DXL6_ID, DXL7_ID, 
    Dynamixels = [DXL8_ID, DXL9_ID, DXL10_ID, DXL11_ID, DXL12_ID, DXL13_ID]
    # Disable Dynamixel#1 Torque
    for dynamixel in Dynamixels: 
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
            portHandler, dynamixel, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))


    # Close port
    portHandler.closePort()

main()

"""
# Add parameter storage for Dynamixel#2 moving value
dxl_addparam_result = groupBulkRead.addParam(DXL2_ID, ADDR_MX_MOVING, LEN_MX_MOVING)
if dxl_addparam_result != True:
    print("[ID:%03d] groupBulkRead addparam failed" % DXL2_ID)
    quit()


    
    

    # Write Dynamixel#2 goal position
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, ADDR_MX_GOAL_POSITION, dxl_goal_position[index])
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


    
    while 1:
        
        # Bulkread present position and moving status
        dxl_comm_result = groupBulkRead.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

        # Check if groupbulkread data of Dynamixel#1 is available
        dxl_getdata_result = groupBulkRead.isAvailable(DXL1_ID, ADDR_MX_PRESENT_POSITION, LEN_MX_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupBulkRead getdata failed" % DXL1_ID)
            quit()
        
        
        # Check if groupbulkread data of Dynamixel#2 is available
        dxl_getdata_result = groupBulkRead.isAvailable(DXL2_ID, ADDR_MX_MOVING, LEN_MX_MOVING)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupBulkRead getdata failed" % DXL2_ID)
            quit()

        # Get Dynamixel#1 present position value
        dxl1_present_position = groupBulkRead.getData(DXL1_ID, ADDR_MX_PRESENT_POSITION, LEN_MX_PRESENT_POSITION)

        # Get Dynamixel#2 moving value
        dxl2_moving_value = groupBulkRead.getData(DXL2_ID, ADDR_MX_MOVING, LEN_MX_MOVING)

        print("[ID:%03d] Present Position : %d \t [ID:%03d] Is Moving: %d" % (DXL1_ID, dxl1_present_position, DXL2_ID, dxl2_moving_value))

        if not (abs(dxl_goal_position[index] - dxl1_present_position) > DXL_MOVING_STATUS_THRESHOLD):
            break
        
    # Change goal position
    #if index == 0:
        #index = 1
    #else:
     #   index = 0


# Clear bulkread parameter storage
groupBulkRead.clearParam()

# Disable Dynamixel#1 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Disable Dynamixel#2 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()
"""
