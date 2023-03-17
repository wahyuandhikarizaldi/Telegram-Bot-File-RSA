import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import aiogram
from aiogram import Bot, Dispatcher, types

# Firebase Admin SDK
key = {
    "<YOUR-SDK-HERE>"
}

# Initialize Firebase credentials
cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred)

# Initialize Firestore database
db = firestore.client()

# Initialize Telegram bot and dispatcher
bot = Bot("<YOUR-BOT-TOKEN-HERE>")
dp = Dispatcher(bot)


### RSA Function

# Finding GCD (Greatest Common Divisor)
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Generate the RSA Key Pair (Public Key and Private Key)
def generate_key_pair(p, q):
  
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Calculate the private key
    d = pow(e, -1, phi)

    # Return public and private key pair
    print (e, n, d)
    return ((e, n), (d, n))

# Encrypt function
def encrypt(public_key, message):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in message]
    return cipher

# Decrypt function
def decrypt(private_key, cipher):
    d, n = private_key
    message = [chr(pow(char, d, n)) for char in cipher]
    return ''.join(message)

# Define prime numbers
p = 61
q = 53
public, private = generate_key_pair(p, q)
print (p)
print (q)
print (public)
print (private)


### Telegram Bot Command Handler

# Sends message after /start
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer('Hello! Welcome to sub_bot! /help for more info!')  
  
# Sends message after /help
@dp.message_handler(commands=['help'])
async def welcome(message: types.Message):
    await message.answer('To get your file, type /get <your code>')    

# Handle /add <url> command, decrypt the url, then add it to database
@dp.message_handler(commands=['add'])
async def add_document(message: types.Message):
    # Extract url from the message
    url = message.text.split(' ')[1]
    # Encrypt the url
    encrypted_url = encrypt(public, url)
    # Generate a random 9-digit ID
    new_code = str(random.randint(100000000, 999999999))
    # Create a new document with the generated ID and URL
    doc_ref = db.collection(u'files').document(new_code)
    doc_ref.set({"url": encrypted_url})
    
    # Send confirmation message to the user
    await message.reply(f"New document added with code: {new_code}")

# Handle /get <code> command, get the encrypted url, decrypt it, then send to the user
@dp.message_handler(commands=['get'])
async def get_document(message: types.Message):
    # Extract code from the message
    code = message.text.split(' ')[1]
    # Query the Firestore database for the document URL
    doc_ref = db.collection(u'files').document(code)
    doc_data = doc_ref.get().to_dict()
    doc_url = doc_data['url']
    # Decrypt the url
    decrypted_url = decrypt(private, doc_url)
    # Send the decrypted url to the user
    await bot.send_message(chat_id=message.chat.id, text=decrypted_url)


### Execute

if __name__ == '__main__':
    # Start the Telegram bot
    aiogram.executor.start_polling(dp, skip_updates=True)
