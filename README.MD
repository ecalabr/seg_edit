# One Time Installation Instructions

## 1. Install ITK Snap
**Instructions**: http://www.itksnap.org/pmwiki/pmwiki.php?n=Documentation.TutorialSectionInstallation

**MacOS**: Make sure you copy itksnap to usr_local_bin (step 4)

**Windows**: Make sure you install in the default location

**Linux**: Make sure you copy folder contents to /usr/local/ (final optional step)

## 2. Install Python
**Instructions**: https://www.python.org/downloads/

## 3. Install Git
**Instructions**: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

## 4. Install seg_edit

### 1. Open a terminal window
Windows: "Windows Terminal"

acOs/Linux: "Terminal"

### 2. Change directories to your home directory: 
Windows
```angular2html
cd C:\Users\<user>\
```
MacOS/Linux
```angular2html
cd ~
```

### 3. Clone the repository
```angular2html
git clone https://github.com/ecalabr/seg_edit
```
If you get an SSL Certificate error, try:
```angular2html
git -c http.sslVerify=false clone https://github.com/ecalabr/seg_edit
```

### 4. Change directories to the repository directory
```angular2html
cd seg_edit
```

### 5. Install dependencies
```angular2html
pip install -r requirements.txt
```
If you get an SSL Certificate error, try:
```angular2html
pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
```

### 6. Connect to network drive
Ensure that you are connected to VPN.

Map the network drive using these instructions: https://answers.uillinois.edu/illinois.engineering/page.php?id=81180

Log in using the credentials provided to you.

If you are using linux or if you map the network drive to a different location, then you will need to manually edit params.yml with the full path to the mounted drive (base_directory).

# Running seg_edit
Use these instructions each time you want to run seg_edit
## Windows
Open a terminal and enter:
```commandline
C:\Users\<user>\seg_edit\windows_run.bat
```
Alternatively you can double click run.bat in Windows explorer.
## MacOS/Linux
Open a terminal and enter:
```
bash ~/seg_edit/run.bash
```

# Using seg_edit
After following the above instructions, a terminal window and a pop-up graphical prompt will open. Follow the instructions on the graphical prompt window. Additional information will be printed to the terminal output.

If you are having trouble finding a prompt window, try Alt (or Apple key) + Tab.
