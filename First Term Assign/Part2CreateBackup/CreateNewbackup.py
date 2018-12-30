# Importing all dependencies needed and reading from configP2 file
import filecmp
import distutils.dir_util
import errno
import os, os.path
import shutil
from sys import exit
import datetime
from datetime import date
from configP2 import FolderToBackup, LocationFolderToBackup, BackupFolder, LocationBackupFolder, MaxThreadsUsed, TimeSinceLastBackup, CompareFolderTime, FirstThreadSourceFile, SecondThreadSourceFile, ThirdThreadSourceFile, FirstThreadTargetFile, SecondThreadTargetFile, ThirdThreadTargetFile, TargetRecoveryfolder, RestoreZipFolder
import itertools
from time import sleep

QUIT = '8'
COMMANDS = ('1', '2', '3', '8')
# My menu System
MENU = """1  Display details on the Folder to Backup and Directory Location
2   Create a New Manual Backup In The Backup Location
3   Start Auto Backup Program
8   Quit the program"""


# Defining Quit and error detection
def main():
    while True:
        print(os.getcwd())
        print(MENU)
        command = acceptCommand()
        runCommand(command)
        if command == QUIT:
            print("Enjoy the Rest of Your Day! GoodBye.")
            exit()


# Error detection...Number not entered.
def acceptCommand():
    """Inputs and returns a legitimate command number."""
    while True:
        command = input("Type A Number from the Options Menu: ")
        if not command in COMMANDS:
            print("Error: Your Input is not recognized")
        else:
            return command


# reading information from configP2 file and printing to console
def runCommand(command):
    """Selects and runs a command."""
    if command == '1':
        cwd = os.getcwd()
        print(" ")
        print("----------------------------------------------------------------")
        print("Your Folder to Be backed up Is: " + FolderToBackup)
        print("The Location of that Folder Is: " + LocationFolderToBackup)
        print("----------------------------------------------------------------")
        print("Your Backup Folder Is called: " + BackupFolder)
        print("The location of The Backup Folder Is: " + LocationBackupFolder)
        print("The Max number Of Threads Used Is: " + MaxThreadsUsed)
        # Getting Date and time of when folder was last accessed and modified.
        path = BackupFolder
        time_accessed = date.fromtimestamp(os.path.getatime(path))
        time_modified = date.fromtimestamp(os.path.getmtime(path))
        print("Date Accessed Last " + str(time_accessed))
        print("Date Backed Up Last " + str(time_modified))
        print("")
        print("----------------------------------------------------------------")
        print("The Auto Backup Time in Secs is: " + TimeSinceLastBackup + "\n")
        print("The Compare Check Time in Secs is: " + CompareFolderTime + "\n")
        print("The Current Directory Your Are In Now Is:  " + os.getcwd())
        print("----------------------------------------------------------------")
        print("Your Archived Data Is Stored Here: " + RestoreZipFolder)
        print("Your Recovery Data Is Stored Here: " + TargetRecoveryfolder + "\n")
        # continue program choice

        choice = input("Would you Like To Continue? (y/n): ")
        print("==============================================")
        if choice.lower() != "y":
            exit()

    # Copy command while naming a folder
    elif command == '2':
        try:
            print("")
            source = LocationFolderToBackup
            target = LocationBackupFolder + input(
                "What Would You Like To Call Your New Folder? ")
            shutil.copytree(source, target)
        except IOError as e:
            print("Unable to copy folder. %s" % e)

        print("Your Folder Has Been copied.. Enjoy!")

        choice = input("Would you Like To Create Another Folder? (y/n): ")
        print("==============================================")
        if choice.lower() != "y":
            choice = input("Would you Like To Continue? (y/n): ")
            print("==============================================")
            if choice.lower() != "y":
                exit()
    # Running a backup scripting a continuous loop copying
    elif command == '3':
        now = datetime.datetime.now()
        nowformat = now.strftime("%Y-%m-%d %H-%M-%S")
        source = LocationFolderToBackup
        target = LocationBackupFolder + "Backup" + " " + str(nowformat)
        while True:
            for i in itertools.count(1, 1):
                try:
                    shutil.copytree(source, target + str(i))
                    print("Backing Up.... CTRL + C to Quit")
                    sleep(int(TimeSinceLastBackup))
                    continue
                    break
                except IOError as e:
                    print("Unable to copy folder. %s" % e)
                    exit(1)

                except:
                    print("Unexpected error:", sys.exc_info())
                    exit(1)


while True:
    if __name__ == "__main__":
        main()
