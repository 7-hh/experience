from telebot import TeleBot
from telebot.types import (
    InlineKeyboardMarkup as Markup,
    InlineKeyboardButton as Button
)
from telebot import apihelper
from datetime import datetime
from json import load, dump
from time import sleep
import sqlite3
import logging
import os
import sys


bot_token = '8455552552:AAGjCX3oPEpaYJu6OieznMTYbPiMUdOlp5Y' # YOUR BOT TOKEN
ben = TeleBot(bot_token)

MAIN_OWNER = 8091096330 # YOUR ID - ضع ايدي التلجرام الخاص بك هنا
owners_ids = [] # OWNERS IDs
channel = '@RPRNN' # YOUR CHANNEL
OWNER_USERNAME = '@J2J_2' # المالك
CHANNEL_USERNAME = '@RPRNN' # القناة
owners_ids.insert(0, MAIN_OWNER)
users_db = './users'
settings_db = './settings'
admins_db = './admins'
logs_db = './logs'

# إعداد نظام التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

ADMINS_MARKUP = Markup([
    [
        Button('📊 الاحصائيات', callback_data = 'statics'),
        Button('📈 احصائيات متقدمة', callback_data = 'advanced_stats')
    ],
    [
        Button('👤 اضافة مستخدم', callback_data = 'adduser'),
        Button('🗑️ حذف مستخدم', callback_data = 'popuser')
    ],
    [
        Button('⚙️ الوضع الحالي : {}', callback_data = 'changemode')
    ],
    [
        Button('👥 الادمنيه', callback_data = 'get_admins')
    ],
    [
        Button('➕ اضافة ادمن', callback_data = 'add_admin'),
        Button('➖ حذف ادمن', callback_data = 'pop_admin')
    ],
    [
        Button('📢 اذاعه', callback_data = 'broadcast')
    ],
    [
        Button('🔗 الاشتراك الاجباري', callback_data = 'force_sub')
    ],
    [
        Button('👥 اظهار لوحة الاعضاء', callback_data = 'users')
    ],
    [
        Button('📋 سجل العمليات', callback_data = 'view_logs'),
        Button('🔄 نسخ احتياطي', callback_data = 'backup_data')
    ],
    [
        Button('🛡️ إعدادات الأمان', callback_data = 'security_settings')
    ]
])


TO_ADMINS_MARKUP = Markup([
    [
        Button('- رجوع -', callback_data = 'admins')
    ]
])


CITIES_MARKUP = Markup([
    [
        Button('🏛️ مثنى', callback_data = 'ct_muthana'),
        Button('🕌 نجف', callback_data = 'ct_najaf'),
        Button('🏛️ نينوى', callback_data = 'ct_nineveh')
    ],
    [
        Button('🌾 ديالى', callback_data = 'ct_diyala'),
        Button('🏔️ دهوك', callback_data = 'ct_duhok'),
        Button('🏔️ اربيل', callback_data = 'ct_erbil')
    ],
    [
        Button('🕌 كربلاء', callback_data = 'ct_karbalaa'),
        Button('🛢️ كركوك', callback_data = 'ct_kirkuk'),
        Button('🏛️ قادسية', callback_data = 'ct_qadisiya')
    ],
    [
        Button('🏛️ صلاح الدين', callback_data = 'ct_salahaldeen'),
        Button('🏔️ سليمانية', callback_data = 'ct_sulaymaniyah'),
        Button('🏛️ واسط', callback_data = 'ct_wasit')
    ],
    [
        Button('🏛️ بابل', callback_data = 'ct_babylon'),
        Button('🏛️ بغداد', callback_data = 'ct_baghdad'),
        Button('🏛️ بلد', callback_data = 'ct_balad')
    ],
    [
        Button('🌊 بصرة', callback_data = 'ct_basrah'),
        Button('🏛️ ذي قار', callback_data = 'ct_dhiqar'),
        Button('🏜️ الانبار', callback_data = 'ct_alanbar')
    ],
    [
        Button('🏛️ ميسان', callback_data = 'ct_mesan')
    ],
    [
        Button('📱 البحث عن الرقم', callback_data='sh_phone')
    ]
])


TO_USERS_MARKUP = Markup([
    [
        Button('- رجوع -', callback_data = 'users')
    ]
])


CITIES ={
	'mesan': 'ميسان',
	'muthana': 'مثنى',
	'najaf': 'نجف',
	'nineveh': 'نينوى',
	'diyala': 'ديالى',
	'duhok': 'دهوك',
	'erbil': 'اربيل',
	'karbalaa': 'كربلاء',
	'kirkuk': 'كركوك',
	'qadisiya': 'قادسية',
	'salahaldeen': 'صلاح الدين',
	'sulaymaniyah': 'سليمانية',
	'wasit': 'واسط',
	'babylon': 'بابل',
	'baghdad': 'بغداد',
	'balad': 'بلد',
	'basrah': 'بصرة',
	'dhiqar': 'ذي قار',
	'alanbar': 'الانبار',
}

@ben.message_handler(
    commands = ['start'],
    chat_types = ['private'],
)
def owners_start(message):
    user_id = message.from_user.id
    log_activity(user_id, "بدء استخدام البوت")
    
    if user_id in owners_ids + admins:
        mode = 'مدفوع' if settings['mode'] == 'private' else 'مجاني'
        markup = ADMINS_MARKUP
        markup.keyboard[2][0].text = '⚙️ الوضع الحالي : {}'.format(mode)
        ben.reply_to(
            message,
            f'🎉 مرحباً بك عزيزي المالك\n\nيمكنك التحكم بالبوت من خلال الأزرار التالية:\n\n👤 المطور: {OWNER_USERNAME}\n📢 القناة: {CHANNEL_USERNAME}',
            reply_markup = markup
        )
    else:
        # جعل البوت متاحاً لجميع المستخدمين
        if users.get(str(user_id)) is None:
            users[str(user_id)] = True  # تفعيل المستخدم تلقائياً
            write(users_db, users)
            ben.send_message(
                MAIN_OWNER,
                f'🔥 دخل شخص جديد الى البوت\n\n👤 ايديه: {user_id}\n📝 معرفه: @{message.from_user.username if message.from_user.username else "لا يوجد"}\n👥 عدد المستخدمين الكلي: {len(users)}\n\n👤 المطور: {OWNER_USERNAME}\n📢 القناة: {CHANNEL_USERNAME}'
            )
        
        ben.reply_to(
            message,
            f'🎉 مرحباً بك في بوت بيانات العراق\n\nيمكنك البحث من خلال الأزرار التالية:\n\n👤 المطور: {OWNER_USERNAME}\n📢 القناة: {CHANNEL_USERNAME}',
            reply_markup = CITIES_MARKUP
        )    


@ben.callback_query_handler(
    func = lambda call: call.data in ['adduser', 'popuser', 'add_admin', 'pop_admin', 'advanced_stats', 'view_logs', 'backup_data', 'security_settings']
)
def add_pop_user(callback):
    user_id = callback.from_user.id
    if user_id not in owners_ids:
        if user_id not in admins: return ben.edit_message_text(
            message_id = callback.message.id,
            chat_id = user_id,
            text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات'
        )
        else:
            if callback.data in ['add_admin', 'pop_admin']:
                return ben.answer_callback_query(
                    callback.id, '- لا يمكنك استخدام هذه الميزهّ!' , show_alert = True
                )
    
    # معالجة الأحداث الجديدة
    if callback.data == 'advanced_stats':
        stats = get_advanced_stats()
        if stats:
            text = f"""📈 الإحصائيات المتقدمة

👥 المستخدمين:
• إجمالي المستخدمين: {stats['total_users']}
• المستخدمين المميزين: {stats['vip_users']}
• المستخدمين العاديين: {stats['normal_users']}

👨‍💼 الإدارة:
• عدد الأدمنية: {stats['total_admins']}
• أنشطة اليوم: {stats['today_activities']}

⚙️ إعدادات البوت:
• وضع البوت: {'مدفوع' if stats['bot_mode'] == 'private' else 'مجاني'}

📊 المطور: {OWNER_USERNAME}
📢 القناة: {CHANNEL_USERNAME}"""
            
            ben.edit_message_text(
                message_id = callback.message.id,
                chat_id = user_id,
                text = text,
                reply_markup = TO_ADMINS_MARKUP
            )
            log_activity(user_id, "عرض الإحصائيات المتقدمة")
        return
    
    elif callback.data == 'view_logs':
        logs = read(logs_db) if os.path.exists(logs_db) else []
        recent_logs = logs[-10:] if len(logs) > 10 else logs
        
        if not recent_logs:
            text = "📋 سجل العمليات\n\nلا توجد عمليات مسجلة حالياً"
        else:
            text = "📋 آخر 10 عمليات:\n\n"
            for log in recent_logs:
                text += f"🕐 {log['timestamp']}\n👤 المستخدم: {log['user_id']}\n📝 العملية: {log['action']}\n\n"
        
        ben.edit_message_text(
            message_id = callback.message.id,
            chat_id = user_id,
            text = text,
            reply_markup = TO_ADMINS_MARKUP
        )
        log_activity(user_id, "عرض سجل العمليات")
        return
    
    elif callback.data == 'backup_data':
        if backup_data():
            ben.answer_callback_query(
                callback.id, "✅ تم إنشاء النسخة الاحتياطية بنجاح!", show_alert = True
            )
            log_activity(user_id, "إنشاء نسخة احتياطية")
        else:
            ben.answer_callback_query(
                callback.id, "❌ فشل في إنشاء النسخة الاحتياطية!", show_alert = True
            )
        return
    
    elif callback.data == 'security_settings':
        text = f"""🛡️ إعدادات الأمان

🔐 المعلومات الحالية:
• المالك: {OWNER_USERNAME}
• القناة: {CHANNEL_USERNAME}
• وضع البوت: {'مدفوع' if settings.get('mode') == 'private' else 'مجاني'}

⚙️ الخيارات المتاحة:
• تغيير وضع البوت
• إدارة الأدمنية
• إعدادات الاشتراك الإجباري"""
        
        markup = Markup([
            [Button('🔄 تغيير الوضع', callback_data = 'changemode')],
            [Button('👥 إدارة الأدمنية', callback_data = 'get_admins')],
            [Button('🔗 إعدادات الاشتراك', callback_data = 'force_sub')],
            [Button('🔙 رجوع', callback_data = 'admins')]
        ])
        
        ben.edit_message_text(
            message_id = callback.message.id,
            chat_id = user_id,
            text = text,
            reply_markup = markup
        )
        log_activity(user_id, "عرض إعدادات الأمان")
        return
    
    # المعالجة الأصلية للأحداث الأخرى
    settings['get_id'][str(user_id)] = callback.data
    write(settings_db, settings)
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = user_id,
        text = '- حسنا عزيزي قم بارسال ايدي المستخدم!',
        reply_markup = TO_ADMINS_MARKUP
    )


@ben.callback_query_handler(
    func = lambda call: call.data == 'changemode'
)
def change_mode(callback):
    user_id = callback.from_user.id
    if user_id not in owners_ids + admins:return ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = user_id,
        text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات'
    )
    settings['mode'] = 'public' if settings['mode'] == 'private' else 'private'
    write(settings_db, settings)
    mode = 'مدفوع' if settings['mode'] == 'private' else 'مجاني'
    ben.answer_callback_query(callback.id, f'- تم تغيير الوضع الى {mode}')
    markup = ADMINS_MARKUP
    markup.keyboard[2][0].text = '- الوضع الحالي : {} -'.format(mode)
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = user_id,
        text = '- مرحبا بك عزيزي المالك يمكنك التحكم بالبوت من خلال الازرار التاليه :',
        reply_markup = markup
    )


@ben.callback_query_handler(
    func = lambda call: call.data == 'admins'
)
def to_admins(callback):
    user_id = callback.from_user.id
    for setting in settings:
        if setting in ['mode', 'channel']: continue
        elif setting in ['get_num', 'get_broadcast', 'get_channel']:
            if user_id in settings[setting]: settings[setting].remove(user_id)
        elif settings[setting].get(str(user_id)): del settings[setting][str(user_id)]
    if user_id not in owners_ids + admins:return ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = user_id,
        text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات'
    )
    mode = 'مدفوع' if settings['mode'] == 'private' else 'مجاني'
    markup = ADMINS_MARKUP
    markup.keyboard[2][0].text = '- الوضع الحالي : {} -'.format(mode)
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = user_id,
        text = '- مرحبا بك عزيزي المالك يمكنك التحكم بالبوت من خلال الازرار التاليه :',
        reply_markup = markup
    )


@ben.message_handler(
    content_types = ['text'],
    chat_types = ['private'],
    func = lambda msg: settings['get_id'].get(str(msg.from_user.id))
)
def get_id(message):
    data = settings['get_id'][str(message.from_user.id)]
    if data == 'adduser':
        if users.get(message.text):
            ben.reply_to(message, '- العضو موجود بالبوت من قبل!', reply_markup = TO_ADMINS_MARKUP)
        else:
            users[message.text] = True
            write(users_db, users)
            ben.reply_to(message, '- تم اضافة العضو للبوت بنجاح!', reply_markup = TO_ADMINS_MARKUP)
    elif data == 'popuser':
        if users.get(message.text) is None:
            ben.reply_to(message, '- العضو غير موجود بالبوت ليتم حذفه!', reply_markup = TO_ADMINS_MARKUP)
        else:
            users[message.text] = False
            write(users_db, users)
            ben.reply_to(message, '- تم حذف العضو من البوت!', reply_markup = TO_ADMINS_MARKUP)
    elif data == 'add_admin':
        if not message.text.isnumeric():
            ben.reply_to(message, '- الايدي غير صالح!', reply_markup = TO_ADMINS_MARKUP)
        elif int(message.text) in admins:
            ben.reply_to(message, '- الادمن موجود بالبوت من قبل!', reply_markup = TO_ADMINS_MARKUP)
        else:
            try: ben.get_chat(int(message.text))
            except:
                ben.reply_to(message ,'- لم يتم ايجاد هذا المستخدم!', reply_markup = TO_ADMINS_MARKUP)
                del settings['get_id'][str(message.from_user.id)]
                write(settings_db, settings)
                return
            admins.append(int(message.text))
            write(admins_db, admins)
            ben.reply_to(message, '- تم اضافة المستخدم لقائمة الادمنيه!', reply_markup = TO_ADMINS_MARKUP)
    elif data == 'pop_admin':
        if not message.text.isnumeric():
            ben.reply_to(message, '- الايدي غير صالح!', reply_markup = TO_ADMINS_MARKUP)
        elif int(message.text) not in admins:
            ben.reply_to(message, '- المستخدم ليس من ادمنية البوت!', reply_markup = TO_ADMINS_MARKUP)
        else:
            try: ben.get_chat(int(message.text))
            except:
                ben.reply_to(message ,'- لم يتم ايجاد هذا المستخدم!', reply_markup = TO_ADMINS_MARKUP)
                del settings['get_id'][str(message.from_user.id)]
                write(settings_db, settings)
                return
            admins.remove(int(message.text))
            write(admins_db, admins)
            ben.reply_to(message, '- تم حذف المستخدم من قائمة الادمنيه', reply_markup = TO_ADMINS_MARKUP)
    del settings['get_id'][str(message.from_user.id)]
    write(settings_db, settings)


@ben.callback_query_handler(
    func = lambda callback: callback.data == 'statics' and callback.from_user.id in (owners_ids + admins)
)
def statics(callback):
    ben.answer_callback_query(callback.id ,'- جاري الحصول على البيانات... -', show_alert = True)
    caption = '- حسنا عزيزي اليك احصائيات البوت!\n\n'
    vips = 0
    norm = 0
    for user in users:
        if users[user]: vips += 1
        else: norm += 1
    caption += '- عدد المستخدمين الكلي: %s\n' % len(users)
    caption += '- عدد المستخدمين المشتركين بالبوت: %s\n' % vips
    caption += '- عدد المستخدمين غير المشتركين بالبوت: %s\n' % norm
    ben.edit_message_text(
        chat_id = callback.from_user.id,
        message_id = callback.message.id,
        text = caption,
        reply_markup = TO_ADMINS_MARKUP
    )


@ben.callback_query_handler(
    func = lambda callback: callback.data == 'get_admins' and callback.from_user.id in (owners_ids + admins)
)
def get_admins(callback):
    ben.answer_callback_query(callback.id ,'- جاري الحصول على البيانات... -', show_alert = True)
    caption = '- حسنا عزيزي اليك ادمنية البوت!\n\n'
    for admin in admins:
        user = ben.get_chat(admin)
        caption += '- [%s](https://t.me/%s)\n' % (user.first_name, user.username)
    ben.edit_message_text(
        chat_id = callback.from_user.id,
        message_id = callback.message.id,
        text = caption,
        reply_markup = TO_ADMINS_MARKUP,
        disable_web_page_preview = True,
        parse_mode = 'MARKDOWN'
    )


@ben.callback_query_handler(
    func = lambda callback: callback.data == 'broadcast' and callback.from_user.id in (owners_ids + admins)
)
def broadcast(callback):
    user_id = callback.from_user.id
    if user_id not in owners_ids:
        if user_id not in admins: return ben.edit_message_text(
            message_id = callback.message.id,
            chat_id = user_id,
            text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات'
        )
        else:
            return ben.answer_callback_query(
                callback.id, '- لا يمكنك استخدام هذه الميزهّ!' , show_alert = True
            )
    settings['get_broadcast'].append(user_id)
    write(settings_db, settings)
    ben.edit_message_text(
        chat_id = user_id,
        message_id = callback. message.id,
        text = '- حسنا عزيزي قم بارسال رسالة الاذاعه الان.',
        reply_markup = TO_ADMINS_MARKUP
    )


@ben.message_handler(
    chat_types = ['private'],
    content_types = ['photo', 'text','audio', 'voice', 'video', 'sticker', 'document'],
    func = lambda message: message.from_user.id in settings['get_broadcast']
)
def get_broadcast(message):
    user_id = message.from_user.id
    settings['get_broadcast'].remove(user_id)
    write(settings_db, settings)
    ben.reply_to(
        message,
        '- جاري الاذاعه!',
        reply_markup = TO_ADMINS_MARKUP
    )
    banned_me = 0
    for user in users:
        try: ben.copy_message(
            chat_id = int(user),
            from_chat_id = user_id,
            message_id = message.id
        )
        except: banned_me += 1
    ben.reply_to(
        message,
        '- تمت الاذاعه بنجاح الى : %s\n\n- الاشخاص الذين قاموا بحظر البوت: %s' % (len(users) - banned_me, banned_me)
    )

@ben.callback_query_handler(
    func = lambda callback: callback.data == 'force_sub' and callback.from_user.id in owners_ids + admins
)
def force_sub(callback):
    user_id = callback.from_user.id
    if user_id not in owners_ids + admins: return ben.edit_message_text(
            message_id = callback.message.id,
            chat_id = user_id,
            text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات'
        )
    ben.edit_message_text(
        chat_id = user_id,
        message_id = callback.message.id,
        text = '- قناة الاشتراك الحاليه : @%s\n- يمكنك تغيير قناة الاشتراك من خلال الزر التالي: ' % (settings['channel']),
        reply_markup = Markup([
            [Button('- تغيير قناة الاشتراك -', callback_data = 'change_force')],
            [Button('- رجوع -', callback_data = 'admins')]
        ])
    )


@ben.callback_query_handler(
    func = lambda callback: callback.data == 'change_force' and callback.from_user.id in owners_ids + admins
)
def change_force(callback):
    user_id = callback.from_user.id
    if user_id not in owners_ids:
        if user_id not in admins: return ben.edit_message_text(
            message_id = callback.message.id,
            chat_id = user_id,
            text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات'
        )
        else:
            return ben.answer_callback_query(
                callback.id, '- لا يمكنك استخدام هذه الميزهّ!' , show_alert = True
            )
    settings['get_channel'].append(user_id)
    write(settings_db, settings)
    ben.edit_message_text(
        chat_id = user_id,
        message_id = callback.message.id,
        text = '- حسنا عزيزي قم بارسال قناة الاشتراك الجديده',
        reply_markup = TO_ADMINS_MARKUP
    )


@ben.message_handler(
    content_types =  ['text'],
    chat_types = ['private'],
    func = lambda message: message.from_user.id in settings['get_channel']
)
def get_channel(message):
    user_id = message.from_user.id
    settings['get_channel'].remove(user_id)
    write(settings_db, settings)
    nchannel = message.text.replace('http', '').replace('https', '').replace('t.me', '').replace('/', '').replace('@', '')
    try: ben.get_chat('@' + nchannel)
    except: return ben.reply_to(
        message,
        '- عذرا عزيزي لم استطع الوصول لهذه القناه',
        reply_markup = TO_ADMINS_MARKUP
    )
    settings['channel'] = nchannel
    write(settings_db, settings)
    ben.reply_to(
        message,
        '- تم تحديث قناة الاشتراك الاجباري!\n\n- تأكد من رفعي مشرف بالقناه الجديده!',
        reply_markup = TO_ADMINS_MARKUP
    )
    ben.send_message(
        MAIN_OWNER,
        '- تم تغيير قناة الاشتراك الاجباري بواسطة : [%s](t.me/%s)' % (message.from_user.first_name, message.from_user.username)
    )
    

@ben.callback_query_handler(
    func = lambda call: ((users.get(str(call.from_user.id)) is None and call.from_user.id not in owners_ids + admins and settings['mode'] == 'private')
                          or (users.get(str(call.from_user.id)) == False and call.from_user.id not in owners_ids + admins and settings['mode'] == 'private'))
)
def not_active(callback):
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = callback.from_user.id,
        text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات!'
    )


@ben.callback_query_handler(
    func = lambda call: call.data.startswith('ct_')
)
def start_search(callback):
    user_id = callback.from_user.id
    settings['get_name'][str(user_id)] = callback.data.split('_')[1]
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = callback.from_user.id,
        text = f'🔍 البحث في {CITIES[callback.data.split("_")[1]]}\n\nقم بإرسال الاسم الثلاثي أو الثنائي للشخص:\n\n📝 مثال:\n• أحمد محمد علي\n• فاطمة حسن',
        reply_markup = TO_USERS_MARKUP
    )
    log_activity(callback.from_user.id, f"بدء البحث في {CITIES[callback.data.split('_')[1]]}")


@ben.message_handler(
    content_types = ['text'],
    chat_types = ['private'],
    func = lambda msg: settings['get_name'].get(str(msg.from_user.id))
)
def get_name(message):
    full_name = message.text.split()
    user_id = message.from_user.id
    city = settings['get_name'][str(user_id)]
    del settings['get_name'][str(user_id)]
    write(settings_db, settings)
    if len(full_name) not in [2, 3]: return ben.reply_to(
        message,
        '- عذرا عزيزي الاسم المعطى غير صحيح!',
        reply_markup = TO_USERS_MARKUP
    )
    wait = ben.reply_to(message, '- جاري البحث...')
    if city == "baghdad":
        town = "rc_name"
        street = "f_street"
        work = "p_job"
    else:
        town = "ss_br_nm"
        street = "ss_lg_no"
        work = "p_work" 
    connection = sqlite3.connect(f'{city}.db')
    connection.text_factory = str
    cursor = connection.cursor()
    fname = full_name[0]
    sname = full_name[1]
    if len(full_name) == 3: lname = full_name[2]
    else: lname = None
    if lname: query = f"SELECT fam_no, p_first, p_father, p_grand, p_birth, {town}, rc_no, seq_no, {street}, {work} FROM person WHERE p_first LIKE '{fname}%' AND p_father LIKE '{sname}%' AND p_grand LIKE '{lname}%'"
    else: query = f"SELECT fam_no, p_first, p_father, p_grand, p_birth, {town}, rc_no, seq_no, {street}, {work} FROM person WHERE p_first LIKE '{fname}%' AND p_father LIKE '{sname}%'"
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows is None or rows == False: return ben.edit_message_text(
        message_id = wait.id,
        chat_id = user_id,
        text = '- عذرا عزيزي لم يتم ايجاد اي نتائج مطابقه!',
        reply_markup = TO_USERS_MARKUP
	)
    for row in rows:
        row = list(row)
        try: age = str(int(datetime.now().year) - int(str(row[4])[:4]))
        except: age = None
        text_template = f"""👤 معلومات الشخص

🏠 رقم العائلة: {str(row[0])}
👤 الاسم الأول: {str(row[1]).replace('\x84', '')}
👤 الاسم الثاني: {str(row[2]).replace('\x84', '')}
👤 الاسم الثالث: {row[3].replace('\x84', '')}
📅 تاريخ الميلاد: {str(row[4])[:4]}
🎂 العمر: {age if age else 'غير محدد'}
💼 الوظيفة: {str(row[9])}
🏛️ المحافظة: {CITIES[city]}
🏘️ القضاء: {str(row[5])}
🏠 المحلة: {str(row[6])}
🛣️ الزقاق: {str(row[8])}
🏠 الدار: {str(row[7])}"""
        ben.send_message(
	        user_id,
	        text_template,
	        reply_markup = Markup([
	            [Button('👨‍👩‍👧‍👦 البحث عن العائلة', callback_data = f'family {str(row[0])} {city}')]
	        ])
	    )
    connection.close()
    ben.delete_message(
	    user_id,
	    wait.id
    )
    ben.send_message(
	    user_id,
	    f'✅ انتهى البحث عن: {message.text}\n\n🔍 يمكنك البحث مرة أخرى من الأزرار أدناه',
	    reply_markup = TO_USERS_MARKUP
    )
    log_activity(user_id, f"انتهاء البحث عن {message.text}")


@ben.callback_query_handler(
    func = lambda call: call.data.startswith('family')
)
def get_family(callback):
    user_id = callback.from_user.id
    data = callback.data.split()[1:]
    family = data[0]
    city = data[1]
    wait = ben.send_message(
        user_id,
        '🔍 جاري البحث عن العائلة...\n\n⏳ يرجى الانتظار...'
    )
    town = 'rc_name' if city == 'baghdad' else 'ss_br_nm'
    connection = sqlite3.connect(f'{city}.db')
    connection.text_factory = str
    cursor = connection.cursor()
    query = f"SELECT fam_no, p_first, p_father, p_grand, p_birth, {str(town)} FROM person WHERE fam_no LIKE '{family}%'"
    cursor.execute(query)
    rows = cursor.fetchall()
    members = ''
    if rows is None or not len(rows) or rows == False: return ben.edit_message_text(
        message_id = wait.id,
        chat_id = user_id,
        text = '- عذرا عزيزي لم يتم ايجاد اي نتائج مطابقه!',
        reply_markup = TO_USERS_MARKUP
    )
    for row in rows:
        row = list(row)
        try: age = str(int(datetime.now().year) - int(str(row[4])[:4]))
        except: age = None
        text_template = '- رقم العائله : %s\n- الاسم الاول : %s\n- الاسم الثاني : %s\n- الاسم الثالث : %s\n- تاريخ الميلاد : %s\n- العمر : %s\n- المحافظه : %s\n- القضاء : %s'  % (
            str(row[0]), str(row[1]).replace('\x84', ''), str(row[2]).replace('\x84', ''), row[3].replace('\x84', ''), 
            str(row[4])[:4], age, CITIES[city], str(row[5])
        )
        members += text_template
        members += '\n\n'
        ben.edit_message_text(
            message_id = wait.id,
            chat_id = user_id,
            text = members
        )
    connection.close()
    members += '- تم الانتهاء.'
    ben.edit_message_text(
        message_id = wait.id,
        chat_id = user_id,
        text = members
    )
    

@ben.callback_query_handler(
    func = lambda call: call.data == 'sh_phone'
)
def sh_phone(callback):
    user_id = callback.from_user.id
    settings['get_num'].append(user_id)
    write(settings_db, settings)
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = callback.from_user.id,
        text = '📱 البحث عن الرقم\n\nقم بإرسال الاسم الثلاثي للشخص:\n\n📝 مثال:\n• أحمد محمد علي\n• فاطمة حسن علي',
        reply_markup = TO_USERS_MARKUP
    )
    log_activity(callback.from_user.id, "بدء البحث عن الرقم")
    

@ben.message_handler(
    content_types = ['text'],
    chat_types = ['private'],
    func = lambda msg: msg.from_user.id in settings['get_num']
)
def get_num(message):
    user_id = message.from_user.id
    settings['get_num'].remove(user_id)
    write(settings_db, settings)
    full_name = message.text
    if len(full_name.split()) not in [2, 3]: return ben.reply_to(
        message,
        '- عذرا عزيزي الاسم المعطى غير صحيح!',
        reply_markup = TO_USERS_MARKUP
    )
    wait = ben.reply_to(message, '- جاري البحث')
    connection = sqlite3.connect('Asiacell.db')
    connection.text_factory = str
    cursor = connection.cursor()
    query = f'SELECT * FROM MAIN_DATA WHERE NAME LIKE "{full_name}%"'
    cursor.execute(query)
    rows = cursor.fetchall()
    if not len(rows) or rows is None or rows == False: return ben.edit_message_text(
        message_id = wait.id,
        chat_id = user_id,
        text = '- عذرا عزيزي لم يتم ايجاد اي نتائج مطابقه!',
        reply_markup = TO_USERS_MARKUP
    )
    for row in rows:
        row = list(row)
        try:ben.reply_to(
            message,
            f"""📱 نتائج البحث

👤 الاسم: {row[0]}
🏛️ المحافظة: {row[1]}
🆔 رقم البطاقة: {row[-1] if row[-1] != '' else 'غير معروف'}
📅 تاريخ الميلاد: {row[3][:8]}
📞 الرقم: {('0' + row[2].replace('.', '')[:10]) if row[2] else 'غير متوفر'}"""
        )
        except apihelper.ApiTelegramException as e:
            if 'A request to the Telegram API was unsuccessful. Error code: 429. Description: Too Many Requests: retry after' in str(e):
                time = int(str(e).rsplit(maxsplit = 1)[1])
                sleep(time)
                ben.reply_to(
                    message,
                    '- الاسم : %s\n- المحافظه : %s\n- رقم البطاقه : %s\n- تاريخ الميلاد: %s\n- الرقم : %s' % (
                        row[0], row[1], row[-1] if row[-1] != '' else 'غير معروف', row[3][:8], 
                        '0' + row[2].replace('.', '')[:10]
                    )
                )
                continue
            else:
                ben.reply_to(message, '- حدث خطأ ما..!')
                continue
    ben.delete_message(user_id, wait.id)
    ben.reply_to(
        message,
        '✅ انتهى البحث\n\n🔍 يمكنك البحث مرة أخرى من الأزرار أدناه',
        reply_markup = TO_USERS_MARKUP
    )
    log_activity(user_id, f"انتهاء البحث عن الرقم لـ {message.text}")
    
    

@ben.callback_query_handler(
    func = lambda call: call.data == 'users'
)
def to_users(callback):
    user_id = callback.from_user.id
    for setting in settings:
        if setting in ['mode', 'channel']: continue
        elif setting in ['get_num', 'get_broadcast', 'get_channel']:
            if user_id in settings[setting]: settings[setting].remove(user_id)
        elif settings[setting].get(str(user_id)): del settings[setting][str(user_id)]
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = user_id,
        text = f'🎉 مرحباً بك في بوت بيانات العراق\n\nيمكنك البحث من خلال الأزرار التالية:\n\n👤 المطور: {OWNER_USERNAME}\n📢 القناة: {CHANNEL_USERNAME}',
        reply_markup = CITIES_MARKUP
    )


read = lambda path: load(open(path))
write = lambda path, data: dump(data ,open(path, 'w'), indent = 4, ensure_ascii = False)

# دوال مساعدة جديدة
def log_activity(user_id, action, details=""):
    """تسجيل نشاط المستخدم"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - User {user_id} - {action} - {details}"
    logger.info(log_entry)
    
    # حفظ في ملف السجل
    if not os.path.exists(logs_db):
        write(logs_db, [])
    
    logs = read(logs_db)
    logs.append({
        'timestamp': timestamp,
        'user_id': user_id,
        'action': action,
        'details': details
    })
    
    # الاحتفاظ بآخر 1000 سجل فقط
    if len(logs) > 1000:
        logs = logs[-1000:]
    
    write(logs_db, logs)

def get_user_info(user_id):
    """الحصول على معلومات المستخدم"""
    try:
        user = ben.get_chat(user_id)
        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    except:
        return None

def backup_data():
    """إنشاء نسخة احتياطية من البيانات"""
    try:
        backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_files = ['users', 'settings', 'admins', 'logs']
        
        for file in backup_files:
            if os.path.exists(file):
                import shutil
                shutil.copy2(file, f"{file}_backup_{backup_time}")
        
        return True
    except Exception as e:
        logger.error(f"خطأ في النسخ الاحتياطي: {e}")
        return False

def get_advanced_stats():
    """الحصول على إحصائيات متقدمة"""
    try:
        total_users = len(users)
        vip_users = sum(1 for user in users.values() if user)
        normal_users = total_users - vip_users
        
        # إحصائيات من السجلات
        logs = read(logs_db) if os.path.exists(logs_db) else []
        today_logs = [log for log in logs if log['timestamp'].startswith(datetime.now().strftime("%Y-%m-%d"))]
        
        return {
            'total_users': total_users,
            'vip_users': vip_users,
            'normal_users': normal_users,
            'today_activities': len(today_logs),
            'total_admins': len(admins),
            'bot_mode': settings.get('mode', 'private')
        }
    except Exception as e:
        logger.error(f"خطأ في الحصول على الإحصائيات: {e}")
        return None


def subscription(user_id):
    # تم إلغاء الاشتراك الإجباري - البوت متاح للجميع
    return True


def main():
    global users, settings, admins
    import os
    
    # إنشاء ملفات البيانات إذا لم تكن موجودة
    if not os.path.exists(users_db):
        write(users_db, {})
    if not os.path.exists(settings_db):
        write(settings_db, {
            'mode' : 'private',
            'get_id': {},
            'get_name': {},
            'get_broadcast': [],
            'channel': channel,
            'get_channel': [],
            'get_num': []
        })
    if not os.path.exists(admins_db):
        write(admins_db, [])
    if not os.path.exists(logs_db):
        write(logs_db, [])
    
    # تحميل البيانات
    settings = read(settings_db)
    users = read(users_db)
    admins = read(admins_db)
    
    # رسالة بدء التشغيل
    logger.info("🚀 بدء تشغيل البوت")
    logger.info(f"👤 المالك: {OWNER_USERNAME}")
    logger.info(f"📢 القناة: {CHANNEL_USERNAME}")
    logger.info(f"👥 عدد المستخدمين: {len(users)}")
    logger.info(f"👨‍💼 عدد الأدمنية: {len(admins)}")
    
    print(f"""
╔══════════════════════════════════════╗
║           🇮🇶 بوت بيانات العراق 🇮🇶        ║
╠══════════════════════════════════════╣
║ 👤 المالك: {OWNER_USERNAME}
║ 📢 القناة: {CHANNEL_USERNAME}
║ 👥 المستخدمين: {len(users)}
║ 👨‍💼 الأدمنية: {len(admins)}
║ ⚙️ الوضع: {'مدفوع' if settings.get('mode') == 'private' else 'مجاني'}
╚══════════════════════════════════════╝
🚀 البوت يعمل بنجاح!
    """)
    
    try:
        ben.infinity_polling(skip_pending = True)
    except Exception as e:
        logger.error(f"خطأ في تشغيل البوت: {e}")
        print(f"❌ خطأ في تشغيل البوت: {e}")


if __name__ == '__main__': main()

# ═══════════════════════════════════════════════════════════════════════════════
# 🇮🇶 بوت بيانات العراق - Iraq Data Bot
# ═══════════════════════════════════════════════════════════════════════════════
# 👤 المطور: @J2J_2
# 📢 القناة: @RPRNN
# 🔧 النسخة المحسنة: 2.0
# 📅 تاريخ التحديث: 2024
# ═══════════════════════════════════════════════════════════════════════════════
# ✨ الميزات الجديدة:
# • واجهة مستخدم محسنة مع إيموجي
# • نظام تسجيل العمليات المتقدم
# • إحصائيات متقدمة
# • نظام نسخ احتياطي
# • إعدادات أمان محسنة
# • رسائل تفاعلية وجذابة
# ═══════════════════════════════════════════════════════════════════════════════
