from flask import Flask,render_template
import telebot

BOT_TOKEN = "7702535826:AAEvM1ADAyZkhiVPkLppJmdblp0GfwQaGK0"
bot = telebot.TeleBot(BOT_TOKEN)

user_id = "Admin"
password = "Admin"

users = set()

pending_user = {}

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    if chat_id in users:
        bot.send_message(chat_id, "✅ You are already logged in.")
        return

    bot.send_message(chat_id, "Welcome! Please enter your **User ID**:")
    pending_user[chat_id] = {"step": "ask_user_id"}

@bot.message_handler(func=lambda message: message.chat.id in pending_user)
def handle_authentication(message):
    chat_id = message.chat.id
    user_data = pending_user.get(chat_id, {})

    if user_data.get("step") == "ask_user_id":
        user_data["user_id"] = message.text
        bot.send_message(chat_id, "Now enter your **Password**:")
        user_data["step"] = "ask_password"
    
    elif user_data.get("step") == "ask_password":
        user_id = user_data.get("user_id")
        password = message.text

        # Validate credentials
        if user_id == user_id and password == password:
            users.add(chat_id)
            bot.send_message(chat_id, "✅ Login successful! Your chat ID is saved.")
        else:
            bot.send_message(chat_id, "❌ Incorrect credentials. Try again.")

        pending_user.pop(chat_id, None)  # Remove user from pending list

@bot.message_handler(commands=["users"])
def list_users(message):
    """Admin command to list all authenticated users"""
    chat_id = message.chat.id
    if chat_id in users:
        bot.send_message(chat_id, f"Authenticated users:\n{users}")
    else:
        bot.send_message(chat_id, "❌ You are not authorized to view this.")

bot.polling()