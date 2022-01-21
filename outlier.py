import pandas as pd 
import numpy as np

clean = pd.read_csv('Group073__dirty_data_solution.csv')
array = [[]]
array.clear()
temp = []
for i in range(3):
    array_temp = []
    array_temp.append(clean['customer_lat'][i])
    array_temp.append(clean['customer_lon'][i])
    array_temp.append(clean['customerHasloyalty?'][i])
    temp.append(clean['delivery_fee'][i])
    array.append(array_temp)


A = np.array(array)
B = np.array(temp) 

# linalg.solve is the function of NumPy to solve a system of linear scalar equations
print("Solutions:\n",np.linalg.solve(A, B ))

