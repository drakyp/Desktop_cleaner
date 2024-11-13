# Download Organizer for Downloads Folder

This project is designed to automatically organize files in the `Downloads` directory based on file type, moving each file to its appropriate subdirectory (e.g., `Music`, `Documents`, `Images`, and `Videos`). It leverages Python’s `watchdog` library to monitor file system changes, making it efficient and real-time.

## Project Overview
The project operates by continuously watching the `Downloads` folder for changes, then moving files based on predefined extensions. It can create unique filenames to prevent overwriting files in the target folders.

### Main Components

1. **Directory and Extension Setup**:
   - Defines specific folders within `Downloads` for each file type (e.g., `Music`, `Documents`).
   - Lists of file extensions for each file type are used to determine where each file should be moved.

2. **File Moving and Duplicate Handling**:
   - Uses a helper function `move_file()` to move files.
   - If a file with the same name already exists in the destination, the `make_unique()` function generates a unique name for the new file.

3. **Real-Time Monitoring**:
   - A `MoveHandler` class inherits from `LoggingEventHandler` to listen for modifications in the `Downloads` directory. When files are added or modified, the handler organizes them based on their extensions.

### Libraries to Install
To run this project, you need the following libraries:

- `watchdog`: For real-time monitoring of the `Downloads` folder.
  ```bash
  pip install watchdog
  ```
- `logging`: For logging operations and updates in the terminal (part of Python’s standard library).


#### Extensions Lists
File type extensions are specified to categorize each file type:

```python
image_extensions = [".jpeg", ".jpg", ".png"]
music_extensions = [".mp3", ".aac", ".mpa"]
video_extensions = [".mov", ".avi", ".mp4", ".wmv"]
document_extensions = [".pdf", ".txt", ".doc", ".docx", ".csv"]
```

#### Unique Filename Generator
The `make_unique()` function ensures that files with the same name are given unique filenames to avoid overwriting:

```python
def make_unique(path, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{path}/{name}"):
        name = f"{filename}({counter}){extension}"
        counter += 1
    return name
```

#### File Moving Function
The `move_file()` function handles moving files to their appropriate directories, using `make_unique()` if needed to avoid overwrites:

```python
def move_file(dest, entry, name):
    if exists(join(dest, name)):
        unique_name = make_unique(dest, name)
    else:
        unique_name = name
    move(entry, join(dest, unique_name))
```

#### File Monitoring and Organization
The `MoveHandler` class listens for modifications in the `Downloads` folder and moves files based on their extensions:

```python
class MoveHandler(LoggingEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.for_document(entry, name)
                self.for_image(entry, name)
                self.for_music(entry, name)
                self.for_video(entry, name)
```

Each file type has its own method to check for corresponding extensions and move files:

```python
def for_image(self, entry, name):
    for im_ext in image_extensions:
        if name.endswith(im_ext) or name.endswith(im_ext.upper()):
            move_file(image_dir, entry, name)
            logging.info(f"Moved image file: {name}")
```

### Running the Script

1. Install dependencies:
   ```bash
   pip install watchdog
   ```

2. Run the script:
   ```bash
   python organize_downloads.py
   ```

3. The script will keep running in the background to monitor the `Downloads` folder. To stop it, use `CTRL+C` in the terminal.

### Example Usage
- **File Added**: A new file, `photo.jpg`, is downloaded to `Downloads`.
- **Monitoring and Movement**: The script detects the file, checks its extension (`.jpg`), and moves it to the `Images` folder.
- **Duplicate Handling**: If `photo.jpg` already exists in `Images`, `make_unique()` renames the new file to `photo(1).jpg` before moving it.

### Notes
- **Customizable Paths and Extensions**: The directories and extensions can be modified as needed.
- **Error Handling**: Basic logging is included to monitor file movements and actions.

This script provides an efficient, real-time way to keep your `Downloads` folder organized and ensures files are correctly categorized without overwrites.