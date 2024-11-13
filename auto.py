import os 
from os.path import splitext, exists, join
import time
from shutil import move 
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

#definition of all the directory to class the downloading things
# assigment them as you want 
source_dir = ""
music_dir = ""
document_dir = ""
image_dir = ""
video_dir = ""


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
                #retrieve the name of the entry 
                name = entry.name
                #check for each function
                self.for_document(entry, name)
                self.for_image(entry, name)
                self.for_music(entry, name)
                self.for_video(entry, name)

    # for the image 
    def for_image(self, entry, name):
        #we simply traverse all the extension we store for the image 
        for im_ext in image_extensions:
            #check if the name end with one of the extension
            if name.endswith(im_ext) or name.endswith(im_ext.upper()):
                #first we try to create the directory if it doesn't exist
                try:
                    os.mkdir(image_dir)
                except:
                    print("Downloads folder exists")
                # moving the file if it correspond to one of the extension we have listed
                move_file(image_dir, entry, name)
                #print on the terminal
                logging.info(f"Move image file :{name}")
    
    # same as for the image just the extension will be for the document and the dest directory too 
    def for_document(self, entry, name):
        for doc_ext in domcument_extensions:
            if name.endswith(doc_ext) or name.endswith(doc_ext.upper()):
                try:
                    os.mkdir(document_dir)
                except:
                    print("Downloads folder exists")
                move_file(document_dir, entry, name)
                logging.info(f"Move Document file :{name}")


    # same as for the image just the extension will be for the video and the dest video too 
    def for_video(self, entry, name):
        for vid_ext in video_extensions:
            if name.endswith(vid_ext) or name.endswith(vid_ext.upper()):
                try:
                    os.mkdir(video_dir)
                except:
                    print("Downloads folder exists")
                move_file(video_dir, entry, name)
                logging.info(f"Move video file :{name}") 

    # same as for the image just the extension will be for the music and the dest music too 
    def for_music(self, entry, name):
        for music_ext in music_extensions:
            if name.endswith(music_ext) or name.endswith(music_ext.upper()):
                try:
                    os.mkdir(music_dir)
                except:
                    print("Downloads folder exists")
                move_file(music_dir, entry, name)
                logging.info(f"Move Music file :{name}")


         

#given function from the internet nothing to modify
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