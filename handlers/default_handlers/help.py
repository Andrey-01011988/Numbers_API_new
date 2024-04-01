from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from keyboards.reply import continue_menu_buttons
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message) -> None:
    """
    bot_help
    Выводит все доступные пользователю команды бота

    :param message:
    :return:
    """
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))


@bot.message_handler(func=lambda message: message.text == 'В меню')
def return_to_menu(message: Message) -> None:
    """
    В случае возврата в меню выводит все доступные пользователю команды бота

    :param message:
    :return:
    """

    # удаляются состояния
    bot.delete_state(message.from_user.id, message.chat.id)

    # Выдается список команд
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text), reply_markup=continue_menu_buttons.remove_buttons())
