from random import choice as random_choice

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.full_list_of_operators import id_operators
from loader import dp

support_callback = CallbackData('contact_support', 'messages', 'user_id', 'who_will_press_button')
cancel_support_callback = CallbackData('cancel_support', 'user_id')


async def check_support_available(support_id: int) -> int | None:
    state = dp.current_state(chat=support_id, user=support_id)
    state_now: str = await state.get_state()
    if state_now != "in_support":
        return support_id


async def get_support_manager() -> int | None:
    for support_id in id_operators:
        support_id: int = await check_support_available(support_id)
        return support_id if support_id else None


async def support_keyboard(messages: str, user_id=None):
    if user_id:
        contact_id, who_will_press_button, text = user_id, 'operator', 'Ответить пользователю'
    else:
        contact_id, who_will_press_button = await get_support_manager(), 'user'
        if messages == 'correspondence_with_operator' and contact_id is None:
            return False
        elif messages == 'contacting support' and contact_id is None:
            contact_id: int = random_choice(id_operators)
        text: str = 'Написать обращение' if messages == 'contacting support' else 'Написать оператору'

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=text,
            callback_data=support_callback.new(
                messages=messages,
                user_id=contact_id,
                who_will_press_button=who_will_press_button
            )
        )
    )

    if messages == 'correspondence_with_operator':
        keyboard.add(InlineKeyboardButton(text='Завершить',
                                          callback_data=cancel_support_callback.new(user_id=contact_id)))
    return keyboard


def cancel_support(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Завершить',
                    callback_data=cancel_support_callback.new(
                        user_id=user_id
                    )
                )
            ]
        ]
    )
