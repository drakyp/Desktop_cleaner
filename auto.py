import os 
import sys
import time
import logging
#from watchdog.observers import Observer
#from watchdog.events import LoggingEventHandler


source_dir = "/Users/williamlam/Downloads"

# scan de current directory and give me back a list of all the files
with os.scandir(source_dir) as entries:
    #traverse the list and print the name of the files or directory 
    for entry in entries:
        print(entry.name)