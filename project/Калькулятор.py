data=input("Введіть суму заборгованості(Сума на яку нараховуються санкції): ")
date_start=input("Введіть дату початку розрахунку(дата з якої виникла заборгованість): ")
date_filing=input("Введіть дату подачі позовної заяви(дата подачі позовної заяви до суду): ")
statute_limit=input("Введіть Строк позовної давності(Строк позовної давності у роках): ")
nbu=input("Введіть ставку НБУ ")
text = data.split()

from datetime import datetime 
date_1 = datetime.strptime(date_start, "%d.%m.%Y").date()
date_2 = datetime.strptime(date_filing, "%d.%m.%Y").date()
quantity_days = (date_2 - date_1 ).days + 1

sum_num = float(data)
nbu_num = float(nbu)
penny_per_day = 15 * nbu_num


def calculate_penalty(*, sum: float, penny_per_day: float, quantity_days: int, ) -> str:
    return f'Ваш місячний пенні: {(sum* penny_per_day /100 /365*quantity_days ):.2f} грн. '
        
print(calculate_penalty(sum=sum_num, penny_per_day=penny_per_day, quantity_days=quantity_days))  


print(f'Кількість днів прострочення: {quantity_days} днів.')