import re
import telebot
from telebot.types import InlineKeyboardButton as b, InlineKeyboardMarkup as mk
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import upload_file
import os
db = Client("stupid.gay")

if not db.exists('banlist'):
    db.set('banlist', [])

if not db.exists('status'):
    db.set('status', {'e': '❌', 's': False})

if not db.exists('force'):
    db.set('force', [])

logs = ['creator', 'member', 'administrator']


def force(user_id, channel):
    b = bot.get_chat_member(chat_id='@' + str(channel), user_id=user_id)
    if str(b.status) in logs:
        return True
    else:
        return False

teletips=Client(
    "MediaToTelegraphLink",
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
    bot_token = os.environ["BOT_TOKEN"]
)


admins = [5089553588, 1558668590]  # admins

bot = telebot.TeleBot(bot_token, num_threads=29, skip_pending=True)


@bot.message_handler(commands=["start"])
def startm(message):
    if not db.get(f"user_{message.from_user.id}"):
        d = {"id": message.from_user.id, "users": []}
        db.set(f"user_{message.from_user.id}", d)
        pass
    user_id = message.from_user.id
    if user_id in admins:
        keyss = mk(row_width=2)
        d = db.get('status')
        t = 'معطل ❌' if not d['s'] else 'مفعل ✅'
        btn, btn1, btn2, btn3, btn4, btn5, btn6 = b('الاحصائيات', callback_data='stats'), \
                                                 b('اذاعة', callback_data='brod'), \
                                                 b('حظر شخص', callback_data='ban'), \
                                                 b('فك حظر ', callback_data='unban'), \
                                                 b('تعيين قنوات اشتراك', callback_data='sub'), \
                                                 b('قائمة المحظورين ..', callback_data='listofban'), \
                                                 b(f'اشعار لدخول: {t}', callback_data='dis')
        keyss.add(btn)
        keyss.add(btn1, btn4)
        keyss.add(btn3, btn2)
        keyss.add(btn5)
        keyss.add(btn6)
        bot.reply_to(message, text='اهلا بك عزيزي الادمن ..', reply_markup=keyss)
    if user_id in db.get('banlist'):
        return
    chs = db.get('force')
    if chs != None:
        for i in chs:
            try:
                s = force(user_id=user_id, channel=i)
            except:
                s = True

            if not s:
                bot.reply_to(message, f'عذرا يجب عليك الاشتراك بقناة البوت:\n- @{i} .\nاشترك وأرسل [/start] ..')
                return
    bot.reply_to(message, f"هلو")





@bot.message_handler(content_types=["text"])
def getlink(message):
    url = message.text
    user_id = message.from_user.id
    if user_id in db.get('banlist'):
        return
    chs = db.get('force')
    if chs != None:
        for i in chs:
            try:
                s = force(user_id=user_id, channel=i)
            except:
                s = True

            if not s:
                bot.reply_to(message, f'عذرا يجب عليك الاشتراك بقناة البوت:\n- @{i} .\nاشترك وأرسل [/start] ..')
                return
@bot.callback_query_handler(func=lambda m: True)
def query(call):
    data, cid, mid = call.data, call.from_user.id, call.message.id
    if cid in db.get('banlist'):
        return

    if data == 'dis':
        d = db.get('status')
        if d['s'] == False:
            db.set('status', {'e': '✅', 's': True})
        else:
            db.set('status', {'e': '❌', 's': False})
        d = db.get('status')
        z = 'معطل ❌' if not d['s'] else 'مفعل ✅'
        bot.edit_message_text(f'حالة الإشعارات: {z}', chat_id=cid, message_id=mid)
        return

    if data == 'listofban':
        d = db.get('banlist')
        if not d or len(d) < 1:
            bot.edit_message_text(text='مافي محظورين ياحب .', chat_id=cid, message_id=mid)
            return
        k = ''
        for i, x in enumerate(d, 1):
            k += f'{i}. {x}'
        bot.edit_message_text(text=f'المحظورين:\n{k}\nعددهم: {len(d)} .', chat_id=cid, message_id=mid)

    if data == 'ban':
        x = bot.edit_message_text(text='ارسل ايدي العضو الورع الي تريد تحظره ..', chat_id=cid, message_id=mid)
        bot.register_next_step_handler(x, banone)

    if data == 'unban':
        x = bot.edit_message_text(text='ارسل ايدي العضو الورع الي تريد تفك حظره ..', chat_id=cid, message_id=mid)
        bot.register_next_step_handler(x, unbanone)

    if data == 'sub':
        ss = "\n".join(db.get('force'))
        x = bot.edit_message_text(text=f'ارسل قنوات الاشتراك الاجباري بهاي الطريقة:\n@first @second @third ..\n\nالقنوات الحالية:\n{ss}', chat_id=cid, message_id=mid)
        bot.register_next_step_handler(x, set_s)

    if data == 'brod':
        x = bot.edit_message_text(text='ارسل الرسالة التي تريد إرسالها للأعضاء.. ', message_id=mid, chat_id=cid)
        bot.register_next_step_handler(x, brod_pro)

    if data == 'stats':
        c = 0
        h = 0
        users = db.keys('user_%')
        bot.answer_callback_query(call.id, 'جارٍ العد ..', cache_time=10, show_alert=True)
        for user in users:
            try:
                d = db.get(user[0])["id"]
                c += 1
            except:
                continue
        bot.edit_message_text(text=f"عدد الأعضاء: {c}", chat_id=cid, message_id=mid)
        return


def banone(message):
    user_id = message.text
    try:
        id = int(user_id)
    except:
        return
    d = db.get('banlist')
    if d != None and id in d:
        bot.reply_to(message, 'العضو محظور بالفعل!!')
        return
    else:
        d.append(id)
        db.set('banlist', d)
        bot.reply_to(message, 'تمت إضافته للمحظورين..')
        try:
            bot.send_message(chat_id=id, text='تم حظرك حبيبي.')
        except:
            pass


def unbanone(message):
    user_id = message.text
    try:
        id = int(user_id)
    except:
        return
    d = db.get('banlist')
    if d != None and id not in d:
        bot.reply_to(message, 'العضو غير محظور!!')
        return
    else:
        d.remove(id)
        db.set('banlist', d)
        bot.reply_to(message, 'تم رفع الحظر عنه..')
        try:
            bot.send_message(chat_id=id, text='تم رفع حظرك.')
        except:
            pass
def brod_pro(message):
    users = db.keys('user_%')
    mid = message.message_id
    dones = 0
    for user in users:
        try:
            user = db.get(user[0])
            id = user['id']
            bot.copy_message(id, message.chat.id, mid)
            dones += 1
        except:
            continue
    bot.reply_to(message, f'تم بنجاح الارسال لـ{dones}')
    return


def set_s(message):
    channels = message.text.replace('@', '').replace('https://t.me', '').split(' ')
    db.set('force', channels)
    t = '\n'.join(channels)
    bot.reply_to(message, f'تم تعيين القنوات:\n{t} ')
    return  

@teletips.on_message(filters.command('start') & filters.private)
async def start(client, message):
    text = f"""
اهلا {message.from_user.mention},
🔮أنا هنا لإنشاء روابط التلجراف لملفات الوسائط الخاصة بك.

👨🏼‍💻ما عليك سوى إرسال ملف وسائط صالح مباشرة إلى هذه الدردشة.
♻️انواع الملفات الصالحه هي:- 'jpeg', 'jpg', 'png', 'mp4' and 'gif'.

🌐لأنشاء الروابط في **المجموعات**,اضفني لمجموعه خارقه اي عامه وارسل الامر <code>/tl</code> ردا علي ملف وسائط صالح.
🖥 | [عالم البرمجه🌀](https://t.me/botatiiii)

☣️ | [˛َِ ٰꫝٰꪑٰ᥉ ᝰ](https://t.me/hms_01)
            """
    await teletips.send_message(message.chat.id, text, disable_web_page_preview=True)
    

@teletips.on_message(filters.media & filters.private)
async def get_link_private(client, message):
    try:
        text = await message.reply("🔮انتظر قليلا...")
        async def progress(current, total):
            await text.edit_text(f"📥 جاري التنزيل... {current * 100 / total:.1f}%")
        try:
            location = f"./media/private/"
            local_path = await message.download(location, progress=progress)
            await text.edit_text("📤 جاري الرفع الي التليجراف...")
            upload_path = upload_file(local_path) 
            await text.edit_text(f"🌐 | رابط التليجراف:\n\n<code>https://telegra.ph{upload_path[0]}</code>")     
            os.remove(local_path) 
        except Exception as e:
            await text.edit_text(f"❌ | فشل رفع الملف\n\n<i>Reason: {e}</i>")
            os.remove(local_path) 
            return                 
    except Exception:
        pass        

@teletips.on_message(filters.command('tl'))
async def get_link_group(client, message):
    try:
        text = await message.reply("🔮انتظر قليلا...")
        async def progress(current, total):
            await text.edit_text(f"📥 جاري التنزيل... {current * 100 / total:.1f}%")
        try:
            location = f"./media/group/"
            local_path = await message.reply_to_message.download(location, progress=progress)
            await text.edit_text("📤 جاري الرفع الي التليجراف...")
            upload_path = upload_file(local_path) 
            await text.edit_text(f"🌐 | رابط التليجراف:\n\n<code>https://telegra.ph{upload_path[0]}</code>")     
            os.remove(local_path) 
        except Exception as e:
            await text.edit_text(f"❌ | فشل رفع الملف\n\n<i>Reason: {e}</i>")
            os.remove(local_path) 
            return         
    except Exception:
        pass                                           

print("البوت شغال!")
teletips.run()
bot.infinity_polling()    