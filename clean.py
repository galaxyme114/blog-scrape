import pandas as pd 
import csv 
import datetime
from zipfile import *
import time
import os 

def clean_data_function(value):
    
    array = [[]]
    array.clear()
    for i in range(len(clean)):
        array_temp = []
        array_temp.append(clean['order_id'][i])
        if '-' in clean['date'][i]:
            array_temp.append(datetime.datetime.strptime(clean['date'][i], "%Y-%d-%m").strftime("%d/%m/%Y"))
            print("Error is discovered in Column date." , i)
        else:
            array_temp.append(clean['date'][i])
        array_temp.append(clean['time'][i])

        if clean['time'][i] > '12:00:01' and clean['time'][i] < '16:00:01':
            if clean['order_type'][i] == 'Lunch':
                array_temp.append(clean['order_type'][i])
            else:
                print("Error is discovered in Column order_type.", i)
                array_temp.append("Lunch")
        elif clean['time'][i] > '16:00:01' and clean['time'][i] < '24:00:00':
            if clean['order_type'][i] == 'Dinner':
                array_temp.append(clean['order_type'][i])
            else:
                print("Error is discovered in Column order_type.", i)
                array_temp.append("Dinner")
        else:
            if clean['order_type'][i] == 'Breakfast':
                array_temp.append(clean['order_type'][i])
            else:
                print("Error is discovered in Column order_type.", i)
                array_temp.append("Breakfast")
        
        array_temp.append(clean['branch_code'][i].upper())
        array_temp.append(clean['order_items'][i])
        array_temp.append(clean['order_price'][i])
        if clean['customer_lat'][i] > 0 and clean['customer_lon'][i] < 0:
            print("Error is discovered in Column customer_lat and customer_lon.", i)
            array_temp.append(clean['customer_lon'][i])
            array_temp.append(clean['customer_lat'][i])
        elif clean['customer_lat'][i] > 0:
            print("Error is discovered in Column customer_lat.", i)
            array_temp.append('-' + str(clean['customer_lat'][i]))
            array_temp.append(clean['customer_lon'][i])
        
        else:
            array_temp.append(clean['customer_lat'][i])
            array_temp.append(clean['customer_lon'][i])
        array_temp.append(clean['customerHasloyalty?'][i])
        array_temp.append(clean['distance_to_customer_KM'][i])
        array_temp.append(clean['delivery_fee'][i])
        array.append(array_temp)
    #print(array)
    return array

def make_clean(array, file_name):
    header = ['order_id', 'date', 'time', 'order_type','branch_code', 'order_items', 'order_price', 'customer_lat', 'customer_lon', 'customerHasloyalty?', 'distance_to_customer_KM', 'delivery_fee']
    if not os.path.exists(file_name):
        with open(file_name, 'a', newline='', encoding="utf-8") as f:
            
            writer = csv.writer(f, delimiter=',')
            writer.writerow(header)  # write the header
            for line in array:
                writer.writerow(line)
    
    

def zip(file_name):
    with ZipFile(file_name.split('.')[0] + '_ass' + '.zip', 'w') as zip:
        zip.write(file_name)
    zip.close()

def outlier():

    outlier = pd.read_csv('Group073_outlier_data.csv')

    Q1 = outlier['delivery_fee'].quantile(.25)
    Q3 = outlier['delivery_fee'].quantile(.75)
    q1 = Q1-1.5*(Q3-Q1)
    q3 = Q3+1.5*(Q3-Q1)
    final = outlier[outlier['delivery_fee'].between(q1, q3)]
    print("Detect and remove outlier rows")
    print("outlier rows:", outlier[outlier['delivery_fee'] >q3])
    print("outlier rows:", outlier[outlier['delivery_fee'] <q1])
    final.to_csv('Group073__outlier_data_solution.csv', index=False)

if __name__ == '__main__':

    clean = pd.read_csv('Group073_dirty_data.csv')
    file_name = 'Group073__dirty_data_solution.csv'
    array = clean_data_function(clean)
    make_clean(array, file_name)
    time.sleep(3)
    zip(file_name)
    outlier()

