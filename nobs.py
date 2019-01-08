import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def read_nobs(file_path, var_code):
    IN_DATA = False
    col_index = None
    time_vals = []
    num_meas = []
    with open(file_path) as f:
        for line in f:
            if IN_DATA:
                data = line.strip().split(',')

                date_str = data[1]
                time_str = data[2]
                day, month, year = date_str.split(':')
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, time_str])
                datestring = '+'.join([datestring, '00:00'])
                time_vals.append(np.datetime64(datestring))
                num_meas.append(int(data[col_index]))
            if var_code in line:
                IN_DATA = True
                cols = line.strip().split(',')
                col_index = cols.index(var_code)
    import pandas as pd
    nobs=pd.Series(num_meas, time_vals)
    return(nobs)



def plot_nobs(var_code, var_name, eureka_path_list, eureka_data):
    for j in range(len(var_code)):
        fig = plt.figure(figsize=(14,7))
        for i in range(len(eureka_path_list)):
            num_obs_i = read_nobs(eureka_path_list[i], var_code[j])

            plt.subplot(len(eureka_path_list), 1, i+1 )
            num_obs_i.plot(label=eureka_data.station_name[i], marker='*', linestyle='None')

            plt.ylabel('number of obs.')
            plt.legend()
            plt.suptitle('Number of observations per day', y=1.08)
            fig.tight_layout() 


            num_obs_i = pd.DataFrame({'time':num_obs_i.index, 'nobs_' + var_name[j] + '_' +eureka_data.station_name[i]:num_obs_i.values})



            if ((j == 0) & (i==0)):
                num_obs_df = num_obs_i
            else:
                num_obs_df = num_obs_df.merge(num_obs_i, how='outer')
        #plt.savefig('results/num_obs_daily.png')
        plt.show()
        
        return num_obs_df

    

def write_df(df, data, model1, model2, model3, lat_aeronet, lon_aeronet):
    # Remove NaNs and records with less than 10 measurements.
    df = df.dropna(how='any') 
    df = df[(df['nobs_aod_OPAL'] > 10) & (df['nobs_aod_PEARL'] > 10)]  
    
    # Append AOD and Angstrom exponent to the data frame num_obs
    for i, name in enumerate(data.station_name):
        station_data = data[i]

        station_data_aod = pd.DataFrame({'time':station_data.od550aer.index,'aod_'+ data.station_name[i]:station_data.od550aer.values})

        station_data_ang = pd.DataFrame({'time':station_data.ang4487aer.index, 'ang_' + data.station_name[i]:station_data.ang4487aer.values})

        df = df.merge(station_data_aod, how='left')
        df = df.merge(station_data_ang, how='left')

    df.set_index('time', inplace=True)
    df.index = df.index.date
    
    # Add models
    
    
    ecmwf_aod_PEARL = model1['od550aer'].sel(lat=lat_aeronet, lon= 360 - abs(lon_aeronet), method='nearest')
    ecmwf_aod_PEARL = ecmwf_aod_PEARL.to_dataframe().drop(columns=['lat', 'lon']).rename(index=str, columns={"od550aer": "ecmwf_aod_PEARL"})
    ecmwf_aod_PEARL.index = pd.to_datetime(ecmwf_aod_PEARL.index).date

    ecmwf_ang_PEARL = model2['ang4487aer'].sel(lat=lat_aeronet, lon= 360 - abs(lon_aeronet), method='nearest')
    ecmwf_ang_PEARL = ecmwf_ang_PEARL.to_dataframe().drop(columns=['lat', 'lon']).rename(index=str, columns={"ang4487aer": "ecmwf_ang_PEARL"})
    ecmwf_ang_PEARL.index = pd.to_datetime(ecmwf_ang_PEARL.index).date

    sprintars_aod_PEARL = model3['od550aer'].sel(lat=lat_aeronet, lon= 360 - abs(lon_aeronet), method='nearest')
    sprintars_aod_PEARL = sprintars_aod_PEARL.to_dataframe().drop(columns=['lat', 'lon']).rename(index=str, columns={"od550aer": "sprintars_aod_PEARL"})
    dtime = sprintars_aod_PEARL.index
    sprintars_aod_PEARL.index = pd.to_datetime(dtime.to_series())
    sprintars_aod_PEARL = sprintars_aod_PEARL.resample('D', how='mean')
    
    df = df.merge(ecmwf_aod_PEARL, left_index=True, right_index=True, how='left')
    df = df.merge(ecmwf_ang_PEARL, left_index=True, right_index=True, how='left')
    df = df.merge(sprintars_aod_PEARL, left_index=True, right_index=True, how='left')


    
    
    
    return df, ecmwf_aod_PEARL

    