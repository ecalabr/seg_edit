# Installation Instructions

## 1. Install ITK Snap
**Instructions**: http://www.itksnap.org/pmwiki/pmwiki.php?n=Documentation.TutorialSectionInstallation

**MacOS**: Make sure you copy itksnap to usr_local_bin (step 4)

**Windows**: Make sure you install in the default location

**Linux**: Make sure you copy folder contents to /usr/local/ (final optional step)

## 2. Install Python
**Instructions**: https://www.python.org/downloads/

## 3. Install Git
**Instructions**: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

## 3. Install seg_edit

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
