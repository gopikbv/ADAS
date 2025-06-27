import can
from can import *
from tkinter import * #tkinter library used to Create GUI to adjust the CAN signals used in the respective Modules
from tkinter import ttk
import threading
from PIL import ImageTk, Image, ImageDraw
import math


ECM_Info=can.Message(arbitration_id=0x180,data=[0],is_extended_id=False) #CAN packet creation
#data[0]= XXXX XXXX
#bit0- bit1 -> Ignition State , bit3-> BSW2 -> status

# To capture the BSW2 Status
def bsw2_pressed(state):
    ECM_Info.data[0]=ECM_Info.data[0] & 0xFB     #1111 1011
    ECM_Info.data[0]=ECM_Info.data[0] | 0x4  
        
def bsw2_released(state):
    ECM_Info.data[0]=ECM_Info.data[0] & 0xFB    

# To capture the Ignition State 
def SetIgnitionState(v):
    ECM_Info.data[0]=ECM_Info.data[0] & 0xFC     #1111 1101
    ECM_Info.data[0]=ECM_Info.data[0] | int(v)  
    
# ECM GUI Creation: 
# Root window -> a). Main window always wait for the user input or threads to begin the action
#                b). It hold only controls like track_bar,text boxes, buttons & it won't hold pictures
# Image drawn -> Took image from net-> with the help of CANVAS the image is drawn in the main or root window
def ECM_GUI():
    
    root=Tk() # ICM GUI Window creation
    root.title("ECM")
    root.geometry("200x200") #set the dimension for root window
    # Creating GroupBox with the help of LabelFrame()--> to set the Ignition state with the help of radio buttons
    frame=LabelFrame(root,text='Ignition Status',padx=5,pady=5)
    r=IntVar()
    radiobutton1=Radiobutton(frame, text="Off",bd=10,variable=r,value=0,cursor = "target",command=lambda:SetIgnitionState(r.get())).pack() 
    radiobutton2=Radiobutton(frame, text="ACC",bd=10,variable=r,value=1,cursor = "target",command=lambda:SetIgnitionState(r.get())).pack()
    radiobutton3=Radiobutton(frame, text="Run",bd=10,variable=r,value=2,cursor = "target",command=lambda:SetIgnitionState(r.get())).pack() 
    frame.pack()
    
    # Button created for BSW2-> Break Switch2
    # Implemented on 31/5/25 Module 14
    bsw2=ttk.Button(root,text='BSW2')
    bsw2.pack()
    bsw2.place(x=10 ,y=150)
    bsw2.bind("<ButtonPress-1>",bsw2_pressed,add="+")
    bsw2.bind("<ButtonRelease-1>",bsw2_released,add="+")
    
    root.mainloop()
    
    
def callback(ch, method, properties, body):
    
    return

# Main thread starts here:
with can.Bus() as bus:
   
    try:
        bus.send_periodic(ECM_Info,0.250) #150ms packet is tx periodically
        print(f"Message Sent on {bus.channel_info}")
    except can.CanError:
        print("Message is not sent")
    # Seperate thread used inside main thread
    threading.Thread(target=ECM_GUI).start() # with the help of thread concept i run a ICM_GUI() to generate the GUI.   
    bus.recv(callback) # This function will wait infinite time to receive packets from other modules. if it receive packets it will go to the callback routine
    #while True:
        #pass
                