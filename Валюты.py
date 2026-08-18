import requests
import json
database={}

url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'

response = requests.get(url ) 
content= response.json()

        
while True:
        choice= input("""Оберіть дію:
                Подивитись курс-+
                Порахувати курс- -  """)
        if choice == '+':
                value = input(
                        """Оберіть валюту для отримання курсу
                        USD-1
                        EUR-2, 
                        GBP(Британський фунт)-3
                        CHF(Швейца́рський фран)-4 
                        PLN(Зло́тий)-5 
                        Вихід-6""")
        for item in content:
                if value == '1' and item['cc'] == 'USD':
                                database[item['cc']] = item['rate']
                                print(f"Курс долару {item['txt'], item['cc'], item['rate'], item['exchangedate']}")
                                
                if value == '2' and item['cc'] == 'EUR':
                                database[item['cc']] = item['rate']
                                print(f"Курс євро {item['txt'], item['cc'], item['rate'], item['exchangedate']}")
                                
                if value == '3' and item['cc'] == 'GBP':
                                database[item['cc']] = item['rate']

                                print(f"Курс фунту {item['txt'],item['cc'], item['rate'], item['exchangedate']} ")
                                
                if value == '4' and item['cc'] == 'CHF':
                                database[item['cc']] = item['rate']
                                print(f"Курс фран {item['txt'],item['cc'], item['rate'], item['exchangedate']} ")
                                
                if value == '5' and item['cc'] == 'PLN':
                                database[item['cc']] = item['rate']
                        
                                print(f"Курс злотих {item['txt'],item['cc'], item['rate'], item['exchangedate']} ")
                if value == '6':
                                print('Вихід')
                                break
        if choice == '-':
                value_2 = input(
                                        """Оберіть валюту для отримання курсу
                                        USD-1
                                        EUR-2, 
                                        GBP(Британський фунт)-3
                                        CHF(Швейца́рський фран)-4 
                                        PLN(Зло́тий)-5 
                                        Вихід-6""")
                for item in content:
                                if value_2 == '1' and item['cc'] == 'USD':
                                                database[item['cc']] = item['rate']
                                                print(f"Курс долару {item['txt'], item['cc'], item['rate'], item['exchangedate']}")
                                                
                                if value_2 == '2' and item['cc'] == 'EUR':
                                                database[item['cc']] = item['rate']
                                                print(f"Курс євро {item['txt'], item['cc'], item['rate'], item['exchangedate']}")
                                                
                                if value_2 == '3' and item['cc'] == 'GBP':
                                                database[item['cc']] = item['rate']
                
                                                print(f"Курс фунту {item['txt'],item['cc'], item['rate'], item['exchangedate']} ")
                                                
                                if value_2 == '4' and item['cc'] == 'CHF':
                                                database[item['cc']] = item['rate']
                                                print(f"Курс фран {item['txt'],item['cc'], item['rate'], item['exchangedate']} ")
                                                
                                if value_2 == '5' and item['cc'] == 'PLN':
                                                database[item['cc']] = item['rate']
                                        
                                                print(f"Курс злотих {item['txt'],item['cc'], item['rate'], item['exchangedate']} ")
                                if value_2 == '6':
                                                print('Вихід')
                                                break
                



    
    