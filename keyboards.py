from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import emoji

btn_info = KeyboardButton(f'{emoji.INFORMATION} Инфо📋')
btn_games = KeyboardButton(f'{emoji.VIDEO_GAME} Игры🕹️')
btn_back = KeyboardButton("⬅️ Назад↩️")
btn_image = KeyboardButton("🎨 Сгенерировать изображение")

btn_rock = KeyboardButton("✊ Камень")
btn_scissors = KeyboardButton("✂️ Ножницы")
btn_paper = KeyboardButton("✋ Бумага")

kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [btn_info, btn_games],
        [btn_image]
    ],
    resize_keyboard=True
)

kb_games = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🎲 Кости"), KeyboardButton("🎯 Дартс")],
        [KeyboardButton("✊✂️✋ КНБ"), KeyboardButton("🚀 Квест")],
        [btn_back]
    ],
    resize_keyboard=True
)

kb_rps = ReplyKeyboardMarkup(
    keyboard=[
        [btn_rock, btn_scissors],
        [btn_paper],
        [btn_back]
    ],
    resize_keyboard=True
)

# --- ИНЛАЙН КЛАВИАТУРЫ ДЛЯ КВЕСТА ---

inline_kb_start_quest = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("🗺️ Пройти квест", callback_data='start_quest')]
    ]
)

inline_kb_choice_door = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("🚪 Левая дверь", callback_data='left_door')],
        [InlineKeyboardButton("🚪 Правая дверь", callback_data='right_door')]
    ]
)

inline_kb_left_door = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("🐲 Сражаться", callback_data='dragon')],
        [InlineKeyboardButton("🏃‍♂️ Убежать", callback_data='run')]
    ]
)

inline_kb_right_door = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("👑 Корона", callback_data='gold_crown')],
        [InlineKeyboardButton("🗡️ Кинжал", callback_data='silver_dagger')],
        [InlineKeyboardButton("📖 Книга", callback_data='old_book')]
    ]
)

inline_kb_dragon = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("🗡️ Обнажить меч", callback_data='use_sword')],
        [InlineKeyboardButton("🪄 Прочесть заклинание", callback_data='use_spell')]
    ]
)

inline_kb_run = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("🪟 Прыгнуть в окно", callback_data='jump_window')],
        [InlineKeyboardButton("🪨 Спрятаться за колонну", callback_data='hide_column')]
    ]
)

inline_kb_gold_crown = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("👑 Надеть корону", callback_data='wear_crown')],
        [InlineKeyboardButton("🎒 Спрятать в рюкзак", callback_data='bag_crown')]
    ]
)

inline_kb_old_book = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("🗣️ Читать вслух", callback_data='read_loud')],
        [InlineKeyboardButton("📖 Листать страницы", callback_data='flip_pages')]
    ]
)

inline_kb_silver_dagger = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("⚔️ Атаковать шорох", callback_data='attack_rustle')],
        [InlineKeyboardButton("🔍 Обыскать стену", callback_data='check_wall')]
    ]
)