from telegram import (ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup)
from telegram.ext import (CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)

from dao.queries import *
from utils.utils import get_logger

# Enable logging
logger = get_logger()

# State definitions for top level conversation
SIGN_UP, HELP = range(2)

# State definitions for second level conversation
ADD_ADDRESS, UPDATE_ADDRESS, REMOVE_ADDRESS, FIND_MEDICINE = range(2, 6)

# Meta states
SELECT_ACTION, TYPING, HOME, STOP = range(6, 10)

# Shortcut for ConversationHandler.END
END = ConversationHandler.END


class HomeController:

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.__process_handlers()

    def start(self, update, context):
        from_user = update.message.from_user
        text = 'Select an action:'
        buttons = [[
            InlineKeyboardButton(text='Find Medicine', callback_data=FIND_MEDICINE),
            InlineKeyboardButton(text='Update Location', callback_data=UPDATE_ADDRESS)
        ]]
        user = get_user(from_user.id)
        if user is None:
            buttons = [[InlineKeyboardButton(text='Sign Up', callback_data=SIGN_UP)]]
            text = "Добро пожаловать в CureMe. Я твой помощник в мире пилюль и таблеточек.💊 " \
                   "Помогу найти необходимые лекарства, подскажу где и по какой стоимости их можно приобрести.\n\n" \
                   "Давай знакомиться! Жми Sign Up.\n" \
                   "Или посмотри, что я умею! Жми Help"
        buttons.append([InlineKeyboardButton(text='Help', callback_data=HELP)])
        update.message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
        print(from_user)
        context.user_data['user'] = from_user

        return SELECT_ACTION

    def sign_up(self, update, context):
        user = context.user_data['user']
        add_user(user.id, user.first_name, user.last_name)
        # TODO add user and location
        update.callback_query.edit_message_text('Please enter full name')
        return HOME

    def find_medicine(self, update, context):
        # TODO search medicine
        update.callback_query.edit_message_text('Find medicine feature is coming soon...')
        return HOME

    def update_address(self, update, context):
        # TODO update address
        update.callback_query.edit_message_text('Update location feature is coming soon...')
        return HOME

    def help(self, update, context):
        update.callback_query.answer()
        update.callback_query.edit_message_text("Вот, что я умею:\n\nДавай поменяем адрес!\n/updatelocation\n\n" +
            "Приступим к поиску!\n/findmedicine\n\nЧем я могу тебе помочь?\n/help")
        return HOME

    def cancel(self, update, context):
        user = update.message.from_user
        logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())
        return END

    def error(self, update, context):
        logger.warning('Update error: "%s" Caused error: "%s"', update, context.error)

    def __process_handlers(self):
        selection_handlers = [
            CallbackQueryHandler(self.sign_up, pattern='^' + str(SIGN_UP) + '$'),
            CallbackQueryHandler(self.find_medicine, pattern='^' + str(FIND_MEDICINE) + '$'),
            CallbackQueryHandler(self.update_address, pattern='^' + str(UPDATE_ADDRESS) + '$'),
            CallbackQueryHandler(self.help, pattern='^' + str(HELP) + '$'),
        ]
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start), CommandHandler('stop', self.cancel)],
            states={
                SELECT_ACTION: selection_handlers,
                HELP: [CommandHandler('help', self.help)],
                HOME: [CommandHandler('start', self.start)]
            },
            fallbacks=[CommandHandler('stop', self.cancel)]
        )
        self.dispatcher.add_handler(conversation_handler)
        self.dispatcher.add_error_handler(self.error)
