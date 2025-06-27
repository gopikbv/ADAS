# 🚗 Rest Bus Simulation for Adaptive Cruise Control (ACC)

This project implements a **Rest Bus Simulation** for the **Adaptive Cruise Control (ACC)** feature of ADAS (Advanced Driver Assistance Systems) using **Python**, **Tkinter**, and **RabbitMQ**.

ACC is a crucial driver-assistance function that automatically adjusts vehicle speed to maintain a safe distance from vehicles ahead. This simulation tests software logic and inter-ECU communication without needing actual CAN hardware.

---

## 🔧 Tech Stack

- **Programming Language**: Python  
- **GUI**: Tkinter  
- **Messaging Protocol**: RabbitMQ (used instead of CAN bus)  
- **Concurrency**: Python Threads for simulating ECU behavior  
- **Sensor Simulation**: Lane monitoring using Tkinter Label widget

---

## 📊 System Architecture

The system mimics the interactions between the following ECUs:

- **ACC Module**
- **Brake Control Module**
- **Engine Control Module**
- **Lane Vision Module** *(Tkinter Label simulates forward/stationary vehicle detection)*
- **Instrument Cluster**
- **Cruise Switches**

All ECUs exchange messages over a **RabbitMQ-based virtual network**, simulating a Rest Bus communication environment.

---

## 🧠 Functional Scenarios Simulated

- Initialization via ignition key states (OFF → ACC → RUN)
- State transitions between: ACC OFF → STANDBY → ACTIVE
- Vehicle detection using Tkinter-based **Lane Vision Module**
- Forward/stationary vehicle simulation using Label widgets
- ACC responds to Time Gap changes, driver brake intervention, and low-speed scenarios
- GUI feedback on ACC status and cruise control switches

---

## 🖼️ GUI Features (Tkinter)

- Simulated **lane with moving/standstill vehicles** using label widgets
- Visual speed, time gap, and ACC status display
- Simulated Cruise Switch panel (Set+, Resume, Cancel, Gap+, Gap-)

---

## 📋 ACC Activation Conditions

- Ignition = RUN  
- ACC state = STANDBY  
- Vehicle speed ≥ 25 mph  
- Brake not pressed  
- Lead vehicle present in lane



## 🚀 How to Run the Simulation

### Prerequisites:
- Python 3.x
- RabbitMQ Server installed & running locally
- Install Python dependencies:
```bash
pip install pika


# Start ECU modules
python acc_module.py
python brake_control_module.py
python engine_control_module.py
python instrument_cluster.py


✅ Output
GUI displays lane activity and ACC state

Vehicle behavior simulated using Label widget

Live RabbitMQ message exchange between ECUs

Console logs show speed, gap, and control decisions

🏁 Future Scope
Add real CAN interface (SocketCAN or CANoe)

Extend to other ADAS features (AEB, LKA, etc.)

Replace Tkinter with PyQt or web-based UI

Add time-logging and playback functionality

👨‍💻 Author
Gopinath B
Battery Management Systems | ADAS | Embedded Software
🔗 LinkedIn

🪪 License
This project is licensed under the MIT License – free to use, modify, and distribute.