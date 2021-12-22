from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from loader import dp




@dp.message_handler(CommandStart(), state='*')
async def start_bot(message: Message, state: FSMContext):
    msg_text: str = ('Привет! Чтобы мы могли тебе помочь выбери способ связи ниже.\n' 
               '(если твоя проблема не требует незамедлительного решения, ' 
               'то лучше воспользоваться письменным обращением).\n' 
               'Проверить статус обращения или обратиться с новым можешь в любой момент через команду\n' 
               '<code>/support</code>')
    await message.answer(msg_text)
    await state.finish()
