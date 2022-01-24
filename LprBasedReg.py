
import logging
import asyncio
import time
import lpr_const as lpr

from aiogram import Bot, Dispatcher, executor, types
from sqlighterReg import SQLighter

from aiogram.utils.exceptions import BotBlocked

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

    # инициализируем бота
bot = Bot(token='1524730102:AAHDcQkEhR1J3XZwKFqFegbkaxGkSH2rJEg')
dp = Dispatcher(bot)

    # инициализируем соединение с БД
db = SQLighter(lpr.dbase)

tconv = lambda x: time.strftime("%d.%m.%Y")


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(lpr.msg_yes)
    item2 = types.KeyboardButton(lpr.msg_no)

    markup.add(item1, item2)

    if db.subscriber_exists(message.from_user.id):
        await message.answer (lpr.msg_already)
    else:
        pho = open('tutor.jpg', 'rb')
        await message.answer(lpr.msg_ask, reply_markup=markup, parse_mode='markdown', disable_web_page_preview=True)
        await message.answer(lpr.msg_tutorial)
        await bot.send_photo(message.chat.id, pho)
        pho.close()


# Команда активации подписки на ЛПР
@dp.message_handler(text=[lpr.msg_yes])
async def subscribe(message: types.Message):
    if db.subscriber_exists(message.from_user.id):
        print (message.from_user.id)
        await message.answer(lpr.msg_already)
    else:
        db.add_subscriber(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
        await message.answer (lpr.msg_yes_final, parse_mode='markdown',
        disable_web_page_preview=True)



# Команда выхода из ЛПР
@dp.message_handler(text=[lpr.msg_no])

async def unsubscribe(message: types.Message):
        if db.subscriber_exists(message.from_user.id):
            await message.answer (lpr.msg_already)
        else:
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item4 = types.KeyboardButton(lpr.msg_no_confirm)
            item5 = types.KeyboardButton(lpr.msg_no_cancel)
            markup2.add(item4, item5)

            # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
            await message.answer(lpr.msg_no_captcha, reply_markup=markup2)

@dp.message_handler(text=[lpr.msg_no_confirm])
async def unsubscribe(message: types.Message):
    if db.subscriber_exists(message.from_user.id):
        await message.answer(lpr.msg_already)
    else:

        db.add_subscriber(message.from_user.id, message.from_user.username, message.from_user.first_name,
                          message.from_user.last_name, False)
        await message.answer (lpr.msg_no_final, parse_mode='markdown',
        disable_web_page_preview=True)

@dp.message_handler(text=[lpr.msg_no_cancel])
async def unsubscribe(message: types.Message):
    if db.subscriber_exists(message.from_user.id):
        await message.answer(lpr.msg_already)
    else:

        markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item2 = types.KeyboardButton(lpr.msg_yes)
        item3 = types.KeyboardButton(lpr.msg_no)
        markup3.add(item2, item3)
        await message.answer(lpr.msg_ask, reply_markup=markup3, parse_mode='markdown', disable_web_page_preview=True)




"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
-----------------------------------------------------------------------------------------------------------------------
                            d                    INLINE-HANDLERS
-----------------------------------------------------------------------------------------------------------------------
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@dp.inline_handler()
async def inline_message(query: types.InlineQuery):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton(lpr.msg_yes, callback_data='yes')
    item2 = types.InlineKeyboardButton(lpr.msg_no, callback_data='no')
    markup.add(item1, item2)

    result = types.InlineQueryResultArticle(
        id=".",
        title=lpr.msg_inline_1,
        description=lpr.msg_inline_2,
        input_message_content=types.InputTextMessageContent(
            lpr.msg_ask, parse_mode='markdown',
        disable_web_page_preview=True
        ),
        reply_markup=markup,
    )

    await bot.answer_inline_query(query.id, [result], cache_time=1, is_personal=True)


@dp.callback_query_handler(lambda callback_data: True)
async def subscribe(call: types.CallbackQuery):
    markup1 = types.InlineKeyboardMarkup(row_width=2)
    item2 = types.InlineKeyboardButton(lpr.msg_no_confirm, callback_data='confirm')
    item3 = types.InlineKeyboardButton(lpr.msg_no_cancel, callback_data='cancel')
    markup1.add(item2, item3)
    try:
        if call.bot:
            if call.data == 'yes':

                if db.subscriber_exists(call.from_user.id):
                    await bot.edit_message_text(inline_message_id=call.inline_message_id,
                                            text=lpr.msg_already,
                                            reply_markup=None)
                else:
                    db.add_subscriber(call.from_user.id, call.from_user.username,
                                      call.from_user.first_name, call.from_user.last_name)
                    await bot.edit_message_text(inline_message_id=call.inline_message_id,
                                                text=lpr.msg_yes_final,
                                                reply_markup=None, parse_mode='markdown', disable_web_page_preview=True)


            elif call.data == 'no':

                if db.subscriber_exists(call.from_user.id):
                    await bot.edit_message_text(inline_message_id=call.inline_message_id,
                                                text=lpr.msg_already,
                                                reply_markup=None)
                else:

                    await bot.edit_message_text(inline_message_id = call.inline_message_id , text=lpr.msg_no_captcha,
                        reply_markup=markup1)

            elif call.data == 'confirm':

                if db.subscriber_exists(call.from_user.id):
                    await bot.edit_message_text(inline_message_id=call.inline_message_id,
                                                text=lpr.msg_already,
                                                reply_markup=None)
                else:

                    db.add_subscriber(call.from_user.id, call.from_user.username,
                                      call.from_user.first_name, call.from_user.last_name, False)
                    await bot.edit_message_text(inline_message_id=call.inline_message_id,
                                                text=lpr.msg_no_final,
                                                reply_markup=None, parse_mode='markdown', disable_web_page_preview=True)
            elif call.data == 'cancel':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton(lpr.msg_yes, callback_data='yes')
                item2 = types.InlineKeyboardButton(lpr.msg_no, callback_data='no')
                markup.add(item1, item2)

                if db.subscriber_exists(call.from_user.id):
                    await bot.edit_message_text(inline_message_id=call.inline_message_id,
                                                text=lpr.msg_already,
                                                reply_markup=None, parse_mode='markdown', disable_web_page_preview=True)
                else:
                    await bot.edit_message_text(inline_message_id = call.inline_message_id , text=lpr.msg_ask,
                        reply_markup=markup, parse_mode='markdown', disable_web_page_preview=True)

    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
  executor.start_polling(dp)
