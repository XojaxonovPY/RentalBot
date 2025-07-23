from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.buttons.reply import reply_button_builder
from db.model import Product, Order
from utils.env_data import BotConfig

payments = Router()
PAYMENT_CLICK_TOKEN = BotConfig.PAYMENT_CLICK_TOKEN


@payments.callback_query(F.data.startswith('day_') | F.data.startswith('hour_'))
async def order_handler(callback: CallbackQuery, state: FSMContext):
    time = callback.data.split('_')
    data = await state.get_data()
    product: Product = data.get('product')
    amount = 0
    if time[0] == 'day':
        amount = int(time[1]) * 24 * product.price * 100
    elif time[0] == 'hour':
        amount = int(time[1]) * product.price * 100

    prices = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
        }
    ]
    await state.update_data(total_price=amount, time=f'{time[1]} {time[0]}')
    prices = [
        LabeledPrice(label=product.name, amount=amount),
    ]
    await callback.message.answer_invoice(
        title="Products",
        description=f"{time[1]} {time[0]} uchun {product.name} mahsulotiga buyurtma.",
        payload="product_invoice",
        provider_token=PAYMENT_CLICK_TOKEN,
        currency="UZS",
        prices=prices
    )


@payments.pre_checkout_query()
async def success_handler(pre_checkout_query: PreCheckoutQuery) -> None:
    await pre_checkout_query.answer(True)


@payments.message(lambda message: bool(message.successful_payment))
async def confirm_handler(message: Message, state: FSMContext):
    user_id = message.chat.id

    data = await state.get_data()
    product = data.get('product')
    if message.successful_payment:
        order = {
            'product_id': product.id,
            'total_price': data.get('total_price'),
            'time': data.get('time'),
            'user_id': user_id,
        }
        order = await Order.create(**order)
        button = [_('◀️ Main back'),_('◀️ Back')]
        markup = await reply_button_builder(button,(2,))
        await state.clear()
        text = f"✅ To'lo'vingiz uchun raxmat😊\n{order.id}\n{order.total_price}"
        await message.answer(text=text, reply_markup=markup)
