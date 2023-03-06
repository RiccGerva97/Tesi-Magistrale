order_folders = {
    'fiducial'  : 0,
    'h_m'       : 1,
    'h_p'       : 2,
    'Mnu_p'     : 3,
    'Mnu_pp'    : 4,
    'Mnu_ppp'   : 5,
    'ns_m'      : 6,
    'ns_p'      : 7,
    'Ob_m'      : 8,
    'Ob_p'      : 9,
    'Ob2_m'     : 10,
    'Ob2_p'     : 11,
    'Om_m'      : 12,
    'Om_p'      : 13,
    's8_m'      : 14,
    's8_p'      : 15,
    'w_m'       : 16,
    'w_p'       : 17
}

boolean = {
    'True' : 1,
    'TRUE' : 1,
    'true' : 1,
    'False' : 0,
    'FALSE' : 0,
    'false' : 0
 }

COSMOPAR = {
    """dictionary to assegnate to a cosmology its parameters
 #                  | Om_m | Om_b |   h   |  n_s  | s_8 | Mnu | w |
    """
    # 'DC_m' :        [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0, -1],
    # 'DC_p' :        [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0, -1],
    
    'fiducial' :    [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0, -1],
    # 'fiducial_HR' : [],
    # 'fiducial_LR' : [],
    # 'fiducial_ZA' : [],
    
    'h_m' :         [0.3175, 0.049, 0.6510, 0.9624, 0.834, 0, -1],
    'h_p' :         [0.3175, 0.049, 0.6912, 0.9624, 0.834, 0, -1],
    
    'Mnu_p' :       [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0.1, -1],
    'Mnu_pp' :      [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0.2, -1],
    'Mnu_ppp' :     [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0.4, -1],
    
    'ns_m' :        [0.3175, 0.049, 0.6711, 0.9432, 0.834, 0, -1],
    'ns_p' :        [0.3175, 0.049, 0.6711, 0.9816, 0.834, 0, -1],
    
    'Ob_m' :        [0.3175, 0.049*0.98, 0.6711, 0.9624, 0.834, 0, -1],
    'Ob_p' :        [0.3175, 0.049*1.02, 0.6711, 0.9624, 0.834, 0, -1],
    'Ob2_m' :       [0.3175, 0.049*0.96, 0.6711, 0.9624, 0.834, 0, -1],
    'Ob2_p' :       [0.3175, 0.049*1.04, 0.6711, 0.9624, 0.834, 0, -1],
    
    'Om_m' :        [0.3075, 0.049, 0.6711, 0.9624, 0.834, 0, -1],
    'Om_p' :        [0.3275, 0.049, 0.6711, 0.9624, 0.834, 0, -1],
    
    's8_m' :        [0.3175, 0.049, 0.6711, 0.9624, 0.834*0.982, 0, -1],
    's8_p' :        [0.3175, 0.049, 0.6711, 0.9624, 0.834*1.018, 0, -1],
    
    'w_m' :         [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0, -0.95],
    'w_p' :         [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0, -1.05]
}