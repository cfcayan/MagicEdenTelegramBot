import telebot
import requests
import urllib.request


from telebot import types
token=''
bot=telebot.TeleBot(token)


sREVIEW_WALLET = "Review Wallet"
sLAUNCHPAD = "Top Launchpad Collections"

sWalletActivities = "Wallet Activities"
sWalletTokens = "Wallet Tokens"
sWalletOffersMade = "Offers Made by Wallet"
sWalletOffersReceived = "Offers Received by Wallet"
sWalletEscrowBalance = "Escrow Balance in Wallet"

sTokenMint = "Token Mint"
sTokenListings = "Token Listings"
sTokenActivities = "Token Activities"
sTokenOffersReceived = "Offers Received for Token"



sCollectionListings = "Collection Listings"
sCollectionActivities = "Collection Activities"
sCollectionStats = "Collection Stats"

global current_launchpad

@bot.message_handler(commands=['start'])

def start_message(message):
    bot.send_message(message.chat.id,'Magic Eden is the leading NFT Marketplace on Solana. Discover the best and latest Solana NFT collections via Telegram.')
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton(sREVIEW_WALLET)
    markup.add(item1)
    item2=types.KeyboardButton(sLAUNCHPAD)
    markup.add(item2)  
    bot.send_message(message.chat.id,'Let me know what do you want to look?',reply_markup=markup)

@bot.message_handler(content_types='text')

def message_reply(message):
    if message.text==sLAUNCHPAD:
        url = "https://api-devnet.magiceden.dev/v2/launchpad/collections?offset=4&limit=1"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonResponse = response.json()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        for collection in jsonResponse:
            bot.send_message(message.chat.id,'Symbol: {0} \nName: {1} \nDescription: {2} \nPrice: {3} \nLaunch Date: {4} \n'.format(collection["symbol"],collection["name"],collection["description"],collection["price"],collection["launchDatetime"]))
            try:
                urllib.request.urlretrieve(collection["image"], collection["symbol"]+".png")
                doc = open(collection["symbol"]+".png", 'rb')
                bot.send_document(chat_id=message.chat.id, document=doc)
            except:
                bot.send_message(message.chat.id,'No image')
            item=types.KeyboardButton(collection["symbol"])
            markup.add(item)
        Launchpad_Collection_Symbol = bot.send_message(message.chat.id,'Please select inerested symbol',reply_markup=markup)
        bot.register_next_step_handler(Launchpad_Collection_Symbol , set_launchpad_collection_symbol)
    elif message.text==sREVIEW_WALLET:
        Wallet_Address = bot.send_message(message.chat.id, "Please enter wallet address for review:")
        bot.register_next_step_handler(Wallet_Address , set_wallet_address)

def set_wallet_address(message,sWallet_Address="Optional"):
    cid = message.chat.id
    if sWallet_Address=="Optional":
        sWallet_Address= message.text

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton(sWalletActivities)
    markup.add(item1)
    item2=types.KeyboardButton(sWalletTokens)
    markup.add(item2)
    item3=types.KeyboardButton(sWalletOffersMade)
    markup.add(item3)    
    item4=types.KeyboardButton(sWalletOffersReceived)
    markup.add(item4)    
    item5=types.KeyboardButton(sWalletEscrowBalance)
    markup.add(item5)    
    Wallet_Option = bot.send_message(message.chat.id,'Please select for wallet information:',reply_markup=markup)
    bot.register_next_step_handler(Wallet_Option , select_wallet_option,Wallet_Option=Wallet_Option,sWallet_Address=sWallet_Address)

def select_wallet_option(message,Wallet_Option,sWallet_Address):
    if message.text == sWalletActivities:
        url = "https://api-devnet.magiceden.dev/v2/wallets/"+sWallet_Address+"/activities?offset=0&limit=10"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonResponse = response.json()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        listings_reply = ''
        for wallet in jsonResponse:
            try:
                listings_reply = bot.send_message(message.chat.id,'Signature: {0} \nType: {1} \nSource: {2} \nToken Mint: {3} \nCollection: {4} \nSlot: {5} \nBuyer: {6} \nSeller: {7} \nPrice: {8}'.format(wallet["signature"],wallet["type"],wallet["source"],wallet["tokenMint"],wallet["collection"],wallet["slot"],wallet["buyer"],wallet["seller"],wallet["price"]))
            except:
                pass
        if listings_reply=='':
            listings_reply = bot.send_message(message.chat.id,'No activities found')
        bot.register_next_step_handler(listings_reply , set_wallet_address,sWallet_Address)  
    elif message.text == sWalletOffersMade:
        url = "https://api-devnet.magiceden.dev/v2/wallets/"+sWallet_Address+"/offers_made?offset=0&limit=10"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonResponse = response.json()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        listings_reply = ''
        for wallet in jsonResponse:
            try:
                listings_reply = bot.send_message(message.chat.id,'pda Address: {0} \nToken Mint: {1} \nBuyer: {2} \nToken Size: {3} \nPrice: {4}'.format(wallet["pdaAddress"],wallet["tokenMint"],wallet["buyer"],wallet["tokenSize"],wallet["price"] ))
            except:
                pass
        if listings_reply=='':
            listings_reply = bot.send_message(message.chat.id,'No offers found')
        bot.register_next_step_handler(listings_reply , set_wallet_address,sWallet_Address)  
    elif message.text == sWalletOffersReceived:
        url = "https://api-devnet.magiceden.dev/v2/wallets/"+sWallet_Address+"/offers_received?offset=0&limit=10"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonResponse = response.json()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        listings_reply = ''
        for wallet in jsonResponse:
            try:
                listings_reply = bot.send_message(message.chat.id,'pda Address: {0} \nToken Mint: {1} \nBuyer: {2} \nToken Size: {3} \nPrice: {4}'.format(wallet["pdaAddress"],wallet["tokenMint"],wallet["buyer"],wallet["tokenSize"],wallet["price"] ))
            except:
                pass
        if listings_reply=='':
            listings_reply = bot.send_message(message.chat.id,'No offers found')
        bot.register_next_step_handler(listings_reply , set_wallet_address,sWallet_Address)         
    elif message.text == sWalletEscrowBalance:
        url = "https://api-devnet.magiceden.dev/v2/wallets/"+sWallet_Address+"/escrow_balance"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonResponse = response.json()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        listings_reply = ''
        listings_reply = bot.send_message(message.chat.id,'Buyer Escrow: {0} \nBalance: {1}'.format(jsonResponse["buyerEscrow"],jsonResponse["balance"]))
        bot.register_next_step_handler(listings_reply , set_wallet_address,sWallet_Address) 
    elif message.text == sWalletTokens:
        url = "https://api-devnet.magiceden.dev/v2/wallets/"+sWallet_Address+"/tokens?offset=0&limit=10&listedOnly=true"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonResponse = response.json()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        for wallet in jsonResponse:
            bot.send_message(message.chat.id,'Mint Address: {0} \nOwner: {1} \nDelegate: {2} \nName: {3} \nUpdate Authority: {4}'.format(wallet["mintAddress"],wallet["owner"],wallet["delegate"],wallet["name"],wallet["updateAuthority"]))
            try:
                urllib.request.urlretrieve(wallet["image"], wallet["symbol"]+".png")
                doc = open(wallet["mintAddress"]+".png", 'rb')
                bot.send_document(chat_id=message.chat.id, document=doc)
            except:
                bot.send_message(message.chat.id,'No image')
            item=types.KeyboardButton(wallet["mintAddress"])
            markup.add(item)
        listings_reply = bot.send_message(message.chat.id,'Please select interested token',reply_markup=markup)
        bot.register_next_step_handler(listings_reply , set_token)

def set_token(message,sToken="Optional"):
    cid = message.chat.id
    if sToken=="Optional":
        sToken= message.text
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton(sTokenMint)
    markup.add(item1)
    item2=types.KeyboardButton(sTokenListings)
    markup.add(item2)
    item3=types.KeyboardButton(sTokenActivities)
    markup.add(item3)    
    item4=types.KeyboardButton(sTokenOffersReceived)
    markup.add(item4)    
    Token_Option = bot.send_message(message.chat.id,'Please select for token information:',reply_markup=markup)
    bot.register_next_step_handler(Token_Option , select_token_option,Token_Option=Token_Option,sToken=sToken)

def select_token_option(message,Token_Option,sToken):
    if message.text == sTokenActivities:
        url = "https://api-devnet.magiceden.dev/v2/tokens/"+sToken+"/activities?offset=0&limit=100"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonResponse = response.json()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        listings_reply = ''
        for token in jsonResponse:
            try:
                listings_reply = bot.send_message(message.chat.id,'Signature: {0} \nType: {1} \nSource: {2} \nToken Mint: {3} \nSlot: {4} \nSeller: {5} \nPrice: {6}'.format(token["signature"],token["type"],token["source"],token["tokenMint"],token["slot"],token["seller"],token["price"]))
            except:
                pass
        if listings_reply=='':
            listings_reply = bot.send_message(message.chat.id,'No tokens found')
        bot.register_next_step_handler(listings_reply , set_token,sToken)  
    elif message.text == sTokenListings:
        url = "https://api-devnet.magiceden.dev/v2/tokens/"+sToken+"/listings"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonResponse = response.json()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        listings_reply = ''
        for token in jsonResponse:
            try:
                listings_reply = bot.send_message(message.chat.id,'pda Address: {0} \nToken Address: {1} \nToken Mint: {2} \nSeller: {3} \nToken Size: {4} \nPrice: {5}'.format(collection["pdaAddress"],collection["tokenAddress"],collection["tokenMint"],collection["seller"],collection["tokenSize"],collection["price"] ))
            except:
                pass
        if listings_reply=='':
            listings_reply = bot.send_message(message.chat.id,'No tokens found')
        bot.register_next_step_handler(listings_reply , set_token,sToken) 
    elif message.text == sTokenOffersReceived:
        url = "https://api-devnet.magiceden.dev/v2/tokens/"+sToken+"/offers_received?offset=0&limit=100"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonResponse = response.json()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        listings_reply = ''
        for token in jsonResponse:
            try:
                listings_reply = bot.send_message(message.chat.id,'pda Address: {0} \nToken Mint: {1} \nBuyer: {2} \nToken Size: {3} \nPrice: {4}'.format(wallet["pdaAddress"],wallet["tokenMint"],wallet["buyer"],wallet["tokenSize"],wallet["price"] ))
            except:
                pass
        if listings_reply=='':
            listings_reply = bot.send_message(message.chat.id,'No tokens found')
        bot.register_next_step_handler(listings_reply , set_token,sToken) 
    elif message.text == sTokenMint:
        url = "https://api-devnet.magiceden.dev/v2/tokens/"+sToken
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonResponse = response.json()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id,'Mint Address: {0} \nOwner: {1} \nCollection: {2} \nName: {3} \nUpdate Authority: {4}'.format(wallet["mintAddress"],wallet["owner"],wallet["collection"],wallet["name"],wallet["updateAuthority"]))
        try:
            urllib.request.urlretrieve(wallet["image"], wallet["symbol"]+".png")
            doc = open(wallet["mintAddress"]+".png", 'rb')
            listings_reply = bot.send_document(chat_id=message.chat.id, document=doc)
        except:
            listings_reply = bot.send_message(message.chat.id,'No image')
        bot.register_next_step_handler(listings_reply , set_token,sToken) 
def set_launchpad_collection_symbol(message,sLaunchpad_Collection_Symbol="Optional"):
    cid = message.chat.id
    if sLaunchpad_Collection_Symbol=="Optional":
        sLaunchpad_Collection_Symbol= message.text

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1=types.KeyboardButton(sCollectionListings)
    markup.add(item1)
    item2=types.KeyboardButton(sCollectionActivities)
    markup.add(item2)
    item3=types.KeyboardButton(sCollectionStats)
    markup.add(item3)    
    Collection_Option = bot.send_message(message.chat.id,'Please select for collection information:',reply_markup=markup)
    bot.register_next_step_handler(Collection_Option , select_collection_option,Collection_Option=Collection_Option,sLaunchpad_Collection_Symbol=sLaunchpad_Collection_Symbol)

def select_collection_option(message,Collection_Option,sLaunchpad_Collection_Symbol):
    if message.text == sCollectionListings:
        url = "https://api-devnet.magiceden.dev/v2/collections/"+sLaunchpad_Collection_Symbol+"/listings?offset=0&limit=10"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonResponse = response.json()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        listings_reply = ''
        for collection in jsonResponse:
            listings_reply = bot.send_message(message.chat.id,'pda Address: {0} \nToken Address: {1} \nToken Mint: {2} \nSeller: {3} \nToken Size: {4} \nPrice: {5}'.format(collection["pdaAddress"],collection["tokenAddress"],collection["tokenMint"],collection["seller"],collection["tokenSize"],collection["price"] ))
        if listings_reply=='':
            listings_reply = bot.send_message(message.chat.id,'No listings found')
        bot.register_next_step_handler(listings_reply , set_launchpad_collection_symbol,sLaunchpad_Collection_Symbol)    
    elif message.text == sCollectionActivities:
        url = "https://api-devnet.magiceden.dev/v2/collections/"+sLaunchpad_Collection_Symbol+"/activities?offset=0&limit=10"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonResponse = response.json()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        listings_reply = ''
        for collection in jsonResponse:
            listings_reply = bot.send_message(message.chat.id,'Signature: {0} \nType: {1} \nSource: {2} \nToken Mint: {3} \nCollection: {4} \nSlot: {5} \nBuyer: {6} \nPrice: {7}'.format(collection["signature"],collection["type"],collection["source"],collection["tokenMint"],collection["collection"],collection["slot"],collection["buyer"],collection["price"]))
        if listings_reply=='':
            listings_reply = bot.send_message(message.chat.id,'No activities found')
        bot.register_next_step_handler(listings_reply , set_launchpad_collection_symbol,sLaunchpad_Collection_Symbol)    
    elif message.text == sCollectionStats:
        url = "https://api-devnet.magiceden.dev/v2/collections/"+sLaunchpad_Collection_Symbol+"/stats"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonResponse = response.json()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        listings_reply = ''
        try:
            listings_reply = bot.send_message(message.chat.id,'Symbol: {0} \nFloor Price: {1} \nListed Count: {2} \nVolume All: {3} \n'.format(jsonResponse["symbol"],jsonResponse["floorPrice"],jsonResponse["listedCount"],jsonResponse["volumeAll"]))
        except:
            listings_reply = bot.send_message(message.chat.id,'Symbol: {0} \n'.format(jsonResponse["symbol"]))
        if listings_reply=='':
            listings_reply = bot.send_message(message.chat.id,'No stats found')
        bot.register_next_step_handler(listings_reply , set_launchpad_collection_symbol,sLaunchpad_Collection_Symbol)    

bot.infinity_polling()
