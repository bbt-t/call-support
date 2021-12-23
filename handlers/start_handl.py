from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from loader import dp
from utils.db.db_commands import add_user




@dp.message_handler(CommandStart())
async def start_bot(message: Message, state: FSMContext):
    msg_text: str = ('Привет! Чтобы мы могли тебе помочь выбери способ связи ниже.\n' 
               '(если твоя проблема не требует незамедлительного решения, ' 
               'то лучше воспользоваться письменным обращением).\n' 
               'Проверить статус обращения или обратиться с новым можешь в любой момент через команду\n' 
               '<code>/support</code>')
    user_info = {
        'telegram_id': message.from_user.id,
        'full_name': message.from_user.full_name,
        'user_name': message.from_user.username
    }
    await add_user(**user_info)

    await message.answer(msg_text)
    await state.finish()
