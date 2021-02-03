![scheme](images/logo.png)
# M2_CIML_Automated-image-capture  
## Project abstract
Applicant: Jérôme Belougne  
Institute: CIML  
Engineer: Mathias Lechelon  
Submission date: 15/07/2020  
Summary : <em>Optimize the automation of the image capture already present ( DMS300 / Workstation Tecan gemini).
The aim of the optimization will be to replace the currently used automaton with an X-Y automated platform system.
Create a plexiglass enclosure to control the environment (humidity, temperature) around the camera and the X-Y platform.
Optimize the imaging instrument, to obtain higher quality images.</em>
  
## How it works
This program aims to track worms (*C.Elegans*) in wells plates, placed inside a CNC router frame. The plates are fixed, and the camera move above/below (depending on the preferences) each well to take a picture. This is repeated n times.

## Command Line Interface (CLI), and how to use it
The file is refered as cli.py in the RaspberryPi folder.  
Steps:  
* Open the terminal (LXTerminal);  
* Change directory to go into the RaspberryPi folder, where the cli.py file is located.  
    ```cd Desktop/M2_CIML_Automated-image-capture/RaspberryPi/```
* To start the scan with default parameter (12 wells boxes, 30 min of delay, 48 hours long):
    ```python cli.py```
    Options:
    * ```--box``` to define the type of box (available options : 6, 12);
        * *Example to use 12 wells boxes: ```python cli.py --box 6```*
    * ```--delay``` to define the delay between each scan. With format hh:mm:ss.
        * *Example to set a 50 min delay: 00:50:00: ```python cli.py --delay 00:50:00```*
    * ```--duration``` to define the total duration of the experiment. With format hh:mm:ss.
        * *Example to set a 24 hours long experiment: ```python cli.py --duration 24:00:00```
    * *Example to set an experiment with 6 wells boxes, with 40 minutes delay, and a total duration of 36 hours: ```python cli.py --box 6 --delay 00:40:00 --duration 36:00:00```.
* Once you type *Enter* a resume of the selected parameters appears. You can type *y* (for yes) if you want to run the scan with the selected parameters. Or type *n* (for no) to abort the scan.
* To cancel a scan, hold *ctrl+c*.

## Electronics
![scheme](images/electronics.png)

## Yet to do
* ~~Placing the end stops on the frame, on each axis;~~
* ~~Defining the bottom left well as the zero position.~~
* ~~Move arg_def(from functions.py) into cli.py~~
* Write a small user guide for the cli into readme
* Update the scheme below with the current path
* Make a scheme for electronics
* ~~Add the config.h file with modification for grbl~~
![scheme](images/scheme.png)
