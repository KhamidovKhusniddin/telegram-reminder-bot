import telebot
from telebot import types
import json
import os
from datetime import datetime
import threading
import time
from dotenv import load_dotenv

# ============= REMINDER SCHEDULER =============
def send_admin_stats():
    """Har soatda admin'ga statistika yuborish"""
    print("📊 Admin stats scheduler ishga tushdi...")

    while True:
        try:
            if ADMIN_ID == 0:
                time.sleep(3600)
                continue

            users = load_users()

            total_users = len(users)

            message = (
                f"╔════════════════════════════════╗\n"
                f"║  👥 BOT - FOYDALANUVCHILAR      ║\n"
                f"╚════════════════════════════════╝\n\n"

                f"📊 UMUMIY STATISTIKA\n"
                f"├─ Jami foydalanuvchilar: {total_users} 👤\n"
                f"├─ Bugun aktiv: ~{int(total_users * 0.7)} 🟢\n"
                f"└─ Yangi: {int(total_users * 0.2)} ✨\n\n"

                f"👥 FOYDALANUVCHILAR RO'YXATI\n"
                f"─────────────────────────────────\n"
            )

            # Barcha foydalanuvchilar
            if total_users > 0:
                for idx, (user_id, user) in enumerate(users.items(), 1):
                    username = user.get("username", "Noma'lum")
                    first_name = user.get("first_name", "")
                    registered = user.get("registered", "")[:10]  # Faqat sana
                    language = user.get("language", "uz")

                    message += (
                        f"{idx}. @{username}\n"
                        f"   👤 {first_name}\n"
                        f"   📅 {registered}\n"
                        f"   🌐 {language}\n\n"
                    )

            message += (
                f"─────────────────────────────────\n"
                f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"⏱️ UTC+5 (Tashkent)\n\n"
                f"╔════════════════════════════════╗\n"
                f"║  ✨ Bot faol va ishga tayyor!  ║\n"
                f"╚════════════════════════════════╝"
            )

            try:
                bot.send_message(ADMIN_ID, message)
                print(f"✅ Admin stats: {total_users} users")
            except Exception as e:
                print(f"Admin'ga yuborish xatosi: {e}")

            # Har 1 soatda
            time.sleep(3600)
        except Exception as e:
            print(f"Admin stats xatosi: {e}")
            time.sleep(3600)


def reminder_scheduler(): import telebot


from telebot import types
import json
import os
from datetime import datetime
import threading
import time
from dotenv import load_dotenv
import random

# .env fayldan token oqish
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # .env'dan oqish

bot = telebot.TeleBot(BOT_TOKEN)
TASKS_FILE = "tasks.json"
USERS_FILE = "users.json"

# Qur'oniy oyatlar va motivatsiyalar
MOTIVATSIYALAR = [
    "💪 Alloh taoloning yordami bilan har bir qiyinchilikni yengib o'tish mumkin. Sabr qil, duolaringni unutma.",
    "✨ Kichik harakatlar ham Alloh yo'lida qilingan bo'lsa, ulkan savob keltiradi.",
    "🌅 Har tongni shukr bilan boshlash, qalbingni tinchlik va baraka bilan to'ldiradi.",
    "📚 Ilm o'rganish va amal qilish, dunyo va oxirat uchun eng katta boylikdir.",
    "🕋 Doim Allohni yod et, qalbingni tinchlik va baraka bilan to'ldir.",
    "✨ Haq yo'lda qilgan har bir amal, sening ruhi va qalbing uchun nur bo'ladi.",
    "🌟 Hayotingda kichik yaxshiliklar qil, Alloh uni ko'paytiradi.",
]

QURAN_OYATLAR = [
    {
        "verse": "Innal-insana lafi khusr",
        "sura": "Al-'Alaq, 96:2",
        "meaning": "Albatta inson ziyon ichidadir."
    },
    {
        "verse": "Fasabbih bismi rabbika al-azim",
        "sura": "Al-Mulk, 67:1",
        "meaning": "Allohning buyuk ism bilan zikr qil."
    },
    {
        "verse": "Wa aqimu s-salat",
        "sura": "Al-Baqara, 2:43",
        "meaning": "Namozni ado eting."
    },
    {
        "verse": "Wa aqimus-salata wa aatuz zakata",
        "sura": "Al-Baqara, 2:110",
        "meaning": "Namozni ado eting va zakot bering."
    },
    {
        "verse": "Inna allaha ma'as-sabirin",
        "sura": "Al-Baqara, 2:153",
        "meaning": "Albatta Alloh sabr qilganlar bilan birga."
    },
]

QAYTARIQ_OGOHLANTIRISHLAR = [
    "⚠️ Dunyo hayotiga berilib ketma, oxiratni unutma. Har bir amaling hisoblanadi.",
    "🚫 G'azab va nafsoniy vasvasalarga berilma, chunki Alloh har narsani ko'radi.",
    "📖 Va'z va eslatmalarni tinglashni unutma, Allohning rizosi faqat amalda namoyon bo'ladi.",
    "💭 Sabr qilmagan inson qiyinchilikda adashadi, ammo sabr qilgan Alloh yo'lida muvaffaqiyat topadi.",
    "🕌 Haram narsalardan uzoq turing, qalbingizni pok saqlang.",
    "🤲 Doimo Allohni yod eting, u sizga to'g'ri yo'l ko'rsatadi.",
    "☮️ Tinchlik va baraka faqat Allohga bo'ysunishda topiladi.",
]


# ============= JSON FUNKSIYALARI =============
def load_tasks():
    """Tasklarni o'qish"""
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        return {}
    except:
        return {}


def save_tasks(tasks):
    """Tasklarni saqlash"""
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Save tasks xatosi: {e}")


def load_users():
    """Foydalanuvchi ma'lumotlarini o'qish"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        return {}
    except:
        return {}


def save_users(users):
    """Foydalanuvchi ma'lumotlarini saqlash"""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Save users xatosi: {e}")


def register_user(message):
    """Foydalanuvchini ro'yxatga olish"""
    user_id = str(message.from_user.id)
    users = load_users()

    if user_id not in users:
        users[user_id] = {
            "id": message.from_user.id,
            "username": message.from_user.username or "Noma'lum",
            "first_name": message.from_user.first_name or "",
            "last_name": message.from_user.last_name or "",
            "full_name": f"{message.from_user.first_name} {message.from_user.last_name}".strip(),
            "registered": datetime.now().isoformat(),
            "language": message.from_user.language_code or "uz"
        }
        save_users(users)
        print(f"✅ Yangi user: {message.from_user.username}")


# ============= START =============
def show_main_menu(chat_id):
    """Asosiy menyuni ko'rsatish"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("➕ Task qo'sh", callback_data="add"),
        types.InlineKeyboardButton("📋 Tasklar", callback_data="list"),
        types.InlineKeyboardButton("💡 Motivation", callback_data="tip"),
        types.InlineKeyboardButton("🗑 O'chir", callback_data="delete")
    )

    bot.send_message(
        chat_id,
        "📱 **ASOSIY MENU**\n\n"
        "Quyidagi tugmalardan foydalaning:",
        reply_markup=markup
    )


@bot.message_handler(commands=['start'])
def start(message):
    """Botning boshlanishi"""
    register_user(message)

    bot.send_message(
        message.chat.id,
        "🎉 Salom! Men sizning Task & Reminder botiniz!\n\n"
    )

    show_main_menu(message.chat.id)


# ============= TASK TURINI TANLASH =============
@bot.callback_query_handler(func=lambda call: call.data == "add")
def add_task_handler(call):
    """Task qo'shish - Tur tanlash"""
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📌 Bir marta", callback_data="type_single"),
        types.InlineKeyboardButton("🔄 Har kuni", callback_data="type_daily")
    )
    markup.add(
        types.InlineKeyboardButton("🏆 Challenge", callback_data="type_challenge")
    )

    bot.send_message(
        call.message.chat.id,
        "📝 Qaysi turda task qo'shmoqchisiz?",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("type_"))
def task_type_handler(call):
    """Task turini tanlash"""
    task_type = call.data.split("_")[1]
    msg = bot.send_message(call.message.chat.id, "📝 Task nomini yozing:")
    bot.register_next_step_handler(msg, get_task_name, call.message.chat.id, task_type)


# ============= TASK NOMINI OLISH =============
def get_task_name(message, chat_id, task_type):
    """Task nomini olish"""
    task_name = message.text

    if task_type == "challenge":
        msg = bot.send_message(chat_id, "📖 Challenge nima haqida?\n(Masalan: 'Kitob o'qish')")
        bot.register_next_step_handler(msg, get_challenge_info, chat_id, task_name)
    else:
        msg = bot.send_message(
            chat_id,
            "⏰ Vaqtni kiriting:\n\n"
            "Formatlar:\n"
            "• HH:MM (09:30)\n"
            "• DD.MM HH:MM (25.11 09:30)\n"
            "• DD.MM.YYYY HH:MM (25.11.2025 09:30)"
        )
        bot.register_next_step_handler(msg, get_task_time, chat_id, task_name, task_type)


# ============= VAQTNI OLISH =============
def get_task_time(message, chat_id, task_name, task_type):
    """Vaqtni olish"""
    time_str = message.text.strip()

    valid_format = False
    try:
        datetime.strptime(time_str, "%H:%M")
        valid_format = True
    except:
        try:
            datetime.strptime(time_str, "%d.%m.%Y %H:%M")
            valid_format = True
        except:
            try:
                datetime.strptime(time_str, "%d.%m %H:%M")
                valid_format = True
            except:
                pass

    if not valid_format:
        msg = bot.send_message(
            chat_id,
            "❌ Noto'g'ri format!\n\n"
            "Qabul qilinadigan formatlar:\n"
            "• HH:MM (09:30)\n"
            "• DD.MM HH:MM (25.11 09:30)\n"
            "• DD.MM.YYYY HH:MM (25.11.2025 09:30)"
        )
        bot.register_next_step_handler(msg, get_task_time, chat_id, task_name, task_type)
        return

    tasks = load_tasks()
    user_id = str(chat_id)

    if user_id not in tasks:
        tasks[user_id] = []

    task = {
        "id": int(time.time() * 1000),
        "name": task_name,
        "time": time_str,
        "type": task_type,
        "done": False,
        "created": datetime.now().isoformat()
    }

    tasks[user_id].append(task)
    save_tasks(tasks)

    task_type_name = "Bir marta" if task_type == "single" else "Har kuni"
    bot.send_message(
        chat_id,
        f"✅ Saqlandi!\n\n"
        f"📌 {task_name}\n"
        f"🔄 Tur: {task_type_name}\n"
        f"⏰ {time_str} da reminder olasiz"
    )

    # Menu qayta ko'rsatish
    show_main_menu(chat_id)


# ============= CHALLENGE FUNCTIONS =============
def get_challenge_info(message, chat_id, task_name):
    """Challenge haqida ma'lumot"""
    challenge_info = message.text
    msg = bot.send_message(chat_id, "📅 Challenge qachondan boshlanadi?\n\nFormat: DD.MM.YYYY (25.11.2025)")
    bot.register_next_step_handler(msg, get_challenge_start, chat_id, task_name, challenge_info)


def get_challenge_start(message, chat_id, task_name, challenge_info):
    """Challenge boshlash sanasi"""
    start_date = message.text.strip()

    try:
        datetime.strptime(start_date, "%d.%m.%Y")
    except:
        msg = bot.send_message(chat_id, "❌ Noto'g'ri format! DD.MM.YYYY da yozing (25.11.2025)")
        bot.register_next_step_handler(msg, get_challenge_start, chat_id, task_name, challenge_info)
        return

    msg = bot.send_message(chat_id, "📅 Challenge qachongacha davom etadi?\n\nFormat: DD.MM.YYYY (30.11.2025)")
    bot.register_next_step_handler(msg, get_challenge_end, chat_id, task_name, challenge_info, start_date)


def get_challenge_end(message, chat_id, task_name, challenge_info, start_date):
    """Challenge tugash sanasi"""
    end_date = message.text.strip()

    try:
        datetime.strptime(end_date, "%d.%m.%Y")
    except:
        msg = bot.send_message(chat_id, "❌ Noto'g'ri format! DD.MM.YYYY da yozing (30.11.2025)")
        bot.register_next_step_handler(msg, get_challenge_end, chat_id, task_name, challenge_info, start_date)
        return

    msg = bot.send_message(chat_id, "⏰ Har kuni qaysi vaqtda eslatma olmoqchisiz?\n\nFormat: HH:MM (09:30)")
    bot.register_next_step_handler(msg, get_challenge_time, chat_id, task_name, challenge_info, start_date, end_date)


def get_challenge_time(message, chat_id, task_name, challenge_info, start_date, end_date):
    """Challenge vaqti"""
    time_str = message.text.strip()

    try:
        datetime.strptime(time_str, "%H:%M")
    except:
        msg = bot.send_message(chat_id, "❌ Noto'g'ri format! HH:MM da yozing (09:30)")
        bot.register_next_step_handler(msg, get_challenge_time, chat_id, task_name, challenge_info, start_date,
                                       end_date)
        return

    tasks = load_tasks()
    user_id = str(chat_id)

    if user_id not in tasks:
        tasks[user_id] = []

    task = {
        "id": int(time.time() * 1000),
        "name": task_name,
        "description": challenge_info,
        "start_date": start_date,
        "end_date": end_date,
        "time": time_str,
        "type": "challenge",
        "done": False,
        "created": datetime.now().isoformat()
    }

    tasks[user_id].append(task)
    save_tasks(tasks)

    bot.send_message(
        chat_id,
        f"🏆 Challenge saqlandi!\n\n"
        f"📌 {task_name}\n"
        f"📖 {challenge_info}\n"
        f"📅 {start_date} dan {end_date} gacha\n"
        f"⏰ Har kuni {time_str} da reminder"
    )

    # Menu qayta ko'rsatish
    show_main_menu(chat_id)


# ============= TASKLARNI KO'RSATISH =============
@bot.callback_query_handler(func=lambda call: call.data == "list")
def show_tasks(call):
    """Barcha tasklarni ko'rsatish"""
    user_id = str(call.message.chat.id)
    tasks = load_tasks()
    user_tasks = tasks.get(user_id, [])

    if not user_tasks:
        bot.send_message(call.message.chat.id, "📭 Hali task yo'q!")
        return

    text = "📋 BARCHA TASKLAR:\n\n"
    markup = types.InlineKeyboardMarkup()

    for task in user_tasks:
        try:
            done = task.get("done", False)
            task_name = task.get("name", "Noma'lum")
            task_id = task.get("id")
            task_time = task.get("time", "?")
            task_type = task.get("type", "single")

            type_icon = {"single": "📌", "daily": "🔄", "challenge": "🏆"}.get(task_type, "📌")
            status = "✅" if done else "⏳"
            text += f"{status} {type_icon} {task_name} - {task_time}\n"

            if task_id:
                markup.add(types.InlineKeyboardButton(
                    f"✓ {task_name[:20]}",
                    callback_data=f"done_{task_id}"
                ))
        except Exception as e:
            print(f"Task loop xatosi: {e}")
            continue

    bot.send_message(call.message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("done_"))
def complete_task(call):
    """Taskni tugatish"""
    try:
        task_id = int(call.data.split("_")[1])
        user_id = str(call.from_user.id)

        tasks = load_tasks()
        found = False

        if user_id in tasks:
            for task in tasks[user_id]:
                if task.get("id") == task_id:
                    task["done"] = True
                    found = True
                    break

        if found:
            save_tasks(tasks)
            bot.answer_callback_query(call.id, "✅ Tugallandi!")
            bot.edit_message_text(
                "✅ Bu task tugallandi!",
                call.message.chat.id,
                call.message.message_id
            )
        else:
            bot.answer_callback_query(call.id, "❌ Task topilmadi!", show_alert=True)
    except Exception as e:
        print(f"Complete task xatosi: {e}")
        bot.answer_callback_query(call.id, f"❌ Xato: {str(e)}", show_alert=True)


# ============= TASKNI O'CHIRISH =============
@bot.callback_query_handler(func=lambda call: call.data == "delete")
def delete_menu(call):
    """O'chirish menyusi"""
    user_id = str(call.message.chat.id)
    tasks = load_tasks()
    user_tasks = tasks.get(user_id, [])

    if not user_tasks:
        bot.send_message(call.message.chat.id, "📭 O'chirish uchun task yo'q!")
        return

    markup = types.InlineKeyboardMarkup()

    for task in user_tasks:
        task_name = task.get("name", "Noma'lum")
        markup.add(types.InlineKeyboardButton(
            f"🗑 {task_name[:20]}",
            callback_data=f"del_{task['id']}"
        ))

    bot.send_message(call.message.chat.id, "🗑 Qaysi taskni o'chirish kerak?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("del_"))
def confirm_delete(call):
    """Taskni o'chirish"""
    task_id = int(call.data.split("_")[1])
    user_id = str(call.message.chat.id)

    tasks = load_tasks()
    if user_id in tasks:
        tasks[user_id] = [t for t in tasks[user_id] if t.get("id") != task_id]

    save_tasks(tasks)
    bot.answer_callback_query(call.id, "🗑 O'chirildi!")


# ============= TAVSIYA =============
@bot.callback_query_handler(func=lambda call: call.data == "tip")
def send_tip(call):
    """Tavsiya yuborish"""
    import random

    motivatsiya = random.choice(MOTIVATSIYALAR)
    quran = random.choice(QURAN_OYATLAR)
    ogohlantirishlar = random.choice(QAYTARIQ_OGOHLANTIRISHLAR)

    message = (
        f"💡 **ISLOMIY TAVSIYALAR:**\n\n"
        f"─────────────────\n"
        f"{motivatsiya}\n\n"
        f"─────────────────\n"
        f"📖 {quran['verse']}\n"
        f"({quran['sura']})\n"
        f"✨ {quran['meaning']}\n\n"
        f"─────────────────\n"
        f"{ogohlantirishlar}"
    )

    bot.send_message(call.message.chat.id, message)


@bot.callback_query_handler(func=lambda call: call.data == "skip")
def skip_reminder(call):
    """Reminderni keyinroq"""
    try:
        bot.answer_callback_query(call.id, "🔕 Keyinroq ko'rsatildi")
        bot.edit_message_text(
            "⏭ Keyinroq qo'yildi!\n\n🔔 Ertaga qayta eslatma beriladi.",
            call.message.chat.id,
            call.message.message_id
        )
    except Exception as e:
        print(f"Skip xatosi: {e}")


# ============= ADMIN COMMANDS =============
@bot.message_handler(commands=['admin'])
def admin_command(message):
    """Admin panel"""
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Siz admin emasiz!")
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="admin_users"),
        types.InlineKeyboardButton("📊 Statistika", callback_data="admin_stats"),
        types.InlineKeyboardButton("📋 Barcha Tasks", callback_data="admin_all_tasks"),
        types.InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
        types.InlineKeyboardButton("🗑 User O'chirish", callback_data="admin_delete_user"),
        types.InlineKeyboardButton("📈 Analitika", callback_data="admin_analytics")
    )

    bot.send_message(
        message.chat.id,
        "╔════════════════════════════════╗\n"
        "║      👨‍💼 ADMIN PANEL            ║\n"
        "╚════════════════════════════════╝",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "admin_users")
def admin_users(call):
    """Foydalanuvchilar ro'yxati"""
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Admin emasiz!", show_alert=True)
        return

    users = load_users()

    message = "👥 **FOYDALANUVCHILAR RO'YXATI**\n\n"

    for idx, (user_id, user) in enumerate(users.items(), 1):
        username = user.get("username", "Noma'lum")
        first_name = user.get("first_name", "")
        registered = user.get("registered", "")[:10]

        message += f"{idx}. @{username}\n"
        message += f"   👤 {first_name}\n"
        message += f"   📅 {registered}\n"
        message += f"   🆔 {user_id}\n\n"

    message += f"\n**Jami: {len(users)} foydalanuvchi**"

    bot.send_message(call.message.chat.id, message)


@bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
def admin_stats(call):
    """Statistika"""
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Admin emasiz!", show_alert=True)
        return

    users = load_users()
    tasks = load_tasks()

    total_users = len(users)
    total_tasks = sum(len(t) for t in tasks.values())
    completed = sum(len([x for x in t if x.get("done")]) for t in tasks.values())
    pending = total_tasks - completed

    percent = int((completed / total_tasks * 100) if total_tasks > 0 else 0)

    message = (
        f"📊 **BOT STATISTIKASI**\n\n"
        f"👥 Foydalanuvchilar: {total_users}\n"
        f"📋 Jami tasks: {total_tasks}\n"
        f"✅ Tugallangan: {completed}\n"
        f"⏳ Qolgan: {pending}\n"
        f"📈 Foiz: {percent}%\n\n"
        f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    bot.send_message(call.message.chat.id, message)


@bot.callback_query_handler(func=lambda call: call.data == "admin_all_tasks")
def admin_all_tasks(call):
    """Barcha tasklar"""
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Admin emasiz!", show_alert=True)
        return

    users = load_users()
    tasks = load_tasks()

    message = "📋 **BARCHA TASKS**\n\n"

    for user_id, user_tasks in tasks.items():
        user = users.get(user_id, {})
        username = user.get("username", "Noma'lum")
        message += f"@{username}:\n"

        for task in user_tasks:
            task_name = task.get("name", "Noma'lum")[:20]
            task_type = task.get("type", "single")
            done_status = "✅" if task.get("done") else "⏳"

            type_icon = {"single": "📌", "daily": "🔄", "challenge": "🏆"}.get(task_type, "📌")
            message += f"  {done_status} {type_icon} {task_name}\n"

        message += "\n"

    bot.send_message(call.message.chat.id, message)


@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast")
def admin_broadcast(call):
    """Broadcast qilish"""
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Admin emasiz!", show_alert=True)
        return

    msg = bot.send_message(call.message.chat.id, "📢 Xabar yozing (barcha userga yuboriladi):")
    bot.register_next_step_handler(msg, send_broadcast)


def send_broadcast(message):
    """Broadcast xabar yuborish"""
    if message.from_user.id != ADMIN_ID:
        return

    broadcast_text = message.text
    users = load_users()

    sent = 0
    failed = 0

    for user_id in users.keys():
        try:
            bot.send_message(
                int(user_id),
                f"📢 **ADMIN XABARI:**\n\n{broadcast_text}"
            )
            sent += 1
        except:
            failed += 1

    bot.send_message(
        message.chat.id,
        f"✅ Broadcast yuborildi!\n\n"
        f"✅ Yuborildi: {sent}\n"
        f"❌ Xatosi: {failed}"
    )


@bot.callback_query_handler(func=lambda call: call.data == "admin_delete_user")
def admin_delete_user(call):
    """User o'chirish"""
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Admin emasiz!", show_alert=True)
        return

    msg = bot.send_message(call.message.chat.id, "🆔 O'chirilishi kerak bo'lgan user ID'ni yozing:")
    bot.register_next_step_handler(msg, delete_user_by_id)


def delete_user_by_id(message):
    """User ID bo'yicha o'chirish"""
    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = str(message.text.strip())
        users = load_users()
        tasks = load_tasks()

        if user_id in users:
            del users[user_id]
            if user_id in tasks:
                del tasks[user_id]

            save_users(users)
            save_tasks(tasks)

            bot.send_message(message.chat.id, f"✅ User {user_id} o'chirildi!")
        else:
            bot.send_message(message.chat.id, f"❌ User {user_id} topilmadi!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xato: {e}")


@bot.callback_query_handler(func=lambda call: call.data == "admin_analytics")
def admin_analytics(call):
    """Analitika"""
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Admin emasiz!", show_alert=True)
        return

    users = load_users()
    tasks = load_tasks()

    single = sum(len([x for x in t if x.get("type") == "single"]) for t in tasks.values())
    daily = sum(len([x for x in t if x.get("type") == "daily"]) for t in tasks.values())
    challenge = sum(len([x for x in t if x.get("type") == "challenge"]) for t in tasks.values())

    message = (
        f"📈 **ANALITIKA**\n\n"
        f"🎯 Task Turlari:\n"
        f"📌 Bir marta: {single}\n"
        f"🔄 Har kuni: {daily}\n"
        f"🏆 Challenge: {challenge}\n\n"
        f"📊 Umumiy: {single + daily + challenge} task\n\n"
        f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    bot.send_message(call.message.chat.id, message)

    # ============= REMINDER SCHEDULER =============
    """Vaqtda reminder yuborish"""
    print("🚀 Scheduler ishga tushdi...")
    last_sent = {}

    while True:
        try:
            now = datetime.now()
            current_datetime = now.strftime("%d.%m.%Y %H:%M")
            current_time = now.strftime("%H:%M")

            tasks = load_tasks()

            if not tasks:
                time.sleep(1)
                continue

            for user_id, user_tasks in tasks.items():
                if not isinstance(user_tasks, list):
                    continue

                for task in user_tasks:
                    if "time" not in task or "name" not in task:
                        continue

                    task_time = task.get("time", "")
                    task_name = task.get("name", "Task")
                    task_type = task.get("type", "single")
                    reminder_key = f"{user_id}_{task['id']}"

                    # Challenge uchun tekshirish
                    if task_type == "challenge":
                        start = task.get("start_date", "")
                        end = task.get("end_date", "")

                        try:
                            start_dt = datetime.strptime(start, "%d.%m.%Y")
                            end_dt = datetime.strptime(end, "%d.%m.%Y")

                            if not (start_dt.date() <= now.date() <= end_dt.date()):
                                continue
                        except:
                            continue

                    time_match = False

                    if len(task_time) == 16:
                        time_match = (task_time == current_datetime)
                    elif len(task_time) == 5:
                        time_match = (task_time == current_time)
                    elif len(task_time) == 11:
                        current_short = now.strftime("%d.%m %H:%M")
                        time_match = (task_time == current_short)

                    if time_match and not task.get("done", False):
                        last_time = last_sent.get(reminder_key)

                        if last_time is None or (now.timestamp() - last_time) > 3600:
                            import random

                            motivatsiya = random.choice(MOTIVATSIYALAR)
                            quran = random.choice(QURAN_OYATLAR)
                            ogohlantirishlar = random.choice(QAYTARIQ_OGOHLANTIRISHLAR)

                            message = (
                                f"🔔 REMINDER!\n\n"
                                f"📌 {task_name}\n"
                                f"⏰ {task_time}\n\n"
                                f"─────────────────\n"
                                f"{motivatsiya}\n\n"
                                f"─────────────────\n"
                                f"📖 {quran['verse']}\n"
                                f"({quran['sura']})\n"
                                f"✨ {quran['meaning']}\n\n"
                                f"─────────────────\n"
                                f"{ogohlantirishlar}"
                            )

                            try:
                                markup = types.InlineKeyboardMarkup()
                                markup.add(
                                    types.InlineKeyboardButton("✅ Tugalladi", callback_data=f"done_{task['id']}"),
                                    types.InlineKeyboardButton("🔕 Keyinroq", callback_data="skip")
                                )

                                bot.send_message(int(user_id), message, reply_markup=markup)
                                last_sent[reminder_key] = now.timestamp()
                                print(f"✅ Reminder: {task_name} - {task_time}")
                            except Exception as e:
                                print(f"Xato: {e}")

            time.sleep(1)
        except Exception as e:
            print(f"Scheduler xatosi: {e}")
            time.sleep(5)


# ============= MAIN =============
if __name__ == "__main__":
    print("🤖 Bot ishga tushdi!")
    print("=" * 50)

    # Admin stats thread
    admin_thread = threading.Thread(target=send_admin_stats, daemon=True)
    admin_thread.start()

    # Scheduler thread
    scheduler_thread = threading.Thread(target=reminder_scheduler, daemon=True)
    scheduler_thread.start()

    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except KeyboardInterrupt:
        print("\n✅ Bot to'xtadi!")
    except Exception as e:
        print(f"Bot xatosi: {e}")