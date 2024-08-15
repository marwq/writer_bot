import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from httpx import AsyncClient

load_dotenv()


if os.environ.get('PROXY'):
    http_client = AsyncClient(proxy=os.environ['PROXY'])
    client = AsyncOpenAI(http_client=http_client)
else:
    client = AsyncOpenAI()

bot = Bot(os.environ["BOT_TOKEN"], default=(DefaultBotProperties(parse_mode='HTML')))
dp = Dispatcher()

with open('prompt_by_claude.txt', 'r', encoding='utf8') as f:
    prompt = f.read()

@dp.message(CommandStart())
async def _(m: types.Message):
    await m.answer('🇬🇧 Hello! Send me text and i will enhance and format it.\n\n'\
                    '🇷🇺 Привет! Отправь мне текст и я улучшу и оформлю его.')

@dp.message()
async def _(m: types.Message):
    msg = await m.answer('One moment...')
    completion = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": prompt
            },
            {
                "role": "user", 
                "content": m.text
            },
        ]
    )
    await msg.edit_text(completion.choices[0].message.content)

asyncio.run(dp.start_polling(bot))
