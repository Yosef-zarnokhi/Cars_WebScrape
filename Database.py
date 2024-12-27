import sys,time
import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
import mysql
import json

car_names = ['bmw','toyota','hyundai','suzuki','mercedes-benz','porsche','dodge','ford','audi','mazda','ferrari','subaru','maserati','lamborghini','chevrolet','lexus']
animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

# how to use:
# 0 - run the program.
# 1 - wait for the program to finish web scraping, it takes a few minutes(about ~10 minutes).

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

try:
    # Connect to the database
    print("Connecting to database...")
    cnc =  mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='cars_db')
    cursor = cnc.cursor()

except Exception as e:
    print(e)

def main():
    usd = requests.get(
        'https://raw.githubusercontent.com/margani/pricedb/main/tgju/current/price_dollar_rl/latest.json')
    usdtext = usd.text
    y = json.loads(usdtext)
    dollar = int(y['p'].replace(',', '')) // 10

    print("Creating tables...")
    print("Inserting used car listings into db, Please wait...")

    for car in car_names:
        c = 0
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS `cars_db`.`{car}` (`ID` VARCHAR(200) NOT NULL PRIMARY KEY  , `name` VARCHAR(100) NOT NULL ,
                        `trim` VARCHAR(50) NOT NULL , `year` INT(4) NOT NULL , `mileage(km)` INT(100) NOT NULL , 
                       `exterior color` VARCHAR(150) NOT NULL , `interior color` VARCHAR(150) NOT NULL ,
                        `price(usd)` VARCHAR(200) NOT NULL , `price(toman)` VARCHAR(300) NOT NULL ,
                        `link` VARCHAR(300) NOT NULL ) ENGINE = InnoDB;''')
        for i in range(1,10):
            r = requests.get(f'https://www.truecar.com/used-cars-for-sale/listings/{car}/?page={c}', headers=headers)
            soup = BeautifulSoup(r.text,'html.parser')
            res = soup.find_all('div', attrs={'class' :"card-content order-3 vehicle-card-body"},limit=20)
            insert(res,dollar,car)
            c +=1
            sys.stdout.write("\r" + animation[c % len(animation)])
            sys.stdout.flush()


def insert(res,dollar,car):
    for i in res:
        mileage = (i.find('div',attrs= {'data-test':"vehicleMileage"})).text.replace(',','').replace('miles','')
        year = (i.find('span',attrs= {'class':"vehicle-card-year text-xs"})).text
        name = (i.find('span',attrs= {'class':"truncate"})).text
        trim = i.find('div',attrs = {'data-test':"vehicleCardTrim"}).text.replace('\'','')

        exterior_color,interior_color = i.find('div',attrs = {'data-test':"vehicleCardColors"}).text.split(',')
        exterior_color = exterior_color.replace('exterior','').strip()
        interior_color = interior_color.replace('interior','').strip()

        car_id = (i.find('div',attrs= {'class':"vehicle-card-vin-carousel mt-1 text-xs"})).text.replace('VIN','')
        link = (i.find('a', attrs={'class':"linkable vehicle-card-overlay order-2"}))['href']
        km = round(int(mileage)*1.609)

        reg = re.findall(r'\$(\d+,\d+)',str(i))
        try:
            if len(reg) > 2:
                price = int((reg[1]).replace(',',''))
            else:
                price = int((reg[0]).replace(',',''))
        except Exception as e:
            break
        price_toman = (price * dollar)

        try:
            cursor.execute(f'''INSERT INTO `{car}`     
             (`ID`, `name`, `trim`, `year`, `mileage(km)`,
            `exterior color`, `interior color`, `price(usd)`, `price(toman)`, `link`) 
    VALUES 
        (\'{car_id}\', \'{name}\', \'{trim}\', \'{year}\', \'{km}\', \'{exterior_color}\', \'{interior_color}\', \'{price}\', \'{price_toman}\', \'https://www.truecar.com{link}\')
    ON DUPLICATE KEY UPDATE
        `name` = \'{name}\',
        `trim` = \'{trim}\',
        `year` = \'{year}\',
        `mileage(km)` = \'{km}\',
        `exterior color` = \'{exterior_color}\', 
        `interior color` = \'{interior_color}\',
        `price(usd)`= \'{price}\',
        `price(toman)`=\'{price_toman}\',
        `link` = \'https://www.truecar.com{link}\'
        ;''')
            cnc.commit()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()

