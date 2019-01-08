import matplotlib.pyplot as plt


def station_map(svalbard_data, eureka_data, dragon_data):
    ax1 = svalbard_data.plot_station_coordinates(marker='*', markersize=200, color='red', label='Svalbard - AERONET')
    eureka_data.plot_station_coordinates(marker='^', markersize=200, color='blue', ax=ax1, label='Eureka - AERONET')
    dragon_data.plot_station_coordinates(markersize=100, color='lime', ax=ax1, label='DRAGON')
    ax1.background_patch.set_alpha(0)
    plt.title("Observation Stations")
    # plt.savefig('results/obs_stations.png')
