# Pi-Tracker

## Introduction
Pi-Eye is a smart surveillance web application built for the Raspberry Pi. 
The web application interface can be accessed from any web browser.
This project touches concepts from computer vision, deep learning, robotics, networking, and real-time data streaming.

## Hardware & Assembly
### Hardware Checklist
  * Raspberry Pi with Raspberry Pi OS installed 
  * Coral USB Accellerator
    * **Note:** This component is optional, but highly recommended as it significantly improves the object detection and frame rate
  * Mini Pan Tilt Kit with 2 Micro Servo Motors 
  * Camera Module for Raspberry Pi
### Assembling the Hardware
  1. Assemble Pan Tilt Hat Kit with camera module according to the instuctions included with the kit
  2. Attach the servo wires to the Raspberry Pi according to the diagram below:
    <img src="/static/img/servo-diagram.png" alt="Servo Diagram" width="50%"/>
  3. Attach the Camera Module ribbon connector cable to the Rasberry Pi.
  4. Plug the Coral USB Accellerator into an available Raspberry Pi USB port (optional but recommended for optimal performance)
  5. Plug the Raspberry Pi into a power source 

## Software Installation & Setup
### Configuring Port Forwarding
  * Port forwarding allows remote computers to connect to the Raspberry Pi that sits behind your private network
  * We need to set up port forwarding so that we can access the control panel from any computer
  * The Pi-Tracker web application runs on port **8000**.
  * Before you set up port forwarding you should have the following items:
    1. The Private IP address of your Raspberry Pi 
    2. The public IP address of your Router 
    3. The port number that the web application will run on (8000)
  * **Note:** The process of enabling port forwarding is different for every router and internet service provider. Research the correct steps for your specific internet provider. Google 'port forwarding flask applications'.
### SSH into the Raspberry Pi from your Laptop or Desktop Computer
  * Open your laptop or desktop terminal application
  * SSH into the Raspberry Pi: 
    * If you are on the same router as the Raspberry Pi:
      * Run `ssh pi@<raspberry-pi-IP-address>`
    * If you accessing the Raspberry Pi from a remote network:
      * Run `ssh pi@<public-IP-address>`
  * You will be prompted for the password of the Raspberry Pi. Enter it.
### Clone Pi-Tracker to your Raspberry Pi
  * In the Raspberry Pi terminal, run: `git clone https://github.com/lukerbs/pi-tracker.git`
### Installing Dependencies
  * cd into root project directory: `cd pi-tracker/`
  * Create and activate a virtual environment: `python3 -m venv venv && . venv/bin/activate`
  * Run `chmod +x setup.sh` to allow execution permissions on the setup script
  * Run `./setup.sh` to install all dependencies

## Running Pi-Tracker & Accessing the GUI
### Launch the Pi-Tracker Web Application on the Raspberry Pi
  * Run `python3 app.py` to start the Pi-Tracker web application
### Open the Web Application in Your Web Browser
  * If you are on the same router as the Raspberry Pi:
    * Go to your-raspberry-pi-IP-address:8000 in your web browser
  * If you accessing the Raspberry Pi from a remote network:
    * Go to your-public-IP-address:8000 in your web browser