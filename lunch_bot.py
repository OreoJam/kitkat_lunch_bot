import telegram
import configparser
from telegram.ext import Updater, CommandHandler
import sys
import random

# Read File - Bot Token
t_file = configparser.ConfigParser()
t_file.read('lunchbot_token.ini')
token_file = t_file['INFO']['token']

# Set Bot
token = token_file
bot = telegram.Bot(token=token)

# var
restaurant_list = []
max_no_restaurant = 0

# Read File - Restaurant
r_list_file = configparser.ConfigParser()
r_list_file.read('restaurant.ini')
for data_key in r_list_file['LIST']:
    restaurant_list.append(r_list_file['LIST'][data_key])
    max_no_restaurant += 1

# Updater
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

# Command Handler
def add(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Awesome! You found new place. I'll remember this.")
    contents = update.message.text
    contents = contents.replace("/add", "")
    contents = contents.strip()
    if contents:
        # Save list
        restaurant_list.append(contents)
        # Write file
        r_list_file.set('LIST', str(len(restaurant_list)-1), contents)
        with open('restaurant.ini', 'w') as r_file:
            r_list_file.write(r_file)
    print('Add - End')

def lunch(update, context):
    r_num = random.randint(0, len(restaurant_list)-1)
    s_message = "This is where you will eat lunch today.\n" + restaurant_list[r_num]
    context.bot.send_message(chat_id=update.effective_chat.id, text=s_message)
    print('Lunch - End')

def show(update, context):
    s_message = "You can see list.\n"
    for item in restaurant_list:
        s_message += str(item) + "\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=s_message)
    print('Show - End')

def helpcommand(update, context):
    s_message = "Commands List\n" + "/lunch for Get Restaurant Name\n" + \
                "/add Restaurant Name for New \n" + "/show for List of Restaurant\n"
    context.bot.sendMessage(chat_id=update.effective_chat.id, text=s_message)
    print('Help - End')

def kill(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm going to die.")
    print('Killed - End')
    sys.exit('Exit')

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello friend! Welcome~")
    s_message = "Commands List\n" + "/lunch for Get Restaurant Name\n" + \
                "/add Restaurant Name for New \n" + "/show for List of Restaurant\n"
    context.bot.sendMessage(chat_id=update.effective_chat.id, text=s_message)
    print('Start - End')

# Regist Handler
add_handler = CommandHandler('add', add)
lunch_handler = CommandHandler('lunch', lunch)
show_handler = CommandHandler('show', show)
help_handler = CommandHandler('help', helpcommand)
kill_handler = CommandHandler('kill', kill)
start_handler = CommandHandler('start', start)

# Attach Handler
updater.dispatcher.add_handler(add_handler)
updater.dispatcher.add_handler(lunch_handler)
updater.dispatcher.add_handler(show_handler)
updater.dispatcher.add_handler(help_handler)
updater.dispatcher.add_handler(start_handler)

# Start
updater.start_polling()
updater.idle()


