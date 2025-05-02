from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton
from bot.buttons.inline import build_inline_buttons
from bot.buttons.reply import reply_button_builder
from bot.functions import save_user, get_category, get_order, to_string,admin
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

main=Router()

@main.message(F.text==__('◀️ Main back'))
@main.message(CommandStart())
async def command_start(message:Message):
    user_id=message.chat.id
    user={
        'user_id':message.from_user.id,
        'username':message.from_user.username,
    }
    await save_user(**user)
    text=[_('🛠 Rental services'),_('🛒 Orders'),_('📞 Call Center'),_('🇬🇧 🇺🇿 Language')]
    if user_id==admin:
        text.append(_('Admin'))
    markup= await reply_button_builder(text,[3]*(len(text)//2))
    await message.answer(text='✅ Main menu:',reply_markup=markup)


@main.message(F.text==__('📞 Call Center'))
async def call_handler(message:Message):
    await message.answer(text='(998)-277-12-81')


@main.message(F.text==__('🛠 Rental services'))
async def main_handler(message:Message):
    category=await get_category()
    text=[InlineKeyboardButton(text=i.name,callback_data=f'category_{i.id}')for i in category]
    text2 = [InlineKeyboardButton(text=_('🔎Search'), switch_inline_query_current_chat='')]
    markup2 = await build_inline_buttons(text2)
    markup=await build_inline_buttons(text,[2]*(len(category) // 2))
    await message.answer(text=_('✅ Searching rents'), reply_markup=markup2)
    await message.answer(text=_('✅ Main category'),reply_markup=markup)


@main.message(F.text==__('🛒 Orders'))
async def order_handler(message:Message):
    user_id=message.from_user.id
    name,price,time=await get_order(user_id)
    name=await to_string(name)
    price=await to_string(price)
    time=await to_string(time)
    await message.answer(text=f'Name:{name}\nTime:{time}\nPrice:{price}')