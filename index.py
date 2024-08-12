from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import json

# Replace 'YOUR_BOT_TOKEN' with the token you got from BotFather
BOT_TOKEN = '7150361716:AAFc7EolKIC1PmhIoeXiWBk2EYXoJiCiWjU'

def save_user_to_json(user_data):
    # Fayl nomi
    file_name = 'users.json'
    
    # Yangi foydalanuvchini faylga yozish uchun avval mavjud ma'lumotlarni yuklash kerak
    try:
        with open(file_name, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    # Yangi foydalanuvchini ro'yxatga qo'shish
    users.append(user_data)
    
    # Yangilangan ma'lumotlarni faylga qayta yozish
    with open(file_name, 'w') as file:
        json.dump(users, file, indent=4)


UZBEKISTAN_CITIES = {
    "Tashkent": "Tashkent",
    "Samarkand": "Samarkand",
    "Bukhara": "Bukhara",
    "Andijan": "Andijan",
    "Guliston": "Gulistan",
    "Fergana": "Fergana",
    "Namangan": "Namangan",
    "Qarshi": "Karshi",
    "Navoi": "Navoiy",
    "Khiva": "Khiva",
    "Jizzakh": "Jizzakh",
    "Nukus": "Nukus",
    "Kokand": "Kokand",
    "Termez": "Termez",
    "Urgench": "Urgench",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(city, callback_data=city)] for city in UZBEKISTAN_CITIES.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Shaharni tanlang:", reply_markup=reply_markup)

async def city_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    city = query.data
    await query.edit_message_text(text=f"{city} uchun namoz vaqtlari:")
    
    url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country=Uzbekistan&method=2"
    # url = f"https://www.namazvakti.com/StateList.php?countryID=209{city}"
    # url = f"https://api.pray.zone/v2/times/today.json?city={city}"


    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        timings = data['data']['timings']
        
        message = f"Namoz vaqtlari ({city}):\n"
        message += f"Bomdod: {timings['Fajr']}\n"
        message += f"Quyosh: {timings['Sunrise']}\n"
        message += f"Peshin: {timings['Dhuhr']}\n"
        message += f"Asr: {timings['Asr']}\n"
        message += f"Shom: {timings['Maghrib']}\n"
        message += f"Xufton: {timings['Isha']}\n"
        message += f"Namozingiz qabul bo`lsin({city}):\n"
        
        await query.edit_message_text(text=message)
    else:
        await query.edit_message_text(text="Namoz vaqtlari olishda xatolik yuz berdi.Qayta urinib ko`ring")

def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers.
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(city_selected))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
