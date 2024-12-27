import mysql.connector
import mysql
import time
from tabulate import tabulate
s = time.process_time()
car_names = ['bmw','toyota','hyundai','suzuki','mercedes-benz','porsche','dodge','ford','audi','mazda','ferrari','subaru','maserati','lamborghini','volkswagen','chevrolet','lexus']

# how to use:
# 0 - run the program.
# 1 - enter a car model or use --help to see all the models.
# 2 - enter your price range for example 20000 to 25000.
# 3 - the program will output 5 best matches for your price range.

try:
    print("Connecting to database...")
    cnc =  mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='cars_db')     # Connect to the database
    cursor = cnc.cursor()

except Exception as e:
    print(e)



print('Welcome! follow the steps to find your desired car!')
print('--------------------------------------------------')
brand = input(f"What car brand do you want?\nuse --help to see list of car brands: ")
while True:
    if brand in car_names:
        break
    elif '--help' in brand:
        print(f'list of cars: {car_names}')
        brand = input("please enter a valid car brand: ")
    else:
        brand = input("please enter a valid car brand: ")

price = input("enter your price range(usd) exp(20000 to 30000): ")
while True:
    if 'to' in price:
        price = price.split('to')
        break
    else:
        price = input("please enter your price range correctly: ")

cursor.execute(f'SELECT * FROM `{brand}` WHERE name LIKE \'%{brand}%\' AND `price(usd)` BETWEEN {price[0].strip()} AND {price[1].strip()}  ORDER BY `mileage(km)`')
cars = cursor.fetchall()
list1 = [['Car model', 'year', 'mileage(km)', 'price(usd)', 'link']]

count = 0
if len(cars) == 0:
    print("No cars found!")
else:
    print("\nHere are the best matches for your price range:")
    for i in cars:
        list1.append([i[1], i[3],f"{int(i[4]):,}", f"{int(i[7]):,}", i[9]])
        #print(f"Car model = {i[1]} year = {i[3]} mileage = {i[4]}, price = {i[7]}, link = {i[9]}")
        count+=1
        if count == 5:
            break
    print(tabulate(list1, headers='firstrow',tablefmt='grid'))
