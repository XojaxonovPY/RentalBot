from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.buttons.inline import build_inline_buttons
from bot.buttons.reply import reply_button_builder
from bot.states import States
from db.model import Product

product = Router()


@product.callback_query(F.data.startswith('category_'))
async def category_handler(callback: CallbackQuery):
    category_id = callback.data.split('_')[1]
    products:list[Product] = await Product.gets(Product.category_id, int(category_id))
    text = [InlineKeyboardButton(text=i.name, callback_data=f'product_{i.id}') for i in products]
    markup = await build_inline_buttons(text, [2] * (len(products) // 2))
    await callback.message.answer(text=_('✅ Rent objects:'), reply_markup=markup)


@product.callback_query(F.data.startswith('product_'))
async def product_handler(callback: CallbackQuery, state: FSMContext):
    product_id = callback.data.split('_')[1]
    product: Product = await Product.get(Product.id, int(product_id))
    caption = f'Name-{product.name}\nPrice-{product.price}\nCount-{product.count}'
    await state.update_data(product=product)
    text = [_('📆 Day'), _('🕰 Hour'), _('◀️ Main back'), _('◀️ Back')]
    markup = await reply_button_builder(text, (2,))
    await callback.message.answer_photo(photo=product.image, caption=caption, reply_markup=markup)


@product.message(F.text == __('📆 Day'))
async def day_handler(message: Message, state: FSMContext):
    text = [InlineKeyboardButton(text=f'{i} day',callback_data=f'day_{i}') for i in range(1, 11)]
    markup = await build_inline_buttons(text, [2] * (len(text) // 2))
    await state.set_state(States.count)
    await message.answer(text=_('✅ How many days:'), reply_markup=markup)


@product.message(F.text == __('🕰 Hour'))
async def day_handler(message: Message, state: FSMContext):
    text = [InlineKeyboardButton(text=f'{i} hour',callback_data=f'hour_{i}') for i in range(1, 13)]
    markup = await build_inline_buttons(text, [3] * (len(text) // 2))
    await state.set_state(States.count)
    await message.answer(text=_('✅ How many hours:'), reply_markup=markup)


# ===============================================Searching========================================

@product.inline_query()
async def inline_query(inline: InlineQuery):
    query = inline.query.lower()
    result = []
    products: list = await  Product.get_all()
    for product in products:
        if query in product.name.lower():
            i = InlineQueryResultArticle(
                id=str(f'👤{product.id}'),
                title=product.name,
                description=str(f'Hour:{product.price}\n Count:{product.count}'),
                thumbnail_url=product.link,
                input_message_content=InputTextMessageContent(message_text=str(product.id)),
            )
            result.append(i)
    await inline.answer(result, cache_time=5, is_personal=True)


@product.message(F.via_bot)
async def any_text(message: Message,state:FSMContext):
    product_id = int(message.text)
    await message.delete()
    product:Product=await Product.get(Product.id,product_id)
    caption = f'Name:{product.name}\nPrice:{product.price}\nCount:{product.count}'
    await state.update_data(product=product)
    text = [_('📆 Day'), _('🕰 Hour'), _('◀️ Main back'), _('◀️ Back')]
    markup = await reply_button_builder(text, (2,))
    await message.answer_photo(photo=product.image,caption=caption,reply_markup=markup)
