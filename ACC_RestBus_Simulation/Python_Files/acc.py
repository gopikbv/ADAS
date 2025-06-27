#ACC Module is created on 25/5/25 --> Module 14 Lecture
import can
from can import *
import tkinter as tk
from tkinter import * #tkinter library used to Create GUI to adjust the CAN signals used in the respective Modules
from tkinter import ttk
import threading
from PIL import ImageTk, Image, ImageDraw
import math
import json

# ACC Output Signal --> 1).ACC state[2bits-->state & 1bit--> fault=3bit] 2).ACC Brake Decel request[Applied/Not applied-> 1bit] 
#3).Acc Driver information message[3bit--> To display the ACC state] 4).Target speed[1 byte]
#data[0]= xxxx xxxx --> Target Speed
#data[1]= xxxx xxxx --> bit0 -bit2 --> ACC state, bit3 ---> Brake decel req ,bit4 -bit6 ---> ACC driver info
ACC_Info=can.Message(arbitration_id=0x456,data=[0,0,50],is_extended_id=False) #CAN packet creation

# To monitor the vehicle speed from bcm module:
global vs
vs=0

# To monitor the BSW1 status:
global bsw1
bsw1=0

# To monitor the BSW2 status:
global bsw2
bsw2=0

# To capture the ignition state:
global ign_st
ign_st=0
 
# To maintain the distance from forward vehicle [Eg: 50m is used here]:
global timegap
timegap=100

# CAR animation 
global car1_xcalib
car1_xcalib=0  
global car2_xcalib
car2_xcalib=0 
global car3_xcalib
car3_xcalib=0 
global carchosen
carchosen  =0
global spinbox
spinbox=0

global label1
label1=0
global label2
label2=0
global label3
label3=0

global root
root=0

global car2_speed
car2_speed=0
global car3_speed
car3_speed=0

# created on 1/6/25 --> Module 16 Lecture
# To handle the Animaton factor for the CAR and Speed is selected by the user and need to validate the selection
def on_spinbox_change():
    global carchosen
    global spinbox
    global car2_xcalib 
    global car3_xcalib  
    global car2_speed
    global car3_speed
    match carchosen.get():
        case "Car2":
            car2_xcalib=(float(spinbox.get())/(3.6*5*0.25))
            car2_speed=int(spinbox.get())
        case "Car3":
            car3_xcalib=(float(spinbox.get())/(3.6*5*0.25))
            car3_speed=int(spinbox.get())
            
# created on 14/6/25 --> Module 17 Lecture
# Function to capture the forward vehicle with respect to ACC vehicle to reduce the target speed and to apply the brake if necessary
def find_widget(x,y,name):
    global label1
    global timegap
    global root
    for child in root.children.values():
        if isinstance(child,tk.Label) and y==child.winfo_y() and (child.winfo_name() =="car2" or child.
        winfo_name()=="car3") and abs(child.winfo_x()-x)<=timegap and label1.winfo_x() < child.winfo_x():
            return child
    return None

# TO capture the arrow key status to move the selected car it makes to switch the lanes:
# Directions -> UP,Down,Right,Left
def move_up(event):
    global label1
    global label2
    global label3
    global carchosen
    match  carchosen.get():
        case "Car1":
            
            label1.place(x=label1.winfo_x(), y=label1.winfo_y()-10)
        case "Car2":
            label2.place(x=label2.winfo_x(), y=label2.winfo_y()-10)
        case "Car3":
            label3.place(x=label3.winfo_x(), y=label3.winfo_y()-10)
       

def move_down(event):
    global label1
    global label2
    global label3
    global carchosen
    match  carchosen.get():
        case "Car1":
            #print("Car1 down")
            label1.place(x=label1.winfo_x(), y=label1.winfo_y()+10)
        case "Car2":
            label2.place(x=label2.winfo_x(), y=label2.winfo_y()+10)
        case "Car3":
            label3.place(x=label3.winfo_x(), y=label3.winfo_y()+10)

   
   
def move_left(event):
    global label1
    global label2
    global label3
    global carchosen
    match  carchosen.get():
        case "Car1":
            label1.place(x=label1.winfo_x()-10, y=label1.winfo_y())
        case "Car2":
            label2.place(x=label2.winfo_x()-10, y=label2.winfo_y())
        case "Car3":
            label3.place(x=label3.winfo_x()-10, y=label3.winfo_y())

def move_right(event):
    global label1
    global label2
    global label3
    global carchosen
   #label.place(x=label.winfo_x()+10, y=label1.winfo_y())
    match carchosen.get():
        case "Car1":
            label1.place(x=label1.winfo_x()+10, y=label1.winfo_y())
        case "Car2":
            label2.place(x=label2.winfo_x()+10, y=label2.winfo_y())
        case "Car3":
            label3.place(x=label3.winfo_x()+10, y=label3.winfo_y())     

# ACC GUI Creation: 
# Picture Creation-> With the help of labels, We created CAR animations for real time experience[using keyboard arrow keys we can move the car --> UP,DOWN,LEFT,RIGHT] 
#For fixed Image-> In tkinter, With the help of canvas the image is placed at (x,y) cordinate]
# Root window -> a). Main window always wait for the user input or threads to begin the action
#                b). It hold only controls like track_bar,text boxes, buttons & it won't hold pictures
# Image drawn -> Took image from net-> with the help of CANVAS the image is drawn in the main or root window
def ACC_GUI():
    global root
    global label1
    global label2
    global label3
    global carchosen
    global spinbox
    root=Tk() # ACC GUI Window creation
    root.title("ACC")
    root.geometry("1000x700") #set the dimension for root window [width -> 1000 pixels]
    
    # Image embed into the GUI for simulation with the help of Labels in tkinter
    image1 = Image.open(r"car1.png")
    image1 = image1.resize((64,64))
    image1 = ImageTk.PhotoImage(image1)
    label1=tk.Label(image=image1,name='car1')
    label1.place(x=0,y=200)
    
    
    #CAR_2
    image2 = Image.open(r"car2.png")
    image2 = image2.resize((64, 64))
    image2 = ImageTk.PhotoImage(image2)
    label2=tk.Label(image=image2,name='car2')
    label2.place(x=0,y=300)
    
    #CAR_3
    image3 = Image.open(r"car3.png")
    image3 = image3.resize((64, 64))
    image3 = ImageTk.PhotoImage(image3)
    label3=tk.Label(image=image3,name='car3')
    label3.place(x=0,y=400)
    
    # CAR1- ACC installed ; CAR2 & CAR3 - User defined [Spin box is use to select the vehicle to move before and after the ACC vehicle using Arrow Keys in Keyboard]
    l = Label(root, text = "Car")
    l.config(font =("Courier", 14))
    #l.pack()
    l.grid(column=0,row=0)
    # Combobox creation 
    n = tk.StringVar() 
    
    carchosen = ttk.Combobox(root, width = 27, textvariable = n,name="carlist") 
  
    # Adding combobox drop down list 
    carchosen['values'] = (  'Car1',
                              'Car2', 
                              'Car3' 
                              ) 
  
 
    carchosen.current(1)
    #carchoosen.pack()
    carchosen.grid(column=1,row=0)
    l2= Label(root, text="Speed")
    
    l2.config(font =("Courier", 14))
    #l2.pack()
    l2.grid(column=0,row=1)
    # Creating a Spinbox
    spinbox = tk.Spinbox(root, from_=0, to=200, width=10, relief="sunken", repeatdelay=500, repeatinterval=100,
                     font=("Courier", 12), bg="lightgrey", fg="blue", command=on_spinbox_change,name="speedinput")
    #spinbox.pack()
    spinbox.grid(column=1,row=1)
    root.bind("<Up>",move_up)

    root.bind("<Down>",move_down)

    root.bind("<Left>",move_left)

    root.bind("<Right>",move_right)
    root.focus_set()
    root.bind("<1>", lambda event: root.focus_set())
    
    moveperiodic()
    root.mainloop()

# CAR animation happens periodically for every 250ms    
# X = 0 to 1000 pixels ; y= 0 to 700 pixels
def moveperiodic():
    global label1
    global label2
    global label3
    global car1_xcalib
    global car2_xcalib 
    global car3_xcalib 
    global car2_speed
    global car3_speed
    label1.place(x=(label1.winfo_x()+round(car1_xcalib))%1000,y=label1.winfo_y())
    label2.place(x=(label2.winfo_x()+round(car2_xcalib))%1000,y=label2.winfo_y())
    label3.place(x=(label3.winfo_x()+round(car3_xcalib))%1000,y=label3.winfo_y())
    # Forward object detection to avoid collision
    k=find_widget(label1.winfo_x(),label1.winfo_y(),label1.winfo_name())
    # To check ACC is active or not, if ACC =Active:
    if ACC_Info.data[1] & 0x07 == 3:
        if k!=None:
            print(k)
            match k.winfo_name():
                case "car2":
                    # When car2_Speed is < 40 KMPH set ACC to STANDBY
                    if car2_speed <40:
                        ACC_Info.data[1]=ACC_Info.data[1] & 0x88 #1000 1000
                        ACC_Info.data[1]=ACC_Info.data[1] | 0x42 #1000 1000 + 0100 0010
                    else:
                        ACC_Info.data[1]= ACC_Info.data[1] & 0xF7
                        ACC_Info.data[1]= ACC_Info.data[1] | 0x8
                        ACC_Info.data[0]=car2_speed
                case "car3":
                    # When car3_Speed is < 40 KMPH set ACC to STANDBY
                    if car3_speed <40:
                        ACC_Info.data[1]=ACC_Info.data[1] & 0x88 #1000 1000
                        ACC_Info.data[1]=ACC_Info.data[1] | 0x42 #1000 1000 + 0100 0010
                    else:
                        ACC_Info.data[1]= ACC_Info.data[1] & 0xF7
                        ACC_Info.data[1]= ACC_Info.data[1] | 0x8
                        ACC_Info.data[0]=car3_speed
                    
        # If forward object is not there in ACC Equipped Vehicle
        # Set the Target_speed that are read from the memory as set speed of the vehicle and to release the brake
        else:
            fp=open("ACCMem.txt","r")
            txt=fp.read()
            data=json.loads(txt)
            ACC_Info.data[0]=int(data["SetSpeed"])
            ACC_Info.data[1]= ACC_Info.data[1] & 0xF7
            
    threading.Timer(0.25,moveperiodic).start()
    
    
def callback(ch, method, properties, body):
    global vs 
    global timegap
    global bsw1
    global bsw2
    global ign_st
    global car1_xcalib  
    
    # converts the bytes received from ICM, BCM & ECM Module into string
    s=str(body, encoding='utf-8')
    msg=bus.strToMessage(s) #Converts the string to message
    # Look for arbitration_id match
    match msg.arbitration_id:
        case 0x123: # Least 3 bits contains the info about the crusie switch status [7 states] from ICM module
            csr=msg.data[0]&0x7 #To get the least 3 bits to know the status of cruise_SW
            #print(csr)
            # To capture the BSW1 status:
            bsw1=(msg.data[0] & 0x8) >>3 # msg.data[0] & 0x8 -> It gives the bit 4 value of msg.data[] & >>3 will move the bit value 3 position to the right
            match csr:
                case 0:  # OFF
                   ACC_Info.data[1]=ACC_Info.data[1] & 0x88 #1000 1000
                   
                case 1:  # ON 
                    ACC_Info.data[1]=ACC_Info.data[1] & 0x88 #1000 1000
                    ACC_Info.data[1]=ACC_Info.data[1] | 0x22 #1000 1000 + 0010 0010
                
                # ACC state transitions based on cruise switch status
                # Acc off -> Press On[ACC ON] Acc Standby -> Press SET -> ACC Active [Speed Control, Time gap control]
                # Acc Active -> Press off [ACC OFF] -> ACC off
                # ACC Active -> Press [BSW1 /BWS2] Acc Standby -> Acc off
                
                case 2:  # SET -> [Acc off -> Press On[ACC ON] Acc Standby -> Press SET -> ACC Active [Speed Control, Time gap control]]
                    # The condition for ACC is in ACTIVE -> Current_ACC_STATE= STANDBY and Ign_st=Run and BSW1=0 and BSW2=0 and vs>=40 km/hr
                    if ACC_Info.data[1] & 0x7 ==0x2 and ign_st==2 and bsw1==0 and bsw2==0 and vs>=40:  # It check whether the Least three bit is equal to set
                        ACC_Info.data[1]=ACC_Info.data[1] & 0x88 #1000 1000
                        ACC_Info.data[1]=ACC_Info.data[1] | 0x33 #1000 1000 + 0011 0011
                        # To write the vehicle speed in the hard disk when ACC is in STANDBY
                        fp=open("ACCMem.txt","w")
                        fp.write("{"+f"\"SetSpeed\":{vs}"+"}")
                        fp.close()
                        # Copy the vehicle speed into the targetspeed when ACC is in STANDBY
                        ACC_Info.data[0]=vs
                    # This helps to increase the Target_speed of the vehicle by 2 km/hr for each press of SET Button when ACC is in ACTIVE state
                    elif ACC_Info.data[1] & 0x7 ==0x3:
                        ACC_Info.data[0]=ACC_Info.data[0]+2
                    
                case 3:  # COAST -> It helps to de-acclerate the vehicle by 2km/hr when ACC is ACTIVE state only for each press
                # It doesn't have any value when the ACC state is standby & off
                    if ACC_Info.data[1] & 0x7 ==0x3:
                        ACC_Info.data[0]=ACC_Info.data[0]-2
                    
                case 4:  # RESUME -> It helps to copy the set speed from the memory to set the target speed when the bsw1 is pressed and To resume the ACC operation where it stops due to emergency 
                    if ACC_Info.data[1] & 0x7 ==0x2: # To check whether ACC is in STANDBY
                        ACC_Info.data[1]=ACC_Info.data[1] & 0x88 # 1000 1000
                        ACC_Info.data[1]=ACC_Info.data[1] | 0x33
                        fp=open("ACCMem.txt","r")
                        txt=fp.read()
                        #To convert the data read as string into dictionary it can achieved with the help of JSON library
                        data=json.loads(txt) # text to dictionary
                        #copy the set speed from the memory to set the target speed
                        ACC_Info.data[0]=int(data["SetSpeed"])
                    
                # It will increase the distance by xx meters when the ACC is in active state only    
                case 5:  # Time Gap +
                    if ACC_Info.data[1] &0x7==0x3:
                        timegap+=1
                        ACC_Info.data[2]=timegap
                        
                # It will decrease the distance by xx meters when the ACC is in active state only        
                case 6:  # Time Gap -
                    if ACC_Info.data[1] &0x7==0x3:
                        timegap-=1
                        ACC_Info.data[2]=timegap
                    
            
            # It is an independent condition [Bsw1-> pressed & ACC--> Active]
            if bsw1==1 and ACC_Info.data[1] & 0x7 ==0x3:
                ACC_Info.data[1]=ACC_Info.data[1] & 0x88 #1000 1000
                ACC_Info.data[1]=ACC_Info.data[1] | 0x22 #1000 1000 + 0010 0010
        
        case 0x110:
            vs=int(msg.data[0])
            # CAR_1 Animation Factor
            # Car1 calibration: where -> 3.6- In seconds [vs[km/hr -> m/s]] , 5- window size in kilo- meters, 0.25- refreshing rate [For every 250 milli seconds]
            car1_xcalib=(float(vs)/(3.6*5*0.25))
            
        case 0x180: # To get the status of BSW2 from ECM module when the ACC is active condition only [Bsw2-> pressed & ACC--> Active]
            # Ignition status check: 
            ign_st=msg.data[0] & 0x03
            if ign_st <2 :
                ACC_Info.data[1]=ACC_Info.data[1] & 0x88 #1000 1000 # if ign_st < switch ACC state to off
                
            # BSW2 status check:    
            bsw2=(msg.data[0] & 0x04) >>2
            if ACC_Info.data[1] &0x7==0x3 and bsw2==1:
                ACC_Info.data[1]=ACC_Info.data[1] & 0x88 #1000 1000
                ACC_Info.data[1]=ACC_Info.data[1] | 0x22 #1000 1000 + 0010 0010 
                
                
    return

# Main thread starts here:
with can.Bus() as bus:
   
    try:
        bus.send_periodic(ACC_Info,0.100) #100ms packet is tx periodically
        print(f"Message Sent on {bus.channel_info}")
    except can.CanError:
        print("Message is not sent")
    # Seperate thread used inside main thread
    threading.Thread(target=ACC_GUI).start() # with the help of thread concept i run a ACC_GUI() to generate the GUI.   
    bus.recv(callback) # This function will wait infinite time to receive packets from other modules. if it receive packets it will go to the callback routine
    
            