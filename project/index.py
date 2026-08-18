data = input("Введите время тренировки  и вес через пробел: ")
text = data.split() 
time_str , weight_str = text
time_num , weight_num  = float(time_str), float(weight_str) 
def calculator_callories(*,time: float, weigth: float) -> str:
    return f"Твой вес: {weigth} кг, время тренировки: {time} минут, сожжено калорий:{round(11 * weigth * time / 70)} ккал"
print(calculator_callories(time=time_num, weigth=weight_num))
    