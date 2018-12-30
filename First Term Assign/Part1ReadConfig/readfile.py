"""" Niall Quinn, 1st Term Assignment, Student Number A00258744"""
""""Backup and Recovery Script"""

"""" With tis Script Your will be able to do a variety of tasks such as Manual and"""
"""" Automatic backups with or without changes and recovery previous documents """

# Importing all dependencies needed and reading from config file
import os.path
from datetime import date
from config import FolderToBackup, LocationFolderToBackup, BackupFolder, LocationBackupFolder, MaxThreadsUsed, TimeSinceLastBackup, CompareFolderTime, FirstThreadSourceFile, SecondThreadSourceFile, ThirdThreadSourceFile, FirstThreadTargetFile, SecondThreadTargetFile, ThirdThreadTargetFile, TargetRecoveryfolder, RestoreZipFolder
# Gets the Information from config.py and prints to console
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

