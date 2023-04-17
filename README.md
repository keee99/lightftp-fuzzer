# LightFTPTesting

## How To Run
1) Go to Source/Release and edit the fftp.conf (click [here](#how-to-edit-the-config-file) to see what needs to be changed)  
2) Copy & paste the updated fftp.conf to Tester/new.  
3) Open terminal and change working directory to Tester/new in the terminal.  
  For example: if the current working directory is `path/to/LightFTPTesting`,  
  type `cd Tester/new` in the terminal  
  to change the current working directory to `path/to/LightFTPTesting/Tester/new`
4) Type `python main_ftp.py` in the terminal.  


## How to edit the config file  
1. Change `logfilepath` value in line `42` to your absolute path in your system that directs to an empty log file.  
2. Change `root` value for each user (line `76`, `81`, `86`) to your absolute path in your system that directs to an empty folder for the `root`.  
