from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import Updater, CallbackContext
import logging
import os

from definitions import DATA_DIR
from service_messages import start_message, teach_message
from chatgpt import ChatGPTEngine
from speech import SpeechEngine

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

voice_file = str(DATA_DIR / "voice.ogg")
TOKEN = os.environ['TOKEN']
user_filters = filters.User(int(os.environ['USER_ID']))

logger.info('Starting engines ...')
speech_engine = SpeechEngine()
chat_engine = ChatGPTEngine()


async def start(update: Updater, context: CallbackContext) -> None:
    logger.info(f"Start with {update.message}")
    await update.message.reply_text(start_message)


async def teach(update: Updater, context: CallbackContext) -> None:
    logger.info(f"Teaching with {update.message.chat.username}")
    text = teach_message
    await update.message.reply_text(f"Your message was: {text}")
    reply = chat_engine.process(text)
    await update.message.reply_text(reply)


async def reset(update: Updater, context: CallbackContext) -> None:
    logger.info(f"Reset with {update.message.chat.username}")
    chat_engine.reset()
    await update.message.reply_text("The conversation has been resetted")


async def voice(update: Updater, context: CallbackContext) -> None:
    logger.info(f"Voice from {update.message.chat.username}")
    file_id = update.message.voice.file_id
    new_file = await context.bot.get_file(file_id)
    await new_file.download_to_drive(voice_file)
    text = speech_engine.process(voice_file)
    await update.message.reply_text(f"Your message was: {text}")
    reply = chat_engine.process(text)
    await update.message.reply_text(reply)


async def text(update: Updater, context: CallbackContext) -> None:
    logger.info(f"Text from {update.message.chat.username}")
    text = update.message.text
    reply = chat_engine.process(text)
    await update.message.reply_text(reply)


def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start, filters=user_filters))
    app.add_handler(CommandHandler('teach', teach, filters=user_filters))
    app.add_handler(CommandHandler('reset', reset, filters=user_filters))
    app.add_handler(MessageHandler(filters.VOICE & user_filters, voice))
    app.add_handler(MessageHandler(filters.TEXT & user_filters, text))
    app.run_polling()


if __name__ == "__main__":
    main()
