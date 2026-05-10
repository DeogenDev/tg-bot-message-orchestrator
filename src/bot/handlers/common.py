"""Общие хендлеры."""

from aiogram import Router, F
from aiogram.enums import ParseMode

from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from aiogram.fsm.context import FSMContext

from src.bot.utils.texts import Texts
from src.bot.utils.buttons import Buttons

router = Router()

@router.message(CommandStart())
async def start_handler(
    message: Message,
    state: FSMContext,
    texts: Texts,
    buttons: Buttons
) -> None:
    await message.answer(
        texts.common.START,
        reply_markup=buttons.START_BUTTONS,
        parse_mode=ParseMode.HTML
    )

    await state.clear()


@router.callback_query(F.data == "start")
async def start_handler_callback(
    callback_query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
    buttons: Buttons
) -> None:
    await callback_query.message.edit_text(
        texts.common.START,
        reply_markup=buttons.START_BUTTONS,
        parse_mode=ParseMode.HTML
    )

    await state.clear()


@router.callback_query(F.data == "config_channels")
async def config_channels_handler_callback(
    callback_query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
    buttons: Buttons
) -> None:
    await callback_query.message.edit_text(
        texts.channels.ABOUT_CHANNELS_INFO,
        reply_markup=buttons.CHANNELS_CONFIG_BUTTONS,
        parse_mode=ParseMode.HTML
    )
    await state.clear()


@router.callback_query(F.data == "config_messages")
async def config_messages_handler_callback(
    callback_query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
    buttons: Buttons
) -> None:
    await callback_query.message.edit_text(
        texts.messages.ABOUT_MESSAGES_INFO,
        reply_markup=buttons.MESSAGES_CONFIG_BUTTONS,
        parse_mode=ParseMode.HTML
    )
    await state.clear()
