
from typing import Any, Dict, Union
from aiogram import types
from aiogram import BaseMiddleware
import asyncio



class AlbumMiddleWare(BaseMiddleware):
    def __init__(self, latency: Union[int, float] = 0.1):
        self.latency = latency # в течение 0.1 секунды ждем другие фотки
        self.album_data = {}

    def collect_album_messages(self, event: types.Message):
        if event.media_group_id not in self.album_data:
            self.album_data[event.media_group_id] = {"messages" : []}
        

        self.album_data[event.media_group_id]["messages"].append(event)


        return len(self.album_data[event.media_group_id]["messages"])

    async def __call__(self, handler, event: types.Message, data: Dict[str, Any]) -> Any:
        if not event.media_group_id:
            return await handler(event, data) # передаем управление следующему обработчику
        
        total_before = self.collect_album_messages(event=event)
        
        await asyncio.sleep(self.latency)

        total_after = len(self.album_data[event.media_group_id]["messages"])

        if total_after != total_before:
            return
        

        album_messages = self.album_data[event.media_group_id]["messages"]
        album_messages.sort(key=lambda x: x.message_id)

        data["album"] = album_messages


        del self.album_data[event.media_group_id]

        return await handler(event, data)
