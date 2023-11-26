folders2download = ['h_m', 'h_p',
                    # 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp',
                    'ns_m', 'ns_p',
                    'Om_m', 'Om_p',
                    'Ob2_m', 'Ob2_p',
                    's8_m', 's8_p',
                    'w_m', 'w_p',
                    'fiducial', 'fiducial_ZA']


with open("files-snap-NY.txt", "a") as f:
    for F in folders2download:
        if "fiducial" not in F:
            for i in range(350):
                f.write("--recursive Snapshots/"+ F +"/" + str(i) + "/snapdir_000 /home/ricc/Data/Snapshots/"+F+"/" + str(i) + "/snapdir_000\n")
        elif "ZA" in F:
            for i in range(1000):
                f.write("--recursive Snapshots/"+ F +"/" + str(i) + "/snapdir_000 /home/ricc/Data/Snapshots/zeldovich" + str(i) + "/snapdir_000\n")
        else:
            for i in range(2000):
                f.write("--recursive Snapshots/"+ F +"/" + str(i) + "/snapdir_000 /home/ricc/Data/Snapshots/fiducial/" + str(1000+i) + "/snapdir_000\n")

with open("allfolders.txt", "a") as f:
    for F in folders2download:
        if "fiducial" not in F:
            for i in range(350):
                f.write("Snapshots/"+ F +"/" + str(i) + "/snapdir_000\n")
        elif "ZA" in F:
            for i in range(1000):
                f.write("Snapshots/"+ F +"/" + str(i) + "/snapdir_000\n")
        else:
            for i in range(2000):
                f.write("Snapshots/"+ F +"/" + str(i) + "/snapdir_000\n")

with open("allfiles.txt", "a") as f:
    for F in folders2download:
        if "fiducial" not in F:
            for i in range(350):
                for j in range(8):
                    f.write("Snapshots/"+ F +"/" + str(i) + "/snapdir_000/snap_000." + str(j) + ".hdf5\n")
        elif "ZA" in F:
            for i in range(1000):
                for j in range(8):
                    f.write("Snapshots/"+ F +"/" + str(i) + "/snapdir_000/snap_000." + str(j) + ".hdf5\n")
        else:
            for i in range(2000):
                for j in range(8):
                    f.write("Snapshots/"+ F +"/" + str(i) + "/snapdir_000/snap_000." + str(j) + ".hdf5\n")

with open("allfiles_flags.txt", "a") as f:
    for F in folders2download:
        if "fiducial" not in F:
            for i in range(350):
                for j in range(8):
                    f.write("Snapshots/"+ F +"/" + str(i) + "/snapdir_000/snap_000." + str(j) + ".hdf5,0,0\n")
        elif "ZA" in F:
            for i in range(1000):
                for j in range(8):
                    f.write("Snapshots/"+ F +"/" + str(i) + "/snapdir_000/snap_000." + str(j) + ".hdf5,0,0\n")
        else:
            for i in range(2000):
                for j in range(8):
                    f.write("Snapshots/"+ F +"/" + str(i) + "/snapdir_000/snap_000." + str(j) + ".hdf5,0,0\n")
