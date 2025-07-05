import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

bot = telebot.TeleBot("import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import os
from datetime import datetime

bot = telebot.TeleBot("7978211870:AAEIIQvzS-ZFHjcxhAPJKvonNdUhAOVL_U4")  # ← BOT TOKEN buraya!

user_data = {}

@bot.message_handler(commands=["start"])
def start(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔍 AdSoyad", callback_data="adsoyad"),
        InlineKeyboardButton("🧾 TC Sorgu", callback_data="tc"),
        InlineKeyboardButton("📱 TC → GSM", callback_data="tcgsm"),
        InlineKeyboardButton("📞 GSM → TC", callback_data="gsmtc"),
        InlineKeyboardButton("🏠 Adres", callback_data="adres"),
        InlineKeyboardButton("👨‍👩‍👧 Aile", callback_data="aile"),
        InlineKeyboardButton("🧬 Sülale", callback_data="sulale"),
        InlineKeyboardButton("👩‍👧 Anne", callback_data="anne"),
        InlineKeyboardButton("🏫 Okul No", callback_data="okul"),
        InlineKeyboardButton("🪵 Log Gönder", callback_data="log"),
    )
    bot.send_message(message.chat.id, "📌 Bir sorgu türü seç:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    cid = call.message.chat.id
    data = call.data
    user_data[cid] = {"sorgu": data}

    if data == "adsoyad":
        bot.send_message(cid, "Adı girin:")
        bot.register_next_step_handler(call.message, get_ad)
    elif data in ["tc", "tcgsm", "gsmtc", "adres", "aile", "sulale", "anne", "okul"]:
        prompt = "TC No girin:" if data != "gsmtc" else "GSM No girin:"
        bot.send_message(cid, prompt)
        bot.register_next_step_handler(call.message, do_simple_query)
    elif data == "log":
        bot.send_message(cid, "Gönderilecek log metnini yaz:")
        bot.register_next_step_handler(call.message, send_log)

# -------- Adsoyad Sorgusu (Adım Adım) --------
def get_ad(message):
    cid = message.chat.id
    user_data[cid]["ad"] = message.text
    bot.send_message(cid, "Soyadı girin:")
    bot.register_next_step_handler(message, get_soyad)

def get_soyad(message):
    cid = message.chat.id
    user_data[cid]["soyad"] = message.text

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("❓ Bilmiyorum", callback_data="bilinmeyen_il"))
    bot.send_message(cid, "🏙️ İl biliyorsan yaz, bilmiyorsan 'Bilmiyorum' butonuna bas:", reply_markup=markup)
    bot.register_next_step_handler(message, save_il)

def save_il(message):
    cid = message.chat.id
    user_data[cid]["il"] = message.text

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("❓ Bilmiyorum", callback_data="bilinmeyen_ilce"))
    bot.send_message(cid, "📍 İlçe biliyorsan yaz, bilmiyorsan 'Bilmiyorum' butonuna bas:", reply_markup=markup)
    bot.register_next_step_handler(message, do_adsoyad_query)

@bot.callback_query_handler(func=lambda call: call.data == "bilinmeyen_il")
def bilinmeyen_il(call):
    cid = call.message.chat.id
    user_data[cid]["il"] = ""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("❓ Bilmiyorum", callback_data="bilinmeyen_ilce"))
    bot.send_message(cid, "📍 İlçe biliyorsan yaz, bilmiyorsan 'Bilmiyorum' butonuna bas:", reply_markup=markup)
    bot.register_next_step_handler(call.message, do_adsoyad_query)

@bot.callback_query_handler(func=lambda call: call.data == "bilinmeyen_ilce")
def bilinmeyen_ilce(call):
    cid = call.message.chat.id
    user_data[cid]["ilce"] = ""
    do_adsoyad_query(call.message)

def do_adsoyad_query(message):
    cid = message.chat.id
    ilce = message.text if message.text else user_data[cid].get("ilce", "")
    data = user_data[cid]
    ad = data.get("ad", "")
    soyad = data.get("soyad", "")
    il = data.get("il", "")

    url = f"https://api.hexnox.pro/sowixapi/adsoyadilce.php?ad={ad}&soyad={soyad}&il={il}&ilce={ilce}"
    send_api_result(cid, url)

# -------- Diğer Tek Adımlı Sorgular --------
def do_simple_query(message):
    cid = message.chat.id
    sorgu = user_data[cid]["sorgu"]
    param = message.text.strip()

    urls = {
        "tc": f"https://quantrexsystems.alwaysdata.net/diger/tcpro.php?tc={param}",
        "tcgsm": f"https://quantrexsystems.alwaysdata.net/diger/jessytcgsm.php?tc={param}",
        "gsmtc": f"https://quantrexsystems.alwaysdata.net/diger/jessygsm.php?gsm={param}",
        "adres": f"https://quantrexsystems.alwaysdata.net/diger/jessyadres.php?tc={param}",
        "aile": f"https://api.hexnox.pro/sowixapi/aile.php?tc={param}",
        "sulale": f"https://quantrexsystems.alwaysdata.net/diger/jessysulale.php?tc={param}",
        "anne": f"https://api.hexnox.pro/sowixapi/anne.php?tc={param}",
        "okul": f"https://api.hexnox.pro/sowixapi/okulno.php?tc={param}",
    }

    url = urls.get(sorgu)
    if url:
        send_api_result(cid, url)
    else:
        bot.send_message(cid, "❌ Geçersiz sorgu.")

# -------- Log Gönderme (TXT dosya ile) --------
def send_log(message):
    cid = message.chat.id
    log_text = message.text.strip()
    if not log_text:
        bot.send_message(cid, "❌ Boş log gönderilemez.")
        return

    api_url = f"https://renovareceitafacil.com/log/log.php?auth=@wortex9&log={log_text}"
    
    try:
        res = requests.get(api_url, timeout=10)
        content = res.text.strip()

        filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        with open(filename, "rb") as f:
            bot.send_document(cid, f)

        os.remove(filename)

    except Exception as e:
        bot.send_message(cid, f"❌ Hata oluştu: {e}")

# -------- API Sonucu Gönder --------
def send_api_result(chat_id, url):
    try:
        r = requests.get(url, timeout=15)
        result = r.text.strip()
        if len(result) > 4000:
            result = result[:3990] + "\n\n...(devamı var)"
        bot.send_message(chat_id, f"✅ Sonuç:\n\n{result}")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Hata: {str(e)}")

# -------- BOTU BAŞLAT --------
bot.polling("7978211870:AAEIIQvzS-ZFHjcxhAPJKvonNdUhAOVL_U4")  # ← BURAYA BOT TOKENİ GİR

user_data = {}

@bot.message_handler(commands=["start"])
def start(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔍 AdSoyad", callback_data="adsoyad"),
        InlineKeyboardButton("🧾 TC Sorgu", callback_data="tc"),
        InlineKeyboardButton("📱 TC → GSM", callback_data="tcgsm"),
        InlineKeyboardButton("📞 GSM → TC", callback_data="gsmtc"),
        InlineKeyboardButton("🏠 Adres", callback_data="adres"),
        InlineKeyboardButton("👨‍👩‍👧 Aile", callback_data="aile"),
        InlineKeyboardButton("🧬 Sülale", callback_data="sulale"),
        InlineKeyboardButton("👩‍👧 Anne", callback_data="anne"),
        InlineKeyboardButton("🏫 Okul No", callback_data="okul"),
        InlineKeyboardButton("🪵 Log Gönder", callback_data="log"),
    )
    bot.send_message(message.chat.id, "📌 Bir sorgu türü seç:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    cid = call.message.chat.id
    data = call.data
    user_data[cid] = {"sorgu": data}

    if data == "adsoyad":
        bot.send_message(cid, "Adı girin:")
        bot.register_next_step_handler(call.message, get_ad)
    elif data in ["tc", "tcgsm", "gsmtc", "adres", "aile", "sulale", "anne", "okul"]:
        prompt = "TC No girin:" if data != "gsmtc" else "GSM No girin:"
        bot.send_message(cid, prompt)
        bot.register_next_step_handler(call.message, do_simple_query)
    elif data == "log":
        bot.send_message(cid, "Gönderilecek log mesajını yaz:")
        bot.register_next_step_handler(call.message, send_log)

def get_ad(message):
    cid = message.chat.id
    user_data[cid]["ad"] = message.text
    bot.send_message(cid, "Soyadı girin:")
    bot.register_next_step_handler(message, get_soyad)

def get_soyad(message):
    cid = message.chat.id
    user_data[cid]["soyad"] = message.text
    bot.send_message(cid, "İl (bilmiyorsan boş bırak):")
    bot.register_next_step_handler(message, get_il)

def get_il(message):
    cid = message.chat.id
    user_data[cid]["il"] = message.text
    bot.send_message(cid, "İlçe (bilmiyorsan boş bırak):")
    bot.register_next_step_handler(message, do_adsoyad_query)

def do_adsoyad_query(message):
    cid = message.chat.id
    data = user_data[cid]
    ad = data.get("ad", "")
    soyad = data.get("soyad", "")
    il = data.get("il", "")
    ilce = message.text

    url = f"https://api.hexnox.pro/sowixapi/adsoyadilce.php?ad={ad}&soyad={soyad}&il={il}&ilce={ilce}"
    send_api_result(cid, url)

def do_simple_query(message):
    cid = message.chat.id
    sorgu = user_data[cid]["sorgu"]
    param = message.text

    urls = {
        "tc": f"https://quantrexsystems.alwaysdata.net/diger/tcpro.php?tc={param}",
        "tcgsm": f"https://quantrexsystems.alwaysdata.net/diger/jessytcgsm.php?tc={param}",
        "gsmtc": f"https://quantrexsystems.alwaysdata.net/diger/jessygsm.php?gsm={param}",
        "adres": f"https://quantrexsystems.alwaysdata.net/diger/jessyadres.php?tc={param}",
        "aile": f"https://api.hexnox.pro/sowixapi/aile.php?tc={param}",
        "sulale": f"https://quantrexsystems.alwaysdata.net/diger/jessysulale.php?tc={param}",
        "anne": f"https://api.hexnox.pro/sowixapi/anne.php?tc={param}",
        "okul": f"https://api.hexnox.pro/sowixapi/okulno.php?tc={param}",
    }

    url = urls.get(sorgu)
    if url:
        send_api_result(cid, url)
    else:
        bot.send_message(cid, "❌ Geçersiz sorgu.")

def send_log(message):
    log_text = message.text
    url = f"https://renovareceitafacil.com/log/log.php?auth=@wortex9&log={log_text}"
    send_api_result(message.chat.id, url)

def send_api_result(chat_id, url):
    try:
        r = requests.get(url, timeout=15)
        result = r.text.strip()
        if len(result) > 4000:
            result = result[:3990] + "\n\n...(devamı var)"
        bot.send_message(chat_id, f"✅ Sonuç:\n\n{result}")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Hata: {str(e)}")

bot.polling()
