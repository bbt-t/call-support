from aiogram.types import Message, ContentTypes, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.full_list_of_operators import id_operators
from loader import dp
from middlewares.throttling import rate_limit

from utils.keyboards.for_support_operator_kb import operator_kb
from utils.keyboards.inline.kb_for_communication_with_support_inl import support_callback, support_kb, free_operator_check, \
    get_operator_id, cancel_support, cancel_support_callback




@rate_limit(5, key='support')
@dp.message_handler(Command('support'))
async def contact_support(message: Message):
    if message.from_user.id in id_operators:
        await message.answer('Привет! Готов поработать?', reply_markup=operator_kb)
    else:
        keyboard_for_msg = await support_kb(messages='contacting_support')
        await message.answer('Привет! Выбери способ связи, письменное обращение?',
                             reply_markup=keyboard_for_msg)
        keyboard_for_chat = await support_kb(messages='correspondence_with_operator')
        await message.answer('или будем чатиться?)', reply_markup=keyboard_for_chat)


@dp.callback_query_handler(support_callback.filter(messages='contacting_support'))
async def send_to_support(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.answer('Пришлите сообщение.')
    await state.set_state('wait_for_support_message')
    async with state.proxy() as data:
        data['user_id'] = callback_data.get('user_id')


@dp.message_handler(state='wait_for_support_message', content_types=ContentTypes.ANY)
async def get_support_message(message: Message, state: FSMContext):
    async with state.proxy() as data:
        second_id: str = data.get('user_id')

    await message.bot.send_message(second_id, f'Вам сообщение! Вы можете ответить нажав на кнопку ниже')
    keyboard = await support_kb(messages='contacting_support', user_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=keyboard)

    await message.answer('Отправлено!')
    await state.reset_state()


@dp.callback_query_handler(support_callback.filter(messages='correspondence_with_operator',
                                                   who_will_press_button='user'))
async def chat_with_support(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.edit_text('OK! теперь ждём ответа от оператора...')

    user_id: str = callback_data.get('user_id')
    support_id = await get_operator_id() if not await free_operator_check(user_id) else user_id

    if not support_id:
        await call.message.edit_text('хммм...не нашла свободных операторов, попробуй обраться ко мне позже.\n'
                                     ':С')
        await state.finish()
    else:
        await state.set_state('wait_call_support')
        await state.update_data(second_id=support_id)

    kb_for_operator = await support_kb(messages='correspondence_with_operator', user_id=call.from_user.id)
    await call.bot.send_message(support_id, f'Пользователь {call.from_user.full_name} ждёт ответа...',
                                reply_markup=kb_for_operator)


@dp.callback_query_handler(support_callback.filter(messages='correspondence_with_operator',
                                                   who_will_press_button='operator'))
async def accept_chat_with_support(call: CallbackQuery, state: FSMContext, callback_data: dict):
    second_id: str = callback_data.get('user_id')
    user_state = dp.current_state(user=second_id, chat=second_id)

    if await user_state.get_state() != 'wait_call_support':
        await call.message.edit_text('УПС! некому отвечать, тебе повезло :D')
    else:
        await user_state.set_state('in_support')
        await state.set_state('in_support')
        await state.update_data(second_id=second_id)

        kb, kb_for_user = cancel_support(second_id), cancel_support(call.from_user.id)

        await call.message.edit_text('ЕСТЬ КОНТАКТ!\nчтобы завершить ваше общение можно нажать кнопку ниже...',
                                     reply_markup=kb)
        await call.bot.send_message(second_id, 'Оператор на связи!\n'
                                               'чтобы завершить ваше общение можно нажать кнопку ниже...',
                                    reply_markup=kb_for_user)


@dp.message_handler(state='wait_call_support', content_types=ContentTypes.ANY)
async def cant_send_msg_support(message: Message, state: FSMContext):
    async with state.proxy() as data:
        second_id: str = data.get('second_id')

    await message.answer('Подожди ответа оператора или отмени звонок...',
                         reply_markup=cancel_support(second_id))


@dp.callback_query_handler(cancel_support_callback.filter(), state=['in_support', 'wait_call_support', None])
async def refuse_support(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user_id: str = callback_data.get('user_id')
    second_state = dp.current_state(user=user_id, chat=user_id)

    if await second_state.get_state() is not None:
        async with second_state.proxy() as data:
            second_id: int = int(data.get("second_id"))
        if second_id == call.from_user.id:
            await call.bot.send_message(user_id, 'завершено.')
            await second_state.finish()

    await call.message.edit_text('Пока пока!')
    await state.finish()
