import mysql.connector
import mysql
from sklearn import tree
from time import sleep

# how to use:
# 0 - run the program.
# 1 - enter a car model or use --help to see all the models.
# 2 - after the program finishes training, enter a year and the mileage.
# 3 - the program will predict a price for you.

car_names = ['bmw','toyota','hyundai','suzuki','mercedes-benz','porsche','dodge','ford','audi','mazda','ferrari','subaru','maserati','lamborghini','volkswagen','chevrolet','lexus']
x = []
y = []

try:
    print("Connecting to database...")
    cnc =  mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='cars_db')     # Connect to the database
    cursor = cnc.cursor()
except Exception as e:
    print(e)

brand = input(f"What car do you want to train with?\nuse --help to see list of car brands: ")
while True:
    if brand in car_names:
        break
    elif '--help' in brand:
        print(f'list of cars: {car_names}')
        brand = input("please enter a valid car brand: ")
    else:
        brand = input("please enter a valid car brand: ")

cursor.execute(f'SELECT * FROM `{brand}`')
cars = cursor.fetchall()

for car in cars:
    x.append([car[3],car[4]])
    y.append(car[7])

try:
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x,y)
    print("Successfully trained...")
    sleep(1)
except Exception as e:
    print(e)

p_year = input("Now you can predict car price with machine learning by entering the year and mileage of the car\ncar year:")
p_mile = input("car mileage: ")
p_price = clf.predict([[p_year, p_mile]])
print(f"predicted price = {int(p_price[0]):,} usd")
