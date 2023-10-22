folders2download = ['h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
                    'ns_m', 'ns_p', 'Ob2_m', 'Ob2_p', \
                    's8_m', 's8_p', 'w_m', 'w_p',\
                    'fiducial', 'fiducial_ZA']


with open("files-snap-NY.txt", "a") as f:
    for F in folders2download:
        if "fiducial" not in F:
            for i in range(350):
                f.write("--recursive Snapshots/"+ F +"/" + str(i) + "/groups_002 /media/fuffolo97/LaCie/QuijoteSimulations/Snapshots/"+F+"/" + str(i) + "/groups_002\n")
        elif "ZA" in F:
            for i in range(1000):
                f.write("--recursive Snapshots/"+ F +"/" + str(i) + "/groups_002 /media/fuffolo97/LaCie/QuijoteSimulations/Snapshots/zeldovich" + str(i) + "/groups_002\n")
        else:
            for i in range(2000):
                f.write("--recursive Snapshots/"+ F +"/" + str(i) + "/groups_002 /media/fuffolo97/LaCie/QuijoteSimulations/Snapshots/fiducial/" + str(1000+i) + "/groups_002\n")
    