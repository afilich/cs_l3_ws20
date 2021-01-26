import logging
import json
import re

from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# define command handlers
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(" 🔐 Safety Guide", callback_data='safetyGuide')],
        [InlineKeyboardButton(" ⚙️ Privacy Settings", callback_data='privacySettings')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('A bot explanatory text will be imported here', reply_markup=reply_markup)


def getJson(k):
    final = open('generated.json')
    content = json.load(final)
    for level1 in content[0]:
        for level2 in content[0][level1]:
            if level2 == k:
                return content[0][level1][level2]
     # Closing file
    final.close()

#someglobals
Generickeyboard = [
            [InlineKeyboardButton("Privacy", callback_data='privacy')],
            [InlineKeyboardButton("Security", callback_data='security')],
            [InlineKeyboardButton("Interaction", callback_data='interaction')],
            [InlineKeyboardButton("Reporting and Blocking", callback_data='blocking')],
            [InlineKeyboardButton("Delete", callback_data='delete')],
        ]
instaPrivacy = ['Make the account private','Hide activity status','Contact Synchronisation', 'Suggestions']
instaSecurity = ['Change the password','Two Factor Authentication','Clear Search History', 'Save login details']
instaInteraction = ['Manage tagging', 'Delete the post','Delete the story','Hide the story', 'Share the story with selected group','Sharing your story', 'Turn off commenting']
instaReporting = ['Block the account','Report the account','Report the story', 'Report the post', 'Report the comment']
instaDelete = ['Temporarily deactivate account','Delete the account']


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == 'safetyGuide':
        query.answer()
        query.message.reply_text('coming soon:)')

    elif query.data == 'privacySettings':
        query.answer()
        keyboard = [
            [InlineKeyboardButton("Instagram", callback_data='insta')],
            [InlineKeyboardButton("TikTok", callback_data='tiktok')],
            [InlineKeyboardButton("Snapchat", callback_data='snapchat')],
            [InlineKeyboardButton("YouTube", callback_data='youtube')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Please select the social media of your choice', reply_markup=reply_markup)

    elif query.data == 'insta':
        query.answer()
        reply_markup = InlineKeyboardMarkup(Generickeyboard)
        query.message.reply_text('You can find the following information about Instagram:', reply_markup=reply_markup)

    elif query.data == 'privacy':
        keyboard = [];
        for i in instaPrivacy:
            keyboard.append([InlineKeyboardButton(i, callback_data=re.sub('[^A-Za-z0-9]+', '', i))])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Privacy aspects', reply_markup=reply_markup)

    elif query.data == 'security':
        keyboard = [];
        for i in instaSecurity:
            keyboard.append([InlineKeyboardButton(i, callback_data=re.sub('[^A-Za-z0-9]+', '', i))])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Important security aspects', reply_markup=reply_markup)

    elif query.data == 'interaction':
        keyboard = [];
        for i in instaInteraction:
            keyboard.append([InlineKeyboardButton(i, callback_data=re.sub('[^A-Za-z0-9]+', '', i))])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Some of the useful aspects about managing your content', reply_markup=reply_markup)

    elif query.data == 'blocking':
        keyboard = [];
        for i in instaReporting:
            keyboard.append([InlineKeyboardButton(i, callback_data=re.sub('[^A-Za-z0-9]+', '', i))])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Reporting and blocking', reply_markup=reply_markup)

    elif query.data == 'delete':
        keyboard = [];
        for i in instaDelete:
            keyboard.append([InlineKeyboardButton(i, callback_data=re.sub('[^A-Za-z0-9]+', '', i))])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Deleting or deactivating your account', reply_markup=reply_markup)
    else:
        query.message.reply_text(getJson(query.data))

def help(update, context):
    # message on /help
    update.message.reply_text('Help!')

def error(update, context):
    #log errors
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    updater = Updater('1502962824:AAEjPI28Agj95tXp00sJNVXtaqr58b1dH0w', use_context=True)
    # dispatcher for registering the handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CallbackQueryHandler(button))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()


    updater.idle()


if __name__ == '__main__':
    main()
