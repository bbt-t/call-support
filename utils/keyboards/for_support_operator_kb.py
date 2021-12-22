from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


operator_kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_yep = KeyboardButton('GO!')
button_no = KeyboardButton('not now / stop it!')
operator_kb.add(
    button_yep,
    button_no
)
