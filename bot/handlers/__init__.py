from bot.dispatcher import dp
from bot.handlers.main_handler import main
from bot.handlers.main_products import product
from bot.handlers.payments import payments
from bot.handlers.lang import lang

dp.include_routers(
    *[main,product,payments,lang]
)