from aiogram.types import Message, ContentTypes, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from utils.keyboards.inline.support_inl import support_callback, support_keyboard




@dp.message_handler(Command('support'))
async def contact_support(message: Message):
    msg_text: str = 'Хотите написать сообщение техподдержке? Нажмите на кнопку ниже!'
    keyboard = await support_keyboard(messages='contacting support')
    await message.answer(msg_text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages='contacting support'))
async def send_to_support(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.answer('Пришлите сообщение.')
    await state.set_state('wait_for_support_message')
    async with state.proxy() as data:
        data['user_id']: int = callback_data.get("user_id")


@dp.message_handler(state='wait_for_support_message', content_types=ContentTypes.ANY)
async def get_support_message(message: Message, state: FSMContext):
    async with state.proxy() as data:
        second_id: int = data.get('user_id')

    await message.bot.send_message(second_id, f'Вам сообщение! Вы можете ответить нажав на кнопку ниже')
    keyboard = await support_keyboard(messages='contacting support', user_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=keyboard)

    await message.answer('Отправлено!')
    await state.reset_state()
