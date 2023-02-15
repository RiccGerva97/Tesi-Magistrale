import subprocess
import shlex

ep1 = "e0eae0aa-5bca-11ea-9683-0e56c063f437"
ep2 = "bbcfa486-90ec-11ed-959b-63a4785a3eec"
root_path = f"{ep1}:Halos/FoF"


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

        download(final_remote_path, "/media/fuffolo97/HDD1/UNI/Tesi")
        # exit()

    # break
