import can
import threading
from tkinter import *
from tkinter import ttk
from can import *
import can.bus as bus
import time
from tkinter import N,W,S,E

global table
global abstime
global contextmenu
global displaymode
global timemode
global msgdic
msgdic={}
displaymode="Fixed"
timemode="abs"
def callback(ch, method, properties, body):
    global table
    global abstime
    s=str(body, encoding='utf-8')
    k=bus.strToMessage(s)
    d=""
    
    
        
    for index in range(0,k.dlc):
        d=d+f"{k.data[index]:02}"+" "
        
    
            
    match displaymode:
        case "Fixed":
            found=False
            for line in table.get_children():
               
                if k.arbitration_id ==int(table.item(line)['values'][1],0):
                    found=True     
                    table.focus()
                    table.item(line,values=(
                        "{:010.5f}".format((k.timestamp-abstime) if timemode=="abs" else (k.timestamp-float(msgdic[k.arbitration_id]))),
                        str(hex(k.arbitration_id)),
                        
                        "X" if k.is_extended_id else "S","Rx" if k.is_rx else "Tx",str(k.dlc),d))
            if found==False:    
               table.insert(parent='',index=0,values=(
                   "{:010.5f}".format(k.timestamp-abstime if timemode=="abs" else (k.timestamp-float(msgdic[k.arbitration_id])))
                   ,str(hex(k.arbitration_id)),"X" if k.is_extended_id else "S","Rx" if k.is_rx else "Tx",str(k.dlc),d))            
        case "Chrono":
             
               table.insert(parent='',index=0,values=(
                   "{:010.5f}".format(k.timestamp-abstime if timemode=="abs" else (k.timestamp-float(msgdic[k.arbitration_id]))),
                   
                   str(hex(k.arbitration_id)),"X" if k.is_extended_id else "S","Rx" if k.is_rx else "Tx",str(k.dlc),d))            
            
    msgdic.update({k.arbitration_id:k.timestamp})   
    
    


def abs_trace():
    global timemode
    timemode="abs"
    return
def rel_trace():
    global timemode
    timemode="rel"
    return
def fixed_mode():
    global table
    for item in table.get_children():
      table.delete(item)
    global displaymode
    displaymode="Fixed"
    return
def chrono_mode():
    global displaymode
    displaymode="Chrono"
    return
def showcontextmenu(event):
    global contextmenu
    contextmenu.tk_popup(event.x_root,event.y_root)
def TraceGUI():
    global table
    global contextmenu
    # Create an instance of tkinter frame
    root = Tk()
    root.title("Bus Traffic")
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    # Set the size of the tkinter window
    root.geometry("700x350")
    
    table=ttk.Treeview(root,columns=("TimeStamp","ID","Type","Direction","Dlc","Data"),show="headings",selectmode="extended")
    for cl in range (0,6):
        table.column(cl,minwidth=100,anchor='c',stretch=False)
    table.grid(row=0,column=0,sticky = N+E+S+W)
    table.columnconfigure(1,weight=1)
    table.rowconfigure(1,weight=1)
    #table.pack(fill='both',expand=True)
    table.heading('TimeStamp',text='Time Stamp')
    table.heading('ID',text='ID')
    table.heading('Type',text='Type')
    table.heading('Direction',text='Direction')
    table.heading('Dlc',text='DLC')
    table.heading('Data',text='Data')
    
    vs=ttk.Scrollbar(root,orient="vertical",command=table.yview)
    table.configure(yscrollcommand=vs.set)
    vs.grid(row=0,column=1,sticky='ns')
    hs=ttk.Scrollbar(root,orient="horizontal",command=table.xview)
    table.configure(xscrollcommand=hs.set)
    hs.grid(row=1,column=0,sticky='ew')
    contextmenu=Menu(root,tearoff=0)
    
    contextmenu.add_command(label='Absolute',command=abs_trace)
    contextmenu.add_command(label='Relative',command=rel_trace)
    contextmenu.add_separator()
    contextmenu.add_command(label='Fixed',command=fixed_mode)
    contextmenu.add_command(label='chronological',command=chrono_mode)
    table.bind("<Button-3>",showcontextmenu)
    root.mainloop()
    
    
with can.Bus() as bus:
    threading.Thread(target=TraceGUI).start()
    abstime=time.time()
    bus.recv(callback)