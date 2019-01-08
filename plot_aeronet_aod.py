import matplotlib.pyplot as plt


def plot_aeronet_aod(svalbard_data, eureka_data):
    plt.figure(figsize=(14,7))

    # dictionaty with latitudes
    # For svalbard I only 
    lat_svalbard = {}
    lon_svalbard = {}

    lat_eureka = {}
    lon_eureka = {}

    for i, name in enumerate(svalbard_data.station_name):
        #ax = station_data.od550aer.plot() 
        station_data = svalbard_data[i]
        #plt.plot(station_data.od550aer)
        plt.subplot(2, 1, 1)
        if i ==2:
            station_data.od550aer.resample('M').mean().plot(label = name, linewidth=3, colors='m')
        else:
            station_data.od550aer.resample('M').mean().plot(label = name, linewidth=3)

        lat_svalbard[name] = station_data.latitude
        lon_svalbard[name] = station_data.longitude
    plt.legend(loc='upper right')
    plt.title('Svalbard')
    plt.ylabel('AOD')


    for i, name in enumerate(eureka_data.station_name):
        station_data = eureka_data[i]
        plt.subplot(2, 1, 2)
        station_data.od550aer.resample('M').mean().plot(label = name, linewidth=3)
        lat_eureka[name] = station_data.latitude
        lon_eureka[name] = station_data.longitude
    plt.legend(loc='upper right')
    plt.title('Eureka')
    plt.ylabel('AOD')
    plt.tight_layout()
    
    plt.show
    #plt.savefig('results/aeronet_measurements.png')
    