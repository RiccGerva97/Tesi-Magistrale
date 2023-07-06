import readfof
import os
from tqdm import tqdm

snapnum = 2
root = '/media/fuffolo97/HDD1/UNI/Tesi/halos/'

####################################################################################

# folders = ['fiducial']
# len_dats = 150000
# for folder in folders:
#     alredy_seen = set()
#     for i in range(len_dats):
#         snapdir = root + folder +'/%d'%i
#         datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
#         if len_dats%500 == 0:
#             print("Calculating:", i/len_dats*100, "%")
#         if (len(datas.GroupMass) == len(datas.GroupLen) == len(datas.GroupPos)):
#             continue
#         else:
#             print("    Error in folder: ", i)

####################################################################################

# folders = ['fiducial', 'h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
#                     'ns_m', 'ns_p', 'Ob_m', 'Ob_p', 'Ob2_m', 'Ob2_p', 'Om_m', 'Om_p', \
#                         's8_m', 's8_p', 'w_m', 'w_p']

folders = os.listdir(root)

for folder in tqdm(folders):
    try:
        for i in tqdm(range(len(os.listdir(root+folder)))):
            snapdir = root + folder +'/%d'%i

            if os.path.isdir(snapdir) == True:
                pass
            else:
                with open("MissingDatas.dts","a") as f:
                    f.write("Missing " + snapdir + " folder realization\n")
                continue

            # try:
            datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
            # except Exception:
            #     with open("MissingDatas.dts", 'a') as f:
            #         f.write("    Missing " + snapdir + " file\n")
            #     continue

            mass = datas.GroupMass * 1e10
            # if (len(datas.GroupMass) == len(datas.GroupLen) == len(datas.GroupPos)):
            #     continue
            # else:
            #     with open("MissingDatas.dts", 'a') as f:
            #         f.write("        " + snapdir + " file corrupted\n")
            for j in range(len(mass)):
                if mass[j] < 1e13: print("\nIn ", folder, "/", i,\
                                         " there's small mass (", mass[j], ")\n")

    except Exception:
        with open("MissingDatas.dts", 'a') as f:
            f.write("\nMissing " + folder + " folder cosmology\n\n")

# folders = ['fiducial', 'h_p', 'Ob2_p']

# # DC_, Ob_, w_ non hanno le cartelle NCV_
# # Ob_ hanno solo cartelle NCV_

# for folder in tqdm(folders):
#     try:
#         if folder == "fiducial":
#             if os.path.isdir(str(root+folder)) == True:
#                 for i in tqdm(range(1000)):
#                     snapdir = root + folder +'/%d'%i
#                     if os.path.isdir(snapdir) == True:
#                         pass
#                     else:
#                         with open("MissingDatas.dts","a") as f:
#                             f.write("Missing " + snapdir + " folder realization\n")
#                         continue
#                     try:
#                         datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
#                     except Exception:
#                         with open("MissingDatas.dts", 'a') as f:
#                             f.write("    Missing " + snapdir + " file\n")
#                         continue
#                     if (len(datas.GroupMass) == len(datas.GroupLen) == len(datas.GroupPos)):
#                         continue
#                     else:
#                         with open("MissingDatas.dts", 'a') as f:
#                             f.write("        " + snapdir + " file corrupted\n")
#             else:
#                 # print("why")
#                 with open("MissingDatas.dts","a") as f:
#                     f.write("\nMissing " + folder + " folder cosmology\n\n")
#                     continue
#         else:
#             if os.path.isdir(str(root+folder)) == True:
            
#                 for i in tqdm(range(1000)):
#                     if i < 500 and "Ob_" not in folder:
#                         snapdir = root + folder +'/%d'%i
#                         if os.path.isdir(str(snapdir + "/groups_002")) == True:
#                             pass
#                         else:
#                             with open("MissingDatas.dts", "a") as f:
#                                 f.write("Missing " + folder +'/%d'%i + " folder realization\n")
#                             continue
#                         try:
#                             datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
#                         except Exception as e:
#                             with open("MissingDatas.dts", 'a') as f:
#                                 f.write("    MISSING " + folder +'/%d'%i + " FILE\n")
#                             continue
#                         if (len(datas.GroupMass) == len(datas.GroupLen) == len(datas.GroupPos)):
#                             pass
#                         else:
#                             with open("MissingDatas.dts", 'a') as f:
#                                 f.write("        " + folder +'/%d'%i + " file corrupted\n")
#                     if "DC_" in folder:
#                         continue
#                     if "Ob_" in folder:
#                         continue
#                     if "w_" in folder:
#                         continue
#                     if i >= 500 and i < 750:
#                         j = i - 500
#                         snapdir = root + folder + "/NCV_0_" + '%d'%j
#                         if os.path.isdir(str(snapdir + "/groups_002")) == True:
#                             pass
#                         else:
#                             with open("MissingDatas.dts","a") as f:
#                                 f.write("Missing " + snapdir + " folder realization\n")
#                             continue
#                         try:
#                             datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
#                         except Exception:
#                             with open("MissingDatas.dts", 'a') as f:
#                                 f.write("    Missing " + snapdir + " file\n")
#                             continue
#                         if (len(datas.GroupMass) == len(datas.GroupLen) == len(datas.GroupPos)):
#                             a=1
#                         else:
#                             with open('MissingDatas.dts', 'a') as f:
#                                 f.write("        " + snapdir + " file corrupted\n")   
#                     if i >= 750:
#                         j = i-750
#                         snapdir = root + folder + "/NCV_0_" + '%d'%j
#                         if os.path.isdir(str(snapdir + "/groups_002")) == True:
#                             pass
#                         else:
#                             with open("MissingDatas.dts","a") as f:
#                                 f.write("Missing " + snapdir + " folder realization\n")
#                             continue
#                         try:
#                             datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
#                         except Exception:
#                             with open("MissingDatas.dts", 'a') as f:
#                                 f.write("    Missing " + snapdir + " file\n")
#                             continue
#                         if (len(datas.GroupMass) == len(datas.GroupLen) == len(datas.GroupPos)):
#                             a=1
#                         else:
#                             with open('MissingDatas.dts', 'a') as f:
#                                 f.write("        " + snapdir + " file corrupted\n")
            
#             else:
#                 # print("why")
#                 with open("MissingDatas.dts","a") as f:
#                     f.write("\nMissing " + folder + " folder cosmology\n\n")
#                     continue

#     except Exception:
#         with open("MissingDatas.dts", 'a') as f:
#             f.write("\nMissing " + folder + " folder cosmology\n\n")

              
#             #     for i in tqdm(range(500)):
#             #         snapdir = root + folder +'/%d'%i
#             #         if os.path.isdir(str(snapdir + "/groups_002")) == True:
#             #             pass
#             #         else:
#             #             with open("MissingDatas.dts","a") as f:
#             #                 f.write("Missing " + snapdir + " folder realization\n")
#             #             continue
#             #         try:
#             #             datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
#             #         except Exception as e:
#             #             with open("MissingDatas.dts", 'a') as f:
#             #                 f.write("    Missing " + snapdir + " FILE\n")
#             #             continue
#             #         if (len(datas.GroupMass) == len(datas.GroupLen) == len(datas.GroupPos)):
#             #             pass
#             #         else:
#             #             with open("MissingDatas.dts", 'a') as f:
#             #                 f.write("        " + snapdir + " file corrupted\n")
#             #     if "DC_" in folder:
#             #         continue
#             #     if "Ob_" in folder:
#             #         continue
#             #     if "w_" in folder:
#             #         continue
#             #     for j in tqdm(range(2)):    
#             #         for i in tqdm(range(250)):
#             #             snapdir = root + folder + "/NCV_" + str(j) + '_%d'%i
#             #             if os.path.isdir(str(snapdir + "/groups_002")) == True:
#             #                 pass
#             #             else:
#             #                 with open("MissingDatas.dts","a") as f:
#             #                     f.write("Missing " + snapdir + " folder realization\n")
#             #                 continue
#             #             try:
#             #                 datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
#             #             except Exception:
#             #                 with open("MissingDatas.dts", 'a') as f:
#             #                     f.write("    Missing " + snapdir + " file\n")
#             #                 continue
#             #             if (len(datas.GroupMass) == len(datas.GroupLen) == len(datas.GroupPos)):
#             #                 a=1
#             #             else:
#             #                 with open('MissingDatas.dts', 'a') as f:
#             #                     f.write("        " + snapdir + " file corrupted\n")
#             # else:
#             #     with open("MissingDatas.dts","a") as f:
#             #        f.write("\nMissing " + folder + " folder cosmology\n\n")

