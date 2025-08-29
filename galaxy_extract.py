import numpy as np
import h5py
import os
from hydrotools.interface import interface as iface_run
from hydrotools.illustris import illustris_common as ils_com

###################################################################################################

def main():

    config_dict = config(number_processes=35)

	#----------------------------------------------------------------------------------------------
	# Get relevant properties from all galaxies in the simulation
	#----------------------------------------------------------------------------------------------
    get_galaxy_properties(config_dict, sim = 'tng35', snap_z = 0.0)


    return

###################################################################################################

def config(user='kleidig', number_processes = 'default'):

    config_dict = {}

    nodename = os.uname().nodename

    if nodename.endswith('.astro.umd.edu'):
        node = nodename[:-14]
        config_dict['machine'] = 'umdastro'
    
    config_dict['output_path'] = f'/{node}a/{user}/'

    if node.startswith('astra'):
        if number_processes == 'default':
            config_dict['num_processes'] = 40
        else:
            config_dict['num_processes'] = number_processes

    return config_dict

def get_galaxy_properties(c_dict, sim, snap_z, output_dir='', file_suffix=''):
    '''
    extract properties from all galaxies in the simulation snapshot in order to make cuts 
    '''

    output_path = c_dict['output_path'] + output_dir
    
    # define fields to extract from subhalos/galaxies
    catsh_fields = ['SubhaloSFR', 
                    'SubhaloSFRinHalfRad', 
                    'SubhaloSFRinMaxRad', 
                    'SubhaloSFRinRad',
                    
                    ###
                    'SubhaloMassType',
                    'SubhaloMassInHalfRadType',  
                    'SubhaloMassInMaxRadType',
                    'SubhaloMassInRadType', 
                         
                    ###
                    'SubhaloGasMetalFractions',
                    'SubhaloGasMetalFractionsHalfRad',
                    'SubhaloGasMetalFractionsMaxRad',
                    'SubhaloGasMetalFractionsSfr',
                    'SubhaloGasMetalFractionsSfrWeighted'

                    ####
					'SubhaloGasMetallicity',
                    'SubhaloGasMetallicityHalfRad', 
                    'SubhaloGasMetallicityMaxRad'
                    'SubhaloGasMetallicitySfr',
                    'SubhaloGasMetallicitySfrWeighted',
                    
                    ###
                    'SubhaloHalfmassRadType',
                    'SubhaloVmaxRad']
	
    #define other scalar values to extract
    scalar_fields = ['m_neutral',
					 'm_neutral_2rad',
					 'm_neutral_H',
					 'm_neutral_H_2rad',
					 'gas_metal_H',
					 'gas_metallicity']
    
    #profile fields

    profile_fields = ['gas_metallicity_2d',
                      'sfr_2d',
                      'f_mol_L08_2d', 'f_mol_GK11_2d',
                      'f_mol_GD14_2d', 'f_mold_K13_2d', 'f_mol_S14_2d',
                      'gas_rho_2d',
                      'f_neutral_H_2d',
                      'rho_neutral_H_2d', 
                      'f_electron_2d']

    #call hydrotools
    iface_run.extractGalaxyData(machine_name = c_dict['machine'], 
								num_processes = c_dict['num_processes'],
								output_path = output_path,
								file_suffix = 'properties',
								
                                sim = sim, snap_z = snap_z,
								Mstar_min = 1.2e7,
                                Mgas_min = 1.2e7,
								
                                # get fields from subhalos
                                catsh_get = True, catsh_fields = catsh_fields,
								
                                # get HI/ H2 fields
								hih2_get = True, hih2_fields = ils_com.default_hih2_fields,
								
                                # get other scalar values
								scalar_get = True, scalar_fields = scalar_fields,
                                
                                # get profiles 
                                profile_get = True, profile_fields = profile_fields,
                                profile_range_rgas = 3.5, profile_range_rstr = 6)
								
    return

###################################################################################################
# Trigger
###################################################################################################

if __name__ == "__main__":
	main()
