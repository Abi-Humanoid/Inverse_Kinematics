# This script uses read in positions to work - need to update if motors have been re-assembled
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
DEVICENAME                  = '/dev/tty.usbserial-FT6RW7PK'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 10           # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 4000            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold


index = 0
      # Goal position

#arrays of all positions
first = [2603, 525, 2425, 2275, 1141, 3670, 2595, 2089, 1563, 2704, 2712, 3182] #standing up, knees slightly bent
one = [2604, 525, 2077, 1987, 1093, 3612, 2607, 2006, 1110, 2929, 3004, 3175] # right leg up
two = [2600, 523, 2154, 2282, 888, 3609, 2606, 2000, 1420, 2656, 3003, 3168] # right leg down
three = [2610, 524, 2249, 2195, 1017, 3628, 2587, 2085, 1484, 2330, 3183, 3124] #left leg up 
four = [2608, 525, 2565, 2165, 1711, 3630, 2587, 2086, 2066, 2017, 3117, 3119] # left leg down
five = [2607, 524, 2473, 2011, 1623, 3631, 2587, 2086, 2033, 2692, 2498, 3170] #right leg up
six = [2504, 472, 2128, 1430, 1634, 3679, 2609, 1992, 1904, 1962, 3026, 3159] #final position standing

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
   
    index=0
    # Write Dynamixel#1 goal position
    for dynamixel in dynamixels:
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dynamixel, ADDR_DXL_GOAL_SPEED, 50)
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
        
        # Write goal velocity ??
        


def main():
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
    moving_components(Dynamixels,first)
    time.sleep(1)
    moving_components(Dynamixels,one)
    time.sleep(1)
    moving_components(Dynamixels,two)
    time.sleep(1)
    moving_components(Dynamixels,three)
    time.sleep(1)
    moving_components(Dynamixels,four)
    time.sleep(1)
    moving_components(Dynamixels,five)
    time.sleep(1)
    moving_components(Dynamixels,six)
    time.sleep(1)
    
    # Clear bulkread parameter storage
    groupBulkRead.clearParam()

    # UNCOMMENT FOLLOWING TO DISABLE TORQUE IE UNLOCK MOTORS 
    # 'Dynamixels2' array below does not contain IDs 2, 3, 8 and 9 becuase we don't want to clear it. Add into array here if you want them unlocked.
    #Dynamixels2 = [DXL4_ID, DXL5_ID, DXL6_ID, DXL7_ID, DXL10_ID, DXL11_ID, DXL12_ID, DXL13_ID]
    #for dynamixel in Dynamixels2:
    #    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
    #        portHandler, dynamixel, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
    #    if dxl_comm_result != COMM_SUCCESS:
    #        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    #    elif dxl_error != 0:
    #        print("%s" % packetHandler.getRxPacketError(dxl_error))

    # Close port
    portHandler.closePort()

main()


