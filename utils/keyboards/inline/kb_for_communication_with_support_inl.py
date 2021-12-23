from random import choice as random_choice

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.full_list_of_operators import id_operators
from loader import dp

support_callback = CallbackData('contact_support', 'messages', 'user_id', 'who_will_press_button')
cancel_support_callback = CallbackData('cancel_support', 'user_id')


async def free_operator_check(support_id: int | str) -> int | str | None:
    """
    Operator 'freedom' check.
    :param support_id: checked operator id
    :return: id or none
    """
    state = dp.current_state(chat=support_id, user=support_id)
    state_now: str = await state.get_state()
    if state_now != "in_support":
        return support_id


async def get_operator_id() -> int | None:
    """
    Selects operator id from the list and checks it for 'freedom'.
    :return: id or none
    """
    for support_id in id_operators:
        support_id: int = await free_operator_check(support_id)
        return support_id if support_id else None


async def support_kb(messages: str, user_id: int | str = None):
    """
    Forms a keyboard for the user and the operator.
    :param messages: one msg or chat with operator
    :param user_id: telegram id's
    :return: keyboards depending on the passed id
    """
    if user_id:
        contact_id, who_will_press_button, text = user_id, 'operator', 'Ответить'
    else:
        contact_id, who_will_press_button = await get_operator_id(), 'user'
        if messages == 'correspondence_with_operator' and not contact_id:
            return False
        elif messages == 'contacting_support' and not contact_id:
            contact_id: int = random_choice(id_operators)
        text: str = 'Написать обращение' if messages == 'contacting_support' else 'Написать оператору'

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
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Завершить', callback_data=cancel_support_callback.new(user_id=user_id))]
    ])
