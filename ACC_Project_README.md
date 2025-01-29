# Adaptive Cruise Control (ACC) Project

This repository contains the implementation of the **Adaptive Cruise Control (ACC)** application, a critical feature of Advanced Driver Assistance Systems (ADAS). The project was developed using **CANoe** and **CAPL** to simulate and test the ACC functionality.

---

## 📁 Folder Structure

- **Bitmap_Files**: Contains image assets or UI bitmaps used in CANoe panels or visualizations.
- **CANoe_Configuration**: Includes CANoe project files and configurations for simulating ACC.
- **CAPEL_Files**: Contains CAPL scripts used for CAN message handling and ACC logic implementation.
- **Database**: Stores the CAN database file (*.dbc) defining messages and signals for CAN communication.
- **Output**: Holds simulation results, logs, or any generated outputs.
- **Panel**: Contains custom CANoe panels for user interaction and visualization of ACC operations.
- **Reference_Paper**: Includes research or documentation references used during project development.

---

## 🚗 Project Overview
The Adaptive Cruise Control system is designed to maintain a safe distance from the vehicle ahead by automatically adjusting the speed of the vehicle. This project simulates the ACC system using CANoe and CAPL to handle the following tasks:

- Real-time vehicle speed regulation.
- Maintaining a safe distance from the lead vehicle.
- Responding to sudden changes in lead vehicle speed.
- Integrating CAN communication for data exchange between ECUs.

---

## 🛠 Tools & Technologies

- **CANoe**: Used for network simulation, testing, and visualization.
- **CAPL**: Used for scripting and implementing control logic.
- **CAN Database (DBC)**: Defines CAN messages and signals for communication.

---

## 🚀 Getting Started

1. Clone this repository to your local system:
   ```bash
   git clone https://github.com/gopikbv/ADAS
   ```

2. Open the **CANoe_Configuration** folder and load the CANoe project file.

3. Ensure the CAN database file in the **Database** folder is linked to the project.

4. Open the **CAPEL_Files** folder and review the CAPL scripts for logic implementation.

5. Run the simulation in CANoe and observe the ACC behavior through custom panels in the **Panel** folder.

---

## 📜 Reference
Refer to the materials in the **Reference_Paper** folder for additional insights and background information.

---

## 📊 Outputs
Simulation results, logs, and other outputs can be found in the **Output** folder.

---

## 🌟 Features

- Adaptive speed regulation based on lead vehicle detection.
- Real-time CAN communication handling.
- User-friendly visualizations through custom panels.

---

## 🤝 Contributions
Feel free to fork this repository and make contributions to enhance the project!

---

## 📧 Contact
For any queries, reach out via gopinathmpt@gmail.com.

