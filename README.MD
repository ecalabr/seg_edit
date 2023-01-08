# One Time Installation Instructions

## 0. Find your terminal application
**Windows**: Search for "Windows Terminal"

**MacOS/Linux**: Search for "Terminal"

Subsequent steps will refer to this application as "a terminal".
```angular2html
Text displayed like this is meant for entry into a terminal.
```

## 1. Install ITK Snap
**Instructions**: http://www.itksnap.org/pmwiki/pmwiki.php?n=Documentation.TutorialSectionInstallation

**Windows**: Make sure you install in the default location

**MacOS**: Make sure you copy itksnap to usr_local_bin (step 4)

**Linux**: Make sure you copy folder contents to /usr/local/ (final optional step)

**MacOS/Linux**: You can check that the installation worked properly by entering this in a terminal:

```angular2html
itksnap
```
Which should open an ITK Snap window.

**Linux libpng error**: if you are getting a libpng error when you open ITK Snap on linx, follow these instructions: https://askubuntu.com/questions/1409363/installing-libpng12-so-on-ubuntu-22-04

## 2. Install Python 3.6 or greater
**Instructions**: https://www.python.org/downloads/

**Note**: Make sure that you choose the option to add the python executable to your PATH

To confirm that installation worked (or to check for an existing install), open a terminal and enter:
```
python --version
```
You should get a result like:
```angular2html
>>> Python 3.9.12
```
Note that version must be greater than or equal to 3.6.x

**MacOS:** If the above command results in a "not found error" even after installation, try:
```
echo "alias python=/usr/local/bin/python3" >> ~/.zshrc
```
Then quit and reopen your terminal application.

## 3. Install Git
**Instructions**: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

**Windows**: Recommend checking the option to use the default Windows Terminal for Git (cmd.exe).

To confirm that installation worked (or to check for an existing install), open a terminal and enter:
```
git --version
```
You should get a result like:
```angular2html
>>> git version 2.34.1
```

## 4. Install seg_edit

### 1. Change directories to your home directory: 
Open a terminal and enter the following:

**Windows**
```angular2html
cd C:\Users\<user>\
```
**MacOS/Linux**
```angular2html
cd ~
```

### 2. Clone the repository
```angular2html
git clone https://github.com/ecalabr/seg_edit
```
If you get an SSL Certificate error, try:
```angular2html
git -c http.sslVerify=false clone https://github.com/ecalabr/seg_edit
```

### 3. Change directories to the repository directory
```angular2html
cd seg_edit
```

### 4. Install dependencies
```angular2html
python -m pip install -r requirements.txt
```
If you get an SSL Certificate error, try:
```angular2html
python -m pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
```

### 5. Connect to network drive
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
