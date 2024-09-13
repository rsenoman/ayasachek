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

# List of allowed group chat IDs
ALLOWED_GROUPS = [-1002493556376]  # Add group chat IDs here

# Function to split a long message into chunks
def split_message(message: str, max_length: int = 4096) -> list:
    return [message[i:i+max_length] for i in range(0, len(message), max_length)]

def group_id_check(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        if chat_id not in ALLOWED_GROUPS:
            await update.message.reply_text('This bot is not authorized to be used in this group.')
            return
        return await func(update, context)
    return wrapper

@group_id_check
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Use /cmds to see all available commands.')

@group_id_check
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
        "/proxy <proxy> - Check a proxy\n"
        "/getproxy <protocol> <anonymity> - Generate proxies and get a file\n"
        "/iplookup <ip> - Look up IP details"
    )
    await update.message.reply_text(commands)

@group_id_check
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

@group_id_check
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

@group_id_check
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

@group_id_check
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

@group_id_check
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

@group_id_check
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

@group_id_check
async def cc_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /chk <cc>')
        return

    cc_number = context.args[0]
    response = requests.get(f'{CC_CHECKER_URL}?cc={cc_number}')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'ok':
            message = (f"Card: {data.get('card')}\n"
                       f"Response: {data.get('response')}")
        else:
            message = 'Credit card details not found.'
    else:
        message = 'Failed to check credit card details.'

    await update.message.reply_text(message)

@group_id_check
async def proxy_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /proxy <proxy>')
        return

    proxy = context.args[0]
    response = requests.get(f'{PROXY_CHECKER_URL}?proxy={proxy}')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'ok':
            proxy_data = data.get('data', {})
            message = (f"IP: {proxy_data.get('ip')}\n"
                       f"Port: {proxy_data.get('port')}\n"
                       f"Type: {proxy_data.get('type')}\n"
                       f"Working: {'Yes' if proxy_data.get('working') else 'No'}\n"
                       f"Country: {proxy_data.get('country')}")
        else:
            message = 'Proxy details not found.'
    else:
        message = 'Failed to retrieve proxy details.'

    await update.message.reply_text(message)

@group_id_check
async def get_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 2:
        await update.message.reply_text('Usage: /getproxy <protocol> <anonymity>')
        return

    protocol = context.args[0]
    anonymity = context.args[1]
    response = requests.get(f'{PROXY_GENERATOR_URL}?protocol={protocol}&anonymity={anonymity}')
    
    if response.status_code == 200:
        proxy_file = io.BytesIO(response.content)
        await update.message.reply_document(document=InputFile(proxy_file, filename='proxies.txt'))
    else:
        await update.message.reply_text('Failed to retrieve proxies.')

@group_id_check
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
                       f"Country: {details.get('country')}\n"
                       f"State: {details.get('state')}\n"
                       f"City: {details.get('city')}\n"
                       f"ISP: {details.get('isp')}\n"
                       f"Organization: {details.get('organization')}\n"
                       f"Latitude: {details.get('latitude')}\n"
                       f"Longitude: {details.get('longitude')}\n"
                       f"Continent: {details.get('continent')}\n"
                       f"Timezone: {details.get('timezone')}\n"
                       f"Connection Type: {details.get('connection_type')}\n"
                       f"Map Link: {details.get('map_link')}")
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
    application.add_handler(CommandHandler('chk', cc_check))  # Updated command
    application.add_handler(CommandHandler('proxy', proxy_check))  # Updated command
    application.add_handler(CommandHandler('getproxy', get_proxy))
    application.add_handler(CommandHandler('iplookup', ip_lookup))  # Added command
    
    application.run_polling()

if __name__ == '__main__':
    main()
