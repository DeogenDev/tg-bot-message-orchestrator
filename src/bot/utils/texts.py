"""Текста бота."""

class Common:
    START = "Добрый день! Я бот который поможет тебе взять себе воду."


class Channels:
    ABOUT_CHANNELS_INFO = "Выберите действие для каналов."
    INPUT_FORWARD_MESSAGE = "Перешлите сообщение из канала, который нужно добавить."
    SUCCESS_ADD_CHANNEL = "Канал успешно добавлен."
    FAIL_ADD_CHANNEL = "Канал не добавлен."
    CHOISE_CHANNEL_FOR_DELETE = "Выберите канал который нужно удалить."
    NO_CHANNELS = "У вас нет каналов."
    SUCCESS_DELETE_CHANNEL = "Канал успешно удален."
    FAIL_DELETE_CHANNEL = "Канал не удален."


class Messages:
    ABOUT_MESSAGES_INFO = "Выберите действие для сообщений."
    INPUT_MESSAGE_TEXT = "Введите текст сообщения."
    INPUT_FORWARD_MESSAGE = "Перешлите сообщение, которое нужно добавить."
    SUCCESS_ADD_MESSAGE = "Сообщение успешно добавлено."
    NO_MESSAGES = "У вас нет сообщений."
    FAIL_ADD_MESSAGE = "Сообщение не добавлено."
    CHOISE_MESSAGE_FOR_DELETE = "Выберите сообщение которое нужно удалить."
    DELETE_MESSAGE = "Сообщение успешно удалено."
    FAIL_DELETE_MESSAGE = "Сообщение не удалено."
    SEND_MESSAGE_TO_CHANNEL = "Выберите канал в который нужно отправить сообщение."
    SUCCESS_SEND_MESSAGE = "Сообщение успешно отправлено."
    FAIL_SEND_MESSAGE = "Сообщение не отправлено."
    OPEN_MESSAGE_INFO = "Выберите действие над сообщением."
    NO_BUTTONS = "У сообщения нет кнопок."
    CHOISE_BUTTON_FOR_DELETE = "Выберите кнопку которую нужно удалить."


class Buttons:
    CHOISE_PLACE_FOR_BUTTON = "Выберите место для кнопки."
    INPUT_BUTTON_FORWARD_MESSAGE = "Перешлите сообщение к которому нужно привзять кнопку."
    INPUT_BUTTON_TEXT = "Введите текст кнопки."
    SUCCESS_ADD_BUTTON = "Кнопка успешно добавлена."
    FAIL_ADD_BUTTON = "Кнопка не добавлена."
    CHOISE_BUTTON_FOR_DELETE = "Выберите кнопку которую нужно удалить."
    SUCCESS_DELETE_BUTTON = "Кнопка успешно удалена."
    FAIL_DELETE_BUTTON = "Кнопка не удалена."


class Texts:
    common = Common
    channels = Channels
    messages = Messages
    buttons = Buttons


texts = Texts
