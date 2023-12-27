# ToDoList Telegram Bot

Todolist is a simple Telegram bot to manage your to-do tasks directly from Telegram.

## Installation

1. Clone this repository to your local machine:

   git clone https://github.com/Edward3lric/ToDoList.git
   cd ToDoList

2. Install dependencies using `pip` and the `requirements.txt` file:

   pip install -r requirements.txt

## Usage

1. Get a token for your Telegram bot by following the instructions on the [official Telegram documentation](https://core.telegram.org/bots).

2. Setting up TELEGRAM_BOT_TOKEN Environment Variable

    - Linux/macOS: `export TELEGRAM_BOT_TOKEN="your_actual_bot_token"`
    - Windows (cmd): `set TELEGRAM_BOT_TOKEN=your_actual_bot_token`
    - Windows (PowerShell): `$env:TELEGRAM_BOT_TOKEN="your_actual_bot_token"`

3. Run the bot:
   - `python app.py`

## Bot Commands

- `/start`: Start the conversation with the bot.
- `/help`: Show help and the list of commands.
- `/newTask`: Create a new task.
- `/viewTasks`: Show your pending tasks.
- `/viewTasks All`: Show all tasks.
- `/edit <task_number>`: Edit a specific task.
- `/complete <task_number>`: Mark a task as completed.
