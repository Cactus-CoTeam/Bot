import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (CommandHandler, MessageHandler, Filters, ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class HomeController:

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.__process_handlers()

    SIGNUP, UPDATE_LOCATION, FIND, HELP = range(4)

    def start(self, update, context):
        reply_keyboard = [['Sign Up', 'Update location', 'Help']]

        update.message.reply_text(
            'Здравствуйте!\n\n',
            'Здесь должно быть какой то текст приветствие и инструкция',
            'Зарегистрироваться?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return self.SIGNUP

    def sign_up(self, update, context):
        user = update.message.from_user
        logger.info("Sign up of %s: %s", user.first_name, update.message.text)
        update.message.reply_text('Please enter your address', reply_markup=ReplyKeyboardRemove())

        return self.FIND

    def update_location(self, update, context):
        user = update.message.from_user
        user_location = update.message.location
        logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                    user_location.longitude)
        update.message.reply_text('Please enter your location')

        return self.FIND

    def find(self, update, context):
        user = update.message.from_user
        user_location = update.message.location
        logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                    user_location.longitude)
        update.message.reply_text('Find medicine')

        return ConversationHandler.END

    def help(self, update, context):
        update.message.reply_text('Here should be some useful information ...')

        if __name__ == '__main__':
            return self.HELP

        return ConversationHandler.END

    def cancel(self, update, context):
        user = update.message.from_user
        logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def __process_handlers(self):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                self.SIGNUP: [MessageHandler(Filters.regex('^(Sign Up|Update location|Help)$'), self.sign_up)],
                self.FIND: [MessageHandler(Filters.text, self.find), CommandHandler('help', self.help)],
                self.UPDATE_LOCATION: [MessageHandler(Filters.location, self.update_location), CommandHandler('help', self.help)],
                self.HELP: [CommandHandler('help', help)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )
        self.dispatcher.add_handler(conversation_handler)
        self.dispatcher.add_error_handler(self.error)
