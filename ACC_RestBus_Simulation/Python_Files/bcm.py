#Brake control Module will send the vehicle speed signal to the ACC through CAN
import can
from can import *
from tkinter import * #tkinter library used to Create GUI to adjust the CAN signals used in the respective Modules
import threading

BCM_Info=can.Message(arbitration_id=0x110,data=[0],is_extended_id=False) #CAN packet creation
# data[0] = vehicle speed

global horizantal
horizantal=0

def setVehicleSpeed(v):
    BCM_Info.data[0]=int(v)% 255
    
# BCM GUI Creation:
def BCM_GUI():
    global horizantal
    root=Tk() # BCM GUI Window creation
    root.title("BCM")
    root.geometry("700x200") #set the dimension for window
    # To create track bar with the help of scale()
    horizantal=Scale(root,label="Vehicle Speed",from_=0,to=250,orient=HORIZONTAL,width=20,length=500,tickinterval=50,
    command=setVehicleSpeed,troughcolor="Black",sliderlength=20,highlightcolor="Red",cursor="bottom_side",
    activebackground="Green",bg="Gray",bd =10)
    horizantal.pack() # It is used to pack the trackbar to the root
    root.mainloop()
    
    
def callback(ch, method, properties, body):
    global horizantal
    # converts the bytes received from ECM Module into string
    s=str(body, encoding='utf-8')
    msg=bus.strToMessage(s)
    #Look for arbitration_id match
    match msg.arbitration_id:
        case 0x180: # ECM to provide Ignition Status
            ign_st=int(msg.data[0]) & 0x03
            if ign_st < 2:
                horizantal.set(0)  #vehicle speed =0
                BCM_Info.data[0]=0 # Bcm data packet =0 
        # ACC provide the status of ACC state, Target speed
        case 0x456:
            # To check ACC state is active and vehicle speed > Target speed
            if msg.data[1]& 0x7 ==3 and BCM_Info.data[0] > msg.data[0]:
                diff=BCM_Info.data[0]-msg.data[0]
                BCM_Info.data[0]=BCM_Info.data[0]-diff
                horizantal.set(horizantal.get()-diff)
            
            # To check ACC state is active and vehicle speed < Target speed
            elif msg.data[1]& 0x7 ==3 and BCM_Info.data[0] < msg.data[0]:
                BCM_Info.data[0]=int(msg.data[0])
                horizantal.set(int(msg.data[0]))
            
    
    return 
    
with can.Bus() as bus:
   
    try:
        bus.send_periodic(BCM_Info,0.250)
        print(f"Message Sent on {bus.channel_info}")
    except can.CanError:
        print("Message is not sent")
    threading.Thread(target=BCM_GUI).start() # with the help of threading i run a BCM_GUI() to generate the GUI.   
    bus.recv(callback) # This function will wait infinite time to receive packets from other modules. if it receive packets it will go to the callback routine
    #while True:
        #pass
            