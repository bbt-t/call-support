from loader import dp
from .throttling import ThrottlingMiddleware
from .support import SupportMiddleware

if __name__ == 'middlewares':
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(SupportMiddleware())
