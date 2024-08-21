import os, asyncio
from io import BytesIO
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from middlewares.album_middleware import AlbumMiddleWare

from join_pdf import join_pdf, delete_pdf
from config import BOT_INFO, BASE_DIR


load_dotenv()


bot_token = os.getenv('TOKEN_BOT')


bot = Bot(bot_token)
dp = Dispatcher() # main router
dp.message.middleware(AlbumMiddleWare())



@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(BOT_INFO)


@dp.message(F.photo)
async def message_with_photo(message: types.Message, album: list = None):  
    buffer_list = []
    
    if album:
        for photo in album:
            photo_id = photo.photo[-1].file_id
            file = await bot.get_file(photo_id)
            buffer = BytesIO()

            await bot.download_file(file.file_path, buffer)
            
            buffer_list.append(buffer)

    else:
        photo_id = message.photo[-1].file_id
        file = await bot.get_file(photo_id)
        buffer = BytesIO()

        await bot.download_file(file.file_path, buffer)
        
        buffer_list.append(buffer)


    file_path = join_pdf(buffer_list, message.from_user.id)
    
    if file_path is not None:
        await message.answer_document(types.FSInputFile(path=file_path, filename="output.pdf"), caption="Your pdf file")

        delete_pdf(file_path)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    asyncio.run(main())