import asyncio,logging
from aiogram import Bot,Dispatcher,F
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN,ADMIN_ID,FREE_REQUESTS_PER_DAY
from database import init_db,add_user,get_usage,increment_usage,get_stats
from keyboards import main_keyboard
from ai import ask_ai
logging.basicConfig(level=logging.INFO)
bot=Bot(token=BOT_TOKEN); dp=Dispatcher(); user_modes={}
WELCOME='''🤖 <b>НейроПомощник</b>\n\nТвой универсальный AI-помощник в Telegram.\n\n✍️ Тексты\n📄 Резюме\n💼 Работа\n🌍 Перевод\n🧠 Объяснения\n💡 Идеи\n🤖 AI-чат\n\nВыбери режим ниже 👇'''
@dp.message(Command('start'))
async def start(m:Message):
 add_user(m.from_user.id,m.from_user.username,m.from_user.first_name); user_modes[m.from_user.id]='chat'; await m.answer(WELCOME,reply_markup=main_keyboard(),parse_mode='HTML')
@dp.message(Command('help'))
async def help_cmd(m:Message): await m.answer('<b>Как пользоваться</b>\n\nВыбери режим и отправь запрос.\n/start — меню\n/profile — профиль\n/help — помощь',parse_mode='HTML')
@dp.message(Command('profile'))
@dp.message(F.text=='👤 Профиль')
async def profile(m:Message):
 add_user(m.from_user.id,m.from_user.username,m.from_user.first_name); used,pro=get_usage(m.from_user.id); await m.answer(f'👤 <b>Профиль</b>\n\nСтатус: {"⭐ PRO" if pro else "🆓 FREE"}\nЗапросов осталось: {"без ограничений" if pro else max(0,FREE_REQUESTS_PER_DAY-used)}',parse_mode='HTML')
async def mode(m,mode,title): user_modes[m.from_user.id]=mode; await m.answer(title+'\n\nОтправь запрос 👇',parse_mode='HTML')
for text,mode,title in [('✍️ Написать текст','text','✍️ <b>Написание текста</b>'),('📄 Резюме','resume','📄 <b>Резюме</b>'),('💼 Работа','work','💼 <b>Работа</b>'),('🌍 Перевод','translate','🌍 <b>Перевод</b>'),('🧠 Объяснить','explain','🧠 <b>Объяснение</b>'),('💡 Идея','idea','💡 <b>Генератор идей</b>')]:
 async def h(m,text=text,mode=mode,title=title): await mode(m,mode,title)
 dp.message.register(h,F.text==text)
@dp.message(F.text=='🤖 AI-чат')
async def chat(m): user_modes[m.from_user.id]='chat'; await m.answer('🤖 <b>AI-чат</b>\n\nПиши вопрос.',parse_mode='HTML')
@dp.message(Command('admin'))
async def admin(m):
 if m.from_user.id==ADMIN_ID:
  u,p=get_stats(); await m.answer(f'📊 Пользователей: {u}\n⭐ PRO: {p}')
@dp.message(F.text)
async def ai_message(m:Message):
 uid=m.from_user.id; add_user(uid,m.from_user.username,m.from_user.first_name); used,pro=get_usage(uid)
 if not pro and used>=FREE_REQUESTS_PER_DAY: return await m.answer('⛔ Бесплатные запросы на сегодня закончились. Попробуй завтра.')
 await m.bot.send_chat_action(m.chat.id,'typing')
 try:
  ans=await ask_ai(m.text,user_modes.get(uid,'chat')); 
  if not pro: increment_usage(uid)
  await m.answer(ans)
 except Exception: logging.exception('AI request failed'); await m.answer('⚠️ Ошибка. Попробуй ещё раз.')
async def main(): init_db(); print('НейроПомощник запущен.'); await dp.start_polling(bot)
if __name__=='__main__': asyncio.run(main())
