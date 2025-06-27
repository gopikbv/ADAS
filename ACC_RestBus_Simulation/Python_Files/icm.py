# Instrument Cluster will send 2 CAN signal to ACC namely a).Cruise Switch Request b).Brake Switch 1 Status
# Default value of the Cruise Switch Request is 7 --> No button pressed
import can
from can import *
from tkinter import * #tkinter library used to Create GUI to adjust the CAN signals used in the respective Modules
from tkinter import ttk
import threading
from PIL import ImageTk, Image, ImageDraw
import math

#data[0]= xxxx xxxx --> 0000 0111 --> cruiseSwitch_status default value =7 
#data[0]-bit 3-> Brake Switch 1 Status
ICM_Info=can.Message(arbitration_id=0x123,data=[7],is_extended_id=False) #CAN packet creation

# Reason to use the same variable as global inside all the function call:
# The variable are used across different threads so the variable becomes local to the specific thread, In order to make their 
# visibility across all the threads the same variable is defined global everywhere in the program.

#global variables to draw needle in the Meter image:
global x
global y
global endx
global endy
global line_id #TO captures the no of times the line has drawn
line_id=0
global vs_prev #TO captures the previous vehicle speed
vs_prev=0
global frame
frame=0
# The co-ordinates are obtain from the paint tool. By open the image and place the cursor over the place where
#I wish to draw the needle
x=560
y=260

global cs_img
cs_img=0

#ACC state Capture:  #ACC Module is created on 25/5/25 --> Module 14 Lecture
global accstate
accstate=0

#To write the Acc state text into the ICM:
global txt_id
txt_id=0

# Implented on 23/5/25 - To capture the button state 
def onoff_btn_pressed(state): #on/off button
    global accstate
    if accstate==0: 
        ICM_Info.data[0]=ICM_Info.data[0] & 0xF8        #1111 1000 ---> clear last 3 bits
        ICM_Info.data[0]=ICM_Info.data[0] | 0x01         #xxxx x001 ----> set to 1 (ON/OFF pressed)
    else:
        ICM_Info.data[0]=ICM_Info.data[0] & 0xF8        #0000 0000 ----> Set to 0 
    
    #print("ACC state → accstate =", accstate)
    #print("ON/OFF Pressed → ICM_Info.data[0] =", ICM_Info.data[0])

def set_btn_pressed(state): #set button
    ICM_Info.data[0]=ICM_Info.data[0] & 0xF8        #1111 1000 ---> clear last 3 bits
    ICM_Info.data[0]=ICM_Info.data[0] | 0x02        #xxxx x010 ----> set to 2 (set pressed)

def coast_btn_pressed(state): #coast button
    ICM_Info.data[0]=ICM_Info.data[0] & 0xF8        #1111 1000 ---> clear last 3 bits
    ICM_Info.data[0]=ICM_Info.data[0] | 0x03        #xxxx x011 ----> set to 3 (Coast pressed) 

def resume_btn_pressed(state): #resume button
    ICM_Info.data[0]=ICM_Info.data[0] & 0xF8        #1111 1000 ---> clear last 3 bits
    ICM_Info.data[0]=ICM_Info.data[0] | 0x04        #xxxx x100 ----> set to 4 (resume pressed)    

def timegapPlus_btn_pressed(state): #tg+ button
    ICM_Info.data[0]=ICM_Info.data[0] & 0xF8        #1111 1000 ---> clear last 3 bits
    ICM_Info.data[0]=ICM_Info.data[0] | 0x05        #xxxx x101 ----> set to 5 (tg+ pressed)        
    
def timegapMinus_btn_pressed(state): #tg- button
    ICM_Info.data[0]=ICM_Info.data[0] & 0xF8        #1111 1000 ---> clear last 3 bits
    ICM_Info.data[0]=ICM_Info.data[0] | 0x06        #xxxx x110 ----> set to 6 (tg- pressed)    
    
        
#To capture the state of the button when it is not pressed:
def btn_released(state):
    ICM_Info.data[0]=ICM_Info.data[0] & 0xF8            #1111 1000
    ICM_Info.data[0]=ICM_Info.data[0] | 0x7             #0000 0111  # set to 7 (released state)
    
    #print("ACC state → accstate =", accstate)
    #print("Button Released → ICM_Info.data[0] =", ICM_Info.data[0])
    
# To capture the BSW1 Status
def bsw1_pressed(state):
    ICM_Info.data[0]=ICM_Info.data[0] & 0xF7     
    ICM_Info.data[0]=ICM_Info.data[0] | 0x8  
        
def bsw1_released(state):
    ICM_Info.data[0]=ICM_Info.data[0] & 0xF7           
        
# Implented on 23/5/25 - Module 13
# The CruiseSwitches is the subwindow of the root window, the screen is appeared based on the CB button is pressed in the main window
# In the subwindow the cruise switch image is drawn and the button is kept into the respective postions
def CruiseSwitches():
    global cs_img
    cs=Toplevel()
    cs.title('Cruise Switches')
    cs.config(width=500, height=370) # set the dimension for sub window
    frame2=Canvas(cs,width=500,height=370) #canvas helps to embed the Cruise_Switch image into the widget
    frame2.pack()
    frame2.create_image(0,0,anchor=NW,image=cs_img) # NW- North west [Top left position in the subwindow] & 0,0 --> x & y co-ordinates
    # Cruise Button Creation:
    
    # ON/OFF
    onoff_btn=ttk.Button(cs,text="ON/OFF")
    onoff_btn.pack()   # pack() helps to place the button in the subwindow 
    onoff_btn.place(x=205,y=70) # place helps to place the button in (250-->x axis,70--> y -axis) the subwindow 
    onoff_btn.bind("<ButtonPress-1>",onoff_btn_pressed,add="+")
    onoff_btn.bind("<ButtonRelease-1>",btn_released,add="+")
    
    
    #Coast Button
    coast_btn=ttk.Button(cs,text="Coast")
    coast_btn.pack()
    coast_btn.place(x=115,y=60)
    coast_btn.bind("<ButtonPress-1>",coast_btn_pressed,add="+")
    coast_btn.bind("<ButtonRelease-1>",btn_released,add="+")
    
    #set Button
    set_btn=ttk.Button(cs,text="Set")
    set_btn.pack()
    set_btn.place(x=180,y=205)
    set_btn.bind("<ButtonPress-1>",set_btn_pressed,add="+")
    set_btn.bind("<ButtonRelease-1>",btn_released,add="+")
    
    # TimeGap+
    timegapPlus_btn=ttk.Button(cs,text="TimeGap+")
    timegapPlus_btn.pack()   
    timegapPlus_btn.place(x=290,y=210) 
    timegapPlus_btn.bind("<ButtonPress-1>",timegapPlus_btn_pressed,add="+")
    timegapPlus_btn.bind("<ButtonRelease-1>",btn_released,add="+")
    
    #TimeGap -
    timegapMinus_btn=ttk.Button(cs,text="TimeGap-")
    timegapMinus_btn.pack()
    timegapMinus_btn.place(x=245,y=140)
    timegapMinus_btn.bind("<ButtonPress-1>",timegapMinus_btn_pressed,add="+")
    timegapMinus_btn.bind("<ButtonRelease-1>",btn_released,add="+")
    
    #Resume
    resume_btn=ttk.Button(cs,text="Resume")
    resume_btn.pack()
    resume_btn.place(x=140,y=145)
    resume_btn.bind("<ButtonPress-1>",resume_btn_pressed,add="+")
    resume_btn.bind("<ButtonRelease-1>",btn_released,add="+")
    
    return
    
    
# ICM GUI Creation: 
# Tkinter : CanvasFrame -> PictureBox -> Image Draw (It will create an object while the simulation triggers )
# Root window -> a). Main window always wait for the user input or threads to begin the action
#                b). It hold only controls like track_bar,text boxes, buttons & it won't hold pictures
# Image drawn -> Took image from net-> with the help of CANVAS the image is drawn in the main or root window
def ICM_GUI():
    global x
    global y
    global endx
    global endy
    global frame
    global line_id
    global cs_img
    root=Tk() # ICM GUI Window creation
    root.title("ICM")
    root.geometry("700x600") #set the dimension for root window
    frame=Canvas(root,width=700,height=600) #canvas helps to embed the image into the widget
    frame.pack()
    img=Image.open('meter.png')
    img=ImageTk.PhotoImage(img)
    frame.create_image(20,20,anchor=NW,image=img)
    # 115- It points the needle length from the center of the image to the zero position in the meter
    
    # Radians of 270 is the angle of the end point to draw
    endx=x+115*math.cos(math.radians(87))
    endy=y+115*math.sin(math.radians(87))
    
    # To draw a line from x,y(starting point) & end_x, end_y (end point)
    line_id=frame.create_line(x,y,endx,endy,fill='Red',arrow='last',smooth=True,width=5)
    frame.create_oval(x-20,y-20,x+20,y+20,fill='Red') # To draw circle in the middle
    frame.create_oval(x-10,y-10,x+10,y+10,fill='Gray')
    
    # Button create To open cruise switch GUI 
    button_open=ttk.Button(root,text='CB',command=CruiseSwitches)
    button_open.place(x=600 ,y=550)
    # Images used in Main or sub window should be loaded from main thread otherwise it won't work
    # sub window image cruise_sw is loaded from the main thread
    cs_img=Image.open('csw.png')  # img is a pointer created in RAM to store the image in binary form into the Permanent memory (Hard disk)
    cs_img=ImageTk.PhotoImage(cs_img) # The PhotoImage() helps to convert the image that is compatible to the TK library
    
    # Button created for BSW1-> Break Switch1
    # Implemented on 31/5/25 Module 14
    csw1=ttk.Button(root,text='BSW1')
    csw1.place(x=600 ,y=500)
    csw1.bind("<ButtonPress-1>",bsw1_pressed,add="+")
    csw1.bind("<ButtonRelease-1>",bsw1_released,add="+")
    cs_img=Image.open('csw.png')
    cs_img=ImageTk.PhotoImage(cs_img)
    
    
    
    root.mainloop()
    
    
def callback(ch, method, properties, body):
    global x
    global y
    global endx
    global endy
    global frame
    global line_id
    global vs_prev
    global accstate
    global txt_id
    # converts the bytes received from bcm vehicle speed into string
    s=str(body, encoding='utf-8')
    msg=bus.strToMessage(s)
    #Look for arbitration_id match
    match msg.arbitration_id:
        case 0x110: # To draw a line whenever the callback is triggered which is captured from bcm module
            vs=int(msg.data[0])
            if vs != vs_prev: # To check any change in the vehicle speed in order to calculate the angle, end point and draw the line
                frame.delete(line_id) # delete the line that already drawn in the image
                
                # To calculate slope in straight line y=mx+c
                angle=(1.33*vs)+87 #starting point
                
                # End points
                endx=x+115*math.cos(math.radians(angle)) 
                endy=y+115*math.sin(math.radians(angle))
                
                #To draw new line 
                line_id=frame.create_line(x,y,endx,endy,fill='Red',arrow='last',smooth=True,width=5)
                frame.create_oval(x-20,y-20,x+20,y+20,fill='Red') # To draw circle in the middle
                frame.create_oval(x-10,y-10,x+10,y+10,fill='Gray')
                
                #After calculation the current speed becomes previous 
                vs_prev=vs
        
        case 0x456: # To capture the ACC state,Acc Driver information message
            accstate=int(msg.data[1] & 0x7)   #It will extract the least three bit from the bytes received
            accdrinfo=int(msg.data[1]>>4)     # It will get the acc driver info i/f from bit 4 to bit 6 and it moves to LSB because of the Right shift
            match accdrinfo:
                case 0:
                    if txt_id:
                        frame.delete(txt_id)
                    txt_id=frame.create_text(350,250,text="ACC Off",fill="#77FF63",font=('Arial 15 bold'))
                case 1:
                    if txt_id:
                        frame.delete(txt_id)
                    txt_id=frame.create_text(350,250,text="ACC ON",fill="#77FF63",font=('Arial 15 bold'))
                case 2:
                    if txt_id:
                        frame.delete(txt_id)
                    txt_id=frame.create_text(350,250,text="ACC standby",fill="#77FF63",font=('Arial 15 bold'))
                case 3:
                    if txt_id:
                        frame.delete(txt_id)
                    txt_id=frame.create_text(350,250,text="ACC Active",fill="#77FF63",font=('Arial 15 bold'))
                    
                case 4:
                    if txt_id:
                        frame.delete(txt_id)
                    txt_id=frame.create_text(350,250,text="Driver\nIntervention\nRequired",fill="#77FF63",font=('Arial 15 bold'))
            
            
            
            
            
            
    return

# Main thread starts here:
with can.Bus() as bus:
   
    try:
        bus.send_periodic(ICM_Info,0.150) #150ms packet is tx periodically
        print(f"Message Sent on {bus.channel_info}")
    except can.CanError:
        print("Message is not sent")
    # Seperate thread used inside main thread
    threading.Thread(target=ICM_GUI).start() # with the help of thread concept i run a ICM_GUI() to generate the GUI.   
    bus.recv(callback) # This function will wait infinite time to receive packets from other modules. if it receive packets it will go to the callback routine
    #while True:
        #pass
            