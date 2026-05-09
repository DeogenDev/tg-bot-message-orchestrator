"""Хендлер для работы с кнопками."""

import logging

from typing import Optional
from aiogram import Router, F

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.fsm.context import FSMContext

from src.bot.utils.texts import Texts
from src.bot.utils.buttons import Buttons
from src.bot.utils.states import InputStates

from src.core.interfaces.messages_service import MessagesServiceBase
from src.core.schemas.message import ButtonModel, DeleteButtonModel


logger = logging.getLogger(__name__)
router = Router()


def build_keyboard_delete_buttons(buttons: list[ButtonModel]) -> Optional[InlineKeyboardMarkup]:

    if not buttons:
        return None

    builder = InlineKeyboardBuilder()
    
    # Сортируем кнопки по рядам, чтобы они шли по порядку
    sorted_buttons = sorted(buttons, key=lambda b: (b.row, b.column))
    
    # Группируем кнопки по рядам
    rows: dict[int, list[ButtonModel]] = {}
    for btn in sorted_buttons:
        rows.setdefault(btn.row, []).append(btn)
    
    # Добавляем кнопки в билдер построчно
    for row_index in sorted(rows.keys()):
        row_btns = [
            InlineKeyboardButton(text=btn.text, callback_data=f"delete_button_id:{btn.id}") 
            for btn in rows[row_index]
        ]
        builder.row(*row_btns)

    builder.row(InlineKeyboardButton(
        text="⬅️ Назад", 
        callback_data="config_messages"
    ))

    return builder.as_markup()


def build_advanced_keyboard(buttons: list[ButtonModel]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # 1. Если кнопок нет вообще
    if not buttons:
        builder.row(InlineKeyboardButton(
            text="✅ Выбрать",
            callback_data="add_button:1:1"
        ))
    else:
        # 2. Группируем существующие кнопки по рядам
        rows: dict[int, list[ButtonModel]] = {}
        for btn in sorted(buttons, key=lambda b: (b.row, b.column)):
            rows.setdefault(btn.row, []).append(btn)
        
        # Проходим по рядам
        for row_index in sorted(rows.keys()):
            current_row_models = rows[row_index]
            
            row_btns = [
                InlineKeyboardButton(text=btn.text, url=btn.url) 
                for btn in current_row_models
            ]
            
            # Если в ряду меньше 3 кнопок, добавляем "Выбрать" справа
            if len(row_btns) < 3:
                # Находим максимальную колонку в текущем ряду
                max_col = max(btn.column for btn in current_row_models)
                row_btns.append(InlineKeyboardButton(
                    text="✅ Выбрать",
                    callback_data=f"add_button:{row_index}:{max_col + 1}"
                ))
            
            builder.row(*row_btns)

    # 3. Кнопка "Назад" всегда в самом низу
    builder.row(InlineKeyboardButton(
        text="⬅️ Назад", 
        callback_data="config_messages"
    ))

    return builder.as_markup()


@router.callback_query(F == "add_button")
async def add_button_handler_callback(
    callback_query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
    messages_service: MessagesServiceBase
) -> None:

    message_id = await state.get_data()["open_message_id"]

    message_model = await messages_service.get_message(id=message_id)

    add_keyboard = build_advanced_keyboard(message_model.buttons)

    await callback_query.message.edit_text(
        texts.buttons.CHOISE_BUTTON_FOR_DELETE,
        reply_markup=add_keyboard
    )

@router.callback_query(F.startwith("add_button:"))
async def add_button_handler_text(
    callback_query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
    buttons: Buttons
) -> None:
    row, col = callback_query.data.split(":")[1:]
    await state.set_data({"add_button": {"row": row, "col": col}})

    await callback_query.message.edit_text(
        texts.buttons.INPUT_BUTTON_TEXT,
        reply_markup=buttons.RETURN_TO_MESSAGES_CONFIG_BUTTONS
    )

    await state.set_state(InputStates.button_text)


@router.message(InputStates.button_text)
async def add_button_handler_url(
    message: Message,
    state: FSMContext,
    texts: Texts,
    buttons: Buttons
) -> None:
    await message.answer(
        texts.buttons.INPUT_BUTTON_FORWARD_MESSAGE,
        reply_markup=buttons.RETURN_TO_MESSAGES_CONFIG_BUTTONS
    )

    await state.set_data({"add_button": {"text": message.text}})

    await state.set_state(InputStates.button_url)


@router.message(InputStates.button_url)
async def add_button(
    message: Message,
    state: FSMContext,
    texts: Texts,
    buttons: Buttons,
    message_service: MessagesServiceBase
) -> None:

    if not message.forward_from_chat or not message.forward_from_message_id:
        await message.answer(
            texts.buttons.FAIL_ADD_BUTTON,
            reply_markup=buttons.RETURN_TO_MESSAGES_CONFIG_BUTTONS
        )
        return

    text = texts.buttons.FAIL_ADD_BUTTON

    chat = message.forward_from_chat
    msg_id = message.forward_from_message_id
    

    if chat.username:
        # Для публичных каналов
        final_url = f"https://t.me{chat.username}/{msg_id}"
    else:
        # Для приватных каналов (нужно убрать префикс -100 из ID)
        clean_id = str(chat.id).replace("-100", "")
        final_url = f"https://t.me/c/{clean_id}/{msg_id}"

    # Получаем данные из стейта один раз для экономии ресурсов
    try:
        state_data = await state.get_data()
        add_data = state_data.get("add_button", {})
        
        button = ButtonModel(
            text=add_data("text"),
            url=final_url,
            row=add_data("row"),
            column=add_data("col"),
            message_id=state_data("open_message_id")
        )

        await message_service.add_button(button)

        text = texts.buttons.SUCCESS_ADD_BUTTON
    except Exception as e:
        logger.error(f"Ошибка при добавлении кнопки: {e}")

    await state.clear()

    await message.answer(
        text=text,
        reply_markup=buttons.RETURN_TO_MESSAGES_CONFIG_BUTTONS
    )

@router.callback_query(F == "delete_button")
async def delete_button_handler_callback(
    callback_query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
    buttons: Buttons,
    messages_service: MessagesServiceBase
) -> None:
    message_id = await state.get_data()["open_message_id"]

    message_model = await messages_service.get_message(id=message_id)

    delete_button_keyboard = build_keyboard_delete_buttons(message_model.buttons)

    if not delete_button_keyboard:
        await callback_query.message.edit_text(
            texts.messages.NO_BUTTONS,
            reply_markup=buttons.RETURN_TO_MESSAGES_CONFIG_BUTTONS
        )
        return

    await callback_query.message.edit_text(
        texts.buttons.CHOISE_BUTTON_FOR_DELETE,
        reply_markup=delete_button_keyboard
    )


@router.callback_query(F.startwith("delete_button_id:"))
async def delete_button_callback(
    callback_query: CallbackQuery,
    texts: Texts,
    buttons: Buttons,
    messages_service: MessagesServiceBase
) -> None:
    button_id = callback_query.data.split(":")[1]
    delete_button_model = DeleteButtonModel(id=button_id)

    text = texts.buttons.FAIL_DELETE_BUTTON

    try:
        await messages_service.delete_button(delete_button_model)
        text = texts.buttons.SUCCESS_DELETE_BUTTON
    except Exception as e:
        logger.error(f"Ошибка при удалении кнопки: {e}")

    await callback_query.message.edit_text(
        text=text,
        reply_markup=buttons.RETURN_TO_MESSAGES_CONFIG_BUTTONS
    )
