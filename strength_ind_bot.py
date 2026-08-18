<<<<<<< HEAD
import json
import asyncio
import os
from unicodedata import category
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton , Message
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

class AddExerciseState(StatesGroup):
    waiting_for_name = State() 

    waiting_for_category = State()  # Ждем нажатия на кнопку мышц
    waiting_for_weight = State() # Вес
    waiting_for_reps = State() # Повторы
    waiting_for_date_of_training = State() # Дата тренировки

class EditExerciseState(StatesGroup):
    waiting_for_new_name = State()  # Ждем ввода нового имени упражнения

class EditDateState(StatesGroup):
    waiting_for_new_date = State() # Ждем ввода новой даты тренировки

class EditWeightState(StatesGroup):
    waiting_for_new_weight = State()

class EditRepsState(StatesGroup):
    waiting_for_new_reps = State()

def reps(database, rep_id, **kwargs):
    database[rep_id] = kwargs

def weights(database, weight_id, **kwargs):
    database[weight_id] = kwargs


def workouts(database,date_id, **kwargs):
      database[date_id] = kwargs 
load_dotenv()

def exercise(database, my_ex, **kwargs):
    database[my_ex] = kwargs



API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)


def add_user_exercise(user_id, category, ex_name):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    str_user_id = str(user_id)

    # Базова структура, якщо користувача ще немає
    if str_user_id not in data:
        data[str_user_id] = {"exercise": {}}
    if "exercise" not in data[str_user_id]:
        data[str_user_id]["exercise"] = {}
    if category not in data[str_user_id]["exercise"]:
        data[str_user_id]["exercise"][category] = []

    # Додаємо вправу та зберігаємо
    data[str_user_id]["exercise"][category].append(ex_name)

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_user_reps_for_training(user_id, date_name, category, ex_name, weight, reps):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    str_user_id = str(user_id)

    # 1. Створюємо базові структури, якщо їх немає
    if str_user_id not in data:
        data[str_user_id] = {}
    if "training" not in data[str_user_id] or not isinstance(data[str_user_id]["training"], dict):
        data[str_user_id]["training"] = {}
    if date_name not in data[str_user_id]["training"] or not isinstance(data[str_user_id]["training"][date_name], dict):
        data[str_user_id]["training"][date_name] = {}
    if category not in data[str_user_id]["training"][date_name] or not isinstance(data[str_user_id]["training"][date_name][category], dict):
        data[str_user_id]["training"][date_name][category] = {}
    if ex_name not in data[str_user_id]["training"][date_name][category] or not isinstance(data[str_user_id]["training"][date_name][category][ex_name], dict):
        data[str_user_id]["training"][date_name][category][ex_name] = {}
    weight = str(weight) if weight is not None else "0"
    # 2. Записуємо кількість повторів для вправи
    data[str_user_id]["training"][date_name][category][ex_name][weight] = reps

    # 3. Зберігаємо у файл
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
def show_user_inf_of_training(user_id, date_name, category, ex_name):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return None

    str_user_id = str(user_id)

    # Перевіряємо наявність даних
    if (str_user_id in data and 
        "training" in data[str_user_id] and 
        date_name in data[str_user_id]["training"] and 
        category in data[str_user_id]["training"][date_name] and 
        ex_name in data[str_user_id]["training"][date_name][category]):
        
        return data[str_user_id]["training"][date_name][category][ex_name]
    
    return None

def add_user_weighht_for_training(user_id, date_name, category, ex_name, weight):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    str_user_id = str(user_id)

    # 1. Створюємо базові структури, якщо їх немає
    if str_user_id not in data:
        data[str_user_id] = {}
    if "training" not in data[str_user_id] or not isinstance(data[str_user_id]["training"], dict):
        data[str_user_id]["training"] = {}
    if date_name not in data[str_user_id]["training"] or not isinstance(data[str_user_id]["training"][date_name], dict):
        data[str_user_id]["training"][date_name] = {}

    # 2. Якщо категорія була списком або відсутня — перетворюємо у словник
    if category not in data[str_user_id]["training"][date_name] or not isinstance(data[str_user_id]["training"][date_name][category], dict):
        data[str_user_id]["training"][date_name][category] = {}

    # 3. Записуємо вагу для вправи
    data[str_user_id]["training"][date_name][category][ex_name] = weight

    # 4. Зберігаємо у файл
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_user_date(user_id, date_name): #Дата тренировки 
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    str_user_id = str(user_id)

    # Базова структура, якщо користувача ще немає
    if str_user_id not in data:
        data[str_user_id] = {"training_dates": []}
    if "training_dates" not in data[str_user_id]:
        data[str_user_id]["training_dates"] = []

    # Додаємо дату та зберігаємо
    data[str_user_id]["training_dates"].append(date_name)

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_categories_stat_of_ex_keyboard():
    builder = InlineKeyboardBuilder()
    categories = ["Грудь", "Спина", "Ноги", "Плечі", "Руки"]
    for cat in categories:
            builder.button(text=cat, callback_data=f"inf_of_ex_categ_{cat}")
    builder.adjust(1)
    return builder.as_markup()

def get_ex_stat_of_ex_keyboard(category , user_id , database):
    builder = InlineKeyboardBuilder()
    
    for ex_name in database[str(user_id)]['exercise'][category]:
        builder.add(InlineKeyboardButton (text=ex_name , callback_data=f"stat_of_ex_{ex_name}"))

    builder.adjust(1) # Выврод конопок по одной в столбик

    return builder.as_markup()
    

def get_categories_add_keyboard(): # Для добавления 
    builder = InlineKeyboardBuilder()
    categories = ["Грудь", "Спина", "Ноги", "Плечі", "Руки"]
    for cat in categories:
        builder.button(text=cat, callback_data=f"addcat_{cat}")
    builder.adjust(1)
    return builder.as_markup()

def get_all_training_exercises_keyboard(date_name, user_id, database):
    builder = InlineKeyboardBuilder()
    
    # Получаем даныне за выбраную дату
    user_data = database.get(str(user_id), {})
    training_data = user_data.get('training', {}).get(date_name, {})

    # Берем все категории
    for category, exercises in training_data.items():
        
        for ex_name in exercises.keys():
            # Добавляем кнопку
            builder.add(InlineKeyboardButton(
                text=f"{ex_name} ({category})", 
                callback_data=f"edit_tr_ex_{ex_name}"
            ))

    builder.adjust(1) 
    return builder.as_markup()

def delete_user_exercise(user_id, category, ex_name):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return

    str_user_id = str(user_id) # Обязательно строчка

    # Перевіряємо, чи є юзер, розділ exercise та потрібна категорія
    if str_user_id in data and 'exercise' in data[str_user_id] and category in data[str_user_id]['exercise']:
        exercises_list = data[str_user_id]['exercise'][category]
        
        # Якщо така вправа є у списку — видаляємо її
        if ex_name in exercises_list:
            exercises_list.remove(ex_name)

        # Записуємо оновлений файл (з indent=4 та ensure_ascii=False)
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def delete_user_date(user_id, date_name):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return

    str_user_id = str(user_id) # Обов'язково стрічка!

    # Перевіряємо, чи є юзер та розділ training_dates
    if str_user_id in data and 'training_dates' in data[str_user_id]:
        dates_list = data[str_user_id]['training_dates']
        
        # Якщо така дата є у списку — видаляємо її
        if date_name in dates_list:
            dates_list.remove(date_name)

        # Записуємо оновлений файл (з indent=4 та ensure_ascii=False)
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def delete_user_ex_in_tr(user_id, date_name, ex_name):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return
    
    str_user_id = str(user_id)
    
    #
    if str_user_id in data and 'training' in data[str_user_id] and date_name in data[str_user_id]['training']:
        day_data = data[str_user_id]['training'][date_name]
            
        for category, exercises in day_data.items():
            if ex_name in exercises:
                del exercises[ex_name]
                break # Цикл зупиняється тут
    
        
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def show_date_of_training(date_name,user_id , database) : # Вывод кнопок дат
    builder = InlineKeyboardBuilder()
    
    for date_name in database[str(user_id)]['training_dates']:
        builder.add(InlineKeyboardButton (text=date_name , callback_data=f"date_{date_name}"))

    builder.adjust(1) # Выврод конопок по одной в столбик

    return builder.as_markup()

def show_exercise_of_training(date_name, user_id, database):
    builder = InlineKeyboardBuilder()
    
    # Безопасно достаем упражнения пользователя
    user_data = database.get(str(user_id), {})
    training_data = user_data.get('training', {}).get(date_name, {})

    for category, exercises in training_data.items():
        for ex_name in exercises:
            builder.add(InlineKeyboardButton(text=f"{category}: {ex_name}", callback_data=f"showtrainex_{ex_name}"))

    builder.adjust(1)  # Вывод кнопок по одной в столбик

    return builder.as_markup()


def add_user_exercise_to_training(user_id, date_name, category, ex_name):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    str_user_id = str(user_id)

    # 1. Створюємо базову структуру, якщо її немає
    if str_user_id not in data:
        data[str_user_id] = {}
    if "training" not in data[str_user_id] or not isinstance(data[str_user_id]["training"], dict):
        data[str_user_id]["training"] = {}
    if date_name not in data[str_user_id]["training"] or not isinstance(data[str_user_id]["training"][date_name], dict):
        data[str_user_id]["training"][date_name] = {}
    if category not in data[str_user_id]["training"][date_name] or not isinstance(data[str_user_id]["training"][date_name][category], dict):
        data[str_user_id]["training"][date_name][category] = {}

    # 2. ⚠️ ЗАМІСТЬ .append() додаємо назву вправи як ключ словника:
    if ex_name not in data[str_user_id]["training"][date_name][category]:
        data[str_user_id]["training"][date_name][category][ex_name] = ""

    # 3. Зберігаємо зміни у файл
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_categories_edit_keyboard(): # Для редактирования 
    builder = InlineKeyboardBuilder()
    categories = ["Грудь", "Спина", "Ноги", "Плечі", "Руки"]
    for cat in categories:
        builder.button(text=cat, callback_data=f"categ_{cat}")
    builder.adjust(1)
    return builder.as_markup()


def get_categories_training_keyboard(): # Для вывода категорий мышц при добавлении упражнений к тренировке
    builder = InlineKeyboardBuilder()
    categories = ["Грудь", "Спина", "Ноги", "Плечі", "Руки"]
    for cat in categories:
        builder.button(text=cat, callback_data=f"train_categ_{cat}")
    builder.adjust(1)
    return builder.as_markup()


def update_user_weight(user_id, date_name, ex_name, new_weight): 
    file_name = 'strenght_inf.json'
    old_w_to_return = None # Создаем сменную для старого веса
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return None
    
    str_user_id = str(user_id)
    
    if str_user_id in data and 'training' in data[str_user_id] and date_name in data[str_user_id]['training']:
        day_data = data[str_user_id]['training'][date_name]
        
        for category, exercises in day_data.items():
            if ex_name in exercises:
                old_weights = list(exercises[ex_name].keys())
                if old_weights:
                    old_w = old_weights[0]
                    old_w_to_return = old_w 
                    reps = exercises[ex_name].pop(old_w) 
                    exercises[ex_name][new_weight] = reps  
                break
                
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    return old_w_to_return 

def update_user_reps(user_id, date_name, ex_name, new_reps): 
    
    file_name = 'strenght_inf.json'
    old_r_to_return = None 
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return None
    
    str_user_id = str(user_id)
    
    if str_user_id in data and 'training' in data[str_user_id] and date_name in data[str_user_id]['training']:
        day_data = data[str_user_id]['training'][date_name]
        
        for category, exercises in day_data.items():
            if ex_name in exercises:
                # Беремо список ключів (це наша вага)
                weights_list = list(exercises[ex_name].keys())
                if weights_list:
                    current_weight = weights_list[0]
                    # Зберігаємо старі повтори (значення словника)
                    old_r_to_return = exercises[ex_name][current_weight] 
                    # Перезаписуємо повтори на нові, не чіпаючи саму вагу!
                    exercises[ex_name][current_weight] = new_reps  
                break
                
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    return old_r_to_return

def get_name_of_exersice (category , user_id , database) : # Вывод кнопок упржнений 
    builder = InlineKeyboardBuilder()
    
    for ex_name in database[str(user_id)]['exercise'][category]:
        builder.add(InlineKeyboardButton (text=ex_name , callback_data=f"ex_{ex_name}"))

    builder.adjust(1) # Выврод конопок по одной в столбик

    return builder.as_markup()

def get_date_of_training (date_name,user_id , database) : # Вывод кнопок дат
    builder = InlineKeyboardBuilder()
    
    for date_name in database[str(user_id)]['training_dates']:
        builder.add(InlineKeyboardButton (text=date_name , callback_data=f"datetrain_{date_name}"))

    builder.adjust(1) # Выврод конопок по одной в столбик

    return builder.as_markup()

def get_main_keyboard():
    builder = InlineKeyboardBuilder()

  
    builder.add(InlineKeyboardButton(text="Створити вправу", callback_data="add_ex"))
    builder.add(InlineKeyboardButton(text=" Подивитись вправи", callback_data="show_ex"))
    
    builder.add(InlineKeyboardButton(text="  Створити дату тренування", callback_data="date_training"))#5
    builder.add(InlineKeyboardButton(text="  Подивитись дати тренувань", callback_data="show_date_training"))#6
    builder.add(InlineKeyboardButton(text="  Додати вправи до тренування", callback_data="add_ex_to_training"))#6
    builder.add(InlineKeyboardButton(text="  Подивитись вправи за  тренування", callback_data="show_ex_of_training"))#7
    builder.add(InlineKeyboardButton(text=" Видалити вправу з тренування", callback_data="del_ex_of_training"))
    builder.add(InlineKeyboardButton(text="  Подивитись статистику вправ", callback_data="show_inf_of_ex"))#8
    
   

    
    builder.adjust(1) # Выврод конопок по одной в столбик

    return builder.as_markup()

def get_variants_of_training_keyboard(date_name): # Вывод кнопок для редактирования и удаления тренировки
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Редагувати тренування", callback_data=f"edit_tr_date_{date_name}"))
    builder.add(InlineKeyboardButton(text="Далі", callback_data="continue_training"))
    

    builder.adjust(1) # Выврод конопок по одной в столбик
    return builder.as_markup()

def get_variants_of_inf_abt_ex_in_tr_keyboard(ex_name):
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text = "Змінити вагу", callback_data="edit_weight"))
    builder.add(InlineKeyboardButton(text="Змінити кількість повторень", callback_data="edit_reps"))

    builder.adjust(1) # Выврод конопок по одной в столбик
    return builder.as_markup()

def show_date_of_training_for_user(prefix, user_id, database):
    builder = InlineKeyboardBuilder()
    str_user_id = str(user_id)
    
    # ⚠️ Правильно: беремо дані тільки зі списку створених дат
    user_dates = database.get(str_user_id, {}).get("training_dates", [])
    
    for date_name in user_dates:
        builder.add(InlineKeyboardButton(text=date_name, callback_data=f"{prefix}{date_name}"))
        
    builder.adjust(1)
    return builder.as_markup()


def get_weight_keyboard(category, user_id, database): # Вывод кнопок для выбора веса
    builder = InlineKeyboardBuilder()
    user_data = database.get(str(user_id), {})
    user_weights = user_data.get('weights', [])
    for weight in user_weights:
        builder.add(InlineKeyboardButton(text=weight, callback_data=f"weight_{weight}"))
    builder.adjust(1)
    return builder.as_markup()

def get_reps_keyboard(category, user_id, database): # Вывод кнопок для выбора количества повторов
    builder = InlineKeyboardBuilder()
    user_data = database.get(str(user_id), {})
    user_reps = user_data.get('reps', [])
    for rep in user_reps:
        builder.add(InlineKeyboardButton(text=rep, callback_data=f"rep_{rep}"))
    builder.adjust(1)
    return builder.as_markup()

def get_exercise_for_training_keyboard(category, user_id, database): # Вывод кнопок упражнений для добавления к тренировке
    builder = InlineKeyboardBuilder()

    # Безопасно достаем упражнения пользователя
    user_data = database.get(str(user_id), {})
    user_exercises = user_data.get('exercise', {}).get(category, [])

    for ex_name in user_exercises:
        builder.add(InlineKeyboardButton(text=ex_name, callback_data=f"trainex_{ex_name}"))

    builder.adjust(1) # Вывод кнопок по одной в столбик

    return builder.as_markup()

def get_variants_of_date_keyboard(): # Вывод кнопок для редактирования и удаления даты
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Редагувати дату", callback_data="edit_date"))
    builder.add(InlineKeyboardButton(text="Видалити дату", callback_data="del_date"))
    builder.add(InlineKeyboardButton(text="Далі", callback_data="continue_date"))

    builder.adjust(1) # Выврод конопок по одной в столбик
    return builder.as_markup()

def get_variants_of_exercise_keyboard(): # Вывод кнопок для редактирования и удаления упражнения
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Редагувати вправу", callback_data="edit_ex"))
    builder.add(InlineKeyboardButton(text="Видалити вправу", callback_data="del_ex"))
    builder.add(InlineKeyboardButton(text="Далі", callback_data="continue_ex"))

    builder.adjust(1) # Выврод конопок по одной в столбик
    return builder.as_markup()



@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.reply(text="Выбирите вариант из списка", reply_markup=get_main_keyboard())    

@router.callback_query(F.data == "add_ex") #Добавить упр
async def add_ex_callback(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    await callback.message.edit_text(text="Ви обрали додати тренування")
    await callback.message.answer(text="Оберіть группу м'язів", reply_markup=get_categories_add_keyboard())    #Выводит выбор группы мышц 
        

@router.callback_query(F.data.startswith("addcat_"))
async def categ_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    category_name = callback.data.replace("addcat_", "")
    await state.update_data(chosen_category=category_name)
    await callback.message.answer("Введіть назву  вправи:")
    await state.set_state(AddExerciseState.waiting_for_name)
    

@router.message(StateFilter(AddExerciseState.waiting_for_name))
async def show_result(message: types.Message, state: FSMContext):
    ex_name = message.text
    data = await state.get_data()
    category = data.get("chosen_category")
    user_id = message.from_user.id

    
    add_user_exercise(user_id, category, ex_name)# Записываем в JSON


    await message.answer(f"Ви додали '{ex_name}'  категорію '{category}'" )
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())
    
    
@router.callback_query(F.data =="show_ex")
async def show_ex_callback(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    await callback.message.edit_text(text="Ви обрали показати вправи")
    await callback.message.answer(text="Оберіть группу м'язів",reply_markup=get_categories_edit_keyboard())    #Выводит выбор группы мышц 


@router.callback_query(F.data.startswith("categ_")) # метод проверки строки
async def categ_callback(callback: types.CallbackQuery, state: FSMContext ):
    
    category_name = callback.data.replace("categ_", "")
    await state.update_data(chosen_category=category_name)
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
           
        database = json.load(f)  
    user_id = callback.from_user.id
    await callback.message.answer( text=f"Оберіть вправу з категорії '{category_name}':", reply_markup=get_name_of_exersice(category_name, user_id, database))


    
@router.callback_query(F.data.startswith("ex_"))
async def ex_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    ex_name = callback.data.replace("ex_", "")

    
    await state.update_data(old_name=ex_name)# Запоминаем в память старое название

    await callback.message.answer(f"Ви обрали вправу '{ex_name}'. Що бажаєте зробити?", reply_markup=get_variants_of_exercise_keyboard())   
@router.callback_query(F.data == "edit_ex")
async def edit_ex_callback(callback: types.CallbackQuery,  state: FSMContext):
      
    await callback.answer()
    await state.set_state(EditExerciseState.waiting_for_new_name)
    await callback.message.edit_text(text="Ви обрали редагувати вправу")
    await callback.message.answer(text="Введіть нову назву вправи:")


def update_user_ex(user_id, category , old_name, new_name_ex):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return

    str_user_id = str(user_id)

    if str_user_id in data:
        # 1. Меняем имя в базовом списке упражнений
        if 'exercise' in data[str_user_id] and category in data[str_user_id]['exercise']:
            exercise_list = data[str_user_id]['exercise'][category]
            
            for m in range(len(exercise_list)):
                if exercise_list[m] == old_name:
                    exercise_list[m] = new_name_ex
                    break

        # 2. Меняем имя во всех сохраненных тренировках
        if 'training' in data[str_user_id]:
            # Используем list() для безопасной итерации по ключам (датам)
            for date_key in list(data[str_user_id]['training'].keys()):
                
                # Проверяем, есть ли в этой дате нужная категория
                if category in data[str_user_id]['training'][date_key]:
                    
                    # Проверяем, есть ли там старое упражнение
                    if old_name in data[str_user_id]['training'][date_key][category]:
                        # Переименовываем ключ
                        data[str_user_id]['training'][date_key][category][new_name_ex] = data[str_user_id]['training'][date_key][category].pop(old_name)

        # Записываем изменения в файл
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

@router.message(StateFilter(EditExerciseState.waiting_for_new_name))
async def process_new_exercise_name(message: types.Message, state: FSMContext):
    new_name_ex = message.text
    user_id = message.from_user.id

    
    user_data = await state.get_data() #Достаем данные из памяти 
    category = user_data.get("chosen_category")
    old_name = user_data.get("old_name")

    update_user_ex(user_id, category, old_name, new_name_ex) #Меняем старое имя на новое в файле

    await message.answer(text=f"Замінено назву вправи '{old_name}' на '{new_name_ex}' у категорії '{category}'")
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "del_ex")
async def del_ex_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    
    
    user_data = await state.get_data()
    category = user_data.get("chosen_category")
    ex_name = user_data.get("old_name") # або ex_name, яке зберігали при виборі
    user_id = callback.from_user.id

    # Викликаємо видалення зі списку
    delete_user_exercise(user_id, category, ex_name)

    await callback.message.edit_text(text=f"Вправу '{ex_name}' успішно видалено з категорії '{category}'!")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())  

@router.callback_query(F.data == "continue_ex")
async def continue_ex_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Далі")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "date_training")
async def date_training_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Ви обрали створити тренування")
    await callback.message.answer(text="Введіть дату тренування у форматі ДД.ММ.РРРР:")
    await state.set_state(AddExerciseState.waiting_for_date_of_training)
        
@router.message(StateFilter(AddExerciseState.waiting_for_date_of_training))
async def show_result(message: types.Message, state: FSMContext):
    date_name = message.text
    data = await state.get_data()
    category = data.get("chosen_category")
    user_id = message.from_user.id

    
    add_user_date(user_id, date_name)# Записываем в JSON


    await message.answer(f"Ви додали дату {date_name}")
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())


@router.callback_query(F.data == "show_date_training")
async def show_date_training_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Ви обрали показати дати тренувань")
    #Выводит даты 
    await callback.message.answer( text="Ваші дати тренувань:", 
                                  reply_markup=show_date_of_training("date_name", callback.from_user.id, json.load(open('strenght_inf.json', 'r', encoding='utf-8'))))
    

@router.callback_query(F.data.startswith("date_")) #Вывод кнопок дат
async def date_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    date_name = callback.data.replace("date_", "")
    await state.update_data(old_date=date_name)# Запоминаем в память старое название

    await callback.message.answer(f"Ви обрали дату {date_name}. Що бажаєте зробити?", reply_markup=get_variants_of_date_keyboard())      



@router.callback_query(F.data == "edit_date") #Вывод кнопок для редактирования даты
async def edit_date_callback(callback: types.CallbackQuery,  state: FSMContext):
      
    await callback.answer()
    await state.set_state(EditDateState.waiting_for_new_date)
    await callback.message.edit_text(text="Ви обрали редагувати дату")
    await callback.message.answer(text="Введіть нову дату тренування у форматі ДД.ММ.РРРР:")


def update_user_date(user_id,  old_date, new_date):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return

    str_user_id = str(user_id)

    if str_user_id in data:
        # 1. Меняем дату в списке training_dates
        if 'training_dates' in data[str_user_id] and old_date in data[str_user_id]['training_dates']:
            dates_list = data[str_user_id]['training_dates']
            
            for m in range(len(dates_list)): 
                if dates_list[m] == old_date:
                    dates_list[m] = new_date
                    break
        
        # 2. Переименовываем ключ в словаре training, чтобы не потерять упражнения
        if 'training' in data[str_user_id] and old_date in data[str_user_id]['training']:
            # Извлекаем все данные за старую дату и переносим в новую
            data[str_user_id]['training'][new_date] = data[str_user_id]['training'].pop(old_date)

        # Записываем изменения в файл
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

@router.message(StateFilter(EditDateState.waiting_for_new_date))
async def process_new_exercise_date(message: types.Message, state: FSMContext):
    new_date = message.text
    user_id = message.from_user.id

    
    user_data = await state.get_data() #Достаем данные из памяти 
    old_date = user_data.get("old_date")

    update_user_date(user_id, old_date, new_date) #Меняем старую дату на новую в файле

    await message.answer(text=f"Замінено дату тренування '{old_date}' на '{new_date}'")
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "del_date") #Вывод кнопок для удаления даты
async def del_date_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    
    # Дістаємо збережені дані з пам'яті FSM
    user_data = await state.get_data()
    date_name = user_data.get("old_date") # або ex_name, яке зберігали при виборі
    user_id = callback.from_user.id

    # Викликаємо видалення зі списку
    delete_user_date(user_id, date_name)

    await callback.message.edit_text(text=f"Дату тренування '{date_name}' успішно видалено!")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())  

@router.callback_query(F.data == "continue_date")
async def continue_date_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Далі")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())



@router.callback_query(F.data == "add_ex_to_training")
async def add_ex_to_training_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Ви обрали додати вправу до тренування")
    await callback.message.answer(text="Оберіть дату тренування:", reply_markup=get_date_of_training("date_name",
                                                         callback.from_user.id, json.load(open('strenght_inf.json', 'r', encoding='utf-8'))))    #Выводит даты


@router.callback_query(F.data.startswith("datetrain_")) #Вывод кнопок дат
async def datetrain_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    date_name = callback.data.replace("datetrain_", "")
    await state.update_data(chosen_date=date_name)# Запоминаем в память старое название

    await callback.message.answer(f"Ви обрали дату {date_name}. Тепер оберіть групу м'язів для додавання вправи:", reply_markup=get_categories_training_keyboard())

@router.callback_query(F.data.startswith("train_categ_")) # метод проверки строки
async def train_categ_callback(callback: types.CallbackQuery, state: FSMContext):
    category_name = callback.data.replace("train_categ_", "")
    await state.update_data(chosen_category=category_name)
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)  
    user_id = callback.from_user.id
    await callback.message.answer(text=f"Оберіть вправу з категорії {category_name} для додавання до тренування:", reply_markup=get_exercise_for_training_keyboard(category_name, user_id, database))


@router.callback_query(F.data.startswith("trainex_"))
async def trainex_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    ex_name = callback.data.replace("trainex_", "")
    await state.update_data(chosen_exercise=ex_name)

    
    user_data = await state.get_data()
    chosen_date = user_data.get("chosen_date")
    chosen_category = user_data.get("chosen_category")
    
    real_user_id = callback.from_user.id

    add_user_exercise_to_training(real_user_id, chosen_date, chosen_category, ex_name)

    await callback.message.answer(f"Вправу '{ex_name}' додано до тренування на дату '{chosen_date}' у категорії '{chosen_category}'.")
    await callback.message.answer("Введіть вагу для цієї вправи:")
    await state.set_state(AddExerciseState.waiting_for_weight)


@router.message(StateFilter(AddExerciseState.waiting_for_weight))
async def process_weight(message: types.Message, state: FSMContext):
    weight = message.text
    await state.update_data(chosen_weight=weight)

    user_id = await state.get_data()
    chosen_date = user_id.get("chosen_date")
    chosen_category = user_id.get("chosen_category")
    chosen_exercise = user_id.get("chosen_exercise")

    # Здесь можно добавить логику для сохранения веса в JSON или другой источник данных
    add_user_weighht_for_training(user_id, chosen_date, chosen_category, chosen_exercise, weight)
    await message.answer(f"Вага '{weight}' додано до вправи '{chosen_exercise}' на дату '{chosen_date}' у категорії '{chosen_category}'.")
    await message.answer("Введіть кількість повторів для цієї вправи:")
    await state.set_state(AddExerciseState.waiting_for_reps)

@router.message(StateFilter(AddExerciseState.waiting_for_reps))
async def process_reps(message: types.Message, state: FSMContext):
    reps = message.text
    await state.update_data(chosen_reps=reps)

    user_id = await state.get_data()
    chosen_date = user_id.get("chosen_date")
    chosen_category = user_id.get("chosen_category")
    chosen_exercise = user_id.get("chosen_exercise")
    chosen_weight = user_id.get("chosen_weight")

    
    #add_user_reps_for_training(user_id, chosen_date, chosen_category, chosen_exercise, chosen_weight, reps)
    add_user_reps_for_training(message.from_user.id, chosen_date, chosen_category, chosen_exercise, chosen_weight, reps)
    await message.answer(f"Кількість повторів '{reps}' додано до вправи '{chosen_exercise}' на дату '{chosen_date}' у категорії '{chosen_category}'.")
    await message.answer("Вправа успішно додана до тренування!")
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

    

@router.callback_query(F.data == "show_ex_of_training")
async def show_ex_of_training_callback(callback: types.CallbackQuery, state: FSMContext):
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)

    keyboard = show_date_of_training_for_user("showdate_", callback.from_user.id, database)
    await callback.message.answer(
        text="Оберіть дату тренування:",
        reply_markup=keyboard)


@router.callback_query(F.data.startswith("showdate_"))
async def show_training_info_callback(callback: types.CallbackQuery):
    await callback.answer()
    
    # 1. Отримуємо чисту дату та ID користувача
    date_name = callback.data.replace("showdate_", "")
    user_id = str(callback.from_user.id)
    
    
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)
        
    # 3. Витягуємо тренування за обрану дату
    training_data = database.get(user_id, {}).get("training", {}).get(date_name, {})

    
    if not training_data:
        await callback.message.answer(f"❌  дата <b>{date_name}</b> тренувань не знайдено.", parse_mode="HTML")
        return

    
    msg_text = f" <b>Тренування за {date_name}</b>\n"

    for category, exercises in training_data.items():
        msg_text += f"💪 <b>Категорія: {category}</b>\n"
        if isinstance(exercises, dict):
            for ex_name, weights in exercises.items():
                msg_text += f"  • <b>{ex_name}</b>:\n"
                if isinstance(weights, dict):
                    for weight, reps in weights.items():
                        msg_text += f"     {weight} кг x {reps} повт.\n"
        msg_text += "\n"

    await callback.message.answer(text=msg_text, parse_mode="HTML")
    
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_variants_of_training_keyboard(date_name))



@router.callback_query(F.data == "edit_training")
async def edit_training_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Ви обрали редагувати тренування")
    await callback.message.answer(
        
        # ЗДЕСЬ МЕНЯЕМ НА "edit_tr_date_"
        reply_markup=show_date_of_training_for_user("edit_tr_date_", callback.from_user.id, json.load(open('strenght_inf.json', 'r', encoding='utf-8')))
    )  
@router.callback_query(F.data.startswith("edit_tr_date_"))
async def show_date_for_edit_tr(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    # И ЗДЕСЬ МЕНЯЕМ НА "edit_tr_date_"
    date_name = callback.data.replace("edit_tr_date_", "")
    
    await state.update_data(chosen_edit_date=date_name)

    # Відкриваємо базу
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)
        
    # Виводимо всі вправи суцільним списком кнопок
    keyboard = get_all_training_exercises_keyboard(date_name, callback.from_user.id, database)
    
    await callback.message.edit_text( text=f"Оберіть вправу для редагування у тренуванні за {date_name}:", reply_markup=keyboard )
    
    

@router.callback_query(F.data.startswith("edit_tr_ex_"))
async def process_exercise_edit_selection(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    
    # 1. Достаем чистое название упражнения
    ex_name = callback.data.replace("edit_tr_ex_", "")
    
    # 2. Запоминаем выбранное упражнение в "оперативную память" бота
    await state.update_data(chosen_edit_ex=ex_name)
    
    # 3. Вызываем клавиатуру, которую мы создали на Шаге 1
    new_keyboard = get_variants_of_inf_abt_ex_in_tr_keyboard(ex_name)
    
    # 4. Обновляем сообщение бота
    await callback.message.edit_text(
        text=f"Ви обрали вправу <b>{ex_name}</b>. Що бажаєте з нею зробити?",
        reply_markup=new_keyboard,
        parse_mode="HTML")

@router.callback_query(F.data =="edit_weight")
async def edit_weight_callback(callback : types.CallbackQuery , state : FSMContext):
    await callback.answer()
    await state.set_state(EditWeightState.waiting_for_new_weight)
    await callback.message.edit_text(text="Ви обрали редагувати вагу")
    await callback.message.answer(text="Введіть нову вагу:")
    
    
@router.message(StateFilter(EditWeightState.waiting_for_new_weight))
async def process_new_weight_for_tr(message: types.Message, state: FSMContext):
    new_weight = message.text
    user_id = message.from_user.id
    
    # Дістаємо дату та назву вправи, які ми запам'ятали раніше
    user_data = await state.get_data() 
    date_name = user_data.get("chosen_edit_date") 
    ex_name = user_data.get("chosen_edit_ex")
    
    
    # Викликаємо нашу нову функцію збереження ваги
    old_weight = update_user_weight(user_id, date_name, ex_name, new_weight)
    await message.answer(text=f"Замінено вагу для вправи '{ex_name} {old_weight}'на {new_weight} кг")
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data =="edit_reps")
async def edit_reps_callback(callback : types.CallbackQuery , state : FSMContext):
    await callback.answer()
    await state.set_state(EditRepsState.waiting_for_new_reps)
    await callback.message.edit_text(text="Ви обрали редагувати кількість повторень")
    await callback.message.answer(text="Введіть нову кількість повторень:")
    
    
@router.message(StateFilter(EditRepsState.waiting_for_new_reps))
async def process_new_reps_for_tr(message: types.Message, state: FSMContext):
    new_reps = message.text
    user_id = message.from_user.id
    
    # Дістаємо дату та назву вправи, які ми запам'ятали раніше
    user_data = await state.get_data() 
    date_name = user_data.get("chosen_edit_date") 
    ex_name = user_data.get("chosen_edit_ex")
    
    
    # Викликаємо нашу нову функцію збереження ваги
    old_reps = update_user_reps(user_id, date_name, ex_name, new_reps)
    await message.answer(text=f"Замінено кількість повторень  для вправи '{ex_name} {old_reps}'на {new_reps} ")
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "continue_training")
async def continue_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Далі")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "del_ex_of_training")
async def del_ex_in_tr_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Ви обрали видалення вправи з тренування")
    
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)
        
    await callback.message.answer(
        text="Оберіть дату тренування:", 
        reply_markup=show_date_of_training_for_user("del_ex_tr_date_", callback.from_user.id, database)
    )

# Крок 2: Створюємо спеціальну клавіатуру, яка виведе вправи саме для видалення
def get_del_training_exercises_keyboard(date_name, user_id, database):
    builder = InlineKeyboardBuilder()
    user_data = database.get(str(user_id), {})
    training_data = user_data.get('training', {}).get(date_name, {})
    
    for category, exercises in training_data.items():
        for ex_name in exercises.keys():
            # Кнопки з унікальним префіксом 'finish_del_ex_'
            builder.add(InlineKeyboardButton(text=f"❌ {ex_name} ({category})", callback_data=f"finish_del_ex_{ex_name}"))
            
    builder.adjust(1) 
    return builder.as_markup()

# Крок 3: Ловимо обрану дату і виводимо список вправ
@router.callback_query(F.data.startswith("del_ex_tr_date_"))
async def process_date_for_del_ex(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    
    # Дістаємо дату і запам'ятовуємо її
    date_name = callback.data.replace("del_ex_tr_date_", "") 
    await state.update_data(del_ex_date=date_name) 
    
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)
        
    # Викликаємо нашу нову клавіатуру
    keyboard = get_del_training_exercises_keyboard(date_name, callback.from_user.id, database)
    
    await callback.message.edit_text(text=f"Оберіть вправу, яку хочете видалити з тренування за {date_name}:", reply_markup=keyboard)

# Крок 4: Ловимо обрану вправу і остаточно видаляємо її
@router.callback_query(F.data.startswith("finish_del_ex_"))
async def finish_del_ex_in_tr(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    
    # Дістаємо назву вправи
    ex_name = callback.data.replace("finish_del_ex_", "")
    user_id = callback.from_user.id
    
    # Дістаємо збережену раніше дату
    user_data = await state.get_data()
    date_name = user_data.get("del_ex_date")
    
    # Викликаємо вашу функцію видалення
    delete_user_ex_in_tr(user_id, date_name, ex_name)
    
    await callback.message.edit_text(text=f"Вправу <b>'{ex_name}'</b> успішно видалено з тренування за <b>{date_name}</b>!", parse_mode="HTML")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "show_inf_of_ex")
async def show_in_of_ex_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Ви обрали подивитись статистику  вправ")
    await callback.message.answer(text="Оберіть группу м'язів",reply_markup=get_categories_stat_of_ex_keyboard())    #Выводит выбор группы мышц 
    
    
@router.callback_query(F.data.startswith("inf_of_ex_categ_")) # метод проверки строки
async def categ_for_inf_callback(callback: types.CallbackQuery, state: FSMContext ):
        
    category_name = callback.data.replace("inf_of_ex_categ_", "")
    await state.update_data(chosen_category=category_name)
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
               
        database = json.load(f)  
        user_id = callback.from_user.id
    await callback.message.answer( text=f"Оберіть вправу з категорії '{category_name}':", reply_markup=get_ex_stat_of_ex_keyboard(category_name, user_id, database))

@router.callback_query(F.data.startswith("stat_of_ex_"))
async def stat_ex_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    ex_name = callback.data.replace("stat_of_ex_", "")
    user_id = str(callback.from_user.id)
    user_data = await state.get_data()
    category_name = user_data.get("chosen_category")

    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)

    # 1. Беремо історію тренувань
    training_history = database.get(user_id, {}).get("training", {})
    
    # 2. Формуємо красиве повідомлення
    msg_text = f"📊 <b>Статистика для вправи: {ex_name}</b>\n"
    found = False

    # 3. Шукаємо цю вправу по всіх збережених датах
    for date_name, date_data in training_history.items():
        # Якщо в цей день робили цю категорію і цю вправу:
        if category_name in date_data and ex_name in date_data[category_name]:
            found = True
            weights = date_data[category_name][ex_name]
            
            # Додаємо у повідомлення дату, вагу та повтори
            for weight, reps in weights.items():
                msg_text += f"📅 <b>{date_name}</b>: \n "
                msg_text += f" 💪 <b> {weight} кг </b>\n"
                msg_text += f"🔢 <b>{reps} повт</b>\n"
    # Якщо вправу жодного разу не робили на тренуваннях
    if not found:
        msg_text += "<i>Ви ще не виконували цю вправу на жодному тренуванні.</i>"

    # Виводимо статистику та повертаємо в меню
    await callback.message.edit_text(text=msg_text, parse_mode="HTML")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard()) 



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    
=======
import json
import asyncio
import os
from unicodedata import category
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton , Message
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

class AddExerciseState(StatesGroup):
    waiting_for_name = State() 

    waiting_for_category = State()  # Ждем нажатия на кнопку мышц
    waiting_for_weight = State() # Вес
    waiting_for_reps = State() # Повторы
    waiting_for_date_of_training = State() # Дата тренировки

class EditExerciseState(StatesGroup):
    waiting_for_new_name = State()  # Ждем ввода нового имени упражнения

class EditDateState(StatesGroup):
    waiting_for_new_date = State() # Ждем ввода новой даты тренировки

class EditWeightState(StatesGroup):
    waiting_for_new_weight = State()

class EditRepsState(StatesGroup):
    waiting_for_new_reps = State()

def reps(database, rep_id, **kwargs):
    database[rep_id] = kwargs

def weights(database, weight_id, **kwargs):
    database[weight_id] = kwargs


def workouts(database,date_id, **kwargs):
      database[date_id] = kwargs 
load_dotenv()

def exercise(database, my_ex, **kwargs):
    database[my_ex] = kwargs



API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)


def add_user_exercise(user_id, category, ex_name):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    str_user_id = str(user_id)

    # Базова структура, якщо користувача ще немає
    if str_user_id not in data:
        data[str_user_id] = {"exercise": {}}
    if "exercise" not in data[str_user_id]:
        data[str_user_id]["exercise"] = {}
    if category not in data[str_user_id]["exercise"]:
        data[str_user_id]["exercise"][category] = []

    # Додаємо вправу та зберігаємо
    data[str_user_id]["exercise"][category].append(ex_name)

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_user_reps_for_training(user_id, date_name, category, ex_name, weight, reps):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    str_user_id = str(user_id)

    # 1. Створюємо базові структури, якщо їх немає
    if str_user_id not in data:
        data[str_user_id] = {}
    if "training" not in data[str_user_id] or not isinstance(data[str_user_id]["training"], dict):
        data[str_user_id]["training"] = {}
    if date_name not in data[str_user_id]["training"] or not isinstance(data[str_user_id]["training"][date_name], dict):
        data[str_user_id]["training"][date_name] = {}
    if category not in data[str_user_id]["training"][date_name] or not isinstance(data[str_user_id]["training"][date_name][category], dict):
        data[str_user_id]["training"][date_name][category] = {}
    if ex_name not in data[str_user_id]["training"][date_name][category] or not isinstance(data[str_user_id]["training"][date_name][category][ex_name], dict):
        data[str_user_id]["training"][date_name][category][ex_name] = {}
    weight = str(weight) if weight is not None else "0"
    # 2. Записуємо кількість повторів для вправи
    data[str_user_id]["training"][date_name][category][ex_name][weight] = reps

    # 3. Зберігаємо у файл
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
def show_user_inf_of_training(user_id, date_name, category, ex_name):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return None

    str_user_id = str(user_id)

    # Перевіряємо наявність даних
    if (str_user_id in data and 
        "training" in data[str_user_id] and 
        date_name in data[str_user_id]["training"] and 
        category in data[str_user_id]["training"][date_name] and 
        ex_name in data[str_user_id]["training"][date_name][category]):
        
        return data[str_user_id]["training"][date_name][category][ex_name]
    
    return None

def add_user_weighht_for_training(user_id, date_name, category, ex_name, weight):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    str_user_id = str(user_id)

    # 1. Створюємо базові структури, якщо їх немає
    if str_user_id not in data:
        data[str_user_id] = {}
    if "training" not in data[str_user_id] or not isinstance(data[str_user_id]["training"], dict):
        data[str_user_id]["training"] = {}
    if date_name not in data[str_user_id]["training"] or not isinstance(data[str_user_id]["training"][date_name], dict):
        data[str_user_id]["training"][date_name] = {}

    # 2. Якщо категорія була списком або відсутня — перетворюємо у словник
    if category not in data[str_user_id]["training"][date_name] or not isinstance(data[str_user_id]["training"][date_name][category], dict):
        data[str_user_id]["training"][date_name][category] = {}

    # 3. Записуємо вагу для вправи
    data[str_user_id]["training"][date_name][category][ex_name] = weight

    # 4. Зберігаємо у файл
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_user_date(user_id, date_name): #Дата тренировки 
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    str_user_id = str(user_id)

    # Базова структура, якщо користувача ще немає
    if str_user_id not in data:
        data[str_user_id] = {"training_dates": []}
    if "training_dates" not in data[str_user_id]:
        data[str_user_id]["training_dates"] = []

    # Додаємо дату та зберігаємо
    data[str_user_id]["training_dates"].append(date_name)

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_categories_stat_of_ex_keyboard():
    builder = InlineKeyboardBuilder()
    categories = ["Грудь", "Спина", "Ноги", "Плечі", "Руки"]
    for cat in categories:
            builder.button(text=cat, callback_data=f"inf_of_ex_categ_{cat}")
    builder.adjust(1)
    return builder.as_markup()

def get_ex_stat_of_ex_keyboard(category , user_id , database):
    builder = InlineKeyboardBuilder()
    
    for ex_name in database[str(user_id)]['exercise'][category]:
        builder.add(InlineKeyboardButton (text=ex_name , callback_data=f"stat_of_ex_{ex_name}"))

    builder.adjust(1) # Выврод конопок по одной в столбик

    return builder.as_markup()
    

def get_categories_add_keyboard(): # Для добавления 
    builder = InlineKeyboardBuilder()
    categories = ["Грудь", "Спина", "Ноги", "Плечі", "Руки"]
    for cat in categories:
        builder.button(text=cat, callback_data=f"addcat_{cat}")
    builder.adjust(1)
    return builder.as_markup()

def get_all_training_exercises_keyboard(date_name, user_id, database):
    builder = InlineKeyboardBuilder()
    
    # Получаем даныне за выбраную дату
    user_data = database.get(str(user_id), {})
    training_data = user_data.get('training', {}).get(date_name, {})

    # Берем все категории
    for category, exercises in training_data.items():
        
        for ex_name in exercises.keys():
            # Добавляем кнопку
            builder.add(InlineKeyboardButton(
                text=f"{ex_name} ({category})", 
                callback_data=f"edit_tr_ex_{ex_name}"
            ))

    builder.adjust(1) 
    return builder.as_markup()

def delete_user_exercise(user_id, category, ex_name):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return

    str_user_id = str(user_id) # Обязательно строчка

    # Перевіряємо, чи є юзер, розділ exercise та потрібна категорія
    if str_user_id in data and 'exercise' in data[str_user_id] and category in data[str_user_id]['exercise']:
        exercises_list = data[str_user_id]['exercise'][category]
        
        # Якщо така вправа є у списку — видаляємо її
        if ex_name in exercises_list:
            exercises_list.remove(ex_name)

        # Записуємо оновлений файл (з indent=4 та ensure_ascii=False)
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def delete_user_date(user_id, date_name):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return

    str_user_id = str(user_id) # Обов'язково стрічка!

    # Перевіряємо, чи є юзер та розділ training_dates
    if str_user_id in data and 'training_dates' in data[str_user_id]:
        dates_list = data[str_user_id]['training_dates']
        
        # Якщо така дата є у списку — видаляємо її
        if date_name in dates_list:
            dates_list.remove(date_name)

        # Записуємо оновлений файл (з indent=4 та ensure_ascii=False)
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def delete_user_ex_in_tr(user_id, date_name, ex_name):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return
    
    str_user_id = str(user_id)
    
    #
    if str_user_id in data and 'training' in data[str_user_id] and date_name in data[str_user_id]['training']:
        day_data = data[str_user_id]['training'][date_name]
            
        for category, exercises in day_data.items():
            if ex_name in exercises:
                del exercises[ex_name]
                break # Цикл зупиняється тут
    
        
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def show_date_of_training(date_name,user_id , database) : # Вывод кнопок дат
    builder = InlineKeyboardBuilder()
    
    for date_name in database[str(user_id)]['training_dates']:
        builder.add(InlineKeyboardButton (text=date_name , callback_data=f"date_{date_name}"))

    builder.adjust(1) # Выврод конопок по одной в столбик

    return builder.as_markup()

def show_exercise_of_training(date_name, user_id, database):
    builder = InlineKeyboardBuilder()
    
    # Безопасно достаем упражнения пользователя
    user_data = database.get(str(user_id), {})
    training_data = user_data.get('training', {}).get(date_name, {})

    for category, exercises in training_data.items():
        for ex_name in exercises:
            builder.add(InlineKeyboardButton(text=f"{category}: {ex_name}", callback_data=f"showtrainex_{ex_name}"))

    builder.adjust(1)  # Вывод кнопок по одной в столбик

    return builder.as_markup()


def add_user_exercise_to_training(user_id, date_name, category, ex_name):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    str_user_id = str(user_id)

    # 1. Створюємо базову структуру, якщо її немає
    if str_user_id not in data:
        data[str_user_id] = {}
    if "training" not in data[str_user_id] or not isinstance(data[str_user_id]["training"], dict):
        data[str_user_id]["training"] = {}
    if date_name not in data[str_user_id]["training"] or not isinstance(data[str_user_id]["training"][date_name], dict):
        data[str_user_id]["training"][date_name] = {}
    if category not in data[str_user_id]["training"][date_name] or not isinstance(data[str_user_id]["training"][date_name][category], dict):
        data[str_user_id]["training"][date_name][category] = {}

    # 2. ⚠️ ЗАМІСТЬ .append() додаємо назву вправи як ключ словника:
    if ex_name not in data[str_user_id]["training"][date_name][category]:
        data[str_user_id]["training"][date_name][category][ex_name] = ""

    # 3. Зберігаємо зміни у файл
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_categories_edit_keyboard(): # Для редактирования 
    builder = InlineKeyboardBuilder()
    categories = ["Грудь", "Спина", "Ноги", "Плечі", "Руки"]
    for cat in categories:
        builder.button(text=cat, callback_data=f"categ_{cat}")
    builder.adjust(1)
    return builder.as_markup()


def get_categories_training_keyboard(): # Для вывода категорий мышц при добавлении упражнений к тренировке
    builder = InlineKeyboardBuilder()
    categories = ["Грудь", "Спина", "Ноги", "Плечі", "Руки"]
    for cat in categories:
        builder.button(text=cat, callback_data=f"train_categ_{cat}")
    builder.adjust(1)
    return builder.as_markup()


def update_user_weight(user_id, date_name, ex_name, new_weight): 
    file_name = 'strenght_inf.json'
    old_w_to_return = None # Создаем сменную для старого веса
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return None
    
    str_user_id = str(user_id)
    
    if str_user_id in data and 'training' in data[str_user_id] and date_name in data[str_user_id]['training']:
        day_data = data[str_user_id]['training'][date_name]
        
        for category, exercises in day_data.items():
            if ex_name in exercises:
                old_weights = list(exercises[ex_name].keys())
                if old_weights:
                    old_w = old_weights[0]
                    old_w_to_return = old_w 
                    reps = exercises[ex_name].pop(old_w) 
                    exercises[ex_name][new_weight] = reps  
                break
                
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    return old_w_to_return 

def update_user_reps(user_id, date_name, ex_name, new_reps): 
    
    file_name = 'strenght_inf.json'
    old_r_to_return = None 
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return None
    
    str_user_id = str(user_id)
    
    if str_user_id in data and 'training' in data[str_user_id] and date_name in data[str_user_id]['training']:
        day_data = data[str_user_id]['training'][date_name]
        
        for category, exercises in day_data.items():
            if ex_name in exercises:
                # Беремо список ключів (це наша вага)
                weights_list = list(exercises[ex_name].keys())
                if weights_list:
                    current_weight = weights_list[0]
                    # Зберігаємо старі повтори (значення словника)
                    old_r_to_return = exercises[ex_name][current_weight] 
                    # Перезаписуємо повтори на нові, не чіпаючи саму вагу!
                    exercises[ex_name][current_weight] = new_reps  
                break
                
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    return old_r_to_return

def get_name_of_exersice (category , user_id , database) : # Вывод кнопок упржнений 
    builder = InlineKeyboardBuilder()
    
    for ex_name in database[str(user_id)]['exercise'][category]:
        builder.add(InlineKeyboardButton (text=ex_name , callback_data=f"ex_{ex_name}"))

    builder.adjust(1) # Выврод конопок по одной в столбик

    return builder.as_markup()

def get_date_of_training (date_name,user_id , database) : # Вывод кнопок дат
    builder = InlineKeyboardBuilder()
    
    for date_name in database[str(user_id)]['training_dates']:
        builder.add(InlineKeyboardButton (text=date_name , callback_data=f"datetrain_{date_name}"))

    builder.adjust(1) # Выврод конопок по одной в столбик

    return builder.as_markup()

def get_main_keyboard():
    builder = InlineKeyboardBuilder()

  
    builder.add(InlineKeyboardButton(text="Створити вправу", callback_data="add_ex"))
    builder.add(InlineKeyboardButton(text=" Подивитись вправи", callback_data="show_ex"))
    
    builder.add(InlineKeyboardButton(text="  Створити дату тренування", callback_data="date_training"))#5
    builder.add(InlineKeyboardButton(text="  Подивитись дати тренувань", callback_data="show_date_training"))#6
    builder.add(InlineKeyboardButton(text="  Додати вправи до тренування", callback_data="add_ex_to_training"))#6
    builder.add(InlineKeyboardButton(text="  Подивитись вправи за  тренування", callback_data="show_ex_of_training"))#7
    builder.add(InlineKeyboardButton(text=" Видалити вправу з тренування", callback_data="del_ex_of_training"))
    builder.add(InlineKeyboardButton(text="  Подивитись статистику вправ", callback_data="show_inf_of_ex"))#8
    
   

    
    builder.adjust(1) # Выврод конопок по одной в столбик

    return builder.as_markup()

def get_variants_of_training_keyboard(date_name): # Вывод кнопок для редактирования и удаления тренировки
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Редагувати тренування", callback_data=f"edit_tr_date_{date_name}"))
    builder.add(InlineKeyboardButton(text="Далі", callback_data="continue_training"))
    

    builder.adjust(1) # Выврод конопок по одной в столбик
    return builder.as_markup()

def get_variants_of_inf_abt_ex_in_tr_keyboard(ex_name):
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text = "Змінити вагу", callback_data="edit_weight"))
    builder.add(InlineKeyboardButton(text="Змінити кількість повторень", callback_data="edit_reps"))

    builder.adjust(1) # Выврод конопок по одной в столбик
    return builder.as_markup()

def show_date_of_training_for_user(prefix, user_id, database):
    builder = InlineKeyboardBuilder()
    str_user_id = str(user_id)
    
    # ⚠️ Правильно: беремо дані тільки зі списку створених дат
    user_dates = database.get(str_user_id, {}).get("training_dates", [])
    
    for date_name in user_dates:
        builder.add(InlineKeyboardButton(text=date_name, callback_data=f"{prefix}{date_name}"))
        
    builder.adjust(1)
    return builder.as_markup()


def get_weight_keyboard(category, user_id, database): # Вывод кнопок для выбора веса
    builder = InlineKeyboardBuilder()
    user_data = database.get(str(user_id), {})
    user_weights = user_data.get('weights', [])
    for weight in user_weights:
        builder.add(InlineKeyboardButton(text=weight, callback_data=f"weight_{weight}"))
    builder.adjust(1)
    return builder.as_markup()

def get_reps_keyboard(category, user_id, database): # Вывод кнопок для выбора количества повторов
    builder = InlineKeyboardBuilder()
    user_data = database.get(str(user_id), {})
    user_reps = user_data.get('reps', [])
    for rep in user_reps:
        builder.add(InlineKeyboardButton(text=rep, callback_data=f"rep_{rep}"))
    builder.adjust(1)
    return builder.as_markup()

def get_exercise_for_training_keyboard(category, user_id, database): # Вывод кнопок упражнений для добавления к тренировке
    builder = InlineKeyboardBuilder()

    # Безопасно достаем упражнения пользователя
    user_data = database.get(str(user_id), {})
    user_exercises = user_data.get('exercise', {}).get(category, [])

    for ex_name in user_exercises:
        builder.add(InlineKeyboardButton(text=ex_name, callback_data=f"trainex_{ex_name}"))

    builder.adjust(1) # Вывод кнопок по одной в столбик

    return builder.as_markup()

def get_variants_of_date_keyboard(): # Вывод кнопок для редактирования и удаления даты
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Редагувати дату", callback_data="edit_date"))
    builder.add(InlineKeyboardButton(text="Видалити дату", callback_data="del_date"))
    builder.add(InlineKeyboardButton(text="Далі", callback_data="continue_date"))

    builder.adjust(1) # Выврод конопок по одной в столбик
    return builder.as_markup()

def get_variants_of_exercise_keyboard(): # Вывод кнопок для редактирования и удаления упражнения
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Редагувати вправу", callback_data="edit_ex"))
    builder.add(InlineKeyboardButton(text="Видалити вправу", callback_data="del_ex"))
    builder.add(InlineKeyboardButton(text="Далі", callback_data="continue_ex"))

    builder.adjust(1) # Выврод конопок по одной в столбик
    return builder.as_markup()



@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.reply(text="Выбирите вариант из списка", reply_markup=get_main_keyboard())    

@router.callback_query(F.data == "add_ex") #Добавить упр
async def add_ex_callback(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    await callback.message.edit_text(text="Ви обрали додати тренування")
    await callback.message.answer(text="Оберіть группу м'язів", reply_markup=get_categories_add_keyboard())    #Выводит выбор группы мышц 
        

@router.callback_query(F.data.startswith("addcat_"))
async def categ_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    category_name = callback.data.replace("addcat_", "")
    await state.update_data(chosen_category=category_name)
    await callback.message.answer("Введіть назву  вправи:")
    await state.set_state(AddExerciseState.waiting_for_name)
    

@router.message(StateFilter(AddExerciseState.waiting_for_name))
async def show_result(message: types.Message, state: FSMContext):
    ex_name = message.text
    data = await state.get_data()
    category = data.get("chosen_category")
    user_id = message.from_user.id

    
    add_user_exercise(user_id, category, ex_name)# Записываем в JSON


    await message.answer(f"Ви додали '{ex_name}'  категорію '{category}'" )
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())
    
    
@router.callback_query(F.data =="show_ex")
async def show_ex_callback(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    await callback.message.edit_text(text="Ви обрали показати вправи")
    await callback.message.answer(text="Оберіть группу м'язів",reply_markup=get_categories_edit_keyboard())    #Выводит выбор группы мышц 


@router.callback_query(F.data.startswith("categ_")) # метод проверки строки
async def categ_callback(callback: types.CallbackQuery, state: FSMContext ):
    
    category_name = callback.data.replace("categ_", "")
    await state.update_data(chosen_category=category_name)
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
           
        database = json.load(f)  
    user_id = callback.from_user.id
    await callback.message.answer( text=f"Оберіть вправу з категорії '{category_name}':", reply_markup=get_name_of_exersice(category_name, user_id, database))


    
@router.callback_query(F.data.startswith("ex_"))
async def ex_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    ex_name = callback.data.replace("ex_", "")

    
    await state.update_data(old_name=ex_name)# Запоминаем в память старое название

    await callback.message.answer(f"Ви обрали вправу '{ex_name}'. Що бажаєте зробити?", reply_markup=get_variants_of_exercise_keyboard())   
@router.callback_query(F.data == "edit_ex")
async def edit_ex_callback(callback: types.CallbackQuery,  state: FSMContext):
      
    await callback.answer()
    await state.set_state(EditExerciseState.waiting_for_new_name)
    await callback.message.edit_text(text="Ви обрали редагувати вправу")
    await callback.message.answer(text="Введіть нову назву вправи:")


def update_user_ex(user_id, category , old_name, new_name_ex):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return

    str_user_id = str(user_id)

    if str_user_id in data:
        # 1. Меняем имя в базовом списке упражнений
        if 'exercise' in data[str_user_id] and category in data[str_user_id]['exercise']:
            exercise_list = data[str_user_id]['exercise'][category]
            
            for m in range(len(exercise_list)):
                if exercise_list[m] == old_name:
                    exercise_list[m] = new_name_ex
                    break

        # 2. Меняем имя во всех сохраненных тренировках
        if 'training' in data[str_user_id]:
            # Используем list() для безопасной итерации по ключам (датам)
            for date_key in list(data[str_user_id]['training'].keys()):
                
                # Проверяем, есть ли в этой дате нужная категория
                if category in data[str_user_id]['training'][date_key]:
                    
                    # Проверяем, есть ли там старое упражнение
                    if old_name in data[str_user_id]['training'][date_key][category]:
                        # Переименовываем ключ
                        data[str_user_id]['training'][date_key][category][new_name_ex] = data[str_user_id]['training'][date_key][category].pop(old_name)

        # Записываем изменения в файл
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

@router.message(StateFilter(EditExerciseState.waiting_for_new_name))
async def process_new_exercise_name(message: types.Message, state: FSMContext):
    new_name_ex = message.text
    user_id = message.from_user.id

    
    user_data = await state.get_data() #Достаем данные из памяти 
    category = user_data.get("chosen_category")
    old_name = user_data.get("old_name")

    update_user_ex(user_id, category, old_name, new_name_ex) #Меняем старое имя на новое в файле

    await message.answer(text=f"Замінено назву вправи '{old_name}' на '{new_name_ex}' у категорії '{category}'")
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "del_ex")
async def del_ex_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    
    
    user_data = await state.get_data()
    category = user_data.get("chosen_category")
    ex_name = user_data.get("old_name") # або ex_name, яке зберігали при виборі
    user_id = callback.from_user.id

    # Викликаємо видалення зі списку
    delete_user_exercise(user_id, category, ex_name)

    await callback.message.edit_text(text=f"Вправу '{ex_name}' успішно видалено з категорії '{category}'!")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())  

@router.callback_query(F.data == "continue_ex")
async def continue_ex_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Далі")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "date_training")
async def date_training_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Ви обрали створити тренування")
    await callback.message.answer(text="Введіть дату тренування у форматі ДД.ММ.РРРР:")
    await state.set_state(AddExerciseState.waiting_for_date_of_training)
        
@router.message(StateFilter(AddExerciseState.waiting_for_date_of_training))
async def show_result(message: types.Message, state: FSMContext):
    date_name = message.text
    data = await state.get_data()
    category = data.get("chosen_category")
    user_id = message.from_user.id

    
    add_user_date(user_id, date_name)# Записываем в JSON


    await message.answer(f"Ви додали дату {date_name}")
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())


@router.callback_query(F.data == "show_date_training")
async def show_date_training_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Ви обрали показати дати тренувань")
    #Выводит даты 
    await callback.message.answer( text="Ваші дати тренувань:", 
                                  reply_markup=show_date_of_training("date_name", callback.from_user.id, json.load(open('strenght_inf.json', 'r', encoding='utf-8'))))
    

@router.callback_query(F.data.startswith("date_")) #Вывод кнопок дат
async def date_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    date_name = callback.data.replace("date_", "")
    await state.update_data(old_date=date_name)# Запоминаем в память старое название

    await callback.message.answer(f"Ви обрали дату {date_name}. Що бажаєте зробити?", reply_markup=get_variants_of_date_keyboard())      



@router.callback_query(F.data == "edit_date") #Вывод кнопок для редактирования даты
async def edit_date_callback(callback: types.CallbackQuery,  state: FSMContext):
      
    await callback.answer()
    await state.set_state(EditDateState.waiting_for_new_date)
    await callback.message.edit_text(text="Ви обрали редагувати дату")
    await callback.message.answer(text="Введіть нову дату тренування у форматі ДД.ММ.РРРР:")


def update_user_date(user_id,  old_date, new_date):
    file_name = 'strenght_inf.json'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return

    str_user_id = str(user_id)

    if str_user_id in data:
        # 1. Меняем дату в списке training_dates
        if 'training_dates' in data[str_user_id] and old_date in data[str_user_id]['training_dates']:
            dates_list = data[str_user_id]['training_dates']
            
            for m in range(len(dates_list)): 
                if dates_list[m] == old_date:
                    dates_list[m] = new_date
                    break
        
        # 2. Переименовываем ключ в словаре training, чтобы не потерять упражнения
        if 'training' in data[str_user_id] and old_date in data[str_user_id]['training']:
            # Извлекаем все данные за старую дату и переносим в новую
            data[str_user_id]['training'][new_date] = data[str_user_id]['training'].pop(old_date)

        # Записываем изменения в файл
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

@router.message(StateFilter(EditDateState.waiting_for_new_date))
async def process_new_exercise_date(message: types.Message, state: FSMContext):
    new_date = message.text
    user_id = message.from_user.id

    
    user_data = await state.get_data() #Достаем данные из памяти 
    old_date = user_data.get("old_date")

    update_user_date(user_id, old_date, new_date) #Меняем старую дату на новую в файле

    await message.answer(text=f"Замінено дату тренування '{old_date}' на '{new_date}'")
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "del_date") #Вывод кнопок для удаления даты
async def del_date_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    
    # Дістаємо збережені дані з пам'яті FSM
    user_data = await state.get_data()
    date_name = user_data.get("old_date") # або ex_name, яке зберігали при виборі
    user_id = callback.from_user.id

    # Викликаємо видалення зі списку
    delete_user_date(user_id, date_name)

    await callback.message.edit_text(text=f"Дату тренування '{date_name}' успішно видалено!")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())  

@router.callback_query(F.data == "continue_date")
async def continue_date_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Далі")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())



@router.callback_query(F.data == "add_ex_to_training")
async def add_ex_to_training_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Ви обрали додати вправу до тренування")
    await callback.message.answer(text="Оберіть дату тренування:", reply_markup=get_date_of_training("date_name",
                                                         callback.from_user.id, json.load(open('strenght_inf.json', 'r', encoding='utf-8'))))    #Выводит даты


@router.callback_query(F.data.startswith("datetrain_")) #Вывод кнопок дат
async def datetrain_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    date_name = callback.data.replace("datetrain_", "")
    await state.update_data(chosen_date=date_name)# Запоминаем в память старое название

    await callback.message.answer(f"Ви обрали дату {date_name}. Тепер оберіть групу м'язів для додавання вправи:", reply_markup=get_categories_training_keyboard())

@router.callback_query(F.data.startswith("train_categ_")) # метод проверки строки
async def train_categ_callback(callback: types.CallbackQuery, state: FSMContext):
    category_name = callback.data.replace("train_categ_", "")
    await state.update_data(chosen_category=category_name)
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)  
    user_id = callback.from_user.id
    await callback.message.answer(text=f"Оберіть вправу з категорії {category_name} для додавання до тренування:", reply_markup=get_exercise_for_training_keyboard(category_name, user_id, database))


@router.callback_query(F.data.startswith("trainex_"))
async def trainex_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    ex_name = callback.data.replace("trainex_", "")
    await state.update_data(chosen_exercise=ex_name)

    
    user_data = await state.get_data()
    chosen_date = user_data.get("chosen_date")
    chosen_category = user_data.get("chosen_category")
    
    real_user_id = callback.from_user.id

    add_user_exercise_to_training(real_user_id, chosen_date, chosen_category, ex_name)

    await callback.message.answer(f"Вправу '{ex_name}' додано до тренування на дату '{chosen_date}' у категорії '{chosen_category}'.")
    await callback.message.answer("Введіть вагу для цієї вправи:")
    await state.set_state(AddExerciseState.waiting_for_weight)


@router.message(StateFilter(AddExerciseState.waiting_for_weight))
async def process_weight(message: types.Message, state: FSMContext):
    weight = message.text
    await state.update_data(chosen_weight=weight)

    user_id = await state.get_data()
    chosen_date = user_id.get("chosen_date")
    chosen_category = user_id.get("chosen_category")
    chosen_exercise = user_id.get("chosen_exercise")

    # Здесь можно добавить логику для сохранения веса в JSON или другой источник данных
    add_user_weighht_for_training(user_id, chosen_date, chosen_category, chosen_exercise, weight)
    await message.answer(f"Вага '{weight}' додано до вправи '{chosen_exercise}' на дату '{chosen_date}' у категорії '{chosen_category}'.")
    await message.answer("Введіть кількість повторів для цієї вправи:")
    await state.set_state(AddExerciseState.waiting_for_reps)

@router.message(StateFilter(AddExerciseState.waiting_for_reps))
async def process_reps(message: types.Message, state: FSMContext):
    reps = message.text
    await state.update_data(chosen_reps=reps)

    user_id = await state.get_data()
    chosen_date = user_id.get("chosen_date")
    chosen_category = user_id.get("chosen_category")
    chosen_exercise = user_id.get("chosen_exercise")
    chosen_weight = user_id.get("chosen_weight")

    
    #add_user_reps_for_training(user_id, chosen_date, chosen_category, chosen_exercise, chosen_weight, reps)
    add_user_reps_for_training(message.from_user.id, chosen_date, chosen_category, chosen_exercise, chosen_weight, reps)
    await message.answer(f"Кількість повторів '{reps}' додано до вправи '{chosen_exercise}' на дату '{chosen_date}' у категорії '{chosen_category}'.")
    await message.answer("Вправа успішно додана до тренування!")
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

    

@router.callback_query(F.data == "show_ex_of_training")
async def show_ex_of_training_callback(callback: types.CallbackQuery, state: FSMContext):
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)

    keyboard = show_date_of_training_for_user("showdate_", callback.from_user.id, database)
    await callback.message.answer(
        text="Оберіть дату тренування:",
        reply_markup=keyboard)


@router.callback_query(F.data.startswith("showdate_"))
async def show_training_info_callback(callback: types.CallbackQuery):
    await callback.answer()
    
    # 1. Отримуємо чисту дату та ID користувача
    date_name = callback.data.replace("showdate_", "")
    user_id = str(callback.from_user.id)
    
    
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)
        
    # 3. Витягуємо тренування за обрану дату
    training_data = database.get(user_id, {}).get("training", {}).get(date_name, {})

    
    if not training_data:
        await callback.message.answer(f"❌  дата <b>{date_name}</b> тренувань не знайдено.", parse_mode="HTML")
        return

    
    msg_text = f" <b>Тренування за {date_name}</b>\n"

    for category, exercises in training_data.items():
        msg_text += f"💪 <b>Категорія: {category}</b>\n"
        if isinstance(exercises, dict):
            for ex_name, weights in exercises.items():
                msg_text += f"  • <b>{ex_name}</b>:\n"
                if isinstance(weights, dict):
                    for weight, reps in weights.items():
                        msg_text += f"     {weight} кг x {reps} повт.\n"
        msg_text += "\n"

    await callback.message.answer(text=msg_text, parse_mode="HTML")
    
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_variants_of_training_keyboard(date_name))



@router.callback_query(F.data == "edit_training")
async def edit_training_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Ви обрали редагувати тренування")
    await callback.message.answer(
        
        # ЗДЕСЬ МЕНЯЕМ НА "edit_tr_date_"
        reply_markup=show_date_of_training_for_user("edit_tr_date_", callback.from_user.id, json.load(open('strenght_inf.json', 'r', encoding='utf-8')))
    )  
@router.callback_query(F.data.startswith("edit_tr_date_"))
async def show_date_for_edit_tr(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    # И ЗДЕСЬ МЕНЯЕМ НА "edit_tr_date_"
    date_name = callback.data.replace("edit_tr_date_", "")
    
    await state.update_data(chosen_edit_date=date_name)

    # Відкриваємо базу
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)
        
    # Виводимо всі вправи суцільним списком кнопок
    keyboard = get_all_training_exercises_keyboard(date_name, callback.from_user.id, database)
    
    await callback.message.edit_text( text=f"Оберіть вправу для редагування у тренуванні за {date_name}:", reply_markup=keyboard )
    
    

@router.callback_query(F.data.startswith("edit_tr_ex_"))
async def process_exercise_edit_selection(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    
    # 1. Достаем чистое название упражнения
    ex_name = callback.data.replace("edit_tr_ex_", "")
    
    # 2. Запоминаем выбранное упражнение в "оперативную память" бота
    await state.update_data(chosen_edit_ex=ex_name)
    
    # 3. Вызываем клавиатуру, которую мы создали на Шаге 1
    new_keyboard = get_variants_of_inf_abt_ex_in_tr_keyboard(ex_name)
    
    # 4. Обновляем сообщение бота
    await callback.message.edit_text(
        text=f"Ви обрали вправу <b>{ex_name}</b>. Що бажаєте з нею зробити?",
        reply_markup=new_keyboard,
        parse_mode="HTML")

@router.callback_query(F.data =="edit_weight")
async def edit_weight_callback(callback : types.CallbackQuery , state : FSMContext):
    await callback.answer()
    await state.set_state(EditWeightState.waiting_for_new_weight)
    await callback.message.edit_text(text="Ви обрали редагувати вагу")
    await callback.message.answer(text="Введіть нову вагу:")
    
    
@router.message(StateFilter(EditWeightState.waiting_for_new_weight))
async def process_new_weight_for_tr(message: types.Message, state: FSMContext):
    new_weight = message.text
    user_id = message.from_user.id
    
    # Дістаємо дату та назву вправи, які ми запам'ятали раніше
    user_data = await state.get_data() 
    date_name = user_data.get("chosen_edit_date") 
    ex_name = user_data.get("chosen_edit_ex")
    
    
    # Викликаємо нашу нову функцію збереження ваги
    old_weight = update_user_weight(user_id, date_name, ex_name, new_weight)
    await message.answer(text=f"Замінено вагу для вправи '{ex_name} {old_weight}'на {new_weight} кг")
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data =="edit_reps")
async def edit_reps_callback(callback : types.CallbackQuery , state : FSMContext):
    await callback.answer()
    await state.set_state(EditRepsState.waiting_for_new_reps)
    await callback.message.edit_text(text="Ви обрали редагувати кількість повторень")
    await callback.message.answer(text="Введіть нову кількість повторень:")
    
    
@router.message(StateFilter(EditRepsState.waiting_for_new_reps))
async def process_new_reps_for_tr(message: types.Message, state: FSMContext):
    new_reps = message.text
    user_id = message.from_user.id
    
    # Дістаємо дату та назву вправи, які ми запам'ятали раніше
    user_data = await state.get_data() 
    date_name = user_data.get("chosen_edit_date") 
    ex_name = user_data.get("chosen_edit_ex")
    
    
    # Викликаємо нашу нову функцію збереження ваги
    old_reps = update_user_reps(user_id, date_name, ex_name, new_reps)
    await message.answer(text=f"Замінено кількість повторень  для вправи '{ex_name} {old_reps}'на {new_reps} ")
    await state.clear()
    await message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "continue_training")
async def continue_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Далі")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "del_ex_of_training")
async def del_ex_in_tr_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Ви обрали видалення вправи з тренування")
    
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)
        
    await callback.message.answer(
        text="Оберіть дату тренування:", 
        reply_markup=show_date_of_training_for_user("del_ex_tr_date_", callback.from_user.id, database)
    )

# Крок 2: Створюємо спеціальну клавіатуру, яка виведе вправи саме для видалення
def get_del_training_exercises_keyboard(date_name, user_id, database):
    builder = InlineKeyboardBuilder()
    user_data = database.get(str(user_id), {})
    training_data = user_data.get('training', {}).get(date_name, {})
    
    for category, exercises in training_data.items():
        for ex_name in exercises.keys():
            # Кнопки з унікальним префіксом 'finish_del_ex_'
            builder.add(InlineKeyboardButton(text=f"❌ {ex_name} ({category})", callback_data=f"finish_del_ex_{ex_name}"))
            
    builder.adjust(1) 
    return builder.as_markup()

# Крок 3: Ловимо обрану дату і виводимо список вправ
@router.callback_query(F.data.startswith("del_ex_tr_date_"))
async def process_date_for_del_ex(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    
    # Дістаємо дату і запам'ятовуємо її
    date_name = callback.data.replace("del_ex_tr_date_", "") 
    await state.update_data(del_ex_date=date_name) 
    
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)
        
    # Викликаємо нашу нову клавіатуру
    keyboard = get_del_training_exercises_keyboard(date_name, callback.from_user.id, database)
    
    await callback.message.edit_text(text=f"Оберіть вправу, яку хочете видалити з тренування за {date_name}:", reply_markup=keyboard)

# Крок 4: Ловимо обрану вправу і остаточно видаляємо її
@router.callback_query(F.data.startswith("finish_del_ex_"))
async def finish_del_ex_in_tr(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    
    # Дістаємо назву вправи
    ex_name = callback.data.replace("finish_del_ex_", "")
    user_id = callback.from_user.id
    
    # Дістаємо збережену раніше дату
    user_data = await state.get_data()
    date_name = user_data.get("del_ex_date")
    
    # Викликаємо вашу функцію видалення
    delete_user_ex_in_tr(user_id, date_name, ex_name)
    
    await callback.message.edit_text(text=f"Вправу <b>'{ex_name}'</b> успішно видалено з тренування за <b>{date_name}</b>!", parse_mode="HTML")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "show_inf_of_ex")
async def show_in_of_ex_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="Ви обрали подивитись статистику  вправ")
    await callback.message.answer(text="Оберіть группу м'язів",reply_markup=get_categories_stat_of_ex_keyboard())    #Выводит выбор группы мышц 
    
    
@router.callback_query(F.data.startswith("inf_of_ex_categ_")) # метод проверки строки
async def categ_for_inf_callback(callback: types.CallbackQuery, state: FSMContext ):
        
    category_name = callback.data.replace("inf_of_ex_categ_", "")
    await state.update_data(chosen_category=category_name)
    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
               
        database = json.load(f)  
        user_id = callback.from_user.id
    await callback.message.answer( text=f"Оберіть вправу з категорії '{category_name}':", reply_markup=get_ex_stat_of_ex_keyboard(category_name, user_id, database))

@router.callback_query(F.data.startswith("stat_of_ex_"))
async def stat_ex_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    ex_name = callback.data.replace("stat_of_ex_", "")
    user_id = str(callback.from_user.id)
    user_data = await state.get_data()
    category_name = user_data.get("chosen_category")

    with open('strenght_inf.json', 'r', encoding='utf-8') as f:
        database = json.load(f)

    # 1. Беремо історію тренувань
    training_history = database.get(user_id, {}).get("training", {})
    
    # 2. Формуємо красиве повідомлення
    msg_text = f"📊 <b>Статистика для вправи: {ex_name}</b>\n"
    found = False

    # 3. Шукаємо цю вправу по всіх збережених датах
    for date_name, date_data in training_history.items():
        # Якщо в цей день робили цю категорію і цю вправу:
        if category_name in date_data and ex_name in date_data[category_name]:
            found = True
            weights = date_data[category_name][ex_name]
            
            # Додаємо у повідомлення дату, вагу та повтори
            for weight, reps in weights.items():
                msg_text += f"📅 <b>{date_name}</b>: \n "
                msg_text += f" 💪 <b> {weight} кг </b>\n"
                msg_text += f"🔢 <b>{reps} повт</b>\n"
    # Якщо вправу жодного разу не робили на тренуваннях
    if not found:
        msg_text += "<i>Ви ще не виконували цю вправу на жодному тренуванні.</i>"

    # Виводимо статистику та повертаємо в меню
    await callback.message.edit_text(text=msg_text, parse_mode="HTML")
    await state.clear()
    await callback.message.answer("Оберіть наступну дію:", reply_markup=get_main_keyboard()) 



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
>>>>>>> 83f76d4d157f3b0cc09e7513bfbbcff9f7c67d28
