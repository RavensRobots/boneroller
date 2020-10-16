import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from uuid import uuid4

import interface_layout as il
from localization import tr


def init_handlers(dispatcher):
    logging.info("Инициализация обработчиков inline кдавиатуры")
    dispatcher.add_handler(InlineQueryHandler(inline_handler))


def inline_handler(update, context):
    options = [
        InlineQueryResultArticle(
            id=uuid4(),
            title=tr("roll_4"),
            description=tr("roll_4_descr"),
            thumb_url="https://i.imgur.com/XqCLXOx.png",
            input_message_content=InputTextMessageContent(il.roll(4), parse_mode="HTML")),
        InlineQueryResultArticle(
            id=uuid4(),
            title=tr("roll_6"),
            description=tr("roll_6_descr"),
            thumb_url="https://i.imgur.com/VXXCjQG.png",
            input_message_content=InputTextMessageContent(il.roll(6), parse_mode="HTML")),
        InlineQueryResultArticle(
            id=uuid4(),
            title=tr("roll_8"),
            description=tr("roll_8_descr"),
            thumb_url="https://i.imgur.com/I5tYPv6.png",
            input_message_content=InputTextMessageContent(il.roll(8), parse_mode="HTML")),
        InlineQueryResultArticle(
            id=uuid4(),
            title=tr("roll_10"),
            description=tr("roll_10_descr"),
            thumb_url="https://i.imgur.com/HCoFo5k.png",
            input_message_content=InputTextMessageContent(il.roll(10), parse_mode="HTML")),
        InlineQueryResultArticle(
            id=uuid4(),
            title=tr("roll_12"),
            description=tr("roll_12_descr"),
            thumb_url="https://i.imgur.com/0ouwReP.png",
            input_message_content=InputTextMessageContent(il.roll(12), parse_mode="HTML")),
        InlineQueryResultArticle(
            id=uuid4(),
            title=tr("roll_20"),
            description=tr("roll_20_descr"),
            thumb_url="https://i.imgur.com/Kw5Sjgf.png",
            input_message_content=InputTextMessageContent(il.roll(20), parse_mode="HTML")),
        InlineQueryResultArticle(
            id=uuid4(),
            title=tr("roll_100"),
            description=tr("roll_100_descr"),
            thumb_url="https://i.imgur.com/x1GcWWu.png",
            input_message_content=InputTextMessageContent(il.roll(100), parse_mode="HTML")),
    ]
    update.inline_query.answer(options, cache_time=0)
