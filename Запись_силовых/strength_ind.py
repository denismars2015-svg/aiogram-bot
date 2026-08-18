import json


            
     # database['exercise']={} #ключ
      #database['exercise']={'Грудь' : [] , 'Спина'  : [] , 'Ноги' : [] , 'Плечі' : [] , 'Руки' : [] } #добавить данные внутри словаря 

try:
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)
except FileNotFoundError:
      database = {'exercise': {'Грудь': [], 'Спина': [], 'Ноги': [], 'Плечі': [], 'Руки': []}}
def  exercise(database,my_ex, **kwargs):
            database[my_ex]=kwargs

def workouts(database,date_id, **kwargs):
      database[date_id] = kwargs 

while True:

      choice=input("""Оберіть дію:
                  Створити вправу-1
                  Редагувати вправу-2
                  Видалити вправу-3
                  Подивитись вправи -4
                  Створити тренування - 5  
                  Додати вправи до тренування-6   
                  Подивитись вправи за  тренування - 7
                  Подивитись статистику вправ - 8 
                  Редагувати тренування - 9
                  Видалити вправу за тренування - 10     """)

      if choice == '1' : 

            type_ex = input("""Оберіть группу м'язів:
                              Грудь-1
                              Спина-2
                              Ноги-3
                              Плечі-4
                              Руки-5  """)

            if type_ex == '1':

                  chest_ex = input("Додайте вправу на грудь")
                  database['exercise']['Грудь'].append(chest_ex) #добавление в словарь
                  print(f"Вправа {chest_ex} додана")

            elif type_ex == '2' :

                  back_ex = input("Додайте вправу на спину")
                  database['exercise']['Спина'].append(back_ex)
                  print(f"Вправа {back_ex} додана")

            elif type_ex == '3':
            
                  leg_ex = input("Додайте вправу на ноги")
                  database['exercise']['Ноги'].append(leg_ex)
                  print(f"Вправа {leg_ex} додана")

            elif type_ex == '4':

                  
                  shoulder_ex = input("Додайте вправу на плечі")
                  database['exercise']['Плечі'].append(shoulder_ex)
                  print(f"Вправа {shoulder_ex} додана")

            elif type_ex == '5':

                  arm_ex = input("Додайте вправу на руки")
                  database['exercise']['Руки'].append(arm_ex)
                  print(f"Вправа {arm_ex} додана")
      elif choice == '2':
            edit_ex = input("""Оберіть группу м'язів для редагування 
                                          Грудь-1
                                          Спина-2
                                          Ноги-3
                                          Плечі-4
                                          Руки-5  """)
            if edit_ex == '1':
                  for number, data in enumerate(database['exercise'] ['Грудь']):
                               
                               print(f"Номер {number}, вправа: {data}")
                  ex_index=int(input("Введіть номер вправи "))
                  new_name_ex=input("Введіть нове ім'я")
                  database['exercise']['Грудь'][ex_index] = new_name_ex

            elif edit_ex == '2':
                              for number, data in enumerate(database['exercise'] ['Спина']):
                                           
                                           print(f"Номер {number}, вправа: {data}")
                              ex_index=int(input("Введіть номер вправи "))
                              new_name_ex=input("Введіть нове ім'я")
                              database['exercise']['Спина'][ex_index] = new_name_ex
            elif edit_ex == '3':
                              for number, data in enumerate(database['exercise'] ['Ноги']):
                                           
                                           print(f"Номер {number}, вправа: {data}")
                              ex_index=int(input("Введіть номер вправи "))
                              new_name_ex=input("Введіть нове ім'я")
                              database['exercise']['Ноги'][ex_index] = new_name_ex
            elif edit_ex == '4':
                              for number, data in enumerate(database['exercise'] ['Плечі']):
                                           
                                           print(f"Номер {number}, вправа: {data}")
                              ex_index=int(input("Введіть номер вправи "))
                              new_name_ex=input("Введіть нове ім'я")
                              database['exercise']['Плечі'][ex_index] = new_name_ex
            elif edit_ex == '5':
                              for number, data in enumerate(database['exercise'] ['Руки']):
                                           
                                           print(f"Номер {number}, вправа: {data}")
                              ex_index=int(input("Введіть номер вправи "))
                              new_name_ex=input("Введіть нове ім'я")
                              database['exercise']['Руки'][ex_index] = new_name_ex
      if choice == '3':
            
            del_ex = input("""Оберіть группу м'язів для видалення
                                          Грудь-1
                                          Спина-2
                                          Ноги-3
                                          Плечі-4
                                          Руки-5  """) 
            if del_ex == '1':
                  for number, data in enumerate(database['exercise'] ['Грудь']):
                        print(f"Номер {number}, вправа: {data}")
                  del_index=int(input("Введіть номер вправи для видалення "))
                  if 0 <= del_index < len(database['exercise']['Грудь']):
                        deleted_ex = database['exercise']['Грудь'].pop(del_index)
                  print(f"Вправа {deleted_ex} успішно видалена!")
            else:

                  print("Вправа з таким номером не знайдена!")

            if del_ex == '2':
                              for number, data in enumerate(database['exercise'] ['Спина']):
                                    print(f"Номер {number}, вправа: {data}")
                              del_index=int(input("Введіть номер вправи для видалення "))
                              if 0 <= del_index < len(database['exercise']['Спина']):
                                    deleted_ex = database['exercise']['Спина'].pop(del_index)
                              print(f"Вправа {deleted_ex} успішно видалена!")
            else:
            
                              print("Вправа з таким номером не знайдена!")

            if del_ex == '3':
                              for number, data in enumerate(database['exercise'] ['Ноги']):
                                    print(f"Номер {number}, вправа: {data}")
                              del_index=int(input("Введіть номер вправи для видалення "))
                              if 0 <= del_index < len(database['exercise']['Ноги']):
                                    deleted_ex = database['exercise']['Ноги'].pop(del_index)
                              print(f"Вправа {deleted_ex} успішно видалена!")
            else:
            
                              print("Вправа з таким номером не знайдена!")

            if del_ex == '4':
                              for number, data in enumerate(database['exercise'] ['Плечі']):
                                    print(f"Номер {number}, вправа: {data}")
                              del_index=int(input("Введіть номер вправи для видалення "))
                              if 0 <= del_index < len(database['exercise']['Плечі']):
                                    deleted_ex = database['exercise']['Плечі'].pop(del_index)
                              print(f"Вправа {deleted_ex} успішно видалена!")
            else:
            
                              print("Вправа з таким номером не знайдена!")
            if del_ex == '5':
                              for number, data in enumerate(database['exercise'] ['Руки']):
                                    print(f"Номер {number}, вправа: {data}")
                              del_index=int(input("Введіть номер вправи для видалення "))
                              if 0 <= del_index < len(database['exercise']['Руки']):
                                    deleted_ex = database['exercise']['Руки'].pop(del_index)
                              print(f"Вправа {deleted_ex} успішно видалена!")
            else:
            
                              print("Вправа з таким номером не знайдена!")

      if choice == '4':
            show_ex = input("""Оберіть группу м'язів:
                                            Грудь-1
                                            Спина-2
                                            Ноги-3
                                            Плечі-4
                                            Руки-5  """)
            if show_ex == '1':

                  for number, data in enumerate(database['exercise'] ['Грудь']):
                        print(f"Номер {number}, вправа: {data}")
                  else:
                              print("Немає вправ")
            elif show_ex == '2':
            
                  for number, data in enumerate(database['exercise'] ['Спина']):
                        print(f"Номер {number}, вправа: {data}")
            else:
                              print("Немає вправ")
            if show_ex == '3':
            
                  for number, data in enumerate(database['exercise'] ['Ноги']):
                        print(f"Номер {number}, вправа: {data}")
            else:
                              print("Немає вправ")
            if show_ex == '4':
                        
                  for number, data in enumerate(database['exercise'] ['Плечі']):
                        print(f"Номер {number}, вправа: {data}")
            else:
                              print("Немає вправ")
            if show_ex == '5':
                        
                  for number, data in enumerate(database['exercise'] ['Руки']):
                        print(f"Номер {number}, вправа: {data}")
            else:
                              print("Немає вправ")
                 
            
      elif choice == '5':
            date_training = input('Введіть дату тренування (25.03.26)')
            
            if 'workouts' not in database:

                  database['workouts'] = {}
            if date_training not in database['workouts']:

                  database['workouts'][date_training] = []
      elif choice == '6':
            
            if 'workouts' not in database or not database['workouts']:
                  print("Немає збережених дат тренувань!")
            else:
                  print("Доступні дати тренувань:")
                  for number, data in enumerate(database['workouts']):
                        print(f"Номер {number}: {data}")


                  choose_date = input("Оберіть дату тренування...")
                  choose_date = list(database['workouts'].keys())[int(choose_date)] #Создает списпок чтобы сохранялось в дату
                  
                 
            show_ex_for_train = input("""Оберіть группу м'язів:
                                                              Грудь-1
                                                              Спина-2
                                                              Ноги-3
                                                              Плечі-4
                                                              Руки-5  """)
            if show_ex_for_train == '1':
                  
                                    for number, data in enumerate(database['exercise'] ['Грудь']):
                                          print(f"Номер {number}, вправа: {data}")
                                    add_ex_in_tr = input("Оберіть вправу...")
                                    weight_ex_tr = input("Введіть вагу вправи")
                                    reps_ex_tr = input("Ввдеіть кількість повторень")
                                    ex_index = int(add_ex_in_tr)
                                    ex_name = database['exercise']['Грудь'][ex_index]

                                    database['workouts'][choose_date].append({
                                    "Вправа": ex_name,
                                    "Вага": weight_ex_tr,
                                    "Повторення": reps_ex_tr
                                    })

            else:
                        print("Немає вправ")

            if show_ex_for_train == '2':
                  
                                    for number, data in enumerate(database['exercise'] ['Спина']):
                                          print(f"Номер {number}, вправа: {data}")
                                    add_ex_in_tr = input("Оберіть вправу...")
                                    weight_ex_tr = input("Введіть вагу вправи")
                                    reps_ex_tr = input("Ввдеіть кількість повторень")
                                    ex_index = int(add_ex_in_tr)
                                    ex_name = database['exercise']['Спина'][ex_index]

                                    database['workouts'][choose_date].append({
                                    "Вправа": ex_name,
                                    "Вага": weight_ex_tr,
                                    "Повторення": reps_ex_tr
                                    })
            
            else:
                        print("Немає вправ")
            if show_ex_for_train == '3':
                  
                                    for number, data in enumerate(database['exercise'] ['Ноги']):
                                          print(f"Номер {number}, вправа: {data}")
                                    add_ex_in_tr = input("Оберіть вправу...")
                                    weight_ex_tr = input("Введіть вагу вправи")
                                    reps_ex_tr = input("Ввдеіть кількість повторень")
                                    ex_index = int(add_ex_in_tr)
                                    ex_name = database['exercise']['Ноги'][ex_index]

                                    database['workouts'][choose_date].append({
                                    "Вправа": ex_name,
                                    "Вага": weight_ex_tr,
                                    "Повторення": reps_ex_tr
                                    })
            
            else:
                        print("Немає вправ")
            if show_ex_for_train == '4':
                  
                                    for number, data in enumerate(database['exercise'] ['Плечі']):
                                          print(f"Номер {number}, вправа: {data}")
                                    add_ex_in_tr = input("Оберіть вправу...")
                                    weight_ex_tr = input("Введіть вагу вправи")
                                    reps_ex_tr = input("Ввдеіть кількість повторень")
                                    ex_index = int(add_ex_in_tr)
                                    ex_name = database['exercise']['Плечі'][ex_index]

                                    database['workouts'][choose_date].append({
                                    "Вправа": ex_name,
                                    "Вага": weight_ex_tr,
                                    "Повторення": reps_ex_tr
                                    })
            
            else:
                        print("Немає вправ")
            if show_ex_for_train == '5':
                  
                                    for number, data in enumerate(database['exercise'] ['Руки']):
                                          print(f"Номер {number}, вправа: {data}")
                                    add_ex_in_tr = input("Оберіть вправу...")
                                    weight_ex_tr = input("Введіть вагу вправи")
                                    reps_ex_tr = input("Ввдеіть кількість повторень")
                                    ex_index = int(add_ex_in_tr)
                                    ex_name = database['exercise']['Руки'][ex_index]

                                    database['workouts'][choose_date].append({
                                    "Вправа": ex_name,
                                    "Вага": weight_ex_tr,
                                    "Повторення": reps_ex_tr
                                    })
            
            else:
                        print("Немає вправ")

      elif choice == "7":

                  for number, data in enumerate(database['workouts']):
                        print(f"Номер {number}: {data}")
                  choose_date = input("Оберіть дату у якій бажаєте подивитись тренування")
                  choose_date = list(database['workouts'].keys())[int(choose_date)] #Создает списпок чтобы сохранялось в дату
                  
                  for item in database['workouts'][choose_date]:
                          print( f""" database'{choose_date}
                              Вправа - {item['Вправа']},
                              Вага- {item['Вага']},
                              Повторення - {item['Повторення']}
                              """ )
      elif choice == "8":

            show_inf_of_ex = input("""Оберіть группу м'язів:
                                                Грудь-1
                                                Спина-2
                                                Ноги-3
                                                Плечі-4
                                                Руки-5  """)

            if show_inf_of_ex == '1':
                        
                                          for number, data in enumerate(database['exercise'] ['Грудь']):
                                                print(f"Номер {number}, вправа: {data}")
                                          choose_if_of_ex = input("Оберіть вправу...")
                                          
                                          for item in database['workouts']['Грудь']:
                                                                    print( f""" database'{choose_date}
                                                                        Вправа - {item['Вправа']},
                                                                        Вага- {item['Вага']},
                                                                        Повторення - {item['Повторення']}
                                                                        """ )
                                          
      
                                          
                 
                  

      with open('strenght_inf.json', 'w', encoding='utf-8') as f:
                  json.dump (database, f , ensure_ascii=False, indent=4)

