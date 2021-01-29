import logging
import json
import re
import random

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# States of conversation handler
(MAIN_LEVEL, SM_LEVEL, CATEGORY_LEVEL) = range(3)

# MAIN_LEVEL
SAFETY_TIPS = "🔐 Safety Tips"
PRIVACY_SETTINGS = "⚙️ Privacy Settings"
#ONLINE_QUIZ = "🎲 Social Media Quiz"
mainKeyboard = [[SAFETY_TIPS], [PRIVACY_SETTINGS]]

# SM_LEVEL
INSTA = "Instagram"
TIKTOK = "TikTok"
SNAPCHAT = "Snapchat"
YOUTUBE = "YouTube"
MAIN_KEYBOARD = "Back to main menu"
smKeyboard = [[INSTA], [TIKTOK], [SNAPCHAT], [MAIN_KEYBOARD]]

# CATEGORY_LEVEL
PRIVACY = "Privacy"
SECURITY = "Security"
INTERACTION = "Interaction"
BLOCKING = "Reporting and Blocking"
DELETE = "Delete"
SM_KEYBOARD = "Back to social media"
categoryKeyboard = [[PRIVACY, SECURITY], [BLOCKING], [INTERACTION, DELETE], [SM_KEYBOARD]]

# JSON
instaPrivacy = ['Make the account private', 'Hide activity status', 'Contact Synchronisation', 'Suggestions']
instaSecurity = ['Change the password', 'Two Factor Authentication', 'Clear Search History', 'Save login details']
instaInteraction = ['Manage tagging', 'Delete the post', 'Delete the story', 'Hide the story',
                    'Share the story with selected group', 'Sharing your story', 'Turn off commenting']
instaReporting = ['Block the account', 'Report the account', 'Report the story', 'Report the post',
                  'Report the comment']
instaDelete = ['Temporarily deactivate account', 'Delete the account']

CATEGORY_KEYBOARD = "Back to categories"


def getJson(k):
    final = open('generated.json')
    content = json.load(final)
    for level1 in content[0]:
        for level2 in content[0][level1]:
            if level2 == k:
                return content[0][level1][level2]
    # Closing file
    final.close()


# Tip generator(from tips.json)
def getTip():
    safety = open('tips.json')
    content = json.load(safety)
    number = random.randint(1, 10)
    cond = "'{}'".format(number)
    for piece in content[0]:
        if piece == cond:
            return content[0][piece]

    safety.close()


# Start function. It gets called only once in the beginning of each session
def start(update, context):
    user = update.message.from_user
    logger.info('Media Privacy Bot session started.')
    greeting = 'Hey {}, I\'m Media Privacy Bot! I\'m here to help you learn skills for safety navigating social media.\n\n'.format(
        user.first_name)
    reply_markup = ReplyKeyboardMarkup(mainKeyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(greeting + 'What would you like to know?', reply_markup=reply_markup)
    return MAIN_LEVEL


# Function processes the choice made on the main keyboard
def main_level(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info("User %s selected option %s", user.first_name, selected)

    if selected == SAFETY_TIPS:
        update.message.reply_text(getTip())
        return MAIN_LEVEL

    elif selected == PRIVACY_SETTINGS:
        message = 'The best place to start to ensure social media safety is to check the *privacy settings* of any social media network you are using.\n\n'
        reply_markup = ReplyKeyboardMarkup(smKeyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(message + 'Please select the social media of your choice.', parse_mode='markdown',
                                  reply_markup=reply_markup)
        return SM_LEVEL

    #elif selected == ONLINE_QUIZ:
    #   message = 'Coming soon 😊\n\n'
    #   reply_markup = ReplyKeyboardMarkup(mainKeyboard, resize_keyboard=True, one_time_keyboard=True)
    #   update.message.reply_text(message + 'Choose an option with the buttons below.', reply_markup=reply_markup)
    #   return MAIN_LEVEL

    return MAIN_LEVEL


# Function processes the choice made on the social media keyboard
def sm_level(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info("User %s selected option %s", user.first_name, selected)

    if selected == INSTA:
        title = '*Instagram*\n\n'
        message = 'Instagram is a picture and video sharing app. Users can post content on their profile grid or to their stories, which last 24 hours. You can follow your friends, family, celebrities and companies on Instagram. Instagram also has a live streaming feature.\n\n _Official age rating_: 13+'
        update.message.reply_text(title + message, parse_mode='markdown')
        reply_markup = ReplyKeyboardMarkup(categoryKeyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('You can find the following information about Instagram:', parse_mode='markdown',
                                  reply_markup=reply_markup)
        return CATEGORY_LEVEL

    elif selected == TIKTOK:
        title = '*TikTok*\n\n'
        message = 'TikTok is a social media platform that lets you create, share and discover 60 second videos. You can use music and effects to enhance your videos and you can also browse other people’s videos and interact with them.\n\n _Official age rating_: 13+'
        update.message.reply_text(title + message, parse_mode='markdown')
        # content for TikTok is not implemented. return back to social media.
        reply_markup = ReplyKeyboardMarkup(smKeyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('TikTok is coming soon. Now you can find the information about *Instagram*.',
                                  parse_mode='markdown', reply_markup=reply_markup)
        return SM_LEVEL

    elif selected == SNAPCHAT:
        title = '*Snapchat*\n\n'
        message = 'The Snapchat app lets you send photos, short videos or messages to your friends. Pictures and videos, known as \'Snaps\', usually appear temporarily before disappearing, though they can be captured via screenshots.\n\n _Official age rating_: 13+'
        update.message.reply_text(title + message, parse_mode='markdown')
        # content for Snapchat is not implemented. return back to social media.
        reply_markup = ReplyKeyboardMarkup(smKeyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('Snapchat is coming soon. Now you can find the information about *Instagram*.',
                                  parse_mode='markdown', reply_markup=reply_markup)
        return SM_LEVEL

    elif selected == YOUTUBE:
        title = '*YouTube*\n\n'
        message = 'YouTube lets you watch, create and comment on videos. You can create your own YouTube account, create a music playlist, and even create your own channel, which means you’ll have a public profile. YouTube allows live streaming.\n\n _Official age rating_: 13+'
        update.message.reply_text(title + message, parse_mode='markdown')
        # content for YouTube is not implemented. return back to social media.
        reply_markup = ReplyKeyboardMarkup(smKeyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('YouTube is coming soon. Now you can find the information about *Instagram*.',
                                  parse_mode='markdown', reply_markup=reply_markup)
        return SM_LEVEL

    elif selected == MAIN_KEYBOARD:
        reply_markup = ReplyKeyboardMarkup(mainKeyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('Choose an option with the buttons below.', reply_markup=reply_markup)
        return MAIN_LEVEL

    else:
        reply_markup = ReplyKeyboardMarkup(mainKeyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('Wrong input!', reply_markup=reply_markup)
        return SM_LEVEL

    return SM_LEVEL


# Function processes the choice made on the category keyboard
def category_level(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info("User %s selected option %s", user.first_name, selected)

    if selected == PRIVACY:
        keyboard = []
        for i in instaPrivacy:
            keyboard.append([i])
        keyboard.append([CATEGORY_KEYBOARD])
        title = '*Privacy aspects*\n\n'
        message = 'Instagram accounts can be set to private so only people who follow you can see your posts. You have to approve all follow requests.\n\nInstagram also has a function that lets you restrict who can comment on your posts or turn off comments completely.\n\nThe app’s default setting for location sharing is off but you should always double check this in settings.'
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(title + message, parse_mode='markdown', reply_markup=reply_markup)

    elif selected == SECURITY:
        keyboard = []
        for i in instaSecurity:
            keyboard.append([i])
        keyboard.append([CATEGORY_KEYBOARD])
        title = '*Security aspects*\n\n'
        message = 'Instagram has a selection of tips and recommendations, including information on safety and two-factor authentication.'
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(title + message, parse_mode='markdown', reply_markup=reply_markup)

    elif selected == INTERACTION:
        keyboard = []
        for i in instaInteraction:
            keyboard.append([i])
        keyboard.append([CATEGORY_KEYBOARD])
        title = '*Content*\n\n'
        message = 'Instagram has built in features that automatically remove offensive words and comments. There is also an option to add your own list of words that you don’t want to appear.\n\nMany children use Instagram to follow their favourite influencers, celebrities or other accounts they find interesting. This means it’s hard to control the sorts of content you’re seeing which means you might still come across something you find upsetting or that you don’t want to see.'
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(title + message, parse_mode='markdown', reply_markup=reply_markup)

    elif selected == BLOCKING:
        keyboard = []
        for i in instaReporting:
            keyboard.append([i])
        keyboard.append([CATEGORY_KEYBOARD])
        title = '*Reporting & blocking*\n\n'
        message = 'To block another account or report images, videos or comments that are upsetting, you just need to click on the three dots in the top right hand corner.'
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(title + message, parse_mode='markdown', reply_markup=reply_markup)

    elif selected == DELETE:
        keyboard = []
        for i in instaDelete:
            keyboard.append([i])
        keyboard.append([CATEGORY_KEYBOARD])
        title = '*Deleting & deactivating*\n\n'
        message = 'Deleting or deactivating your account.'
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(title + message, parse_mode='markdown', reply_markup=reply_markup)

    elif selected == SM_KEYBOARD:
        reply_markup = ReplyKeyboardMarkup(smKeyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('Choose an option with the buttons below.', reply_markup=reply_markup)
        return SM_LEVEL

    # back to categories
    elif selected == CATEGORY_KEYBOARD:
        reply_markup = ReplyKeyboardMarkup(categoryKeyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('Choose an option with the buttons below.', reply_markup=reply_markup)
        return CATEGORY_LEVEL

    else:

        update.message.reply_text(getJson(selected.replace(" ", "")))
        return CATEGORY_LEVEL

    return CATEGORY_LEVEL


def help(update, context):
    # message on /help
    update.message.reply_text('Help!')


def error(update, context):
    update.message.reply_text("Wrong input!")
    # log errors
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# message = 'Choose an option with the buttons below.'
# reply_markup = ReplyKeyboardMarkup(mainKeyboard, resize_keyboard =True, one_time_keyboard=True)
# update.message.reply_text(message, reply_markup=reply_markup)
# return MAIN_LEVEL

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater('1622917851:AAE_kPAzx3x-K1t56Er_L9MJnKeNxaO_lDU', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MAIN_LEVEL: [MessageHandler(Filters.update.message, main_level)],

            SM_LEVEL: [MessageHandler(Filters.update.message, sm_level)],

            CATEGORY_LEVEL: [MessageHandler(Filters.update.message, category_level)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
