import asyncio
from datetime import datetime
import random
import json

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from pyrogram import Client, filters
from pyrogram.types import KeyboardButton, InputMediaPhoto, ForceReply
import config
import keyboards

from Stablecog_AI import generate

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name='Matvey_Super_Bot'
)


def button_filter(button):
    async def func(_, __, msg):
        return msg.text == button.text

    return filters.create(func, "ButtonFilter", button=button)


@bot.on_message(filters.command("start") | button_filter(keyboards.btn_back))
async def start(client, message):
    await message.reply(
        "Добро пожаловать в главное меню!",
        reply_markup=keyboards.kb_main
    )
    await message.reply_sticker("CAACAgIAAxkBAAERWAhqJAITrcKp3zLKetZc8WWG71WWNgACLw0AAsdZOErZJ3jXurXSqDsE")

    with open("users.json", "r") as file:
        users = json.load(file)

    user_id = str(message.from_user.id)
    if user_id not in users.keys():
        users[user_id] = {"coins": 100}
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)


@bot.on_message(filters.command("info") | button_filter(keyboards.btn_info))
async def info(client, message):
    text_info = (
        "Привет! Вот что умеет мой бот:\n\n"
        "Базовые команды:\n"
        "/start - Перезапустить бота и открыть главное меню\n"
        "/info - Показать эту справку\n"
        "/time - Узнать точное время\n\n"
        "Нейросети:\n"
        "Нажми кнопку '🎨 Сгенерировать изображение', чтобы создать картинку при помощи ИИ!\n\n"
        "Экономика и Игры:\n"
        "Каждому новому игроку выдается 100 стартовых монет!\n"
        "В меню 'Игры' тебя ждут:\n"
        "🎲 Кости и 🎯 Дартс — бесплатные развлечения.\n"
        "✊✂️✋ КНБ — игра на монеты (вход 10 монет).\n\n"
        "Приключения:\n"
        "🚀 Квест — интерактивная история с выбором дверей. Попробуй выжить при встрече с драконом и найти сокровища!\n\n"
        "Используй кнопки внизу экрана для навигации. А еще можешь просто написать мне 'Привет' или 'Пока'!"
    )
    await message.reply(text_info)


@bot.on_message(button_filter(keyboards.btn_image))
async def image_command(bot, message):
    await message.reply(
        "Введи запрос для генерации изображения",
        reply_markup=ForceReply(selective=True)
    )


@bot.on_message(filters.reply)
async def reply(bot, message):
    if message.reply_to_message and message.reply_to_message.text == "Введи запрос для генерации изображения":
        query = message.text
        await message.reply_text(f"Генерирую изображение по запросу **{query}**. Ожидание около минуты")
        try:
            images = await asyncio.to_thread(generate, query)
            if images and len(images) >= 2:
                await bot.send_media_group(
                    chat_id=message.chat.id,
                    media=[
                        InputMediaPhoto(images[0]),
                        InputMediaPhoto(images[1])
                    ],
                    reply_to_message_id=message.id
                )
                await message.reply(
                    "Возврат в главное меню",
                    reply_markup=keyboards.kb_main
                )
            else:
                await message.reply_text(
                    "Возникла ошибка, попробуйте еще раз",
                    reply_to_message_id=message.id,
                    reply_markup=keyboards.kb_main
                )
        except Exception as e:
            print(f"Ошибка при генерации: {e}")
            await message.reply_text(
                "Не удалось сгенерировать изображение. Проверьте настройки API.",
                reply_to_message_id=message.id,
                reply_markup=keyboards.kb_main
            )


@bot.on_message(filters.command("games") | button_filter(keyboards.btn_games))
async def games_menu(client, message):
    await message.reply(
        "Вы перешли в меню игр. Выберите действие или вернитесь назад:",
        reply_markup=keyboards.kb_games
    )


@bot.on_message(button_filter(KeyboardButton("🎲 Кости")))
async def play_dice(client, message):
    await message.reply("Удачи! Бросаю кость...")
    await client.send_dice(chat_id=message.chat.id, emoji="🎲")


@bot.on_message(button_filter(KeyboardButton("🎯 Дартс")))
async def play_darts(client, message):
    await message.reply("Целюсь в мишень... Метаю дротик!")
    await client.send_dice(chat_id=message.chat.id, emoji="🎯")


@bot.on_message(button_filter(KeyboardButton("✊✂️✋ КНБ")))
async def rps_menu(client, message):
    user_id = str(message.from_user.id)

    with open("users.json", "r") as file:
        users = json.load(file)

    if user_id not in users:
        users[user_id] = {"coins": 100}
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

    user_balance = users[user_id]["coins"]

    if user_balance >= 10:
        await message.reply(
            f"Добро пожаловать в игральный автомат 'Камень, Ножницы, Бумага'!\n"
            f"Стоимость игры: 10 монет. Твой баланс: {user_balance} монет.\n"
            f"Сделай свой выбор:",
            reply_markup=keyboards.kb_rps
        )
    else:
        await message.reply(
            f"Не хватает средств.\n"
            f"На твоем счету {user_balance} монет.\n"
            f"Минимальная сумма для игры - 10 монет."
        )


@bot.on_message(button_filter(keyboards.btn_rock) | button_filter(keyboards.btn_scissors) | button_filter(keyboards.btn_paper))
async def choice_rps(bot, message):
    user_id = str(message.from_user.id)

    with open("users.json", "r") as file:
        users = json.load(file)

    if users[user_id]["coins"] < 10:
        await message.reply("У вас закончились монеты для продолжения игры!", reply_markup=keyboards.kb_main)
        return

    rock = keyboards.btn_rock.text
    scissors = keyboards.btn_scissors.text
    paper = keyboards.btn_paper.text

    user = message.text
    pc = random.choice([rock, scissors, paper])

    if user == pc:
        await message.reply(
            f"Ничья! Я тоже выбрал {pc}.\nБаланс не изменился: {users[user_id]['coins']} монет.",
            reply_markup=keyboards.kb_rps
        )
    elif (user == rock and pc == scissors) or \
            (user == scissors and pc == paper) or \
            (user == paper and pc == rock):
        users[user_id]["coins"] += 10
        await message.reply(
            f"Ты выиграл! Начислено +10 монет! 🎉\nЯ выбрал {pc}.\nТвой баланс: {users[user_id]['coins']} монет.",
            reply_markup=keyboards.kb_rps
        )
    else:
        users[user_id]["coins"] -= 10
        await message.reply(
            f"Ты проиграл. Списано -10 монет. 😔\nЯ выбрал {pc}.\nТвой баланс: {users[user_id]['coins']} монет.",
            reply_markup=keyboards.kb_rps
        )

    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)


@bot.on_message(button_filter(KeyboardButton("🚀 Квест")))
async def start_quest(client, message):
    await message.reply_text(
        "Хотите ли вы отправиться в увлекательное путешествие, полное приключений и загадок?",
        reply_markup=keyboards.inline_kb_start_quest
    )


@bot.on_callback_query()
async def handle_query(bot, query):
    if query.data == 'start_quest':
        await bot.answer_callback_query(
            query.id,
            text="Добро пожаловать в квест под названием Поиски Затерянного Сокровища!",
            show_alert=True
        )
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="Ты стоишь перед двумя дверьми. Какую из них выберешь?",
            reply_markup=keyboards.inline_kb_choice_door
        )
    elif query.data == 'left_door':
        await bot.answer_callback_query(query.id)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="Ты входишь в комнату и видишь злого дракона! У тебя есть два варианта действий:",
            reply_markup=keyboards.inline_kb_left_door
        )
    elif query.data == 'right_door':
        await bot.answer_callback_query(query.id)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="Ты входишь в комнату, наполненную сокровищами! Тебе нужно выбрать только одно сокровище.",
            reply_markup=keyboards.inline_kb_right_door
        )
    elif query.data == 'dragon':
        await bot.answer_callback_query(query.id)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="Ты решаешь встретить опасность лицом к лицу! Дракон делает глубокий вдох, готовясь извергнуть пламя. Что ты предпримешь?",
            reply_markup=keyboards.inline_kb_dragon
        )
    elif query.data == 'run':
        await bot.answer_callback_query(query.id)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="Ты разворачиваешься и бежишь назад, но тяжелая дубовая дверь намертво захлопнулась! Дракон медленно приближается. Где укрыться?",
            reply_markup=keyboards.inline_kb_run
        )
    elif query.data == 'gold_crown':
        await bot.answer_callback_query(query.id)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="Ты берёшь в руки массивную золотую корону, украшенную рубинами. Она словно манит тебя магическим блеском. Каковы твои действия?",
            reply_markup=keyboards.inline_kb_gold_crown
        )
    elif query.data == 'silver_dagger':
        await bot.answer_callback_query(query.id)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="Ты берешь серебряный кинжал, но вдруг слышишь странный пугающий шорох за спиной, будто кто-то крадется во тьме сокровищницы!",
            reply_markup=keyboards.inline_kb_silver_dagger
        )
    elif query.data == 'old_book':
        await bot.answer_callback_query(query.id)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="Ты открываешь пыльную древнюю книгу. Её пожелтевшие страницы исписаны светящимися символами. Что сделаешь?",
            reply_markup=keyboards.inline_kb_old_book
        )
    elif query.data == 'use_sword':
        await bot.answer_callback_query(query.id, text="Ты одолел чудовище!", show_alert=True)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="⚔️ **Победа!** Ты ловко уклонился от огня дракона и пронзил его сердце мечом! За поверженным монстром открылся тайный проход к сокровищам древнего королевства. Ты богат! Возврат в главное меню.",
            reply_markup=keyboards.kb_main
        )
    elif query.data == 'use_spell':
        await bot.answer_callback_query(query.id, text="Магия подвела тебя...", show_alert=True)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="💀 **Игра окончена!** Ты попытался вспомнить заклинание огненного щита, но от страха перепутал слова. Дракон не пощадил тебя. Возврат в главное меню.",
            reply_markup=keyboards.kb_main
        )
    elif query.data == 'jump_window':
        await bot.answer_callback_query(query.id, text="Удачный побег!", show_alert=True)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="🪟 **Квест окончен.** Ты заметил старое витражное окно и без раздумий выпрыгнул в него! Тебе повезло приземлиться на огромный стог сена под замком. Ты жив и невредим, но сокровища остались внутри. Возврат в главное меню.",
            reply_markup=keyboards.kb_main
        )
    elif query.data == 'hide_column':
        await bot.answer_callback_query(query.id, text="Плохое укрытие...", show_alert=True)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="💀 **Игра окончена!** Ты спрятался за каменной колонной, но для яростного пламени дракона это не послужило преградой. Колонна превратилась в пепел вместе с тобой. Возврат в главное меню.",
            reply_markup=keyboards.kb_main
        )
    elif query.data == 'wear_crown':
        await bot.answer_callback_query(query.id, text="Древнее проклятие!", show_alert=True)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="💀 **Игра окончена!** Поддавшись искушению, ты надел корону на голову. В тот же миг твоё тело превратилось в холодный камень — это было проклятие старого короля. Теперь ты часть замка. Возврат в главное меню.",
            reply_markup=keyboards.kb_main
        )
    elif query.data == 'bag_crown':
        await bot.answer_callback_query(query.id, text="Умный выбор!", show_alert=True)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="🎒 **Победа!** Ты аккуратно завернул золотую корону в свой плащ и убрал в рюкзак, не касаясь её головой. Ловушка не сработала! Ты успешно выбрался из замка невероятно богатым человеком. Возврат в главное меню.",
            reply_markup=keyboards.kb_main
        )
    elif query.data == 'read_loud':
        await bot.answer_callback_query(query.id, text="Магия сработала!", show_alert=True)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="✨ **Победа!** Ты прочитал первое попавшееся заклинание вслух. Комната озарилась ярким неоновым светом, и тебя телепортировало прямо в королевскую сокровищницу, откуда есть безопасный выход. Ты победил! Возврат в главное меню.",
            reply_markup=keyboards.kb_main
        )
    elif query.data == 'flip_pages':
        await bot.answer_callback_query(query.id, text="Опасная книга...", show_alert=True)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="💀 **Игра окончена!** Ты решил просто полистать страницы в поисках картинок. Из книги вырвалось ядовитое облако древней усыпляющей пыльцы, и ты уснул вечным сном. Возврат в главное меню.",
            reply_markup=keyboards.kb_main
        )
    elif query.data == 'attack_rustle':
        await bot.answer_callback_query(query.id, text="Ложная тревога...", show_alert=True)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="🦇 **Квест окончен.** Ты резко развернулся и атаковал тень! Но это оказалась всего лишь испуганная летучая мышь. От неожиданности ты выронил серебряный кинжал в глубокую расщелину в полу. Ты цел, но уходишь с пустыми руками. Возврат в главное меню.",
            reply_markup=keyboards.kb_main
        )
    elif query.data == 'check_wall':
        await bot.answer_callback_query(query.id, text="Тайник найден!", show_alert=True)
        await query.message.delete()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="🔍 **Победа!** Ты проигнорировал шорох и начал ощупывать стену рядом. Твои пальцы наткнулись на секретный каменный рычаг! Стена отодвинулась, открыв скрытый сундук с золотом. Ты успешно забираешь его. Возврат в главное меню.",
            reply_markup=keyboards.kb_main
        )


@bot.on_message(filters.command("time"))
async def show_time(client, message):
    current_time = datetime.now().strftime("%H:%M:%S")
    await message.reply(f"Текущее время: {current_time}")


@bot.on_message()
async def echo(client, message):
    if message.text is None:
        return
    if message.text.lower() == 'привет':
        await message.reply('Привет')
    elif message.text.lower() == 'пока':
        await message.reply('Пока')
    else:
        await message.reply(f'Ты написал: {message.text}')


bot.run()