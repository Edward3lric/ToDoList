import logging
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

from db import dbTasks, dbUsers
dbTasks, dbUsers = dbTasks(), dbUsers()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and not update.message.edit_date:
        """Send a message when the command /start is issued."""
        user = update.effective_user
            
        if (dbUsers.checkUser(user.id)):
            await update.message.reply_text(f"Hi {user.name}!, you had already signed up")
        else:
            dbUsers.addUser(user.id)
            await update.message.reply_text(f"Hi {user.name}!, you have successfully registered",)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and not update.message.edit_date:
        """Send a message when the command /help is issued."""
        help_message = (
            "Here are the available commands:\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/newTask - Create a new task\n"
            "/viewTasks - View tasks\n"
            "/viewTasks All - View all tasks\n"
            "/edit <task_number> - Edit a task\n"
            "/complete <task_number> - Complete a task"
        )
        await update.message.reply_text(help_message)

async def default_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and not update.message.edit_date:
        """Default message for user."""
        await update.message.reply_text("Sorry, I don't understant your message")

# Functions for create new task
    
async def new_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Create a new task"""
    await update.message.reply_text("Writte your task")
    return 0

async def text_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    dbTasks.addTask(update.effective_user.id, update.message.text)
    await update.message.reply_text("Saved Task")
    return ConversationHandler.END

async def cancel_new(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("The task was not created")
    return ConversationHandler.END

# Function to view tasks

async def view_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and not update.message.edit_date:
        textToTheUser = """
            These are your to-dos
            ---------------------"""
        
        if not context.args:
            tasks = dbTasks.getTasks(update.effective_user.id)
        elif context.args[0].lower() == "all":
            tasks = dbTasks.getAllTasks(update.effective_user.id)
        else:
            return

        count = 1
        for task in tasks:
            textToTheUser += f"\n {count} - {task[1]}"
            count += 1

        await update.message.reply_text(textToTheUser)

# Functions to edit tasks
        
async def edit_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not context.args:
        await update.message.reply_text("Use /edit + #task\nExample /edit 1")

        textToTheUser = """
        These are your to-dos
        ---------------------"""
        count = 1
        for task in dbTasks.getTasks(update.effective_user.id):
            textToTheUser += f"\n {count} - {task[1]}"
            count += 1
        await update.message.reply_text(textToTheUser)
        return ConversationHandler.END
    else:  
        context.user_data["numTask"] = context.args[0]
        await update.message.reply_text("Writte your new task")
        return 0
    
async def new_text_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    numTask = context.user_data["numTask"]
    try:
        position = (int(numTask) - 1)
        idTask = dbTasks.getTasks(update.effective_user.id)[position][0]
        dbTasks.editTask(idTask, update.message.text)
        await update.message.reply_text("Edited Task")
    except ValueError:
        await update.message.reply_text("Unedited Task")
    except IndexError:
        await update.message.reply_text("Unedited Task")
    return ConversationHandler.END

async def cancel_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("The task was not edited")
    return ConversationHandler.END

# Functions to complete tasks
    
async def complete_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and not update.message.edit_date:
        if not context.args:
            await update.message.reply_text("Use /complete + #task\nExample /complete 1")

            textToTheUser = """
            These are your to-dos
            ---------------------"""
            count = 1
            for task in dbTasks.getTasks(update.effective_user.id):
                textToTheUser += f"\n {count} - {task[1]}"
                count += 1
            await update.message.reply_text(textToTheUser)
        else:        
            keyboard = [[
                InlineKeyboardButton("Yes", callback_data = context.args[0]),
                InlineKeyboardButton("No", callback_data = "-1"),
            ]]
            await update.message.reply_text("You're sure to eliminate this task", reply_markup=InlineKeyboardMarkup(keyboard))

async def confirmation_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    numTask = query.data

    if (numTask == "-1"):
        await query.edit_message_text(text="Task Not Completed")
    else:
        try:
            position = (int(numTask) - 1)
            idTask = dbTasks.getTasks(update.effective_user.id)[position][0]
            dbTasks.completeTask(idTask)
            await query.edit_message_text(text="Task Completed")
        except ValueError:
            await query.edit_message_text(text="Invalid Task")
        except IndexError:
            await query.edit_message_text(text="Invalid Task")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
        
    application.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("newTask", new_task)],
            states={
                0: [MessageHandler(filters.TEXT & ~filters.COMMAND, text_task)]
            },
            fallbacks=[CommandHandler("cancel", cancel_new)]
        )
    )
    application.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("edit", edit_task)],
            states={
                0: [MessageHandler(filters.TEXT & ~filters.COMMAND, new_text_task)]
            },
            fallbacks=[CommandHandler("cancel", cancel_edit)]
        )
    )
    
    application.add_handler(CommandHandler("viewTasks", view_tasks))
    application.add_handler(CommandHandler("complete", complete_task))
    application.add_handler(CallbackQueryHandler(confirmation_button))

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT, default_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
