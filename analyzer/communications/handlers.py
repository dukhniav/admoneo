from typing import Dict

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (MessageHandler, Filters,
                          CallbackContext, ConversationHandler, CommandHandler)

from ..communications import (CHOOSING, STATUS, TYPING_REPLY, TYPING_CHOICE)

top_menu = [
    ["💵 Averages", 'Favourite colour'],
    ['Number of siblings', 'Something else...'],
    ['Done'],
]

keyboard = [
    ["💵 Averages"],
    ["📈 Progress", "➗ Current ratios"],
    ["🔍 Check bot status", "⌛ Trade History"],
    ["🛠 Maintenance", "⚙️ Configurations"],
]

markup = ReplyKeyboardMarkup(
    top_menu, one_time_keyboard=True)



def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def get_averages(update: Update, context: CallbackContext):
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        f'Getting {text.lower()}...')

    return TYPING_REPLY


def regular_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        f'Your {text.lower()}? Yes, I would love to hear about that!')

    return TYPING_REPLY


def custom_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for a description of a custom category."""
    update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )

    return TYPING_CHOICE


def received_information(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)} You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )

    return CHOOSING


def done(self, update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"I learned these facts about you: {self.facts_to_str(user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        "Starting telegram bot...",
        reply_markup=markup,
    )

    return CHOOSING


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        STATUS: [
            MessageHandler(
                Filters.regex(
                    '^(💵 Averages)$'), get_averages
            ),
            MessageHandler(Filters.regex(
                '^Something else...$'), custom_choice),
        ],
        CHOOSING: [
            MessageHandler(
                Filters.regex(
                    '^(💵 Averages|Favourite colour|Number of siblings)$'), regular_choice
            ),
            MessageHandler(Filters.regex(
                '^Something else...$'), custom_choice),
        ],
        TYPING_CHOICE: [
            MessageHandler(
                Filters.text & ~(Filters.command | Filters.regex(
                    '^Done$')), regular_choice
            )
        ],
        TYPING_REPLY: [
            MessageHandler(
                Filters.text & ~(Filters.command |
                                 Filters.regex('^Done$')),
                received_information,
            )
        ],
    },
    fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
)
