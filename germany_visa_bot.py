import logging
import os
from openai import OpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot va AI Tokenlari
# MANA SHU YANGI QATORLARNI KO'CHIRIB QO'YASIZ
TOKEN = os.environ.get("TELEGRAM_TOKEN")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# Auslandportal havolasi
AUSLANDPORTAL_URL = "https://digital.diplo.de/visa"

# Viza ma'lumotlari
VISA_INFO = {
    "fachkraft": {
        "name": "👔 Fachkraft (Malakali mutaxassis)",
        "info": (
            "**Fachkraft - Malakali mutaxassis vizasi**\n\n"
            "Germaniyada oliy ma'lumotli yoki kasb-hunar diplomiga ega mutaxassislar uchun.\n\n"
            "**Asosiy talablar:**\n"
            "1. Germaniyadagi ish beruvchidan aniq ish taklifi.\n"
            "2. Diplomning Germaniyada tan olinganligi (Anabin yoki ZAB).\n"
            "3. Mutaxassislik bo'yicha ish tajribasi.\n"
            "4. Nemis tili (sohaga qarab, odatda B1/B2)."
        )
    },
    "weiterbildung": {
        "name": "📚 Weiterbildung (Malaka oshirish)",
        "info": (
            "**Weiterbildung - Kasbiy malaka oshirish**\n\n"
            "Germaniyada o'z sohangiz bo'yicha qo'shimcha bilim olish uchun.\n\n"
            "**Asosiy talablar:**\n"
            "1. Malaka oshirish kursi yoki amaliyot shartnomasi.\n"
            "2. Moliyaviy ta'minot (Sperrkonto yoki ish haqi).\n"
            "3. Nemis tili (kamida B1)."
        )
    },
    "seasonal": {
        "name": "🍎 Mavsumiy ish (8 oylik)",
        "info": (
            "**Mavsumiy ish (Saisonbeschäftigung)**\n\n"
            "Qishloq xo'jaligi va boshqa sohalarda 8 oygacha ishlash uchun.\n\n"
            "**Asosiy talablar:**\n"
            "1. Germaniya Bandlik Agentligi (ZAV) tomonidan tasdiqlangan shartnoma.\n"
            "2. Haftasiga kamida 30 soatlik ish.\n"
            "3. Turar joy bilan ta'minlanganlik."
        )
    },
    "process_flow": {
        "name": "🔄 Auslandportal Jarayoni",
        "info": (
            "**Auslandportal orqali ariza topshirish bosqichlari:**\n\n"
            "1️⃣ **Ariza yuklash:** Hujjatlarni PDF formatda sifatli yuklang.\n\n"
            "2️⃣ **Warteliste (Kutish ro'yxati):** 2-6 oy davomida navbat kutasiz.\n\n"
            "3️⃣ **Vorprüfung (Dastlabki tekshiruv):** Hujjatlar tekshiriladi, yetishmasa qayta yuklash so'raladi.\n\n"
            "4️⃣ **Termin (Uchrashuv):** Vorprüfungdan o'tgach, Termin belgilashga ruxsat beriladi. Pasport, Email va Tel raqami kerak bo'ladi.\n\n"
            "5️⃣ **Tasdiqlash:** Emailingizga tasdiqlash xati keladi."
        )
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = f"Assalomu alaykum, {user.first_name}! 🇩🇪🇺🇿\n\nMen Germaniya vizasi bo'yicha yordamchingizman. Savolingizni yozing yoki menyudan foydalaning:"
    keyboard = [
        [InlineKeyboardButton("📝 Auslandportal Yo'riqnomasi", callback_data="visa_process_flow")],
        [InlineKeyboardButton("👔 Fachkraft / 📚 Weiterbildung", callback_data="visa_types_work")],
        [InlineKeyboardButton("🍎 Mavsumiy ish (8 oy)", callback_data="visa_seasonal")],
        [InlineKeyboardButton("🏠 Oila birlashishi / 👶 Kindernachzug", callback_data="visa_family_all")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "visa_process_flow":
        info = VISA_INFO["process_flow"]["info"]
        await query.edit_message_text(text=info, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Orqaga", callback_data="main_menu")]]), parse_mode="Markdown")
    elif query.data == "main_menu":
        user = update.effective_user
        welcome_text = f"Assalomu alaykum, {user.first_name}! 🇩🇪🇺🇿\n\nSavolingizni yozing yoki menyudan foydalaning:"
        keyboard = [[InlineKeyboardButton("📝 Auslandportal Yo'riqnomasi", callback_data="visa_process_flow")],[InlineKeyboardButton("⬅️ Orqaga", callback_data="main_menu")]]
        await query.edit_message_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    print("Bot ishga tushdi...")
    application.run_polling()

if __name__ == "__main__":
    main()
