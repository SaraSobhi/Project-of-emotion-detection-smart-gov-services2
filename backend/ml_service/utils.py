import re

def clean_text(text):
    text = str(text)
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("g", "q", text)
    text = re.sub(r'[^\u0600-\u06ff\u0750-\u077f\ufb50-\ufdff\ufe70-\ufeff\s]', '', text)
    return text.strip()

ARABIC_NEGATIVE_KEYWORDS = [
    # Basic negation particles
    'لا', 'لن', 'لم', 'ليس', 'ليست', 'ليسوا', 'لست', 'لسنا', 'لسن',
    'ما', 'غير', 'بدون', 'دون', 'بلا',

    # Colloquial/Egyptian negation (IMPORTANT for sarcasm)
    'محدش', 'مفيش', 'مافيش', 'ولا', 'مش', 'مو', 'موش',
    'ماحدش', 'محد', 'ماحد', 'مالوش', 'ملوش', 'مليش', 'ماليش',

    # Negative verbs and expressions
    'لا يوجد', 'لا توجد', 'لا اعتقد', 'لا افكر', 'لا اظن',
    'لا احب', 'لا اريد', 'لا استطيع', 'لا اقدر',
    'ما ينفعش', 'مينفعش', 'ما يصحش', 'مايصحش',

    # Negative adjectives and words
    'سيء', 'سيئ', 'سيئه', 'سيئين', 'فاشل', 'فشل', 'رديء', 'ردئ',
    'مقرف', 'قبيح', 'كريه', 'مزعج', 'محبط', 'مخيب',
    'ضعيف', 'سخيف', 'تافه', 'حقير', 'وحش', 'فظيع',
    'مرعب', 'مخيف', 'مؤلم', 'حزين', 'كئيب', 'محزن',
    'غاضب', 'زعلان', 'منزعج', 'مستاء', 'ساخط',
    'زباله', 'قمامه', 'خرا', 'تعبان', 'وسخ',

    # Negative phrases and warnings
    'لا يعجبني', 'لا يعجب', 'لا افضل', 'لا انصح', 'ما انصحش',
    'غير جيد', 'غير مقبول', 'غير صحيح', 'غير مناسب',
    'بدون فائده', 'بلا فائده', 'بلا معني', 'بدون معني',
    'ما تجربوش', 'ماتجربوش', 'ما تشتروش', 'ماتشتروش',
    'ما تنزلوش', 'ماتنزلوش', 'ينزله', 'تنزله', 'يشتريه', 'تشتريه',

    # Common negative expressions
    'للاسف', 'مع الاسف', 'يا للاسف', 'واحسرتاه',
    'مشكله', 'مشاكل', 'عيب', 'عيوب', 'خطا', 'اخطاء',
    'فاشل', 'خساره', 'خسران', 'ضرر', 'اضرار',
    'كارثه', 'كوارث', 'مصيبه', 'مصائب', 'ازمه', 'ازمات'
]

def has_negation(text):
    """
    Word-based negation detection using token matching.
    """
    tokens = text.split()
    neg_set = set(ARABIC_NEGATIVE_KEYWORDS)

    return any(token in neg_set for token in tokens)

def add_negation_feature(text):
    """
    Appends a special token if negation is detected to help the model context.
    """
    if has_negation(text):
        return  "سئ " + text
    return text
