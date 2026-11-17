import html
import os
import random
import re
import sys
import time

import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
POST_TYPE = (os.environ.get("POST_TYPE") or "random").strip().lower()
PLATFORM = "https://alfathplatform3.vercel.app"

CHANNELS = [@VlP_2P, @zz28r]

SURAHS = [
    "الفاتحة","البقرة","آل عمران","النساء","المائدة","الأنعام","الأعراف","الأنفال","التوبة","يونس","هود","يوسف",
    "الرعد","إبراهيم","الحجر","النحل","الإسراء","الكهف","مريم","طه","الأنبياء","الحج","المؤمنون","النور","الفرقان",
    "الشعراء","النمل","القصص","العنكبوت","الروم","لقمان","السجدة","الأحزاب","سبأ","فاطر","يس","الصافات","ص",
    "الزمر","غافر","فصلت","الشورى","الزخرف","الدخان","الجاثية","الأحقاف","محمد","الفتح","الحجرات","ق","الذاريات",
    "الطور","النجم","القمر","الرحمن","الواقعة","الحديد","المجادلة","الحشر","الممتحنة","الصف","الجمعة","المنافقون",
    "التغابن","الطلاق","التحريم","الملك","القلم","الحاقة","المعارج","نوح","الجن","المزمل","المدثر","القيامة","الإنسان",
    "المرسلات","النبأ","النازعات","عبس","التكوير","الانفطار","المطففين","الانشقاق","البروج","الطارق","الأعلى","الغاشية",
    "الفجر","البلد","الشمس","الليل","الضحى","الشرح","التين","العلق","القدر","البينة","الزلزلة","العاديات","القارعة",
    "التكاثر","العصر","الهمزة","الفيل","قريش","الماعون","الكوثر","الكافرون","النصر","المسد","الإخلاص","الفلق","الناس"
]

HADITHS = [
    {"text": "«إنما الأعمالُ بالنيات، وإنما لكل امرئ ما نوى»", "source": "متفق عليه"},
    {"text": "«الدين النصيحة» قلنا: لمن؟ قال: «لله، ولكتابه، ولرسوله، ولأئمة المسلمين وعامتهم»", "source": "رواه مسلم"},
    {"text": "«لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه»", "source": "متفق عليه"},
    {"text": "«من كان يؤمن بالله واليوم الآخر فليقل خيراً أو ليصمت»", "source": "متفق عليه"},
    {"text": "«اتق الله حيثما كنت، وأتبع السيئة الحسنة تمحها، وخالق الناس بخلق حسن»", "source": "رواه الترمذي"},
    {"text": "«المسلم من سلم المسلمون من لسانه ويده»", "source": "متفق عليه"},
    {"text": "«الراحمون يرحمهم الرحمن، ارحموا من في الأرض يرحمكم من في السماء»", "source": "رواه أبو داود والترمذي"},
    {"text": "«تبسمك في وجه أخيك صدقة»", "source": "رواه الترمذي"},
    {"text": "«الكلمة الطيبة صدقة»", "source": "متفق عليه"},
    {"text": "«احرص على ما ينفعك، واستعن بالله ولا تعجز»", "source": "رواه مسلم"},
    {"text": "«عجباً لأمر المؤمن، إن أمره كله خير، وليس ذاك لأحد إلا للمؤمن»", "source": "رواه مسلم"},
    {"text": "«كلمتان خفيفتان على اللسان، ثقيلتان في الميزان، حبيبتان إلى الرحمن: سبحان الله وبحمده، سبحان الله العظيم»", "source": "متفق عليه"},
    {"text": "«خيركم من تعلم القرآن وعلمه»", "source": "رواه البخاري"},
    {"text": "«من سلك طريقاً يلتمس فيه علماً سهل الله له به طريقاً إلى الجنة»", "source": "رواه مسلم"},
    {"text": "«من صلى عليّ صلاة صلى الله عليه بها عشراً»", "source": "رواه مسلم"},
    {"text": "«أحب الأعمال إلى الله أدومها وإن قل»", "source": "متفق عليه"},
    {"text": "«الطهور شطر الإيمان، والحمد لله تملأ الميزان»", "source": "رواه مسلم"},
    {"text": "«لا تحقرن من المعروف شيئاً ولو أن تلقى أخاك بوجه طلق»", "source": "رواه مسلم"},
    {"text": "«من دل على خير فله مثل أجر فاعله»", "source": "رواه مسلم"},
    {"text": "«أنا وكافل اليتيم في الجنة هكذا، وأشار بالسبابة والوسطى»", "source": "رواه البخاري"},
    {"text": "«ما نقصت صدقة من مال، وما زاد الله عبداً بعفو إلا عِزاً»", "source": "رواه مسلم"},
    {"text": "«يسروا ولا تعسروا، وبشروا ولا تنفروا»", "source": "متفق عليه"},
    {"text": "«من قال: سبحان الله وبحمده في يوم مائة مرة حُطّت خطاياه وإن كانت مثل زبد البحر»", "source": "متفق عليه"},
    {"text": "«دع ما يريبك إلى ما لا يريبك»", "source": "رواه الترمذي والنسائي"},
    {"text": "«إن الله رفيق يحب الرفق في الأمر كله»", "source": "متفق عليه"},
    {"text": "«من لزم الاستغفار جعل الله له من كل هم فرجاً، ومن كل ضيق مخرجاً، ورزقه من حيث لا يحتسب»", "source": "رواه أبو داود"},
    {"text": "«من يرد الله به خيراً يفقهه في الدين»", "source": "متفق عليه"},
    {"text": "«أفضل الذكر: لا إله إلا الله، وأفضل الدعاء: الحمد لله»", "source": "رواه الترمذي وحسنه"}
]

BISMILLAH = "بسم الله الرحمن الرحيم"


def norm(text):
    text = re.sub(r"[\u064B-\u065F\u0670\u06D6-\u06ED\u0640]", "", text)
    text = text.replace("ٱ", "ا").replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    return text.replace("ة", "ه").replace("ى", "ي").strip()


def strip_bismillah(text):
    words = text.split()
    if len(words) > 4 and norm(" ".join(words[:4])) == BISMILLAH:
        return " ".join(words[4:])
    return text


def fetch_json(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception:
        return None


def surah_name(number):
    if 1 <= number <= len(SURAHS):
        return SURAHS[number - 1]
    return str(number)


def ayah_from_alquran():
    for _ in range(6):
        data = fetch_json(f"https://api.alquran.cloud/v1/ayah/{random.randint(1, 6236)}/quran-uthmani")
        if not data or "data" not in data:
            continue
        d = data["data"]
        surah = d["surah"]["number"]
        number = d["numberInSurah"]
        text = d["text"]
        if number == 1 and surah not in (1, 9):
            text = strip_bismillah(text)
        if 12 <= len(norm(text)) <= 900:
            return {"text": text, "surah": surah, "ayah": number}
    return None


def ayah_from_platform():
    data = fetch_json(f"{PLATFORM}/api/v1/random/ayah")
    if not data or "data" not in data:
        return None
    d = data["data"]
    text = d["text"]
    if d["ayah"] == 1 and d["surah"] not in (1, 9):
        text = strip_bismillah(text)
    return {"text": text, "surah": d["surah"], "ayah": d["ayah"]}


def get_ayah_post():
    ayah = ayah_from_alquran() or ayah_from_platform()
    if not ayah:
        return None
    text = html.escape(ayah["text"], quote=False)
    return (
        "📖 <b>آية اليوم</b> 🍁\n\n"
        f"﴿ {text} ﴾\n\n"
        f"📌 سورة {surah_name(ayah['surah'])} — الآية رقم ({ayah['ayah']})"
    )


def get_hadith_post():
    data = fetch_json(f"{PLATFORM}/api/v1/hadith.json")
    items = data.get("data") if data else None
    h = random.choice(items) if items else random.choice(HADITHS)
    text = html.escape(h["text"], quote=False)
    post = f"📜 <b>حديث نبوي شريف</b>\n\n{text}\n\n📚 <b>المصدر:</b> {html.escape(h['source'], quote=False)}"
    explanation = h.get("explanation")
    if explanation:
        post += f"\n\n💡 <b>الشرح:</b> {html.escape(explanation, quote=False)}"
    return post


def generate_post():
    kind = POST_TYPE if POST_TYPE in ("ayah", "hadith") else random.choice(["ayah", "hadith"])
    if kind == "ayah":
        return get_ayah_post() or get_hadith_post()
    return get_hadith_post()


def load_channels():
    found = list(CHANNELS)
    found += re.split(r"[\s,]+", os.environ.get("CHANNEL_ID", ""))
    if os.path.exists("channels.txt"):
        with open("channels.txt", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    found.append(line)
    channels = []
    for item in found:
        item = str(item).strip()
        if not item or item.startswith("@your_channel"):
            continue
        if re.fullmatch(r"-?\d+", item):
            item = int(item)
        if item not in channels:
            channels.append(item)
    return channels


def send(url, chat, message):
    payload = {
        "chat_id": chat,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    res = requests.post(url, json=payload, timeout=12).json()
    if not res.get("ok") and res.get("error_code") == 429:
        time.sleep(min(res.get("parameters", {}).get("retry_after", 3), 30))
        res = requests.post(url, json=payload, timeout=12).json()
    return res


def broadcast():
    if not BOT_TOKEN:
        print("خطأ: لم يتم العثور على BOT_TOKEN في المتغيرات البيئية.")
        sys.exit(1)

    channels = load_channels()
    if not channels:
        print("خطأ: لا توجد قنوات. أضفها في CHANNEL_ID أو channels.txt")
        sys.exit(1)

    signature = '🕌 <a href="https://alfathplatform.vercel.app">منصة الفتح</a>'
    message = f"{generate_post()}\n\n---\n{signature}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    success_count = 0

    for chat in channels:
        try:
            res = send(url, chat, message)
            if res.get("ok"):
                print(f"✅ تم النشر في: {chat}")
                success_count += 1
            else:
                print(f"❌ فشل النشر في {chat}: {res.get('description')}")
        except Exception as e:
            print(f"⚠️ استثناء أثناء الإرسال إلى {chat}: {e}")
        time.sleep(0.2)

    print(f"\nاكتملت العملية: نُشر بنجاح في {success_count} من {len(channels)} قناة/مجموعة.")
    if success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    broadcast()
