"""A python script to download from Globus choosen halo catalogues.
You must pay attention to:
- have a Globus account
- modify online and local repositories UUID (`ep1` and `ep2` variables)
- modify online starting path (`root_path` variable)
- modify your persolal download path destination (search for comment below inside `download` function)
- set your persolal download path destination avaiable to reading/writing by Globus (https://docs.globus.org/how-to/globus-connect-personal-linux/#config-paths)
"""

import subprocess
import shlex
from tqdm import tqdm

LOG_FILE = "logger.txt"

# ep1 = "e0eae0aa-5bca-11ea-9683-0e56c063f437"    # Quijote - NewYork
ep1 = "f4863854-3819-11eb-b171-0ee0d5d9299f"    # Quijote - SanDiego
ep2 = "bbcfa486-90ec-11ed-959b-63a4785a3eec"    # local for NY
# root_path = f"{ep1}:Halos/FoF"                # local for SD
root_path = f"{ep1}:Halos"

def ls(path):
    process = subprocess.Popen(shlex.split("globus ls " + path),
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr is not None and len(stderr) != 0:
        error_msg = stderr.decode("UTF-8")
        print("ERROR: " + error_msg)
        raise Exception("LS interrotto")

    return [p for p in stdout.decode("UTF-8").split("\n") if len(p) > 0]


def download(remote_path, local_path):
    local_partial_path = ":".join(remote_path.split(":")[1:])

    cmd = f"globus transfer {remote_path} {ep2}:{local_path}/{local_partial_path} --recursive"
    process = subprocess.Popen(shlex.split(cmd),
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    print(stdout.decode("UTF-8"))
    if stderr is not None and len(stderr) != 0:
        error_msg = stderr.decode("UTF-8")
        print("ERROR: " + error_msg)
        with open(LOG_FILE, "a") as f:
            f.write(error_msg)

def download_batch(local_batch_file):
    cmd = f"globus transfer --batch {local_batch_file} {ep1} {ep2} "
    process = subprocess.Popen(shlex.split(cmd),
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    print(stdout.decode("UTF-8"))
    if stderr is not None and len(stderr) != 0:
        error_msg = stderr.decode("UTF-8")
        print("ERROR: " + error_msg)

###########################################################à

# files_da_scaricare = list()

# for root_dir_raw in ls(root_path):
#     print(root_dir_raw)

#     if "latin" in root_dir_raw or "fiducial_" in root_dir_raw:
#         continue

#     root_dir = root_dir_raw.strip()

#     inner_path = f"{root_path}/{root_dir}"
#     for inner_dir in tqdm(ls(inner_path)):
#         try:
#             if int(inner_dir[:-1]) >= 500:
#                 continue
#         except Exception:
#             pass

#         final_remote_path = f"{inner_path}{inner_dir}groups_002"
#         print(final_remote_path)

#         local_partial_path = ":".join(final_remote_path.split(":")[1:])
#         local_complete_path = f"/media/fuffolo97/HDD1/UNI/Tesi/{local_partial_path}"
    
#         files_da_scaricare.append(f"--recursive {final_remote_path} {local_complete_path}")
#         # download(final_remote_path, "/media/fuffolo97/HDD1/UNI/Tesi")   # <- modify here your personal path
# #         # exit()


# with open("second-download-files.txt","w") as f:
#     for fpath in files_da_scaricare:
#         f.write(fpath + "\n")

#     # break
# with open("files-da-scaricare","w") as f:
#     for fpath in files_da_scaricare:
#         f.write(fpath + "\n")

download_batch("third-download-files.txt")

#######################################################################################

# CosmoToDownload = ['h_p','Ob2_p']
# InFoldsToDownload = ['NCV_0_', 'NCV_1_']

# with open("second-download-files.txt", "a") as f:
#     for i in range(500):
#         f.write("--recursive Halos/fiducial/" + str(i) + "/groups_002 /media/fuffolo97/HDD1/UNI/Tesi/Halos2/fiducial/" + str(i) + "/groups_002\n")
    
#     for i in CosmoToDownload:
#         for j in InFoldsToDownload:
#             for k in range(250):
#                 a = "--recursive Halos/" + i + "/" + j + str(k) + "/groups_002 /media/fuffolo97/HDD1/UNI/Tesi/Halos2/" + i + "/" + j + str(k) + "/groups_002\n"
#                 f.write(a)

# with open("third-download-files.txt", 'a') as f:
#     for i in range(500):
#         f.write("--recursive Halos/fiducial/" + str(500+i) + "/groups_002 /media/fuffolo97/HDD1/UNI/Tesi/Halos2/fiducial/" + str(500+i) + "/groups_002\n")
#     for i in range(500):
#         f.write(("--recursive Halos/h_p/" + str(i) + "/groups_002 /media/fuffolo97/HDD1/UNI/Tesi/Halos2/h_p/" + str(i) + "/groups_002\n"))
#     for i in range(500):
#         f.write(("--recursive Halos/Ob2_p/" + str(i) + "/groups_002 /media/fuffolo97/HDD1/UNI/Tesi/Halos2/Ob2_p/" + str(i) + "/groups_002\n"))
