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
    reply_markup = InlineKeyboardMarkup(mainKeyboard)
    greeting = 'Hey, I\'m Media Privacy Bot! I\'m here to help you learn skills for safety navigating social media.\n\n'
    update.message.reply_text(greeting + 'What would you like to know?', reply_markup=reply_markup)


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
mainKeyboard = [
            [InlineKeyboardButton(" 🔐 Safety Guide", callback_data='safetyGuide')],
            [InlineKeyboardButton(" ⚙️ Privacy Settings", callback_data='privacySettings')],
        ]

smKeyboard = [
            [InlineKeyboardButton("Instagram", callback_data='insta')],
            [InlineKeyboardButton("TikTok", callback_data='tiktok')],
            [InlineKeyboardButton("Snapchat", callback_data='snapchat')],
            [InlineKeyboardButton("YouTube", callback_data='youtube')],
            [InlineKeyboardButton("Back to main menu", callback_data='mainKeyboard')],
        ]

categoryKeyboard = [
            [InlineKeyboardButton("Privacy", callback_data='privacy')],
            [InlineKeyboardButton("Security", callback_data='security')],
            [InlineKeyboardButton("Interaction", callback_data='interaction')],
            [InlineKeyboardButton("Reporting and Blocking", callback_data='blocking')],
            [InlineKeyboardButton("Delete", callback_data='delete')],
            [InlineKeyboardButton("Back to social media", callback_data='smKeyboard')],
        ]

instaPrivacy = ['Make the account private','Hide activity status','Contact Synchronisation', 'Suggestions']
instaSecurity = ['Change the password','Two Factor Authentication','Clear Search History', 'Save login details']
instaInteraction = ['Manage tagging', 'Delete the post','Delete the story','Hide the story', 'Share the story with selected group','Sharing your story', 'Turn off commenting']
instaReporting = ['Block the account','Report the account','Report the story', 'Report the post', 'Report the comment']
instaDelete = ['Temporarily deactivate account','Delete the account']

backToCategories = [InlineKeyboardButton("Back to categories", callback_data='categoryKeyboard')]


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # mainKeyboard
    if query.data == 'safetyGuide':
        query.answer()
        query.message.reply_text('coming soon:)')

    elif query.data == 'privacySettings':
        query.answer()
        message = 'The best place to start to ensure social media safety is to check the privacy settings of any social media network you are using.\n\n'
        reply_markup = InlineKeyboardMarkup(smKeyboard)
        query.message.reply_text(message + 'Please select the social media of your choice.', reply_markup=reply_markup)

    # smKeyboard
    elif query.data == 'insta':
        query.answer()
        title = '*Instagram*\n\n'
        message = 'Instagram is a picture and video sharing app. Users can post content on their profile grid or to their stories, which last 24 hours. You can follow your friends, family, celebrities and companies on Instagram. Instagram also has a live streaming feature.\n\n _Official age rating_: 13+'
        query.message.reply_text(title + message, parse_mode='markdown')
        reply_markup = InlineKeyboardMarkup(categoryKeyboard) 
        query.message.reply_text('You can find the following information about Instagram:', parse_mode='markdown', reply_markup=reply_markup)

    elif query.data == 'tiktok':
        query.answer()
        title = '*TikTok*\n\n'
        message = 'TikTok is a social media platform that lets you create, share and discover 60 second videos. You can use music and effects to enhance your videos and you can also browse other people’s videos and interact with them.\n\n _Official age rating_: 13+'
        # content for TikTok is not implemented. return back to social media.
        reply_markup = InlineKeyboardMarkup(smKeyboard)
        query.message.reply_text(title + message, parse_mode='markdown')
        query.message.reply_text('TikTok is coming soon. Now you can find the information about *Instagram*.', parse_mode='markdown', reply_markup=reply_markup)

    elif query.data == 'snapchat':
        query.answer()
        title = '*Snapchat*\n\n'
        message = 'The Snapchat app lets you send photos, short videos or messages to your friends. Pictures and videos, known as \'Snaps\', usually appear temporarily before disappearing, though they can be captured via screenshots.\n\n _Official age rating_: 13+'
        query.message.reply_text(title + message, parse_mode='markdown')
        # content for Snapchat is not implemented. return back to social media.
        reply_markup = InlineKeyboardMarkup(smKeyboard) 
        query.message.reply_text('Snapchat is coming soon. Now you can find the information about *Instagram*.', parse_mode='markdown', reply_markup=reply_markup)
    
    elif query.data == 'youtube':
        query.answer()
        title = '*YouTube*\n\n'
        message = 'YouTube lets you watch, create and comment on videos. You can create your own YouTube account, create a music playlist, and even create your own channel, which means you’ll have a public profile. YouTube allows live streaming.\n\n _Official age rating_: 13+'
        query.message.reply_text(title + message, parse_mode='markdown')
        # content for YouTube is not implemented. return back to social media.
        reply_markup = InlineKeyboardMarkup(smKeyboard) 
        query.message.reply_text('YouTube is coming soon. Now you can find the information about *Instagram*.', parse_mode='markdown', reply_markup=reply_markup)

    # back to main menu
    elif query.data == 'mainKeyboard':
        reply_markup = InlineKeyboardMarkup(mainKeyboard)
        query.message.reply_text('Choose an option with the buttons below.', reply_markup=reply_markup) 

    # categoryKeyboard
    elif query.data == 'privacy':
        keyboard = []
        for i in instaPrivacy:
            keyboard.append([InlineKeyboardButton(i, callback_data=re.sub('[^A-Za-z0-9]+', '', i))])
        keyboard.append(backToCategories)
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Privacy aspects', reply_markup=reply_markup)

    elif query.data == 'security':
        keyboard = []
        for i in instaSecurity:
            keyboard.append([InlineKeyboardButton(i, callback_data=re.sub('[^A-Za-z0-9]+', '', i))])
        keyboard.append(backToCategories)
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Important security aspects', reply_markup=reply_markup)

    elif query.data == 'interaction':
        keyboard = []
        for i in instaInteraction:
            keyboard.append([InlineKeyboardButton(i, callback_data=re.sub('[^A-Za-z0-9]+', '', i))])
        keyboard.append(backToCategories)
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Some of the useful aspects about managing your content', reply_markup=reply_markup)

    elif query.data == 'blocking':
        keyboard = []
        for i in instaReporting:
            keyboard.append([InlineKeyboardButton(i, callback_data=re.sub('[^A-Za-z0-9]+', '', i))])
        keyboard.append(backToCategories)
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Reporting and blocking', reply_markup=reply_markup)

    elif query.data == 'delete':
        keyboard = []
        for i in instaDelete:
            keyboard.append([InlineKeyboardButton(i, callback_data=re.sub('[^A-Za-z0-9]+', '', i))])
        keyboard.append(backToCategories)
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Deleting or deactivating your account', reply_markup=reply_markup)
    
    # back to social media
    elif query.data == 'smKeyboard':
        reply_markup = InlineKeyboardMarkup(smKeyboard)
        query.message.reply_text('Choose an option with the buttons below.', reply_markup=reply_markup)

    # back to categories
    elif query.data == 'categoryKeyboard':
        reply_markup = InlineKeyboardMarkup(categoryKeyboard)
        query.message.reply_text('Choose an option with the buttons below.', reply_markup=reply_markup)

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
