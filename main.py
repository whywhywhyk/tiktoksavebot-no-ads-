import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from pytube import YouTube

# Жёстко прописанный токен
BOT_TOKEN = "8062837606:AAGBZEsGRChFfZ6GKOOwuoYoYv0Dc_NQW-M"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ----------- TikTok -------------
async def download_tiktok(url: str) -> str | None:
    api_url = "https://www.tikwm.com/api/"
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, data={"url": url}) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data.get("data") and "play" in data["data"]:
                    play_url = data["data"]["play"]
                    if play_url.startswith("//"):
                        return "https:" + play_url
                    elif play_url.startswith("http"):
                        return play_url
    return None

# ----------- YouTube Shorts -------------
async def download_shorts(url: str) -> str | None:
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
        if stream:
            file_path = f"temp_{yt.video_id}.mp4"
            stream.download(filename=file_path)
            return file_path
    except Exception as e:
        print("Ошибка YouTube:", e)
        return None

# ----------- Хэндлеры -------------
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Пришли мне ссылку на TikTok или YouTube Shorts, и я скачаю видео.")

@dp.message(F.text.contains("tiktok.com"))
async def tiktok_handler(message: Message):
    url = message.text.strip()
    await message.answer("Почекай, ща скачаю TikTok...")
    video_url = await download_tiktok(url)
    if not video_url:
        await message.answer("Не получилось скачать TikTok. Перепроверь ссылку.")
        return
    await message.answer_video(video_url, caption="Тримай своё видео!")

@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def youtube_handler(message: Message):
    url = message.text.strip()
    await message.answer("Почекай, ща скачаю YouTube Shorts...")
    file_path = await download_shorts(url)
    if not file_path:
        await message.answer("Не получилось скачать видео. Проверь ссылку.")
        return
    await message.answer_video(open(file_path, "rb"), caption="Тримай своё видео!")
    os.remove(file_path)

# ----------- Запуск -------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
