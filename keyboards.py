from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
def main_keyboard():
 return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='✍️ Написать текст'),KeyboardButton(text='📄 Резюме')],[KeyboardButton(text='💼 Работа'),KeyboardButton(text='🌍 Перевод')],[KeyboardButton(text='🧠 Объяснить'),KeyboardButton(text='💡 Идея')],[KeyboardButton(text='🤖 AI-чат'),KeyboardButton(text='👤 Профиль')]],resize_keyboard=True)
