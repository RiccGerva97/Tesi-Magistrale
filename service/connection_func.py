import os, subprocess
# from multiprocessing import Pool, cpu_count

# cosmology index
i = 0

# relization index
k = 0

cosmo_list = ['h_m', 'h_p',
              'ns_m', 'ns_p',
              'Om_m', 'Om_p',
              'Ob2_m', 'Ob2_p',
              's8_m', 's8_p',
              'w_m', 'w_p',
              'fiducial', 'fiducial_ZA']

# source folder
src = "/home/ricc/Snapshots/" + cosmo_list[i] + '/' + str(k) + "/snapdir_000/"
# destination folder
dest = "/workplace/riccardo/Snapshots/" + cosmo_list[i] + '/' + str(k) + '/snapdir_000/'

# def transfer2Doraemon():
    