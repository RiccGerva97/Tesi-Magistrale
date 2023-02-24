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

    return stdout.decode("UTF-8").split("\n")


def download(remote_path, local_path):
    local_partial_path = ":".join(remote_path.split(":")[1:])

    cmd = f"globus transfer {remote_path} {ep2}:{local_path}/{local_partial_path} --recursive"
    process = subprocess.Popen(shlex.split(cmd),
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    print(stdout.decode("UTF-8"))


for root_dir_raw in ls(root_path):
    if "latin" in root_dir_raw:
        continue

    root_dir = root_dir_raw.strip()

    inner_path = f"{root_path}/{root_dir}"
    for inner_dir in ls(inner_path):
        final_remote_path = f"{inner_path}{inner_dir}groups_002"

        download(final_remote_path, "/media/fuffolo97/HDD1/UNI/Tesi")   # <- modify here your personal path
        # exit()

    # break
