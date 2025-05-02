
from aiogram.fsm.context import FSMContext
from aiogram import Router
from bot.buttons.reply import reply_button_builder
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from utils.env_data import BotConfig
from bot.functions import  check_count,order_save
from bot.states import States


payments=Router()
PAYMENT_CLICK_TOKEN = BotConfig.PAYMENT_CLICK_TOKEN


@payments.message(States.count)
async def order_handler(message: Message, state: FSMContext):
    quantity = message.text.strip()
    data = await state.get_data()
    id_ = data.get('product_id')
    name = data.get('name')
    price = data.get('price')
    total = data.get('total')
    count = data.get('count')
    prices=[
        {
            'id':id_,
            'name':name,
            'price': price
        }
    ]
    amount = await check_count(quantity,price,total)
    await state.update_data(price=amount)
    prices = [
        LabeledPrice(label=name, amount=amount),
    ]
    await message.answer_invoice('Products', f"Jami {quantity} mahsulot sotib  qilindi",
                                '1',"UZS",prices, PAYMENT_CLICK_TOKEN)


@payments.pre_checkout_query()
async def success_handler(pre_checkout_query: PreCheckoutQuery) -> None:
    await pre_checkout_query.answer(True)


@payments.message(lambda message: bool(message.successful_payment))
async def confirm_handler(message: Message, state: FSMContext):
    user_id = message.chat.id
    data=await state.get_data()
    product_id = data.get('product_id')
    product_name = data.get('name')
    product_price = data.get('price')
    product_count = data.get('count')
    product_price = float(product_price)
    product_count = int(product_count)
    if message.successful_payment:
        total_amount = message.successful_payment.total_amount//100
        order_id = int(message.successful_payment.invoice_payload)
        order = {
            'product_id': product_id,
            'product_name': product_name,
            'product_price': product_price,
            'product_count': product_count,
            'user_id': user_id,
        }
        await order_save(**order)
        await state.clear()
        await message.answer(text=f"✅ To'lo'vingiz uchun raxmat 😊 \n{total_amount}\n{order_id}")