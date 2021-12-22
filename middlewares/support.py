from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from loader import dp




class SupportMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data: dict):
        state_data = dp.current_state(user=message.from_user.id, chat=message.from_user.id)
        match await state_data.get_state():
            case 'in_support':
                data = await state_data.get_data()
                second_id: str = data.get('second_id')
                await message.copy_to(second_id)

                raise CancelHandler()
