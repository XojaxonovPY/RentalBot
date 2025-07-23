from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.buttons.reply import reply_button_builder
from bot.functions import admin
from bot.states import States

lang = Router()


@lang.message(F.text == __('🇬🇧 🇺🇿 Language'))
async def language_user(message: Message, state: FSMContext):
    text = ['🇺🇿 Uzbek', '🇬🇧 English', '◀️ Main back']
    markup = await reply_button_builder(text, [2] * (len(text) // 2))
    await state.set_state(States.language)
    await message.answer(text=_('Choose language:'), reply_markup=markup)


@lang.message(States.language)
async def language_handler(message: Message, state: FSMContext, i18n):
    map_lang = {
        '🇺🇿 Uzbek': 'uz',
        '🇬🇧 English': 'en'
    }
    code = map_lang.get(message.text)
    i18n.current_locale = code
    await state.update_data(locale=code)
    await state.clear()
    await state.update_data({'locale': lang})
    await state.update_data(locale=code)
    text = [_('🛠 Rental services'), _('🛒 Orders'), _('📞 Call Center'), _('🇬🇧 🇺🇿 Language')]
    if message.chat.id == admin:
        text.append(_('Admin'))
    markup = await reply_button_builder(text, [3] * (len(text) // 2))
    await message.answer(_('✅ Main menu:'), reply_markup=markup)


@lang.message(F.photo)
async def send_id(message: Message):
    file_id = message.photo[-1].file_id
    await message.answer(text=f'Image_id:{file_id}')
