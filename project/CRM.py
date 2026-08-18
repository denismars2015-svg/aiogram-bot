database=dict( )
def CRM(database,order_id, **kwargs):
      database[order_id] = kwargs       
def calc_total_sum(*args):  
    return sum(args)
while True:
    choice = input("Введите цифру действия: 1-Добавить заказ, 2-Удалить заказ, 3-Вывести все заказы, 4-Редактировать заказ, 5-Общая выручка за заказы, 6-Выход: ")
    if choice == "1":
        order_id = input("Введите номер заказа: ")
        client_name = input("Введите имя клиента: ")
        platform = input("Введите платформу: ")
        service = input("Введите услугу: ")
        price = float(input("Введите цену: "))
        CRM(database, order_id, Имя_клиента=client_name, Платформа=platform, Услуга=service, Цена=price)
        print(f"Заказ с номером {order_id} добавлен.")
    if choice == "2":
        action=input("Удалить все заказы-1, удалить заказ по номеру-2: ")
        if action == "1":
            database.clear()
            print("Все заказы удалены.")
        else:
            order_id=input("Введите номер заказа для удаления: ")
            if order_id in database:
                del database[order_id]
                print(f"Заказ с номером {order_id} удален.")
            else:
                print(f"Заказ с номером {order_id} не найден.")
    if choice == "3":
        if database:
            print("database:")
            for order_id, order_details in database.items():
                  print(
                        f"-------------------\n" +
                        f"Номер заказа: {order_id}\n" +
                        f"Имя клиента: {order_details['Имя_клиента']}\n" +
                        f"Платформа: {order_details['Платформа']}\n" +
                        f"Услуга: {order_details['Услуга']}\n" +
                        f"Цена: {order_details['Цена']}\n" +
                        f"-------------------"
)
        else:
            print("Нету заказов")
    if choice == "4":
        order_id=input("Введите номер заказа для редактирования: ")
        if order_id in database:
            client_choice=input("Введите цифру действия: 1-Изменить имя клиента, 2-Изменить платформу, 3-Изменить услугу, 4-Изменить цену: ")
        if client_choice == "1":
                new_client_name=input("Введите новое имя клиента: ")
                print(f"Имя клиента для заказа с номером {order_id} изменено на {new_client_name}.")
                database[order_id]['Имя_клиента'] = new_client_name
        elif client_choice == "2":
                    new_platform=input("Введите новую платформу: ")
                    database[order_id]['Платформа'] = new_platform
                    print(f"Платформа для заказа с номером {order_id} изменена на {new_platform}.")
        elif client_choice == "3":
                    new_service=input("Введите новую услугу: ")
                    database[order_id]['Услуга'] = new_service
                    print(f"Услуга для заказа с номером {order_id} изменена на {new_service}.")
        elif client_choice == "4":
                    new_price=float(input("Введите новую цену: "))
                    database[order_id]['Цена'] = new_price
                    print(f"Цена для заказа с номером {order_id} изменена на {new_price}.")
        else:
            print(f"Заказ с номером {order_id} не найден.")
    if choice == "5":
        total_sum = calc_total_sum(*[arg["Цена"] for arg in database.values()])
        print(f"Общая выручка за заказы: {total_sum}")
    if choice == "6":
        print("Выход из программы.")
        break        


   