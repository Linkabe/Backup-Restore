"""" Niall Quinn, 1st Term Assignment, Student Number A00258744"""
""""Backup and Recovery Script"""

"""" With tis Script Your will be able to do a variety of tasks such as Manual and"""
"""" Automatic backups with or without and threading backup """
# Importing all dependencies needed and reading from configP2 file
import filecmp
import distutils.dir_util
import errno
import os, os.path
import shutil
from sys import exit
import datetime
from datetime import date
from configP5 import FolderToBackup, LocationFolderToBackup, BackupFolder, LocationBackupFolder, MaxThreadsUsed, TimeSinceLastBackup, CompareFolderTime, FirstThreadSourceFile, SecondThreadSourceFile, ThirdThreadSourceFile, FirstThreadTargetFile, SecondThreadTargetFile, ThirdThreadTargetFile, TargetRecoveryfolder, RestoreZipFolder
import itertools
from time import sleep
import threading

QUIT = '8'
COMMANDS = ('1', '2', '3', '4', '5', '6', '8')
# My menu System
MENU = """1  Display details on the Folder to Backup and Directory Location
2   Create a New Manual Backup In The Backup Location
3   Start Auto Backup Program
4   Compare The Folders and Copy if Changes were made
5   Create a Log of your Backup Details in Reports.txt
6   Speed up Your Backup Using Threads
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

        except:
            print("Unexpected error:", sys.exc_info())
            exit(1)

        print("Your Folder Has Been copied.. Enjoy!")

        choice = input("Would you Like To Create Another Folder? (y/n): ")
        print("==============================================")
        if choice.lower() != "y":
            choice = input("Would you Like To Continue? (y/n): ")
            print("==============================================")
            if choice.lower() != "y":
                exit()

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
    # Comparing and copying folder if changes have been made.
    elif command == '4':
        print("")
        while True:
            for i in itertools.count(1, 1):
                try:
                    comparison = filecmp.dircmp(LocationFolderToBackup, LocationBackupFolder)
                    comparison.report_full_closure()

                    total_size = 0
                    start_path = LocationFolderToBackup  # To get size of current directory
                    for path, dirs, files in os.walk(start_path):
                        for f in files:
                            fp = os.path.join(path, f)
                            total_size += os.path.getsize(fp)
                    print("Directory size: " + str(total_size))

                    total_size2 = 0
                    start_path2 = LocationBackupFolder  # To get size of current directory
                    for path, dirs, files in os.walk(start_path2):
                        for f in files:
                            fp2 = os.path.join(path, f)
                            total_size2 += os.path.getsize(fp2)
                    print("Directory size: " + str(total_size2))

                    compare = filecmp.cmp(LocationFolderToBackup, LocationBackupFolder)
                    print(compare)

                    if total_size == total_size2:
                        print('The Folder has not been changed')
                        sleep(int(CompareFolderTime))

                    elif total_size != total_size2:
                        try:
                            distutils.dir_util.copy_tree(LocationFolderToBackup, LocationBackupFolder)
                            print("Your Changes Have been Backed up!")
                            sleep(int(CompareFolderTime))
                        # Depend what you need here to catch the problem
                        except OSError as exc:
                            # File already exist
                            if exc.errno == errno.EEXIST:
                                distutils.dir_util.copy_tree(LocationFolderToBackup, LocationBackupFolder)
                            # The directory does not exist
                            if exc.errno == errno.ENOENT:
                                distutils.dir_util.copy_tree(LocationFolderToBackup, LocationBackupFolder)
                            else:
                                raise ValueError('A very specific bad thing happened.')
                except Exception as error:
                    print('Caught this error: ' + repr(error))
    # Rights from the config file to a report.txt file. makes file if it does not exists and amends file if it does not
    elif command == '5':
        print("")
        r = open("./report.txt", "a")
        datenow = datetime.datetime.now()
        try:
            # File Name To Be backed Up
            path = LocationFolderToBackup
            files = os.listdir(path)
            r.write("Todays date Is " + str(datenow)+"\n")
            r.write("================================================="+"\n")
            r.write("                 " + FolderToBackup + "          "+"\n")
            r.write("================================================="+"\n")
            r.write(" Located:" + LocationFolderToBackup + "\n")
            r.write("List of Files and Folders in " + FolderToBackup + " That will be backed up!"+"\n")
            for name in files:
                r.write("       " + name)
                r.write("" + "\n")

            total_size = 0
            start_path = LocationFolderToBackup  # To get size of current directory
            for path, dirs, files in os.walk(start_path):
                for f in files:
                    fp = os.path.join(path, f)
                    total_size += os.path.getsize(fp)
                    r.write("Total Size of " + FolderToBackup + " file: " + str(total_size) + "b"+"\n")
            time_accessed = date.fromtimestamp(os.path.getatime(path))
            time_modified = date.fromtimestamp(os.path.getmtime(path))
            r.write("         Date accessed Last " + str(time_accessed)+"\n")
            r.write("         Date modified Last " + str(time_modified)+"\n")
            r.write(""+"\n")
            r.write("================================================="+"\n")
            r.write("       Backup Folder Name: " + BackupFolder + "\n")
            r.write("================================================="+"\n")
            r.write(" Located: " + LocationBackupFolder + "\n")

            comparison = filecmp.dircmp(LocationFolderToBackup, LocationBackupFolder)
            comparison.report_full_closure()

            total_size2 = 0
            start_path2 = LocationBackupFolder  # To get size of current directory
            for path, dirs, files in os.walk(start_path2):
                for f in files:
                    fp = os.path.join(path, f)
                    total_size2 += os.path.getsize(fp)
                    r.write("Total Size of " + BackupFolder + " file: " + str(total_size2) + "b"+"\n")
            time_accessed = date.fromtimestamp(os.path.getatime(path))
            time_modified = date.fromtimestamp(os.path.getmtime(path))
            r.write("         Date accessed Last " + str(time_accessed)+"\n")
            r.write("         Date modified Last " + str(time_modified)+"\n")
            r.write(""+"\n")

            compare = filecmp.cmp(LocationFolderToBackup, LocationBackupFolder)
            print(compare)

            r.write("----------------------------------------------------------------" + "\n")
            r.write("The Auto Backup Time in Secs is: " + TimeSinceLastBackup + "\n")
            r.write("The Compare Check Time in Secs is: " + CompareFolderTime + "\n")
            r.write("The Current Directory Your Are In Now Is:  " + os.getcwd() + "\n")
            r.write("----------------------------------------------------------------" + "\n")
            r.write("Your Archived Data Is Stored Here: " + RestoreZipFolder + "\n")
            r.write("Your Recovery Data Is Stored Here: " + TargetRecoveryfolder + "\n")

            choice = input("Would you Like To Continue? (y/n): ")
            print("==============================================")
            if choice.lower() != "y":
                exit()

        except Exception as error:
            print('Caught this error: ' + repr(error))
    # Each Thread has a spcific task and runs simultaneously to speed up the backup
    elif command == '6':
        now = datetime.datetime.now()
        nowformat = now.strftime("%Y-%m-%d %H-%M-%S-%f")
        source1 = FirstThreadSourceFile
        source2 = SecondThreadSourceFile
        source3 = ThirdThreadSourceFile
        target1 = FirstThreadTargetFile + " " + str(nowformat)
        target2 = SecondThreadTargetFile + " " + str(nowformat)
        target3 = ThirdThreadTargetFile + " " + str(nowformat)
        try:
            def copy1stThread():
                print(threading.currentThread().getName(), 'Starting')
                shutil.copytree(source1, target1)
                print(threading.currentThread().getName(), 'Exiting')

            def copy2ndThread():
                print(threading.currentThread().getName(), 'Starting')
                shutil.copytree(source2, target2)
                print(threading.currentThread().getName(), 'Exiting')

            def copy3rdThread():
                print(threading.currentThread().getName(), 'Starting')
                shutil.copytree(source3, target3)
                print(threading.currentThread().getName(), 'Exiting')

            Copy1 = threading.Thread(name='copy1stThread', target=copy1stThread)
            Copy2 = threading.Thread(name='copy2ndThread', target=copy2ndThread)
            Copy3 = threading.Thread(name='copy3rdThread', target=copy3rdThread)

            Copy1.start()
            Copy2.start()
            Copy3.start()

            Copy1.join()
            Copy2.join()
            Copy3.join()
            print("Exiting the Program!!!")
        except IOError as e:
            print("Unable to copy folder. %s" % e)
            exit(1)

        choice = input("Would you Like To Continue? (y/n): ")
        print("==============================================")
        if choice.lower() != "y":
            exit()


while True:
    if __name__ == "__main__":
        main()

