"""Хендлер для работы с каналами."""

import logging

from aiogram import Router, F

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from src.bot.utils.texts import Texts
from src.bot.utils.buttons import Buttons
from src.bot.utils.states import InputStates

from src.core.interfaces.channels_service import ChannelServiceBase
from src.core.schemas.channel import DeleteChannelModel, ChannelModel


logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F == "add_channel")
async def add_channel_handler_callback(
    callback_query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
    buttons: Buttons
) -> None:
    await callback_query.message.edit_text(
        texts.channels.INPUT_FORWARD_MESSAGE,
        reply_markup=buttons.RETURN_TO_CHANNELS_CONFIG_BUTTONS
    )

    await state.set_state(InputStates.channel_link)


@router.message(InputStates.channel_link)
async def add_channel_handler(
    message: Message,
    state: FSMContext,
    channel_service: ChannelServiceBase,
    texts: Texts,
    buttons: Buttons
) -> None:
    await state.clear()

    chat_data = message.forward_from_chat

    if not chat_data:
        await message.answer(
            texts.channels.FAIL_ADD_CHANNEL,
            reply_markup=buttons.RETURN_TO_CHANNELS_CONFIG_BUTTONS
        )
        return

    channel = ChannelModel(
        channel_id=chat_data.id,
        author_id=message.from_user.id,
        channel_username=chat_data.username,
        title=chat_data.title,
        author_username=message.from_user.username
    )

    await channel_service.add_channel(channel)

    await message.answer(
        texts.channels.SUCCESS_ADD_CHANNEL,
        reply_markup=buttons.RETURN_TO_CHANNELS_CONFIG_BUTTONS
    )


@router.callback_query(F == "delete_channel")
async def choise_delete_channel_handler_callback(
    callback_query: CallbackQuery,
    texts: Texts,
    buttons: Buttons,
    channel_service: ChannelServiceBase,
) -> None:
    channels = await channel_service.get_channels()

    if not channels:
        await callback_query.message.edit_text(
            texts.channels.NO_CHANNELS,
            reply_markup=buttons.RETURN_TO_CHANNELS_CONFIG_BUTTONS
        )
        return

    channels_buttons = []

    for channel in channels:
        channels_buttons.append(
            InlineKeyboardButton(
                text=channel.title,
                callback_data=f"delete_channel_id:{channel.channel_id}"
            )
        )

    channels_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            channels_buttons,
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="config_channels")
            ]
        ]
    )

    await callback_query.message.edit_text(
        texts.channels.CHOISE_CHANNEL_FOR_DELETE,
        reply_markup=channels_keyboard
    )


@router.callback_query(F.startwith("delete_channel_id:"))
async def delete_channel_handler_callback(
    callback_query: CallbackQuery,
    texts: Texts,
    buttons: Buttons,
    channel_service: ChannelServiceBase,
) -> None:
    channel_id = callback_query.data.split(":")[1]

    delete_channel_model = DeleteChannelModel(
        channel_id=int(channel_id)
    )
    text = texts.channels.FAIL_DELETE_CHANNEL

    try:
        await channel_service.delete_channel(delete_channel_model)
        text = texts.channels.SUCCESS_DELETE_CHANNEL
    except Exception as e:
        logger.error(f"Ошибка при удалении канала: {e}")

    try:
        await callback_query.message.edit_text(
            text=text,
            reply_markup=buttons.RETURN_TO_CHANNELS_CONFIG_BUTTONS
        )
    except Exception as e:
        logger.warning(f"Не удалось обновить сообщение: {e}")
