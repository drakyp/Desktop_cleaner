import os 
from os.path import splitext, exists, join
import sys
import time
from shutil import move 
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

#definition of all the directory to class the downloading things 
source_dir = "/Users/williamlam/Downloads"
music_dir = "/Users/williamlam/Downloads/Music"
document_dir = "/Users/williamlam/Downloads/document"
image_dir = "/Users/williamlam/Downloads/Images"
video_dir = "/Users/williamlam/Downloads/Videos"


# definition of all the extensions that i can possibly use
image_extensions = [".jpeg", ".jpg", ".png"]
music_extensions = [".mp3", ".aac", ".mpa"]
video_extensions = [".mov" , ".avi", ".mp4", ".wmv"]
domcument_extensions = [".pdf", ".txt", ".doc", ".docx" , ".csv"]

#entry is the whole original path 
#name is the just the name of the file 


#this function have for purpose to create a unique filename if one already exists
def make_unique(path, name):
    #we split the filename and the extension
    filename, extension = splitext(name)
    #create a counter to add the number at the end of the file
    counter = 1
    #we continue while in the dest directory the filename is already present 
    while exists(f"{path}/{name}"):
        #create the new name
        name = f"{filename}({str(counter)}){extension}"
        #incrementing the counter 
        counter += 1
    return name




def move_file(dest, entry, name):
    #try to see if the file we want to put in the destination already exist
    if exists(join(dest,name)):
        # create a new name for the file 
        unique_name = make_unique(dest, name)
    else:
        unique_name = name
    #moving the file to it new destination
    move(entry, join(dest, unique_name))
    



class MoveHandler(LoggingEventHandler):
    #function that check if there is any modification 
    def on_modified(self, event):
       # scan de current directory and give me back a list of all the files
        with os.scandir(source_dir) as entries:
            #traverse the list and print the name of the files or directory 
            for entry in entries: 
                name = entry.name
                self.for_document(entry, name)
                self.for_image(entry, name)
                self.for_music(entry, name)
                self.for_video(entry, name)

    
    def for_image(self, entry, name):
        for im_ext in image_extensions:
            if name.endswith(im_ext) or name.endswith(im_ext.upper()):
                move_file(image_dir, entry, name)
                logging.info(f"Move image file :{name}")
    
    def for_document(self, entry, name):
        for doc_ext in domcument_extensions:
            if name.endswith(doc_ext) or name.endswith(doc_ext.upper()):
                move_file(document_dir, entry, name)
                logging.info(f"Move Document file :{name}")


    def for_video(self, entry, name):
        for vid_ext in video_extensions:
            if name.endswith(vid_ext) or name.endswith(vid_ext.upper()):
                move_file(video_dir, entry, name)
                logging.info(f"Move video file :{name}") 

    
    def for_music(self, entry, name):
        for music_ext in music_extensions:
            if name.endswith(music_ext) or name.endswith(music_ext.upper()):
                move_file(music_dir, entry, name)
                logging.info(f"Move Music file :{name}")


         


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()