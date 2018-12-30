"""" Niall Quinn, 1st Term Assignment, Student Number A00258744"""
""""Backup and Recovery Script"""

"""" With tis Script Your will be able to do a variety of tasks such as Manual and"""
"""" Automatic backups with or without changes and recovery previous documents """
# Importing all dependencies needed and reading from configP6 file
import filecmp
import distutils.dir_util
import errno
import os, os.path
import shutil
from shutil import make_archive
from sys import exit
import datetime
from datetime import date
from configP7 import FolderToBackup, LocationFolderToBackup, BackupFolder, LocationBackupFolder, MaxThreadsUsed, TimeSinceLastBackup, CompareFolderTime, TargetRecoveryfolder, RestoreZipFolder
import itertools
from time import sleep
import threading
import zipfile
from zipfile import ZipFile
import glob

QUIT = '8'
COMMANDS = ('1', '2', '3', '4', '5', '6', '8')
# My menu System
MENU = """1  Display details on the Folder to Backup and Directory Location
2   Create a New Manual Backup In The Backup Location
3   Start Auto Backup Program
4   Compare The Folders and Copy if Changes were made
5   Restore a File to Last Version
6   Restore a Specific File to a Specific Version..... Eg. myarchive.zip 2018-12-30 14-52-351
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


# reading information from configP6 file and printing to console
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

    # Copy and zip command while naming a folder
    elif command == '2':
        try:
            print("")
            filename = input("What Would You Like To Call Your New Folder? ")
            now = datetime.datetime.now()
            nowformat = now.strftime("%Y-%m-%d %H-%M-%S")
            archive_name = os.path.expanduser(os.path.join('./RestoreZips', filename + " " + str(nowformat)))
            root_dir = os.path.expanduser(os.path.join(LocationFolderToBackup))
            # Defining Each Thread and its Job
            def Copy1stThread():
                print(threading.currentThread().getName(), 'Starting')
                shutil.copytree("./FoldersToBackup/", "./BackupFolder/" + filename)
                print(threading.currentThread().getName(), 'Exiting')
            def Zip1stThread():
                print(threading.currentThread().getName(), 'Starting')
                make_archive(archive_name, 'zip', root_dir)
                print(threading.currentThread().getName(), 'Exiting')

            def Report1stThread():
                print(threading.currentThread().getName(), 'Starting')
                r = open("./report.txt", "a")
                try:
                    # File Name To Be backed Up
                    path = LocationFolderToBackup
                    files = os.listdir(path)
                    r.write(" ")
                    r.write("Todays date Is " + str(nowformat) + "\n")
                    r.write("=================================================" + "\n")
                    r.write("                 " + FolderToBackup + "          " + "\n")
                    r.write("=================================================" + "\n")
                    r.write(" Located:" + LocationFolderToBackup + "\n")
                    r.write("List of Files and Folders in " + FolderToBackup + " That will be backed up!" + "\n")
                    for name in files:
                        r.write("       " + name)
                        r.write("" + "\n")

                    total_size = 0
                    start_path = LocationFolderToBackup  # To get size of current directory
                    for path, dirs, files in os.walk(start_path):
                        for f in files:
                            fp = os.path.join(path, f)
                            total_size += os.path.getsize(fp)
                            r.write("Total Size of " + FolderToBackup + " file: " + str(total_size) + "b" + "\n")
                    time_accessed = date.fromtimestamp(os.path.getatime(path))
                    time_modified = date.fromtimestamp(os.path.getmtime(path))
                    r.write("         Date accessed Last " + str(time_accessed) + "\n")
                    r.write("         Date modified Last " + str(time_modified) + "\n")
                    r.write("" + "\n")
                    r.write("=================================================" + "\n")
                    r.write("       Backup Folder Name: " + BackupFolder + "\n")
                    r.write("=================================================" + "\n")
                    r.write(" Located: " + LocationBackupFolder + "\n")

                    comparison = filecmp.dircmp(LocationFolderToBackup, LocationBackupFolder)
                    comparison.report_full_closure()

                    total_size2 = 0
                    start_path2 = LocationBackupFolder  # To get size of current directory
                    for path, dirs, files in os.walk(start_path2):
                        for f in files:
                            fp = os.path.join(path, f)
                            total_size2 += os.path.getsize(fp)
                            r.write("Total Size of " + BackupFolder + " file: " + str(total_size2) + "b" + "\n")
                    time_accessed = date.fromtimestamp(os.path.getatime(path))
                    time_modified = date.fromtimestamp(os.path.getmtime(path))
                    r.write("         Date accessed Last " + str(time_accessed) + "\n")
                    r.write("         Date modified Last " + str(time_modified) + "\n")
                    r.write("" + "\n")

                    compare = filecmp.cmp(LocationFolderToBackup, LocationBackupFolder)
                    print(compare)

                    r.write("----------------------------------------------------------------" + "\n")
                    r.write("The Auto Backup Time in Secs is: " + TimeSinceLastBackup + "\n")
                    r.write("The Compare Check Time in Secs is: " + CompareFolderTime + "\n")
                    r.write("The Current Directory Your Are In Now Is:  " + os.getcwd() + "\n")
                    r.write("----------------------------------------------------------------" + "\n")
                    r.write("Your Archived Data Is Stored Here: " + RestoreZipFolder + "\n")
                    r.write("Your Recovery Data Is Stored Here: " + TargetRecoveryfolder + "\n")

                except Exception as error:
                    print('Caught this error: ' + repr(error))

            print(threading.currentThread().getName(), 'Exiting')

            Copy1 = threading.Thread(name='Copy1stThread', target=Copy1stThread)
            Zip1 = threading.Thread(name='Zip1stThread', target=Zip1stThread)
            Rep1 = threading.Thread(name='Report1stThread', target=Report1stThread)
            # Starting & Stopping Each Thread and its Job
            Copy1.start()
            Rep1.start()
            Copy1.join()
            Rep1.join()

            Zip1.start()
            Zip1.join()

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

            # Running a backup scripting a continuous loop copying and archiving the folders
    elif command == '3':
        now = datetime.datetime.now()
        nowformat = now.strftime("%Y-%m-%d %H-%M-%S")
        archive_name = os.path.expanduser(os.path.join('./RestoreZips', 'myarchive' + " " + str(nowformat)))
        root_dir = os.path.expanduser(os.path.join(LocationFolderToBackup))
        source = LocationFolderToBackup
        target = LocationBackupFolder + "Backup" + " " + str(nowformat)
        while True:
            for i in itertools.count(1, 1):
                try:
                    def Copy1stThread():
                        print(threading.currentThread().getName(), 'Starting')
                        shutil.copytree(source, target + str(i))
                        print(threading.currentThread().getName(), 'Exiting')

                    def Zip1stThread():
                        print(threading.currentThread().getName(), 'Starting')
                        make_archive(archive_name + str(i), 'zip', root_dir)
                        print(threading.currentThread().getName(), 'Exiting')

                    def Report1stThread():
                        print(threading.currentThread().getName(), 'Starting')
                        r = open("./report.txt", "a")
                        try:
                            # File Name To Be backed Up
                            path = LocationFolderToBackup
                            files = os.listdir(path)
                            r.write(" ")
                            r.write(" ")
                            r.write("Todays date Is " + str(nowformat) + "\n")
                            r.write("=================================================" + "\n")
                            r.write("                 " + FolderToBackup + "          " + "\n")
                            r.write("=================================================" + "\n")
                            r.write(" Located:" + LocationFolderToBackup + "\n")
                            r.write(
                                "List of Files and Folders in " + FolderToBackup + " That will be backed up!" + "\n")
                            for name in files:
                                r.write("       " + name)
                                r.write("" + "\n")

                            total_size = 0
                            start_path = LocationFolderToBackup  # To get size of current directory
                            for path, dirs, files in os.walk(start_path):
                                for f in files:
                                    fp = os.path.join(path, f)
                                    total_size += os.path.getsize(fp)
                                    r.write(
                                        "Total Size of " + FolderToBackup + " file: " + str(total_size) + "b" + "\n")
                            time_accessed = date.fromtimestamp(os.path.getatime(path))
                            time_modified = date.fromtimestamp(os.path.getmtime(path))
                            r.write("         Date accessed Last " + str(time_accessed) + "\n")
                            r.write("         Date modified Last " + str(time_modified) + "\n")
                            r.write("" + "\n")
                            r.write("=================================================" + "\n")
                            r.write("       Backup Folder Name: " + BackupFolder + "\n")
                            r.write("=================================================" + "\n")
                            r.write(" Located: " + LocationBackupFolder + "\n")

                            comparison = filecmp.dircmp(LocationFolderToBackup, LocationBackupFolder)
                            comparison.report_full_closure()

                            total_size2 = 0
                            start_path2 = LocationBackupFolder  # To get size of current directory
                            for path, dirs, files in os.walk(start_path2):
                                for f in files:
                                    fp = os.path.join(path, f)
                                    total_size2 += os.path.getsize(fp)
                                    r.write("Total Size of " + BackupFolder + " file: " + str(total_size2) + "b" + "\n")
                            time_accessed = date.fromtimestamp(os.path.getatime(path))
                            time_modified = date.fromtimestamp(os.path.getmtime(path))
                            r.write("         Date accessed Last " + str(time_accessed) + "\n")
                            r.write("         Date modified Last " + str(time_modified) + "\n")
                            r.write("" + "\n")

                            compare = filecmp.cmp(LocationFolderToBackup, LocationBackupFolder)
                            print(compare)

                            r.write("----------------------------------------------------------------" + "\n")
                            r.write("The Auto Backup Time in Secs is: " + TimeSinceLastBackup + "\n")
                            r.write("The Compare Check Time in Secs is: " + CompareFolderTime + "\n")
                            r.write("The Current Directory Your Are In Now Is:  " + os.getcwd() + "\n")
                            r.write("----------------------------------------------------------------" + "\n")
                            r.write("Your Archived Data Is Stored Here: " + RestoreZipFolder + "\n")
                            r.write("Your Recovery Data Is Stored Here: " + TargetRecoveryfolder + "\n")

                        except Exception as error:
                            print('Caught this error: ' + repr(error))

                    print(threading.currentThread().getName(), 'Exiting')

                    Copy1 = threading.Thread(name='Copy1stThread', target=Copy1stThread)
                    Zip1 = threading.Thread(name='Zip1stThread', target=Zip1stThread)
                    Rep1 = threading.Thread(name='Report1stThread', target=Report1stThread)

                    Copy1.start()
                    Rep1.start()
                    Copy1.join()
                    Rep1.join()

                    Zip1.start()
                    Zip1.join()

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
        now = datetime.datetime.now()
        nowformat = now.strftime("%Y-%m-%d %H-%M-%S")
        archive_name = os.path.expanduser(os.path.join('./RestoreZips', 'myarchive' + " " + str(nowformat)))
        root_dir = os.path.expanduser(os.path.join(LocationFolderToBackup))
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
                    # If the bytes size of the files are equal do nothing
                    if total_size == total_size2:
                        print('The Folder has not been changed')
                        print(".... CTRL + C to Quit ....")
                        sleep(int(CompareFolderTime))
                    # If the bytes size of the files are not equal copy and archive changes
                    elif total_size >= total_size2:
                        try:
                            now = datetime.datetime.now()
                            nowformat = now.strftime("%Y-%m-%d %H-%M-%S")

                            def Copy1stThread():
                                print(threading.currentThread().getName(), 'Starting')
                                distutils.dir_util.copy_tree(LocationFolderToBackup, LocationBackupFolder + "Updated Backup" + " " + str(nowformat))
                                print(threading.currentThread().getName(), 'Exiting')

                            def Zip1stThread():
                                print(threading.currentThread().getName(), 'Starting')
                                make_archive(archive_name + str(i), 'zip', root_dir)
                                print(threading.currentThread().getName(), 'Exiting')

                            def Report1stThread():
                                print(threading.currentThread().getName(), 'Starting')
                                r = open("./report.txt", "a")
                                try:
                                    # File Name To Be backed Up
                                    path = LocationFolderToBackup
                                    files = os.listdir(path)
                                    r.write(" ")
                                    r.write("Todays date Is " + str(nowformat) + "\n")
                                    r.write("=================================================" + "\n")
                                    r.write("                 " + FolderToBackup + "          " + "\n")
                                    r.write("=================================================" + "\n")
                                    r.write(" Located:" + LocationFolderToBackup + "\n")
                                    r.write(
                                        "List of Files and Folders in " + FolderToBackup + " That will be backed up!" + "\n")
                                    for name in files:
                                        r.write("       " + name)
                                        r.write("" + "\n")

                                    total_size = 0
                                    start_path = LocationFolderToBackup  # To get size of current directory
                                    for path, dirs, files in os.walk(start_path):
                                        for f in files:
                                            fp = os.path.join(path, f)
                                            total_size += os.path.getsize(fp)
                                            r.write("Total Size of " + FolderToBackup + " file: " + str(
                                                total_size) + "b" + "\n")
                                    time_accessed = date.fromtimestamp(os.path.getatime(path))
                                    time_modified = date.fromtimestamp(os.path.getmtime(path))
                                    r.write("         Date accessed Last " + str(time_accessed) + "\n")
                                    r.write("         Date modified Last " + str(time_modified) + "\n")
                                    r.write("" + "\n")
                                    r.write("=================================================" + "\n")
                                    r.write("       Backup Folder Name: " + BackupFolder + "\n")
                                    r.write("=================================================" + "\n")
                                    r.write(" Located: " + LocationBackupFolder + "\n")

                                    comparison = filecmp.dircmp(LocationFolderToBackup, LocationBackupFolder)
                                    comparison.report_full_closure()

                                    total_size2 = 0
                                    start_path2 = LocationBackupFolder  # To get size of current directory
                                    for path, dirs, files in os.walk(start_path2):
                                        for f in files:
                                            fp = os.path.join(path, f)
                                            total_size2 += os.path.getsize(fp)
                                            r.write("Total Size of " + BackupFolder + " file: " + str(
                                                total_size2) + "b" + "\n")
                                    time_accessed = date.fromtimestamp(os.path.getatime(path))
                                    time_modified = date.fromtimestamp(os.path.getmtime(path))
                                    r.write("         Date accessed Last " + str(time_accessed) + "\n")
                                    r.write("         Date modified Last " + str(time_modified) + "\n")
                                    r.write("" + "\n")

                                    compare = filecmp.cmp(LocationFolderToBackup, LocationBackupFolder)
                                    print(compare)

                                    r.write("----------------------------------------------------------------" + "\n")
                                    r.write("The Auto Backup Time in Secs is: " + TimeSinceLastBackup + "\n")
                                    r.write("The Compare Check Time in Secs is: " + CompareFolderTime + "\n")
                                    r.write("The Current Directory Your Are In Now Is:  " + os.getcwd() + "\n")
                                    r.write("----------------------------------------------------------------" + "\n")
                                    r.write("Your Archived Data Is Stored Here: " + RestoreZipFolder + "\n")
                                    r.write("Your Recovery Data Is Stored Here: " + TargetRecoveryfolder + "\n")

                                except Exception as error:
                                    print('Caught this error: ' + repr(error))

                            print(threading.currentThread().getName(), 'Exiting')

                            Copy1 = threading.Thread(name='Copy1stThread', target=Copy1stThread)
                            Zip1 = threading.Thread(name='Zip1stThread', target=Zip1stThread)
                            Rep1 = threading.Thread(name='Report1stThread', target=Report1stThread)

                            Copy1.start()
                            Rep1.start()
                            Copy1.join()
                            Rep1.join()

                            Zip1.start()
                            Zip1.join()

                            print("Your Changes Have been Backed up!")
                            print(".... CTRL + C to Quit ....")
                            sleep(int(CompareFolderTime))
                        # error this Depends what you need here to catch the problem
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

    # finds the file that needs restoring and recovers the to a recovery folder.
    elif command == '5':
        try:
            now = datetime.datetime.now()
            nowformat = now.strftime("%Y-%m-%d %H-%M-%S")
            list_of_files = glob.glob(RestoreZipFolder + '/*')  # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getctime)
            print(latest_file)

            recovery_folder = input("Please enter Your Specific Folder your File was Located :")
            recovery_file = recovery_folder + "/" + input("Please enter Your Specific FileName.txt you would like to Recover :")

            zip_filepath = latest_file
            archive = ZipFile(zip_filepath, 'r')
            target_Dir = TargetRecoveryfolder + "/"
            files = archive.namelist()
            print(files)
            fantasy_zip = zipfile.ZipFile(zip_filepath)
            file = fantasy_zip.extract(recovery_file, target_Dir)
            os.rename(target_Dir + "/" + recovery_folder, target_Dir + "/Recovery " + recovery_folder + " " + str(nowformat))

            print(file)
            print("Your File Has been restored to The RecoveryFolder")
        except IOError as e:
            print("Unable to complete this function. %s" % e)
            exit(1)

        choice = input("Would you Like To Continue? (y/n): ")
        print("==============================================")
        if choice.lower() != "y":
            exit()

    elif command == '6':
        try:
            now = datetime.datetime.now()
            nowformat = now.strftime("%Y-%m-%d %H-%M-%S")
            list_of_files = glob.glob(RestoreZipFolder + '/*')  # * means all if need specific format then *.csv
            print(list_of_files)

            recovery_archive = input("Please enter Your Specific Archive.Zip Version you would like to Recover :")
            recovery_folder = input("Please enter Your Specific Folder your File was Located :")
            recovery_file = recovery_folder + "/" + input("Please enter Your Specific FileName.txt you would like to Recover :")

            zip_filepath = './RestoreZips/' + recovery_archive
            archive = ZipFile(zip_filepath, 'r')
            target_Dir = TargetRecoveryfolder + "/"
            files = archive.namelist()
            print(files)
            fantasy_zip = zipfile.ZipFile(zip_filepath)
            file = fantasy_zip.extract(recovery_file, target_Dir)
            os.rename(target_Dir + "/" + recovery_folder, target_Dir + "/Recovery" + " " + recovery_folder + " " + str(nowformat))

            print(file)
            print("Your File Has been restored to The RecoveryFolder")

        except IOError as e:
            print("Unable to complete this function. %s" % e)
            exit(1)

        choice = input("Would you Like To Continue? (y/n): ")
        print("==============================================")
        if choice.lower() != "y":
            exit()


while True:
    if __name__ == "__main__":
        main()

