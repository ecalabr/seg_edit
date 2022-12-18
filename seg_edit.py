import os
from glob import glob
import shutil
from tkinter import messagebox, simpledialog
import yaml
import random
import psutil
import time
import filecmp
from datetime import datetime
import subprocess
import platform


# load params
def load_params():
    # get file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    param_file = os.path.join(script_dir, "params.yml")
    if not os.path.isfile(param_file):
        error_gui(f"Did not find params.yml file in expected location: {param_file}")

    with open(param_file, 'r') as file:
        parameters = yaml.safe_load(file)

    return parameters


def get_itksnap_path():
    # initialize to None
    itksnap = None
    # check which type of system
    system_name = os.name
    # windows
    if system_name == 'nt':
        matches = glob(f"C:/Program Files/ITK-SNAP*/bin/ITK-SNAP.exe")
        if matches:
            itksnap = matches[0]
    elif system_name == "posix":
        if shutil.which("itksnap") is not None:
            itksnap = "itksnap"
    else:
        error_message = f"Did not recognize system type {system_name}"
        error_gui(error_message)

    if itksnap is None:
        error_message = f"Could not find ITK Snap! Please check installation and try again."
        error_gui(error_message)
    else:
        return itksnap


# get a case
def select_case(parameters, not_these=()):
    # get list of cases
    subdirs = sorted(glob(parameters["base_directory"] + "/*/"))

    # remove not_these
    subdirs = [item for item in subdirs if item not in not_these]

    # select a case
    random.shuffle(subdirs)
    all_suff = parameters["image_suffixes"] + [parameters["label_suffix"]]
    mc_suffix = parameters["corrected_suffix"]
    for subdir in subdirs:
        if all([glob(subdir + f"*{item}.nii.gz") for item in all_suff]) and not glob(subdir + f"*{mc_suffix}.nii.gz"):
            # copy segmentation file to manually corrected name
            seg = glob(subdir + f"*{parameters['label_suffix']}.nii.gz")[0]
            seg_mc = seg.replace(parameters["label_suffix"], parameters["corrected_suffix"])
            shutil.copy(seg, seg_mc)

            return subdir

    return None


# make itksnap command
def build_itksnap_command(snap_path, case_dir, parameters):
    # get full file names
    images = [glob(case_dir + f"/*{item}.nii.gz")[0] for item in parameters["image_suffixes"]]
    label_image = glob(case_dir + f"/*{parameters['corrected_suffix']}.nii.gz")[0]
    label_file = get_label_file_path(parameters)

    # build command
    join_str = '" "'
    cmd = f'"{snap_path}" -g "{images[0]}" -o "{join_str.join(images[1:])}" -s "{label_image}" -l "{label_file}"'

    return cmd


# run command
def run_command(cmd, case_dir, parameters, uname):

    # define completion
    complete = False

    # run command
    subprocess.call(fr"{cmd}", shell=True)

    # check for running itk snap
    running = True
    while running:
        running = check_itk_running()
        time.sleep(2)

    # once not running, perform checks
    corrected_label_image = glob(case_dir + f"/*{parameters['corrected_suffix']}.nii.gz")
    original_label_image = glob(case_dir + f"*{parameters['label_suffix']}.nii.gz")[0]
    # check for manually edited output
    if corrected_label_image:
        corrected_label_image = corrected_label_image[0]
        # raise save prompt
        case_id = os.path.basename(os.path.dirname(case_dir))
        message = f"Would you like to claim credit for manually correcting the following case: {case_id}?"
        response = messagebox.askyesno("Claim Credit?", message)
        if response:
            # check for identical files
            same = filecmp.cmp(original_label_image, corrected_label_image)
            if same:
                message = f"No manual corrections were detected! Original and corrected files are identical. "\
                          "Are you certain that no edits were required?"
                response = messagebox.askyesno("No edits detected!", message)
        if not response:
            message = f"Are you sure you want to discard your work for this case?"
            response = messagebox.askyesno("Confirm Discard?", message)
            if response:
                os.remove(corrected_label_image)
        # confirm that corrected image still present and claim credit
        if os.path.isfile(corrected_label_image):
            write_credit_log(case_dir, uname)
            complete = True

    return complete


# welcome
def start_session():
    mesg = """
    Welcome to the Segmentation correction tool!
    
    Please read the following instructions carefully:
    
    1. Please ensure you have completed all of the installation steps in the included README.MD file.
    
    2. Please carefully read the included segmentation_instructions.pdf
    
    3. When you have completed correcting a case, close the ITK Snap window, click "Save All" to save your work.
    
    4. After closing a case, look for a popup dialogue (it may be in the background, try Alt+Tab).
    
    5. Please contact us for any issues!
    
    Would you like to view the Segmentation Instructions now?
    
    Click "Yes" to view instructions or "No" to skip.
    """
    response = messagebox.askyesno("View Instructions?", mesg)
    if response:
        view_pdf()
    uname = get_username()

    return uname


# close session
def close_session(num_complete):
    mesg = f"Segmentation session ended. You completed {num_complete} case(s) during this session."
    messagebox.showinfo("Session Completed!", mesg)


# open instructions pdf with default viewer
def view_pdf():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    pdf_path = os.path.join(script_dir, "segmentation_instructions.pdf")
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', pdf_path))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(pdf_path)
    else:  # linux variants
        subprocess.call(('xdg-open', pdf_path))


# write credit log
def write_credit_log(case_dir, uname=None):
    logfile = os.path.join(case_dir, "log.txt")
    with open(logfile, "a+") as f:
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        if not uname:
            uname = os.getlogin()
        log_string = f"\n{date_time}: {uname}"
        f.write(log_string)


# function for checking for running processes of ITK snap
def check_itk_running(name='ITK-SNAP'):
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


# get label file path
def get_label_file_path(parameters):
    # get file path
    script_dir = os.path.dirname(os.path.realpath(__file__))
    label_file = os.path.join(script_dir, parameters["label_file"])
    if not os.path.isfile(label_file):
        error_gui(f"Did not find label file in expected location: {label_file}")
    return label_file


# get username
def get_username():
    mesg = "Enter your unique username to start correcting cases.\n" \
           "This can be anything you want, as long as it is unique to you.\n" \
           "Please use the same username each time you use this tool."
    uname = simpledialog.askstring("Enter Username", mesg, initialvalue=os.getlogin())
    return uname


# raise error gui with message
def error_gui(message):
    messagebox.showerror("Error", message)
    exit()


# raise warn gui with message
def warn_gui(message):
    messagebox.showwarning("Warning!", message)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # check for running itksnap and error if open
    if check_itk_running():
        error_gui(f"Detected running ITK Snap instance. Please close all ITK Snap windows and try again.")
        exit()

    # load params
    params = load_params()

    # check if base directory exists
    if not os.path.isdir(params["base_directory"]):
        error_gui(f"Cannot find base directory: {params['base_directory']}. Confirm you are connected to VPN and "
                  f"can access this directory, then try again.")

    # get ITK Snap path
    itksnap_path = get_itksnap_path()

    # start session
    username = start_session()

    # iterate through cases
    already_viewed = []
    completed = 0
    keep_going = True
    while keep_going:
        case = select_case(params, not_these=already_viewed)
        # no cases found
        if case is None:
            warn_gui(f"Did not find any remaining eligible cases to correct.")
            keep_going = False
        else:
            command = build_itksnap_command(itksnap_path, case, params)
            success = run_command(command, case, params, username)
            if success:
                completed += 1
            already_viewed.append(case)
            # continue editing?
            mesg = f"Would you like to correct another case?"
            resp = messagebox.askyesno("Continue Editing?", mesg)
            if not resp:
                keep_going = False

    # end session
    close_session(completed)
