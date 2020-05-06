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
SELECT_ACTION, TYPING, STOPPING, SHOWING = range(6, 10)

# Shortcut for ConversationHandler.END
END = ConversationHandler.END


class HomeController:

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.__process_handlers()

    def start(self, update, context):
        update.message.reply_text('Здравствуйте!\n\nЗдесь должно быть текст приветствие и инструкция ...\n')

        user = get_user(update.message.from_user.id)
        if user is None:
            buttons = [
                [InlineKeyboardButton(text='Sign Up', callback_data=SIGN_UP)],
                [InlineKeyboardButton(text='Stop', callback_data=END)]
            ]
            update.message.reply_text(text='Please sign up first!', reply_markup=InlineKeyboardMarkup(buttons))
        else:
            buttons = [
                [InlineKeyboardButton(text='Find Medicine...', callback_data=FIND_MEDICINE)],
                [InlineKeyboardButton(text='Help', callback_data=HELP)]
            ]
            update.message.reply_text(text=f'Welcome back {user.name}!', reply_markup=InlineKeyboardMarkup(buttons))

        return SELECT_ACTION

    def sign_up(self, update, context):
        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        if update.callback_query.data == str(SIGN_UP):
            update.callback_query.edit_message_text('Please enter your address')
        else:
            update.callback_query.edit_message_text('Ok, bye!')

    def help(self, update, context):
        update.message.reply_text('Here should be some useful information ...\nUse /start to test this bot.')

    def cancel(self, update, context):
        user = update.message.from_user
        logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())

        return END

    def error(self, update, context):
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def __process_handlers(self):
        # conversation_handler = ConversationHandler(
        #     entry_points=[CommandHandler('start', self.start)],
        #     states={
        #         SIGN_UP: [CallbackQueryHandler(self.sign_up)],
        #         FIND_MEDICINE: [CommandHandler('help', self.help)],
        #         # SELECT_ACTION: [MessageHandler(Filters.text, self.sign_up), CommandHandler('help', self.help)],
        #         HELP: [CommandHandler('help', help)]
        #     },
        #     fallbacks=[CommandHandler('stop', self.cancel)]
        # )
        # self.dispatcher.add_handler(conversation_handler)
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CallbackQueryHandler(self.sign_up))
        self.dispatcher.add_handler(CommandHandler('help', self.help))
        self.dispatcher.add_handler(CommandHandler('stop', self.help))
        self.dispatcher.add_error_handler(self.error)
