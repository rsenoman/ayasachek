from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import io

# Replace 'YOUR_TOKEN' with your bot's token
TOKEN = '7545599113:AAGEdLMMVtNx0qdyVicGvnv-M9dIaCG8Biw'
BIN_API_URL = 'https://drlabapis.onrender.com/api/bin'
SK_API_URL = 'https://drlabapis.onrender.com/api/skgenerator'
SK_CHECKER_URL = 'https://drlabapis.onrender.com/api/skchecker'
SK_FULL_INFO_URL = 'https://drlabapis.onrender.com/api/skfull'
IBAN_API_URL = 'https://drlabapis.onrender.com/api/generateiban'
CC_GENERATOR_URL = 'https://drlabapis.onrender.com/api/ccgenerator'
CC_CHECKER_URL = 'https://drlabapis.onrender.com/api/chk'
PROXY_CHECKER_URL = 'https://drlabapis.onrender.com/api/proxycheck'
PROXY_GENERATOR_URL = 'https://drlabapis.onrender.com/api/getproxy'
IP_LOOKUP_URL = 'https://drlabapis.onrender.com/api/iplookup'

# List of allowed user IDs
ALLOWED_USERS = [1307708031,1801215302,5523467443,5894998246]  # Add user IDs here

# Function to split a long message into chunks
def split_message(message: str, max_length: int = 4096) -> list:
    return [message[i:i+max_length] for i in range(0, len(message), max_length)]

def user_id_check(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        if user_id not in ALLOWED_USERS:
            await update.message.reply_text('You are not authorized to use this bot.')
            return
        return await func(update, context)
    return wrapper

@user_id_check
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Use /cmds to see all available commands.')

@user_id_check
async def cmds(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands = (
        "/start - Start the bot\n"
        "/cmds - List all commands\n"
        "/bin <BIN> - Look up BIN details\n"
        "/sk <count> - Generate SK keys\n"
        "/skcheck <SK> - Check an SK key\n"
        "/skfull <SK> - Full SK key information\n"
        "/iban <country> - Generate an IBAN\n"
        "/cc <bin> [count] - Generate credit cards\n"
        "/chk <cc> - Check a credit card\n"
        "/proxycheck <proxy> - Check a proxy\n"
        "/proxycheckfile - Check proxies from a file\n"
        "/getproxy <protocol> <anonymity> - Generate proxies and get a file\n"
        "/iplookup <ip> - Look up IP details"
    )
    await update.message.reply_text(commands)

@user_id_check
async def bin_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /bin <BIN>')
        return

    bin_number = context.args[0]
    response = requests.get(f'{BIN_API_URL}?bin={bin_number}')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'ok':
            message = (f"Type: {data.get('type')}\n"
                       f"Scheme: {data.get('scheme')}\n"
                       f"Tier: {data.get('tier')}\n"
                       f"Country: {data.get('country')}\n"
                       f"Issuer: {data.get('issuer')}")
        else:
            message = 'No details found for this BIN.'
    else:
        message = 'Failed to retrieve BIN details.'

    await update.message.reply_text(message)

@user_id_check
async def sk_generator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /sk <count> (Max count: 10000)')
        return

    try:
        count = int(context.args[0])
        if count < 1 or count > 10000:
            await update.message.reply_text('Count must be between 1 and 10000.')
            return
    except ValueError:
        await update.message.reply_text('Count must be an integer.')
        return

    response = requests.get(f'{SK_API_URL}?count={count}')
    
    if response.status_code == 200:
        keys = response.text.splitlines()
        message = '\n'.join(keys)
    else:
        message = 'Failed to retrieve SK keys.'

    await update.message.reply_text(message)

@user_id_check
async def sk_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /skcheck <SK>')
        return

    sk_key = context.args[0]
    response = requests.get(f'{SK_CHECKER_URL}?sk={sk_key}')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'ok':
            valid_status = 'valid' if data.get('valid') else 'invalid'
            message = f"SK Key: {data.get('sk')}\nStatus: {valid_status}"
        else:
            message = 'SK Key not found.'
    else:
        message = 'Failed to check SK key.'

    await update.message.reply_text(message)

@user_id_check
async def sk_full_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /skfull <SK>')
        return

    sk_key = context.args[0]
    response = requests.get(f'{SK_FULL_INFO_URL}?sk={sk_key}')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'ok':
            info = data.get('data', {})
            message = (f"Available Balance: {info.get('available_balance')}\n"
                       f"Card Payment: {info.get('card_payment')}\n"
                       f"Charges Enabled: {info.get('charges_enabled')}\n"
                       f"Country: {info.get('country')}\n"
                       f"Currency: {info.get('currency')}\n"
                       f"Display Name: {info.get('display_name')}\n"
                       f"Email: {info.get('email')}\n"
                       f"Pending Balance: {info.get('pending_balance')}\n"
                       f"Phone: {info.get('phone')}\n"
                       f"URL: {info.get('url')}")
        else:
            message = 'No details found for this SK key.'
    else:
        message = 'Failed to retrieve SK key details.'

    await update.message.reply_text(message)

@user_id_check
async def iban_generator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /iban <country>')
        return

    country = context.args[0]
    response = requests.get(f'{IBAN_API_URL}?country={country}')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'ok':
            info = data
            message = (f"IBAN: {info.get('iban')}\n"
                       f"Account Code: {info.get('account_Code')}\n"
                       f"Bank Code: {info.get('bank_code')}\n"
                       f"Bank Name: {info.get('bank_name')}\n"
                       f"BIC: {info.get('bic')}\n"
                       f"Branch Code: {info.get('branch_code')}\n"
                       f"Country: {info.get('country')}")
        else:
            message = 'No details found for this country.'
    else:
        message = 'Failed to retrieve IBAN details.'

    await update.message.reply_text(message)

@user_id_check
async def cc_generator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 1:
        await update.message.reply_text('Usage: /cc <bin> [count] (Default count: 10)')
        return

    bin_number = context.args[0]
    count = context.args[1] if len(context.args) > 1 else 10
    try:
        count = int(count)
        if count < 1:
            await update.message.reply_text('Count must be at least 1.')
            return
    except ValueError:
        await update.message.reply_text('Count must be an integer.')
        return

    response = requests.get(f'{CC_GENERATOR_URL}?bin={bin_number}&count={count}')
    
    if response.status_code == 200:
        cards = response.text.splitlines()
        message = '\n'.join(cards)
    else:
        message = 'Failed to retrieve credit card numbers.'

    await update.message.reply_text(message)

@user_id_check
async def cc_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /chk <cc>')
        return

    cc_info = context.args[0]
    response = requests.get(f'{CC_CHECKER_URL}?cc={cc_info}')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'ok':
            message = (f"Card Number: {data.get('card_number')}\n"
                       f"Card Type: {data.get('card_type')}\n"
                       f"Bank: {data.get('bank')}\n"
                       f"Country: {data.get('country')}\n"
                       f"Valid: {'Yes' if data.get('valid') else 'No'}")
        else:
            message = 'No details found for this card.'
    else:
        message = 'Failed to check credit card.'

    await update.message.reply_text(message)

@user_id_check
async def proxy_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /proxycheck <proxy>')
        return

    proxy = context.args[0]
    response = requests.get(f'{PROXY_CHECKER_URL}?proxy={proxy}')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'ok':
            proxy_info = data.get('data', {})
            message = (f"IP: {proxy_info.get('ip')}\n"
                       f"Port: {proxy_info.get('port')}\n"
                       f"Country: {proxy_info.get('country')}\n"
                       f"Type: {proxy_info.get('type')}\n"
                       f"Working: {'Yes' if proxy_info.get('working') else 'No'}")
        else:
            message = 'No details found for this proxy.'
    else:
        message = 'Failed to check proxy.'

    await update.message.reply_text(message)

@user_id_check
async def proxy_check_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.document:
        file_id = update.message.document.file_id
        new_file = await context.bot.get_file(file_id)
        file_path = new_file.file_path

        response = requests.get(file_path)
        if response.status_code == 200:
            proxies = response.text.splitlines()
            results = []

            for proxy in proxies:
                proxy_response = requests.get(f'{PROXY_CHECKER_URL}?proxy={proxy}')
                if proxy_response.status_code == 200:
                    data = proxy_response.json()
                    if data.get('status') == 'ok':
                        proxy_info = data.get('data', {})
                        result = (f"IP: {proxy_info.get('ip')}\n"
                                  f"Port: {proxy_info.get('port')}\n"
                                  f"Country: {proxy_info.get('country')}\n"
                                  f"Type: {proxy_info.get('type')}\n"
                                  f"Working: {'Yes' if proxy_info.get('working') else 'No'}")
                        results.append(result)
                    else:
                        results.append(f"Proxy {proxy}: No details found.")
                else:
                    results.append(f"Proxy {proxy}: Failed to check.")
            
            message = '\n\n'.join(results)
            messages = split_message(message)  # Split the message if it's too long
            for msg in messages:
                await update.message.reply_text(msg)
        else:
            await update.message.reply_text('Failed to download the file.')
    else:
        await update.message.reply_text('Please send a file.')

@user_id_check
async def get_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 2:
        await update.message.reply_text('Usage: /getproxy <protocol> <anonymity>')
        return

    protocol = context.args[0]
    anonymity = context.args[1]
    if protocol not in ['http', 'socks4', 'socks5', 'all']:
        await update.message.reply_text('Protocol must be one of: http, socks4, socks5, all.')
        return
    if anonymity not in ['elite', 'anonymous', 'transparent', 'all']:
        await update.message.reply_text('Anonymity must be one of: elite, anonymous, transparent, all.')
        return

    response = requests.get(f'{PROXY_GENERATOR_URL}?protocol={protocol}&anonymity={anonymity}')
    
    if response.status_code == 200:
        proxies = response.text.splitlines()
        
        # Create a file with proxies
        file_content = '\n'.join(proxies)
        file = io.BytesIO(file_content.encode())
        file.name = 'proxies.txt'
        
        await update.message.reply_document(document=InputFile(file), filename='proxies.txt')
    else:
        await update.message.reply_text('Failed to retrieve proxies.')

@user_id_check
async def ip_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /iplookup <ip>')
        return

    ip_address = context.args[0]
    response = requests.get(f'{IP_LOOKUP_URL}?ip={ip_address}')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'ok':
            details = data.get('details', {})
            message = (f"IP: {ip_address}\n"
                       f"ASN Number: {details.get('asn_number')}\n"
                       f"City: {details.get('city')}\n"
                       f"Connection Type: {details.get('connection_type')}\n"
                       f"Continent: {details.get('continent')}\n"
                       f"Country: {details.get('country')}\n"
                       f"ISP: {details.get('isp')}\n"
                       f"Latitude: {details.get('latitude')}\n"
                       f"Longitude: {details.get('longitude')}\n"
                       f"Map: {details.get('map_link')}\n"
                       f"Organization: {details.get('organization')}\n"
                       f"State: {details.get('state')}\n"
                       f"Timezone: {details.get('timezone')}\n"
                       f"User Type: {details.get('user_type')}")
        else:
            message = 'No details found for this IP address.'
    else:
        message = 'Failed to retrieve IP details.'

    await update.message.reply_text(message)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('cmds', cmds))
    application.add_handler(CommandHandler('bin', bin_lookup))
    application.add_handler(CommandHandler('sk', sk_generator))
    application.add_handler(CommandHandler('skcheck', sk_check))
    application.add_handler(CommandHandler('skfull', sk_full_info))
    application.add_handler(CommandHandler('iban', iban_generator))
    application.add_handler(CommandHandler('cc', cc_generator))
    application.add_handler(CommandHandler('chk', cc_check))
    application.add_handler(CommandHandler('proxycheck', proxy_check))
    application.add_handler(CommandHandler('proxycheckfile', proxy_check_file))
    application.add_handler(CommandHandler('getproxy', get_proxy))
    application.add_handler(CommandHandler('iplookup', ip_lookup))

    application.run_polling()

if __name__ == '__main__':
    main()
