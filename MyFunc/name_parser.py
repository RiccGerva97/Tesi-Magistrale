def info_name(name):
    """Obtain realization information from namefile"""
    # assert type(name) == str
    print("TYPE: ", type(name))
    # info = name.split('_')
    info = name.split('_')[-3:]
    print("TYPE: ", info, "\n", type(info))
    info[2] = info[2].replace(".wst", "")
    N_hgrid = info[0]
    N_WSTgrid = info[1]
    n_realiz = info[2].replace(".wst", "")
    
    return [int(N_hgrid), int(N_WSTgrid), int(n_realiz)]

# import sys
# sys.path.insert(1, './MyFunc')
# from MyFunc.name_parser import info_name
# NAME = "fiducial_coefficients_30_50_1000.wst"
# info_name(NAME)

def cosmo_parser(name):
    """Obtain cosmology from .wst file"""
    info = name.split('_')
    if info[0] == "fiducial":
        return info[0]
    elif info[0] == "zeldovich":
        return info[0]
    else:
        return info[0] + "_" + info[1]
