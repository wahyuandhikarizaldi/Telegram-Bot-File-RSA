# Telegram-Bot-File-RSA
## ETS RSA Kriptografi B | Kelompok 2
- Wahyu Andhika Rizaldi - 5027211003
- Aqila Aqsa - 5027211032
- Caroline Permatasari - 5027211048
- Vira Datry - 5027211050

## Library
- firebase_admin : For database
- aiogram : For Telegram bot

## What does the bot do?
It can add an RSA encrypted url to the database, also decrypt it for the client.

## How the bot works?
- /add <url> will encrypt the url then add it to the database
- /get <"code"> will get the specified url, encrypt it, then send it to the client.
