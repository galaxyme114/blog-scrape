import pandas as pd 
import numpy as np

router = pd.read_csv('Group073_missing_data.csv')
route = router.replace(np.nan, '', regex=True)
array = [[]]
array.clear()
for i in range(len(route)):
    array_temp = []
    array_temp.append(route['order_id'][i])
    array_temp.append(route['date'][i])
    array_temp.append(route['time'][i])
    array_temp.append(route['order_type'][i])
    if route['branch_code'][i] != '':
        array_temp.append(route['branch_code'][i])
    else:
        array_temp.append('')
    
    array_temp.append(route['order_items'][i])
    array_temp.append(route['order_price'][i])
    array_temp.append(route['customer_lat'][i])
    array_temp.append(route['customer_lon'][i])
    array_temp.append(route['customerHasloyalty?'][i])
    array_temp.append(route['distance_to_customer_KM'][i])
    array_temp.append(route['delivery_fee'][i])
    array.append(array_temp)

for line in array:
    if line[4] == '' or line[10] == '' or line[11] == '':
        print(line)
    

