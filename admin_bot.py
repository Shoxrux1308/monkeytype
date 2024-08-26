import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from main import get_wpm_accuracy,get_user_info,get_users_wpm_accuracy

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a message to the group

    users = get_user_info('monkeytype.csv')
    users_wpm_accuracy = get_users_wpm_accuracy(users,15)
    from prettytable import PrettyTable

    table = PrettyTable()
    table.field_names = ["Full Name", "Username", "WPM", "Accuracy"]

    for user in users_wpm_accuracy:
        table.add_row([user['full_name'], user['username'], user['wpm'], user['accuracy']])

    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=str(table))

async def send_results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    users = get_user_info('monkeytype.csv')



    users_wpm_accuracy = get_users_wpm_accuracy(users,15)
    results=''
    for idx,user in enumerate(users_wpm_accuracy):
        if idx==0:
            results+=f'🥇 {user["full_name"]}\t WPM: {user["wpm"]} Accuracy: {user["accuracy"]}\n'
        elif idx==1:
            results+=f'🥈 {user["full_name"]}\t WPM: {user["wpm"]} Accuracy: {user["accuracy"]}\n'
        elif idx==2:
            results+=f'🥉 {user["full_name"]}\t WPM: {user["wpm"]} Accuracy: {user["accuracy"]}\n'
        else:
            results+=f'{idx+1}. {user["full_name"]}\t WPM: {user["wpm"]} Accuracy: {user["accuracy"]}\n'
        
    # Send a message to the group
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=results)
# GROUP chat ID
GROUP_CHAT_ID =-4509575820
TOKEN = os.environ['TOKEN']

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("sendResults", send_results))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))

app.run_polling()