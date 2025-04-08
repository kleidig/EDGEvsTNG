import numpy as np
import h5py
import os
from hydrotools.interface import interface as iface_run
from hydrotools.illustris import illustris_common as ils_com

###################################################################################################

def main():

    config_dict = config()

	#----------------------------------------------------------------------------------------------
	# Get relevant properties from all galaxies in the simulation
	#----------------------------------------------------------------------------------------------
    get_galaxy_properties(config_dict, sim = 'tng35', snap_z = 0.0)


    return

###################################################################################################

def config(user='kleidig'):

    config_dict = {}

    nodename = os.uname().nodename

    if nodename.endswith('.astro.umd.edu'):
        node = nodename[:-14]
        config_dict['machine'] = 'umdastro'
    
    config_dict['output_path'] = f'/{node}a/{user}/'

    if node.startswith('astra'):
        config_dict['num_processes'] = 60

    return config_dict

def get_galaxy_properties(c_dict, sim, snap_z, output_dir='', file_suffix=''):
    '''
    extract properties from all galaxies in the simulation snapshot in order to make cuts 
    '''

    output_path = c_dict['output_path'] + output_dir
    
    # define fields to extract from subhalos/galaxies
    catsh_fields = ['SubhaloSFR', 'SubhaloMassType', 
					'SubhaloMassInHalfRadType', 'SubhaloHalfmassRadType',
					'SubhaloGasMetallicity']
	
    #define other scalar values to extract
    scalar_fields = ['m_neutral',
					 'm_neutral_2rad',
					 'm_neutral_H',
					 'm_neutral_H_2rad',
					 'gas_metal_H',
					 'gas_metallicity']

    #call hydrotools
    iface_run.extractGalaxyData(machine_name = c_dict['machine'], 
								num_processes = c_dict['num_processes'],
								output_path = output_path,
								file_suffix = 'properties',
								
                                sim = sim, snap_z = snap_z,
								Mstar_min = 1.2e7,
                                Mgas_min = 1.2e7,
								
                                # get fields from subhalos
                                catsh_get =True, catsh_fields= catsh_fields,
								
                                # get HI/ H2 fields
								hih2_get=True, hih2_fields= ils_com.default_hih2_fields,
								
                                #get other scalar values
								scalar_get= True, scalar_fields=scalar_fields)
								
    return

###################################################################################################
# Trigger
###################################################################################################

if __name__ == "__main__":
	main()
