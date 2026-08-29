from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    MessageHandler, ContextTypes, ConversationHandler, filters
)

TOKEN = "8935804839:AAGuCoga2Q2V6x76iz9sa9FtJ2fVtiJdosk"

NAME, CATEGORY, LOCATION, EXPERIENCE, PHONE = range(5)

WORKERS = [
    {
        "name": "አበበ ከበደ",
        "category": "ኤሌክትሪክ",
        "location": "አዲስ አበባ",
        "experience": "5 ዓመት",
        "phone": "+251906116249"
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👨‍🔧 ባለሙያ መፈለግ", callback_data="find_worker")],
        [InlineKeyboardButton("📝 በባለሙያነት መመዝገብ", callback_data="register_worker")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("እንኳን ወደ ET DIGITAL WORK በሰላም መጡ! ምን ማድረግ ይፈልጋሉ?", reply_markup=reply_markup)

async def find_worker_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "find_worker":
        if not WORKERS:
            await query.edit_message_text("ለጊዜው የተመዘገበ ባለሙያ የለም።")
            return

        msg = "📋 **የተመዘገቡ ባለሙያዎች ዝርዝር፦**\n\n"
        for w in WORKERS:
            msg += f"👤 **ስም:** {w['name']}\n🛠 **ሙያ:** {w['category']}\n📍 **አካባቢ:** {w['location']}\n📜 **ልምድ:** {w['experience']}\n📞 **ስልክ:** {w['phone']}\n-------------------\n"
        
        await query.edit_message_text(msg, parse_mode="Markdown")

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("እባክዎን ሙሉ ስምዎን ያስገቡ፦")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("እባክዎን የሙያ ዘርፍዎን በጽሁፍ ያስገቡ (ምሳሌ፦ የቤት እቃ ጥገና፣ ድህረ ገጽ ዲዛይን)፦")
    return CATEGORY

async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['category'] = update.message.text
    await update.message.reply_text("የሚሰሩበትን አካባቢ/ከተማ ያስገቡ (ምሳሌ፦ አዲስ አበባ)፦")
    return LOCATION

async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['location'] = update.message.text
    await update.message.reply_text("የስራ ልምድዎን በጥቂቱ ይጻፉ (ምሳሌ፦ 3 ዓመት)፦")
    return EXPERIENCE

async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['experience'] = update.message.text
    await update.message.reply_text("እባክዎን የቴሌግራም/የስልክ ቁጥርዎን ያስገቡ (ምሳሌ፦ +2519...)፦")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    
    new_worker = {
        "name": context.user_data['name'],
        "category": context.user_data['category'],
        "location": context.user_data['location'],
        "experience": context.user_data['experience'],
        "phone": context.user_data['phone']
    }
    WORKERS.append(new_worker)

    await update.message.reply_text("🎉 ምዝገባው በተሳካ ሁኔታ ተጠናቋል! አሁን መረጃዎ በቦቱ ላይ ይገኛል።")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ምዝገባው ተቋርጧል።")
    return ConversationHandler.END

if __name__ == '__main__':
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_registration, pattern="^register_worker$")],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_category)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
            EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_experience)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(find_worker_menu, pattern="^find_worker$"))

    print("Bot is running...")
    app.run_polling()
