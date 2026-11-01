import time
import random
import telebot
from telebot import types

# 🔴 ВСТАВЬ СВОЙ ТОКЕН ИЗ @BotFather:
API_TOKEN = '9122132996:AAHYzy9Zug2RCD2-vZmjDdcDBJksQ8h2hXM'
ADMIN_USERNAME = '@kIewvwer'

# 🔴 ВСТАВЬ СВОЙ TELEGRAM ID СЮДА (чтобы бот слушал твои команды на выдачу фишек):
# Свой ID можно узнать в боте @VerifyBot или @userinfobot
ADMIN_ID = 6635166707  

bot = telebot.TeleBot(API_TOKEN)
users_db = {}

def get_user_data(user_id):
    if user_id not in users_db:
        users_db[user_id] = {
            "balance": 0,  # Стартовый баланс теперь 0, пока ты не начислишь
            "last_daily": 0
        }
    return users_db[user_id]

def main_menu(message):
    uid = message.from_user.id
    udata = get_user_data(uid)
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, 
        row_width=2
    )
    
    b1 = types.KeyboardButton("🎰 Играть: Слоты (10 🌟)")
    b2 = types.KeyboardButton("📦 Игровые Кейсы")
    b3 = types.KeyboardButton("💳 Баланс / Касса")
    
    markup.add(b1)
    markup.add(b2, b3)
    
    txt = (
        f"⚙️ Game FlorNFT Gaming Platform\n"
        f"──────────────────\n"
        f"👤 ID: `{uid}`\n"
        f"💰 Доступно: {udata['balance']} звезд.\n"
        f"──────────────────\n"
        f"Выберите интересующий раздел:"
    )
    bot.send_message(
        message.chat.id, 
        txt, 
        parse_mode="Markdown",
        reply_markup=markup
    )

def cases_menu(message):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, 
        row_width=2
    )
    
    b1 = types.KeyboardButton("🎁 Daily Case (Бесплатно)")
    b2 = types.KeyboardButton("🍀 Case: Luck (25 🌟)")
    b3 = types.KeyboardButton("❤️ Case: Love (50 🌟)")
    b4 = types.KeyboardButton("🌿 Case: Clover (100 🌟)")
    b5 = types.KeyboardButton("👑 Case: Magnat (150 🌟)")
    b6 = types.KeyboardButton("⬅️ Назад")
    
    markup.add(b1)
    markup.add(b2, b3)
    markup.add(b4, b5)
    markup.add(b6)
    
    bot.send_message(
        message.chat.id, 
        "Выбор сертифицированного кейса:", 
        reply_markup=markup
    )

@bot.message_handler(commands=['start'])
def start_cmd(message):
    main_menu(message)

# СЕКРЕТНАЯ КОМАНДА ДЛЯ ТЕБЯ: выдача баланса игрокам в чате
# Формат: /give [ID игрока] [количество]
# Пример: /give 77712345 500
@bot.message_handler(commands=['give'])
def give_balance(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        amount = int(parts[2])
        
        tdata = get_user_data(target_id)
        tdata['balance'] += amount
        
        bot.send_message(
            message.chat.id, 
            f"✅ Успешно начислено {amount} звезд игроку `{target_id}`.",
            parse_mode="Markdown"
        )
        # Уведомляем игрока, если он запустил бота
        try:
            bot.send_message(
                target_id, 
                f"💳 Баланс пополнен администратором на **{amount}** звезд!"
            )
        except:
            pass
    except:
        bot.send_message(
            message.chat.id, 
            "Ошибка. Формат: /give [ID] [Сумма]"
        )

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    uid = message.from_user.id
    udata = get_user_data(uid)
    now = time.time()

    if message.text == "⬅️ Назад":
        main_menu(message)
        return
    elif message.text == "📦 Игровые Кейсы":
        cases_menu(message)
        return
    
    elif message.text == "💳 Баланс / Касса":
        txt = (
            f"💳 УПРАВЛЕНИЕ СЧЕТОМ FlorNFT\n"
            f"──────────────────\n"
            f"💰 Твой баланс: {udata['balance']} звезд.\n\n"
            f"📥 ДЛЯ ПОПОЛНЕНИЯ:\n"
            f"Напишите администратору {ADMIN_USERNAME} в ЛС. "
            f"Укажите ваш ID: `{uid}` и способ оплаты (Карта/Крипта).\n\n"
            f"📤 ДЛЯ ВЫВОДА:\n"
            f"Также напишите в ЛС {ADMIN_USERNAME}, указав сумму выигрыша."
        )
        bot.send_message(
            message.chat.id, 
            txt, 
            parse_mode="Markdown"
        )
        return

    # === ИГРА СЛОТЫ (30%) ===
    elif message.text == "🎰 Играть: Слоты (10 🌟)":
        if udata['balance'] < 10:
            bot.send_message(
                message.chat.id, 
                "❌ Недостаточно средств на балансе. Пополните счет через контакты кассы."
            )
            return
        
        udata['balance'] -= 10
        
        if random.random() < 0.30:
            win = random.randint(20, 100)
            udata['balance'] += win
            txt = (
                f"🎰 ИГРОВОЙ АВТОМАТ\n"
                f"📊 Статус ставка: Выигрыш [x{win/10:.1f}]\n"
                f"💵 Начислено: +{win} фишек.\n"
                f"💳 Текущий баланс: {udata['balance']}"
            )
            bot.send_message(message.chat.id, txt)
        else:
            txt = (
                f"🎰 ИГРОВОЙ АВТОМАТ\n"
                f"📊 Статус ставка: Проигрыш [x0.0]\n"
                f"💵 Списание: -10 фишек.\n"
                f"💳 Текущий баланс: {udata['balance']}"
            )
            bot.send_message(message.chat.id, txt)

    # === DAILY CASE (10%, 24ч) ===
    elif message.text == "🎁 Daily Case (Бесплатно)":
        if now - udata['last_daily'] < 86400:
            rem = int(86400 - (now - udata['last_daily']))
            bot.send_message(
                message.chat.id, 
                f"🔒 Доступ заблокирован. Повторное открытие возможно через: "
                f"{rem // 3600}ч {(rem % 3600) // 60}м."
            )
            return
        
        udata['last_daily'] = now
        if random.random() < 0.10:
            win = random.randint(10, 50)
            udata['balance'] += win
            bot.send_message(
                message.chat.id, 
                f"🎁 КЕЙС ОТКРЫТ\n📊 Результат: Успешно\n💰 Награда: +{win} фишек."
            )
        else:
            udata['balance'] += 1
            bot.send_message(
                message.chat.id, 
                f"🎁 КЕЙС ОТКРЫТ\n📊 Результат: Минимальный дроп\n💰 Награда: +1 фишка."
            )

    # === CASE LUCK (25 фишек, 20%) ===
    elif message.text == "🍀 Case: Luck (25 🌟)":
        if udata['balance'] < 25:
            bot.send_message(message.chat.id, "❌ Недостаточно средств.")
            return
        udata['balance'] -= 25
        if random.random() < 0.20:
            win = random.randint(60, 150)
            udata['balance'] += win
            bot.send_message(
                message.chat.id, 
                f"📦 CASE LUCK\n📊 Статус: Окупаемость\n💵 Зачислено: +{win} фишек."
            )
        else:
            udata['balance'] += 5
            bot.send_message(
                message.chat.id, 
                f"📦 CASE LUCK\n📊 Статус: Неокупаемый дроп\n💵 Зачислено: +5 фишек."
            )

    # === CASE LOVE (50 фишек, 20%) ===
    elif message.text == "❤️ Case: Love (50 🌟)":
        if udata['balance'] < 50:
            bot.send_message(message.chat.id, "❌ Недостаточно средств.")
            return
        udata['balance'] -= 50
        if random.random() < 0.20:
            win = random.randint(120, 300)
            udata['balance'] += win
            bot.send_message(
                message.chat.id, 
                f"📦 CASE LOVE\n📊 Статус: Окупаемость\n💵 Зачислено: +{win} фишек."
            )
        else:
            udata['balance'] += 10
            bot.send_message(
                message.chat.id, 
                f"📦 CASE LOVE\n📊 Статус: Неокупаемый дроп\n💵 Зачислено: +10 фишек."
            )

    # === CASE CLOVER (100 фишек, 21%) ===
    elif message.text == "🌿 Case: Clover (100 🌟)":
        if udata['balance'] < 100:
            bot.send_message(message.chat.id, "❌ Недостаточно средств.")
            return
        udata['balance'] -= 100
        if random.random() < 0.21:
            win = random.randint(250, 600)
            udata['balance'] += win
            bot.send_message(
                message.chat.id, 
                f"📦 CASE CLOVER\n📊 Статус: Высокая окупаемость\n💵 Зачислено: +{win} фишек."
            )
        else:
            udata['balance'] += 20
            bot.send_message(
                message.chat.id, 
                f"📦 CASE CLOVER\n📊 Статус: Неокупаемый дроп\n💵 Зачислено: +20 фишек."
            )

    # === CASE MAGNAT (150 фишек, Мишка 50%, NFT 15%) ===
    elif message.text == "👑 Case: Magnat (150 🌟)":
        if udata['balance'] < 150:
            bot.send_message(message.chat.id, "❌ Недостаточно средств.")
            return
        udata['balance'] -= 150
        rand = random.random()
        if rand < 0.15:
            udata['balance'] += 700
            bot.send_message(
                message.chat.id, 
                f"👑 CASE MAGNAT\n📊 СТАТУС: ДЖЕКПОТ\n🎁 Дроп: NFT Подарок (Эквивалент 700 фишек)."
            )
        elif rand < 0.65:
            udata['balance'] += 15
            bot.send_message(
                message.chat.id, 
                f"👑 CASE MAGNAT\n📊 Статус: Минимальный дроп\n🎁 Дроп: Игрушка Медведь (Эквивалент 15 фишек)."
            )
        else:
            win = random.randint(150, 300)
            udata['balance'] += win
            bot.send_message(
                message.chat.id, 
                f"👑 CASE MAGNAT\n📊 Статус: Средняя окупаемость\n💵 Зачислено: +{win} фишек."
            )

if __name__ == '__main__':
    print("Бот FlorNFT запущен в Termux!")
    bot.infinity_polling()
