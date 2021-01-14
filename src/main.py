import logging
import requests
import re
from telegram.ext import (
	Updater,
	InlineQueryHandler,
	CommandHandler,
	MessageHandler,
	ConversationHandler,
	Filters,
	CallbackContext
)

#Enable Logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def start(update, context):
	
	logger.info('The bot has started.')
	update.message.reply_text("Hi, I'm a bot. How can I help?")

def cancel(update, context):

	logger.info("User canceled the conversation!")
	update.message.reply_text("Bye bye!")

	return ConversationHandler.END

def error(update, context):

	#Logs errors caused by updates.
	update.message.reply_text("Wrong input!")
	logger.warning('Update "%s" caused error "%s"', update, context.error)
	


def main() :
	
	# Create the Updater and pass it your bot's token.
	updater = Updater('_insert_telegram_bot_token_here_')
	dp = updater.dispatcher
	
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start)],
		states={},
		fallbacks=[CommandHandler('cancel', cancel)]
	)
		
	#adding conversation to handler.
	dp.add_handler(conv_handler)
	
	# log all errors
	dp.add_error_handler(error)

	#start bot
	updater.start_polling()

	#Runs the bot until ctrl-c is pressed or the process is terminated!
	updater.idle()






if __name__ == '__main__':
	main()