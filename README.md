# LightFTPTesting  
This github contains greybox fuzzer to test [LightFTP](https://github.com/hfiref0x/LightFTP)  

## System Requirements
* x86-32/x64 POSIX compliant OS, e.g. Linux.
* x86-32/x64 Windows 7/8/8.1/10 with Cygwin (see Build section of this readme).
* No admin/root privileges required. FTP server must be allowed in firewall.  

## Build (This section is referred from [here](https://github.com/hfiref0x/LightFTP/blob/master/README.md#build))

* LightFTP comes with full source code, written in C;
* In order to build from source in Windows you need Cygwin environment (https://www.cygwin.com/) with GNU make, gnutls and pthreads packages installed. Also make sure Cygwin bin folder is set in system wide PATH variable (e.g. PATH=SomeOfYourOtherValues;C:\Cygwin\bin;C:\Cygwin\usr\bin). To build executable run make command in the Release directory;
* In order to build from source in Linux you need GCC C compiler, run make command in the Release directory. LigthFTP uses GnuTLS, make sure you have headers (libgnutls-dev or gnutls-dev) installed.

### Example for Linux Mint 19.3/Ubuntu 18.04

You need GCC and Make installed. If they are not installed you can install them as part of build-essential package:

      sudo apt install build-essential
      
LightFTP uses GnuTLS library. It need to be installed before compiling LightFTP. To install it, open terminal and use:

      sudo apt install gnutls-dev
	  
or if this doesn't work try:

      sudo apt install libgnutls28-dev  

## How To Run
Download source from [https://github.com/Stygian84/LightFTPTesting.git](https://github.com/Stygian84/LightFTPTesting.git) or use git. 

In case if you want to use git and git is not installed, install it first:

      sudo apt install git
      
Next use the following:

      git clone https://github.com/Stygian84/LightFTPTesting.git  
      
1) Go to `Source/Release` and edit the `fftp.conf` (click [here](#how-to-edit-the-config-file) to see what needs to be changed)  
2) Copy & paste the updated `fftp.conf` to `Tester/new`.  
3) Open terminal and change working directory to `Tester/new` in the terminal.  
  For example: if the current working directory is `path/to/LightFTPTesting`,  
  type `cd Tester/new` in the terminal  
  to change the current working directory to `path/to/LightFTPTesting/Tester/new`
4) Type `python main_ftp.py` in the terminal.  


## How to edit the config file  
1. Change `logfilepath` value in line `42` to your absolute path in your system that directs to an empty log file.  
2. Create an empty folder anywhere in your system.  
3. Change `root` value for each user (line `76`, `81`, `86`) to your absolute path in your system that directs to the empty folder for the `root`.  

If you are interested on each section of the config file, you can look [here](https://github.com/hfiref0x/LightFTP#configuration) for more details.


## FAQ
1. After running the `python main_ftp.py`, this line appears for each iteration `550 permission denied`. How to fix?  
   Ensure that the `root` value for each user is properly defined in the `fftp.conf` in both `Source/Release` and `Tester/new` directcory and ensure the empty folder exists in that path.
