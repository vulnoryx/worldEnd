import os
import time
from datetime import datetime
import sys
import getpass # for getting username
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# color definition
COLOR_RESET =   "\033[0m"
COLOR_WHITE =   "\033[0m"
COLOR_GRAY =    "\033[30m"
COLOR_RED =     "\033[31m"
COLOR_GREEN =   "\033[32m"
COLOR_YELLOW =  "\033[33m"
COLOR_BLUE =    "\033[34m"
COLOR_PURPLE =  "\033[35m"
COLOR_CYAN =    "\033[36m"

# path...ye...just path
path = ''

# folder definition
pictures_folder = 'Pictures'
documents_folder = 'Documents'
compressed_archives_folder = 'Archives'
sounds_and_music_folder = 'Sounds'
videos_folder = 'Videos'
executables_folder = 'Executables'
other_files_folder = 'Other'

# extentions definition
image_extentions =                ['.png', '.jpg', '.jpeg', '.jpg_large', '.webp', '.gif', '.tiff', '.psd', '.bmp', '.heif', '.indd', '.svg']
document_extentions =             ['.doc', '.docx', '.html', '.htm', '.odt', '.pdf', '.xls', '.xlsx', '.ods', '.ppt', '.pptx', '.txt', '.ppsx']
compressed_archive_extentions =   ['.zip', '.tar', '.xz', '.tgz', '.gz', '.rar', '.jar', '.iso', '.vsix']
sound_and_music_file_extentions = ['.m4a', '.flac', '.mp3', '.wav', '.wma', '.aac']
video_file_extentions =           ['.mp4', '.avi', '.webm', '.mkv', '.flv', '.vob', '.ogv', '.ogg', '.avi', '.mov']
executable_file_extentions =      ['.exe', '.bin', '.AppImage']

ignore_extentions =               ['.crdownload', '.part', '.download', '.tmp', '.filepart', '.opdownload', '.!ut', '.bc!', '.dwl', '.asd',
                                   '.wbk', '.swp', '.swo', '.lk', '.gz.tmp', '.log']

ignore_prefixes =                 ["Unconfirmed ", ".org.chromium.Chromium", "fileOverseer"]

def fileExtits(path):
    return os.path.isfile(path)

# moves a file to the "move_folder"
# if a file with the same name is found, the file will have a "_" at the end of its name to not override the already present file
def moveFile(currentTime, file_data, file_path, move_folder):
    moved = False
    currentTime = COLOR_YELLOW+currentTime+":"+COLOR_WHITE

    if fileExtits(path+move_folder+"/"+file_data[0]+file_data[1]):
        os.rename(file_path, path+move_folder+"/"+file_data[0]+"_"+file_data[1])
        moved = True
    else:
        os.rename(file_path, path+move_folder+"/"+file_data[0]+file_data[1])
        moved = True
    
    if moved:
        print(currentTime+" moving '"+COLOR_BLUE+"{}".format(file_data[0]+file_data[1])+COLOR_WHITE+"' to "+move_folder)
        logging.info("moved '"+file_data[0]+file_data[1]+"' to "+move_folder)

    return moved;

# checks if a folder exists. If not the folder will be created
def createFolder(path, folder_name):
    if not os.path.exists(path+folder_name):
        os.makedirs(path+folder_name)
        createdFolderTxt = "created "+folder_name+" folder";
        print(createdFolderTxt)
        logging.info(createdFolderTxt)

def checkDefaultDirectories(path):
    createFolder(path, pictures_folder)
    createFolder(path, documents_folder)
    createFolder(path, compressed_archives_folder)
    createFolder(path, sounds_and_music_folder)
    createFolder(path, videos_folder)
    createFolder(path, executables_folder)
    createFolder(path, other_files_folder)

def shouldIgnoreBasedOnPrefix(file_name):
    return (any(file_name.startswith(prefix) for prefix in ignore_prefixes))

def moveBasedOnExtention(currentTime, file_path, move_folder, extention_list):
    file_data = os.path.splitext(os.path.basename(file_path))

    for extention in extention_list:
        if file_data[1] == extention:
            if moveFile(currentTime, file_data, file_path, move_folder):
                return True
    
    return False

def moveIgnoringExtention(currentTime, file_path, move_folder, extention_list):
    file_data = os.path.splitext(os.path.basename(file_path))
    shouldMoveFile = True
    
    # check extentions
    for extention in extention_list:
        if file_data[1] == extention:
            shouldMoveFile = False
            break
    
    # check prefixes 
    shouldMoveFile = not shouldIgnoreBasedOnPrefix(file_data[0])
    
    # if not listed as ignored, proceed to move file
    if shouldMoveFile:
        moveFile(currentTime, file_data, file_path, move_folder)


class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        currentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        for filename in os.listdir(path):
            f = os.path.join(path, filename)

            if os.path.isfile(f):
                if moveBasedOnExtention(currentTime, f, pictures_folder,               image_extentions):
                    continue
                if moveBasedOnExtention(currentTime, f, documents_folder,              document_extentions):
                    continue
                if moveBasedOnExtention(currentTime, f, compressed_archives_folder,    compressed_archive_extentions):
                    continue
                if moveBasedOnExtention(currentTime, f, sounds_and_music_folder,       sound_and_music_file_extentions):
                    continue
                if moveBasedOnExtention(currentTime, f, videos_folder,                 video_file_extentions):
                    continue
                if moveBasedOnExtention(currentTime, f, executables_folder,            executable_file_extentions):
                    continue

                moveIgnoringExtention(  currentTime, f, other_files_folder,            ignore_extentions)

if __name__ == "__main__":
    # set working path based on os (unless path provided via argument)
    if sys.platform == "linux" or sys.platform == "linux2":
        path = sys.argv[1] if len(sys.argv) > 1 else '/home/'+getpass.getuser()+'/Downloads/'
    elif sys.platform == "darwin":
        path = sys.argv[1] if len(sys.argv) > 1 else '/Users/'+getpass.getuser()+'/Downloads/'
    elif sys.platform == "win32":
        path = sys.argv[1] if len(sys.argv) > 1 else 'C::\\Users\\'+getpass.getuser()+'\\Downloads\\'
    
    # check if folder exists
    if not os.path.exists(path):
        print("Folder with path '"+path+ "' does not exist")
        quit()

    # add / if missing
    if path[-1] != "/":
        path += "/"
    

    logFilePath = path+"fileOverseer.log"
    logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S', filename=str(logFilePath), encoding='utf-8', level=logging.INFO)

    print(COLOR_YELLOW+"working directory: "+COLOR_WHITE+path)

    checkDefaultDirectories(path)

    currentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    for filename in os.listdir(path):
        f = os.path.join(path, filename)

        if os.path.isfile(f):
            if moveBasedOnExtention(currentTime, f, pictures_folder,               image_extentions):
                continue
            if moveBasedOnExtention(currentTime, f, documents_folder,              document_extentions):
                continue
            if moveBasedOnExtention(currentTime, f, compressed_archives_folder,    compressed_archive_extentions):
                continue
            if moveBasedOnExtention(currentTime, f, sounds_and_music_folder,       sound_and_music_file_extentions):
                continue
            if moveBasedOnExtention(currentTime, f, videos_folder,                 video_file_extentions):
                continue
            if moveBasedOnExtention(currentTime, f, executables_folder,            executable_file_extentions):
                continue

            moveIgnoringExtention(  currentTime, f, other_files_folder,            ignore_extentions)
