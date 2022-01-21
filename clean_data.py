'''
import numpy as np
EARTH_R = 6372.8

def geocalc(lat0, lon0, lat1, lon1):
    """Return the distance (in km) between two points
    in geographical coordinates."""
    lat0 = np.radians(lat0)
    lon0 = np.radians(lon0)
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    dlon = lon0 - lon1
    y = np.sqrt((np.cos(lat1) * np.sin(dlon)) ** 2 +
        (np.cos(lat0) * np.sin(lat1) - np.sin(lat0) *
         np.cos(lat1) * np.cos(dlon)) ** 2)
    x = np.sin(lat0) * np.sin(lat1) + \
        np.cos(lat0) * np.cos(lat1) * np.cos(dlon)
    c = np.arctan2(y, x)
    print(EARTH_R * c)
    return EARTH_R * c

if __name__ == "__main__":
    
    np.sum(geocalc(-37.7738026, 144.9836466, -37.8132093, 145.014444199999))


import datetime
dayofweek = datetime.date(1994, 2, 10).strftime("%A")
print(dayofweek)
'''
import numpy as np
# define matrix A using Numpy arrays
A = np.array([[2, 1, 1],
 [1, 3, 2],
 [1, 6, 0],
 [1, 6, 0]]) 

#define matrix B
B = np.array([4, 5, 6, 7]) 

# linalg.solve is the function of NumPy to solve a system of linear scalar equations
print("Solutions:\n",np.linalg.solve(A, B ))
