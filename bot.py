import html
import os
import random
import re
import sys
import time

import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
POST_TYPE = (os.environ.get("POST_TYPE") or "random").strip().lower()
PLATFORM = (os.environ.get("PLATFORM_URL") or "https://alfathplatform.vercel.app").rstrip("/")
FALLBACK_PLATFORM = "https://alfathplatform3.vercel.app"

CHANNELS = ["@VlP_2P", "@zz28r"]

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

SHORT_SURAHS = list(range(78, 115))

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
BISMILLAH_UTHMANI = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"


def esc(text):
    return html.escape(str(text or ""), quote=False)


def to_ar_num(n):
    ar_digits = "٠١٢٣٤٥٦٧٨٩"
    return "".join(ar_digits[int(ch)] if ch.isdigit() else ch for ch in str(n))


def norm(text):
    text = re.sub(r"[\u064B-\u065F\u0670\u06D6-\u06ED\u0640]", "", str(text or ""))
    text = text.replace("ٱ", "ا").replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    return text.replace("ة", "ه").replace("ى", "ي").strip()


def strip_bismillah(text):
    words = str(text or "").split()
    if len(words) > 4 and norm(" ".join(words[:4])) == BISMILLAH:
        return " ".join(words[4:])
    return str(text or "").strip()


def fetch_json(url):
    try:
        res = requests.get(url, timeout=12)
        res.raise_for_status()
        return res.json()
    except Exception:
        return None


def api_json(path):
    clean = path.lstrip("/")
    for base in (PLATFORM, FALLBACK_PLATFORM):
        data = fetch_json(f"{base}/api/v1/{clean}")
        if data is not None:
            return data
    return None


def surah_name(number):
    try:
        num = int(number)
        if 1 <= num <= len(SURAHS):
            return SURAHS[num - 1]
    except Exception:
        pass
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
    data = api_json("random/ayah")
    if not data or "data" not in data:
        return None
    d = data["data"]
    if isinstance(d, list) and d:
        d = random.choice(d)
    if not isinstance(d, dict) or not d.get("text"):
        return None
    surah = d.get("surah")
    if isinstance(surah, dict):
        surah = surah.get("number") or 1
    number = d.get("ayah") or d.get("numberInSurah") or 1
    text = d["text"]
    if int(number) == 1 and int(surah) not in (1, 9):
        text = strip_bismillah(text)
    return {"text": text, "surah": surah, "ayah": number}


def get_ayah_post():
    ayah = ayah_from_alquran() or ayah_from_platform()
    if not ayah:
        return None
    text = esc(ayah["text"])
    return (
        "📖 <b>آية اليوم</b> 🍁\n\n"
        f"﴿ {text} ﴾\n\n"
        f"📌 سورة {surah_name(ayah['surah'])} — الآية رقم ({ayah['ayah']})"
    )


def get_short_surah_post():
    surah_num = random.choice(SHORT_SURAHS)
    name = surah_name(surah_num)

    payload = api_json(f"surah/{surah_num}")
    ayahs = []
    if payload and isinstance(payload.get("data"), dict):
        ayahs = payload["data"].get("ayahs") or []

    if not ayahs:
        aq = fetch_json(f"https://api.alquran.cloud/v1/surah/{surah_num}/quran-uthmani")
        if aq and isinstance(aq.get("data"), dict):
            ayahs = aq["data"].get("ayahs") or []

    if not ayahs:
        return None

    parts = []
    for a in ayahs:
        num = a.get("numberInSurah") or a.get("number")
        txt = str(a.get("text") or "").strip()
        if int(num or 0) == 1 and surah_num not in (1, 9):
            txt = strip_bismillah(txt)
        parts.append(f"{esc(txt)} ﴿{to_ar_num(num)}﴾")

    verses_joined = " ".join(parts)
    bism_block = "" if surah_num in (1, 9) else f"<b>{esc(BISMILLAH_UTHMANI)}</b>\n\n"

    return (
        f"📖 <b>سورة {esc(name)}</b> 🍁\n\n"
        f"{bism_block}"
        f"﴿ {verses_joined} ﴾"
    )


def get_hadith_post():
    data = api_json("hadith.json")
    items = data.get("data") if isinstance(data, dict) else None
    h = random.choice(items) if isinstance(items, list) and items else random.choice(HADITHS)
    text = esc(h["text"])
    post = f"📜 <b>حديث نبوي شريف</b>\n\n{text}\n\n📚 <b>المصدر:</b> {esc(h['source'])}"
    explanation = h.get("explanation")
    if explanation:
        post += f"\n\n💡 <b>الشرح:</b> {esc(explanation)}"
    return post


def get_dua_post():
    data = api_json("duas.json")
    d = None
    if isinstance(data, dict) and isinstance(data.get("data"), dict):
        pool = []
        for arr in data["data"].values():
            if isinstance(arr, list):
                pool.extend(arr)
        if pool:
            d = random.choice(pool)
    if not d:
        return None
    title = esc(d.get("name") or d.get("title") or "دعاء مأثور")
    text = esc(d.get("text") or "")
    source = esc(d.get("source") or "")
    out = f"🤲 <b>{title}</b>\n\n{text}"
    if source:
        out += f"\n\n📌 <b>المصدر:</b> {source}"
    return out


def get_azkar_post():
    data = api_json("azkar.json")
    if not isinstance(data, dict) or not isinstance(data.get("data"), dict):
        return None
    items_map = data["data"].get("items") if isinstance(data["data"].get("items"), dict) else data["data"]
    cat_names = {
        "morning": "أذكار الصباح",
        "evening": "أذكار المساء",
        "sleep": "أذكار النوم",
        "afterPrayer": "أذكار بعد الصلاة",
        "wakeup": "أذكار الاستيقاظ"
    }
    available_keys = [k for k, v in items_map.items() if isinstance(v, list) and v]
    if not available_keys:
        return None
    chosen_key = random.choice(available_keys)
    picked = random.sample(items_map[chosen_key], k=min(3, len(items_map[chosen_key])))
    lines = []
    for z in picked:
        if isinstance(z, dict) and z.get("text"):
            cnt = z.get("count")
            rep = f" ({to_ar_num(cnt)} مرات)" if isinstance(cnt, int) and cnt > 1 else ""
            lines.append(f"• {esc(z['text'])}{rep}")
        elif isinstance(z, str) and z.strip():
            lines.append(f"• {esc(z.strip())}")
    if not lines:
        return None
    label = esc(cat_names.get(chosen_key, chosen_key))
    return f"🌿 <b>{label}</b>\n\n" + "\n\n".join(lines)


def get_prophet_post():
    data = api_json("prophets.json")
    items = data.get("data") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        return None
    p = random.choice(items)
    name = esc(p.get("name") or "")
    desc = esc(p.get("desc") or "")
    lesson = esc(p.get("lesson") or "")
    out = f"⭐ <b>من قصص الأنبياء</b>\n\nنبي الله: <b>{name}</b>"
    if desc:
        out += f" — {desc}"
    if lesson:
        out += f"\n\n💡 <b>الدرس والعبرة:</b> {lesson}"
    return out


def get_quran_story_post():
    data = api_json("quran-stories.json")
    items = data.get("data") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        return None
    s = random.choice(items)
    name = esc(s.get("name") or "")
    desc = esc(s.get("desc") or "")
    lesson = esc(s.get("lesson") or "")
    out = f"📚 <b>من قصص القرآن</b>\n\nقصة: <b>{name}</b>"
    if desc:
        out += f"\n{desc}"
    if lesson:
        out += f"\n\n💡 <b>الدرس والعبرة:</b> {lesson}"
    return out


def get_asmaa_post():
    data = api_json("asmaa.json")
    items = data.get("data") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        return None
    a = random.choice(items)
    num = a.get("number")
    name = esc(a.get("name") or "")
    meaning = esc(a.get("meaning") or "")
    head = f"✨ <b>من أسماء الله الحسنى</b>" + (f" ({to_ar_num(num)})" if num else "")
    return f"{head}\n\n<b>{name}</b>\n\n📖 <b>المعنى:</b> {meaning}"


def get_question_post():
    data = api_json("questions.json")
    items = data.get("data") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        return None
    q = random.choice(items)
    question = esc(q.get("question") or "")
    opts = q.get("options") or []
    corr = q.get("correct")
    ans = esc(opts[corr]) if isinstance(corr, int) and 0 <= corr < len(opts) else ""
    expl = esc(q.get("explanation") or "")
    out = f"❓ <b>سؤال ديني</b>\n\n{question}"
    if ans:
        out += f"\n\n✅ <b>الإجابة:</b> {ans}"
    if expl:
        out += f"\n💡 <b>التوضيح:</b> {expl}"
    return out


def get_tajweed_post():
    data = api_json("tajweed.json")
    cats = (data.get("data") or {}).get("categories") if isinstance(data, dict) else None
    if not isinstance(cats, list) or not cats:
        return None
    lessons = []
    for c in cats:
        for l in (c.get("lessons") or []):
            lessons.append((c.get("name") or "", l))
    if not lessons:
        return None
    cat_name, l = random.choice(lessons)
    title = esc(l.get("title") or "")
    defn = esc(l.get("definition") or "")
    tip = esc(l.get("tip") or "")
    out = f"🎙️ <b>أحكام التجويد — {esc(cat_name)}</b>\n\n<b>{title}</b>\n\n{defn}"
    if tip:
        out += f"\n\n💡 <b>فائدة:</b> {tip}"
    return out


def get_ruqyah_post():
    data = api_json("ruqyah.json")
    duas = (data.get("data") or {}).get("duas") if isinstance(data, dict) else None
    if not isinstance(duas, list) or not duas:
        return None
    d = random.choice(duas)
    title = esc(d.get("title") or "من الرقية الشرعية")
    text = esc(d.get("text") or "")
    src = esc(d.get("source") or "")
    rep = esc(d.get("repetition") or "")
    out = f"🛡️ <b>الرقية الشرعية — {title}</b>\n\n{text}"
    if rep:
        out += f"\n🔁 <b>التكرار:</b> {rep}"
    if src:
        out += f"\n📚 <b>المصدر:</b> {src}"
    return out


HANDLERS = {
    "ayah": get_ayah_post,
    "short_surah": get_short_surah_post,
    "hadith": get_hadith_post,
    "dua": get_dua_post,
    "azkar": get_azkar_post,
    "prophet": get_prophet_post,
    "quran_story": get_quran_story_post,
    "asmaa": get_asmaa_post,
    "question": get_question_post,
    "tajweed": get_tajweed_post,
    "ruqyah": get_ruqyah_post,
}


def generate_post():
    if POST_TYPE in HANDLERS:
        res = HANDLERS[POST_TYPE]()
        if res:
            return res
        return get_ayah_post() or get_hadith_post()

    order = list(HANDLERS.keys())
    random.shuffle(order)
    for k in order:
        res = HANDLERS[k]()
        if res:
            return res
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
