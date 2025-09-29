import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

BOT_TOKEN = "8062837606:AAGY1KIbxrZhNLyKXtJmGsC077XQ6_kVFME"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Функция для получения ссылки на видео
async def download_tiktok(url: str) -> str | None:
    api_url = "https://www.tikwm.com/api/"
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, data={"url": url}) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data.get("data") and "play" in data["data"]:
                    play_url = data["data"]["play"]

                    # Проверяем формат
                    if play_url.startswith("//"):
                        return "https:" + play_url
                    elif play_url.startswith("http"):
                        return play_url
    return None


# Команда /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("привет!\nпришли мне ссылку на тикток, и я скачаю видео.")


# Обработка TikTok-ссылок
@dp.message(F.text.contains("tiktok.com"))
async def tiktok_handler(message: Message):
    url = message.text.strip()
    await message.answer("чекай ща скачаю...")

    video_url = await download_tiktok(url)
    if not video_url:
        await message.answer("не получилось. перепроверь ссылку.")
        return

    # Отправляем видео напрямую по URL
    await message.answer_video(video_url, caption="тримай твое видео")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
