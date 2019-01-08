import pyaerocom as pya

def print_loc(Opal, Pearl):
    print('Location of Opal: ', round(Opal.latitude, 2),'N, ', round(Opal.longitude, 2), 'E' )
    print('Location of Pearl: ', round(Pearl.latitude, 2), 'N, ', round(Pearl.longitude, 2), 'E' )
    print('Altitude of Opal: ', round(Opal.altitude, 2), 'm' )
    print('Altitude of Pearl: ', round(Pearl.altitude, 2), 'm' )

