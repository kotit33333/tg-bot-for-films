import asyncio
import logging
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import  Command
import config



bot = Bot(token=config.bot_token, parse_mode=ParseMode.HTML)
