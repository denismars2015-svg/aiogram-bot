data=input('Введите дистанцию(в километрах).время пробежки(в минутах)  пульс и возвраст . через пробел')
text=data.split()
distance_str, time_str, pulse_str, age_str = text
distance_num, time_num, pulse_num, age_num = float(distance_str), float(time_str), float(pulse_str), float(age_str) 
def analyze_run(*, distance: float, time: float, pulse: float, age: float) -> str:
        result: str  = f"Ваш темп бега: {round(time/distance, 1)} минут на км. " 
        max_pulse=220 - age_num
        min_pulse=max_pulse*0.5 

        if pulse   > max_pulse:
            result += "Ваш пульс выше нормы, рекомендуется снизить нагрузку."
        elif pulse <= min_pulse:
            result += "Ваш пульс ниже нормы, рекомендуется увеличить нагрузку или обратиться к врачу"
        else:
            result += "Ваш пульс в пределах нормы. Отличная тренировка!"    

        return result   
print(analyze_run(distance=distance_num, time=time_num, pulse=pulse_num, age=age_num))

    
