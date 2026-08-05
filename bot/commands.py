from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤘 Benvenuto su Metal Radar!\n\n"
        "Sistema di monitoraggio concerti metal, rock e hard rock attivo.\n\n"
        "Comandi disponibili presto:\n"
        "/lista - mostra band monitorate\n"
        "/ultime - ultime notizie\n"
        "/stato - stato del radar"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛰️ Metal Radar operativo!\n"
        "Monitoraggio in preparazione."
    )


def setup_commands(application):
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("stato", status)
    )
