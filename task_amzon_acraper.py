import requests ,json
import pandas as pd
from bs4 import BeautifulSoup
import mysql.connector


connection = mysql.connector.connect(

    host="localhost",
    user="root",
    #   password="ITSYS5o!utions",
    password='',
    database="amazon_data"
    )

cursor = connection.cursor()


cursor.execute("SELECT * FROM data_table")

myresult = cursor.fetchall()


headers ={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}




for key in myresult:
    if 'X' in key[2]:
        product_key = key[2]

        country = key[3]

        url = f'https://www.amazon.{country}/dp/{product_key}'
        print(url)
        response = requests.get(url ,headers=headers)
        
        if response.status_code != 200:
            print(url,'---->',response.status_code)
            continue

        soup = BeautifulSoup(response.text,'lxml')

        Product_Title = soup.find('span',{'id':'productTitle'}).text.strip().replace('  ',' ').strip()
        try:Product_Image_URL =  soup.find('div',{'id':'imgTagWrapperId'}).find('img')['src']
        except: Product_Image_URL =soup.find('div',{'id':'img-canvas'}).find('img')['src']
        try:Price_of_the_Product = soup.find('span',{'class':'a-offscreen'}).text.strip().split('\xa0')[1]+soup.find('span',{'class':'a-offscreen'}).text.strip().split('\xa0')[0]
        except:
            try:Price_of_the_Product = soup.find('span',{'class':'a-offscreen'}).text.strip()
            except: Price_of_the_Product = '<NISSING>'
        pd_d = soup.find('ul',{'class':'a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list'}).find_all('li')
        pd_ds = []
        for details in pd_d:
            a = details.find('span',{'class':'a-text-bold'}).text.split(':')[0].replace('\u200e','').replace('\u200f','').replace('\n','').strip()
            b =str(pd_d[1]).split('</span> <span>')[1].split('<')[0]
            Product_Details = a+':'+b
            pd_ds.append(Product_Details)
        
        dt={
            'Product_Title':Product_Title,
            'Product_Image_URL':Product_Image_URL,
            'Price_of_the_Product':Price_of_the_Product,
            'Product_Details':pd_ds,
            }
        # js_data.append(dt)
        json_data = json.dumps(dt)
        sql = "INSERT INTO am_json (json_column) VALUES (%s)"
        cursor.execute(sql, (json_data,))
        connection.commit() 



