import re
import openai
from telethon import TelegramClient, events

# Настройки Telegram API
api_id = 'ВАШ_API_ID'
api_hash = 'ВАШ_API_HASH'
source_channel = 'username_or_id_канала_источника'
target_channel = 'username_or_id_целевого_канала'
phone_number = 'ВАШ_НОМЕР_ТЕЛЕФОНА'

# Настройки OpenAI API
openai.api_key = 'ВАШ_API_KEY_OPENAI'

# Инициализация клиента Telegram
client = TelegramClient('session_name', api_id, api_hash)

# Функция для определения рекламных постов
def is_advertisement(post_text):
    ad_keywords = [
        'реклама', 'рекламный', 'подписывайтесь', 'скидка', 'акция', 
        'спонсор', 'поддержите', 'партнёр', '@', 'переходите по ссылке'
    ]
    return any(keyword in post_text.lower() for keyword in ad_keywords)

# Функция для перефразирования текста с помощью ChatGPT
def paraphrase_text(text):
    prompt = f"Перефразируй этот текст как опытный крипто-трейдер: {text}\n    Пиши просто, понятно и интересно, 2024 год."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты опытный трейдер криптовалюты, пишешь просто и понятно."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message['content'].strip()

# Обработчик новых сообщений в канале
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    post_text = event.message.message
    
    # Отсечение рекламных постов
    if is_advertisement(post_text):
        print("Рекламный пост, пропускаем...")
        return
    
    # Перефразирование текста
    paraphrased_text = paraphrase_text(post_text)
    
    # Отправка перефразированного текста в другой канал
    await client.send_message(target_channel, paraphrased_text)
    print("Пост отправлен в целевой канал.")

# Запуск клиента
with client:
    client.start(phone=phone_number)
    print("Клиент запущен...")
    client.run_until_disconnected()
