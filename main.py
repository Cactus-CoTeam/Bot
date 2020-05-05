from telegram.ext import Updater

from controller.home_controller import HomeController
from config import BotConfig
from database_connect import engine
from model.models import Base

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    updater = Updater(BotConfig.token, use_context=True)
    dispatcher = updater.dispatcher
    test_controller = HomeController(dispatcher=dispatcher)
    updater.start_polling()
    updater.idle()