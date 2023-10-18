# folders2download = ['h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
#                     'ns_m', 'ns_p', 'Ob2_m', 'Ob2_p', \
#                     's8_m', 's8_p', 'w_m', 'w_p']


with open("files-DM.txt", "a") as f:
    # for F in folders2download:
    #     for i in range(350):
    #         f.write("--recursive 3D_cubes/"+ F +"/" + str(i) + "/groups_002 /media/fuffolo97/HDD1/UNI/Tesi/3D_cubes/"+F+"/" + str(i) + "/groups_002\n")
    for i in range(1001):
        f.write("--recursive Halos/FoF/fiducial/" + str(1000+i) + "/groups_002 /media/fuffolo97/HDD1/UNI/Tesi/more/fiducial/" + str(1000+i) + "/groups_002\n")
    # for i in range(2000):
    #     f.write("--recursive 3D_cubes/zeldovich/" + str(i) + "/groups_002 /media/fuffolo97/HDD1/UNI/Tesi/3D_cubes/zeldovich/" + str(i) + "/groups_002\n")