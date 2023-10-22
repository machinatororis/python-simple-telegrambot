import telebot # імпортували набір інструментів
from telebot import types # інструменти для кнопок

token = token # токен бота

alex = telebot.TeleBot(token) # створення об'екту класу TeleBot

keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True) # кажемо, що keyboard_menu це об'єкт клавіатури'
product = types.KeyboardButton("Товари 🛍")
cart = types.KeyboardButton("Кошик 🗑")
contacts = types.KeyboardButton("Контакти 📞")
keyboard_menu.add(product, cart, contacts)

@alex.message_handler(commands=['start'])
def start(message):
    alex.send_message(message.chat.id, "Меню:", reply_markup=keyboard_menu)
    new_order = open(f"orders/new_order_{message.chat.id}.txt", "w")
    new_order.close()


@alex.message_handler(content_types=["text"]) # вчимо Алекса обробляти текст.повідомлення
def menu_check(message): # Функція обробки
    # умови
    if message.text == "hello":
        print(message.chat.id)
        alex.send_message(message.chat.id, "hello")
    if message.text == "Товари 🛍":
        keyboard_category = types.ReplyKeyboardMarkup(resize_keyboard=True)
        phone = types.KeyboardButton('Телефони 📱')
        tv = types.KeyboardButton('Телевізори 📺')
        menu = types.KeyboardButton('🔙 Меню')
        keyboard_category.add(phone, tv, menu)
        alex.send_message(message.chat.id, "Оберіть категорію", reply_markup=keyboard_category)

    if message.text == "Кошик 🗑":
        file_cart = open(f"orders/new_order_{message.chat.id}.txt", "r")
        cart = file_cart.read().split('\n')
        file_cart.close()
        message_text = ''
        total_price = 0
        for element in cart:
            if element:
                text_parse = element.split(";")
                total_price = total_price + int(text_parse[2].replace(" ", "")) # додаємо до загальної суми вартість товару
                message_text = message_text + f'{text_parse[0]} - {text_parse[1]}, ціна: {text_parse[2]}\n'
        message_text = message_text + f'Загальна сума: {total_price}₴' # естетично виводимо дані у текст повідомлення
        orders_keyboard = types.InlineKeyboardMarkup()
        orders_button = types.InlineKeyboardButton(text="Оформити замовлення", callback_data="Оформити")
        orders_keyboard.add(orders_button)
        alex.send_message(message.chat.id, message_text, reply_markup=orders_keyboard)
    if message.text == "🔙 Меню":
        alex.send_message(message.chat.id, "Меню:", reply_markup=keyboard_menu)
    if message.text == "Контакти 📞":
        alex.send_message(message.chat.id, "📍 вулиця Хрещатик, 1\n        Київ, 02000\n📞 +380 67 123 45 67")
    if message.text == "Телефони 📱":
        file_phone = open('phone.txt', "r")
        db_phone = file_phone.read().split('\n')
        file_phone.close()
        phone_keyboard = types.InlineKeyboardMarkup()
        for i in db_phone:
            text_parse = i.split(";")
            button = types.InlineKeyboardButton(text=f'{text_parse[0]} - {text_parse[1]}, ціна: {text_parse[2]}₴', callback_data=i)
            phone_keyboard.add(button)
        alex.send_message(message.chat.id, "Категорія телефони 📱:", reply_markup=phone_keyboard)
    if message.text == "Телевізори 📺":
        file_phone = open('tv.txt', "r")
        db_phone = file_phone.read().split('\n')
        file_phone.close()
        phone_keyboard = types.InlineKeyboardMarkup()
        for i in db_phone:
            text_parse = i.split(";")
            button = types.InlineKeyboardButton(text=f'{text_parse[0]} - {text_parse[1]} дюймів, ціна: {text_parse[2]}₴',
                                                callback_data=i)
            phone_keyboard.add(button)
        alex.send_message(message.chat.id, "Категорія телевізори 📺:", reply_markup=phone_keyboard)

@alex.callback_query_handler(func=lambda call: True)
def call_data_me(call):
    if call.data:
        if call.data == "Оформити":
            user_number = alex.send_message(call.message.chat.id, "Напишіть номер телефону та наш менеджер зв'яжеться з вами протягом п'яти хвилин")
            alex.register_next_step_handler(user_number, check_order)
        else:
            new_order = open(f"orders/new_order_{call.message.chat.id}.txt", "a")
            new_order.write(call.data + '\n')
            new_order.close()
            text_parse = call.data.split(";")
            alex.send_message(call.message.chat.id, f'{text_parse[0]} - {text_parse[1]} додано до кошика')

def check_order(message):
    file_cart = open(f"orders/new_order_{message.chat.id}.txt", "r")
    cart = file_cart.read().split('\n')
    file_cart.close()
    message_text = ''
    total_price = 0
    for element in cart:
        if element:
            text_parse = element.split(";")
            total_price = total_price + int(text_parse[2].replace(" ", ""))  # додаємо до загальної суми вартість товару
            message_text = message_text + f'{text_parse[0]} - {text_parse[1]}, ціна: {text_parse[2]}\n'
    message_text = message_text + f'Загальна сума: {total_price}₴'  # естетично виводимо дані у текст повідомлення
    alex.send_message(-4066157954, f'Нове замовлення.\n{message_text}\nНомер телефону: {message.text}')

alex.polling(none_stop=True, interval=0) # графік роботи Алекса
