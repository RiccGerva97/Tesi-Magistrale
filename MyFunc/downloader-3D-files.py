import subprocess, shlex

folders2download = [
#    'h_m', 'h_p',
#    'Mnu_p', 'Mnu_pp' ,'Mnu_ppp',
#    'ns_m', 'ns_p',
#    'Om_m', 'Om_p',
#    'Ob2_m', 'Ob2_p',
#    's8_m', 's8_p',
#    'w_m', 'w_p',
    'fiducial', 'fiducial_ZA'
]

endpoints = {
    "3D_density_Quijote" : "bbcfa486-90ec-11ed-959b-63a4785a3eec",
    "DebianServer"       : "abf51c76-7723-11ee-b166-7d6eafac2be9",
    "DoraemonRicc"       : "9545d8ac-74d6-11ee-b164-7d6eafac2be9",
    "HDD1disk"           : "9eb93f5a-6c2a-11ee-ad2b-9197a4554f81",
    "VolD"               : "40f0f796-70d5-11ee-b162-7d6eafac2be9",
    "Quijote_NY"         : "e0eae0aa-5bca-11ea-9683-0e56c063f437"
}

def download_batch(local_batch_file):
    cmd = f"globus transfer --batch {local_batch_file} {ep1} {ep2} "
    process = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    print(stdout.decode("UTF-8"))
    if stderr is not None and len(stderr) != 0:
        error_msg = stderr.decode("UTF-8")
        print("ERROR: " + error_msg)

root_local = "/media/fuffolo97/LaCie/QuijoteSimulations"
sim_type = "3D_cubes"
file256 = "df_m_256_CIC_z=0.npy"
file512 = "df_m_512_z=0.npy"

with open("files-3D-NY2.txt", "a") as f:
    for F in folders2download:
        if "fiducial" not in F:
            for i in range(350):
                f.write(f" /{sim_type}/"+ F +"/" + str(i) + f"/df_m_256_CIC_z=0.npy {root_local}/{sim_type}/"+F+"/" + str(i) + "/df_m_256_CIC_z=0.npy\n")
                # f.write(f"/{sim_type}/"+ F +"/" + str(i) + f"/df_m_512_z=0.npy {root_local}/{sim_type}/"+F+"/" + str(i) + "/df_m_512_z=0.npy\n")
        elif "ZA" in F:
            for i in range(500):
                f.write(f"/{sim_type}/"+ F +"/" + str(i) + f"/df_m_256_CIC_z=0.npy {root_local}/{sim_type}/zeldovich/" + str(i) + "/df_m_256_CIC_z=0.npy\n")
                # f.write(f"/{sim_type}/"+ F +"/" + str(i) + f"/df_m_512_z=0.npy {root_local}/{sim_type}/zeldovich/" + str(i) + "/df_m_512_z=0.npy\n")
        elif "fiducial" == F:
            for i in range(1000):
                f.write(f"/{sim_type}/"+ F +"/" + str(i) + f"/df_m_256_CIC_z=0.npy {root_local}/{sim_type}/"+F+"/" + str(i) + f"/df_m_256_CIC_z=0.npy\n")
                # f.write(f"/{sim_type}/"+ F +"/" + str(i) + f"/df_m_512_z=0.npy {root_local}/{sim_type}/"+F+"/" + str(i) + f"/df_m_512_z=0.npy\n")

ep1 = "e0eae0aa-5bca-11ea-9683-0e56c063f437"    # Quijote - NewYork
# ep1 = "f4863854-3819-11eb-b171-0ee0d5d9299f"    # Quijote - SanDiego
ep2 = "bbcfa486-90ec-11ed-959b-63a4785a3eec"    # local - 3D_density_Quijote
ep2 = endpoints["VolD"]

download_batch("files-3D-NY2.txt")