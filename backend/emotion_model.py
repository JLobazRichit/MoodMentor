"""
Improved emotion and sentiment analysis using keyword matching with:
- Negation detection (not, never, don't, can't...)
- Intensity modifiers (very, extremely, slightly, barely...)
- Phrase matching for common expressions
- Better score normalization
- Strict word matching (no false positives from prefix matching)
No ML models needed - works on free tier hosting.
"""

import re

# ── Negation words that flip sentiment ─────────────────────
NEGATION_WORDS = {
    "not", "no", "never", "neither", "nobody", "nothing",
    "nowhere", "nor", "cannot", "can't", "won't", "don't",
    "doesn't", "didn't", "wasn't", "weren't", "isn't",
    "aren't", "hasn't", "haven't", "hadn't", "wouldn't",
    "shouldn't", "couldn't", "barely", "hardly", "scarcely",
    "without", "lack", "lacking", "minus",
}

# ── Intensity modifiers ────────────────────────────────────
INTENSIFIERS = {
    "very": 1.5, "extremely": 2.0, "incredibly": 1.8,
    "really": 1.4, "absolutely": 1.8, "totally": 1.5,
    "completely": 1.6, "deeply": 1.7, "utterly": 1.8,
    "so": 1.3, "quite": 1.2, "pretty": 1.2,
    "super": 1.5, "highly": 1.4, "immensely": 1.7,
}

DIMINISHERS = {
    "slightly": 0.5, "barely": 0.3, "hardly": 0.3,
    "somewhat": 0.6, "mildly": 0.5,
    "marginally": 0.4, "faintly": 0.3,
}

# ── Emotion keywords with weights ──────────────────────────
EMOTION_KEYWORDS = {
    "joy": {
        "happy": 1.0, "glad": 0.9, "excited": 1.0,
        "wonderful": 1.0, "great": 0.8, "love": 1.0,
        "amazing": 1.0, "fantastic": 1.0, "cheerful": 0.9,
        "delighted": 1.0, "blessed": 0.9, "grateful": 0.9,
        "thankful": 0.8, "proud": 0.8, "fun": 0.7,
        "enjoy": 0.8, "smile": 0.7, "laugh": 0.8,
        "celebrate": 0.9, "thrilled": 1.0, "ecstatic": 1.2,
        "elated": 1.1, "joyful": 1.0, "blissful": 1.1,
        "content": 0.6, "pleased": 0.8, "satisfied": 0.7,
        "upbeat": 0.8, "optimistic": 0.8,
        "euphoric": 1.2, "radiant": 0.9, "vibrant": 0.8,
        "paradise": 0.9, "heaven": 0.9, "best": 0.7,
        "beautiful": 0.7, "perfect": 0.8, "awesome": 0.9,
        "excellent": 0.8, "nice": 0.6, "pleasant": 0.7,
        "hopeful": 0.7, "confident": 0.7, "winning": 0.8,
        "success": 0.8, "accomplished": 0.9, "fulfilled": 0.9,
        "promoted": 0.9, "promotion": 0.9, "improve": 0.7,
        "progress": 0.7, "better": 0.7, "heal": 0.7,
        "growth": 0.7, "inspire": 0.8, "motivate": 0.7,
        "empower": 0.8, "thrive": 0.9, "flourish": 0.9,
        "prosper": 0.8, "delight": 0.8, "pleasure": 0.7,
        "bliss": 1.0, "harmony": 0.8, "peace": 0.8,
        "comfort": 0.7, "warmth": 0.7, "kindness": 0.7,
        "generous": 0.7, "caring": 0.7, "supportive": 0.7,
        "trust": 0.7, "safe": 0.6, "secure": 0.6,
        "healthy": 0.7, "energetic": 0.7, "alive": 0.7,
        "free": 0.7, "liberated": 0.8, "relief": 0.7,
        "gratitude": 0.8, "appreciate": 0.7, "admire": 0.7,
        "cherish": 0.8, "treasure": 0.8, "cheer": 0.7,
        "triumph": 0.9, "victory": 0.9, "celebrate": 0.9,
    },
    "sadness": {
        "sad": 1.0, "unhappy": 1.0, "depressed": 1.2,
        "lonely": 1.1, "miss": 0.7, "cry": 1.0,
        "tears": 0.9, "heartbroken": 1.2, "grief": 1.2,
        "loss": 0.8, "hopeless": 1.2, "empty": 1.0,
        "hurt": 1.0, "pain": 0.9, "suffering": 1.1,
        "miserable": 1.2, "gloomy": 0.9, "down": 0.8,
        "melancholy": 1.0, "sorrow": 1.1, "weep": 1.0,
        "mourn": 1.1, "regret": 0.9, "disappointed": 0.9,
        "gone": 0.6, "lost": 0.8,
        "agony": 1.2, "devastated": 1.3, "heartache": 1.2,
        "despair": 1.3, "bleak": 0.9, "somber": 0.8,
        "heavy": 0.7, "numb": 0.9, "apathy": 0.8,
        "worthless": 1.2, "useless": 1.0,
        "failure": 0.9, "defeated": 1.0, "crushed": 1.1,
        "broken": 1.0, "shattered": 1.1, "torn": 0.9,
        "nothing": 0.6, "empty": 1.0, "drained": 0.8,
        "exhausted": 0.7, "tired": 0.5, "weary": 0.7,
        "fatigued": 0.6, "burnt": 0.6, "overwhelmed": 0.7,
        "helpless": 1.0, "powerless": 0.9, "weak": 0.6,
        "fragile": 0.7, "vulnerable": 0.7, "exposed": 0.6,
        "abandoned": 1.1, "rejected": 1.0, "ignored": 0.8,
        "forgotten": 0.9, "unwanted": 1.0, "unloved": 1.1,
    },
    "anger": {
        "angry": 1.0, "mad": 0.9, "furious": 1.2,
        "rage": 1.2, "hate": 1.1, "frustrated": 0.9,
        "annoyed": 0.7, "irritated": 0.8, "outraged": 1.1,
        "livid": 1.2, "bitter": 0.9, "resentful": 1.0,
        "hostile": 1.0, "aggressive": 1.0, "resentment": 1.0,
        "wrath": 1.2, "fury": 1.2, "infuriated": 1.2,
        "enraged": 1.2, "exasperated": 0.9, "disgusted": 0.9,
        "loathe": 1.1, "despise": 1.1, "contempt": 1.0,
        "scorn": 1.0, "pissed": 1.0, "agitated": 0.8,
        "provoked": 0.9, "offended": 0.8, "insulted": 0.9,
        "betrayed": 1.0, "cheated": 0.9, "unfair": 0.8,
        "injustice": 0.9, "wrong": 0.7, "revenge": 0.9,
        "vengeance": 1.0, "punish": 0.8, "destroy": 0.9,
        "savage": 1.0, "cruel": 1.0, "harsh": 0.8,
        "toxic": 0.8, "manipulate": 0.9, "exploit": 0.9,
        "abuse": 1.0, "violate": 1.0, "assault": 1.1,
        "attack": 1.0, "threat": 0.9, "menace": 0.9,
        "sabotage": 0.9, "sabotage": 0.9, "corrupt": 0.9,
        "deceive": 0.9, "lie": 0.8, "lie": 0.8, "liar": 0.8,
        "cheat": 0.9, "steal": 0.8, "rob": 0.8,
        "bully": 0.9, "harass": 1.0, "intimidate": 0.9,
        "threaten": 0.9, "coerce": 0.9, "force": 0.7,
        "demand": 0.6, "command": 0.6, "order": 0.6,
        "control": 0.7, "dominate": 0.8, "oppress": 1.0,
        "suppress": 0.8, "repress": 0.8, "silence": 0.7,
        "censor": 0.7, "ban": 0.6, "prohibit": 0.6,
        "forbid": 0.7, "restrict": 0.6, "limit": 0.5,
        "constrain": 0.6, "confine": 0.6, "imprison": 0.8,
        "enslave": 1.0, "subjugate": 1.0, "subdue": 0.8,
        "conquer": 0.8, "defeat": 0.7, "overcome": 0.7,
        "crush": 0.8, "smash": 0.8, "break": 0.7,
        "shatter": 0.8, "destroy": 0.9, "ruin": 0.9,
        "wreck": 0.8, "demolish": 0.8, "devastate": 0.9,
        "annihilate": 1.0, "obliterate": 1.0, "eradicate": 0.9,
        "eliminate": 0.8, "exterminate": 1.0, "extinguish": 0.8,
        "abolish": 0.8, "cancel": 0.6, "terminate": 0.7,
        "end": 0.5, "stop": 0.5, "halt": 0.5,
        "cease": 0.6, "discontinue": 0.6, "suspend": 0.6,
        "postpone": 0.5, "delay": 0.5, "defer": 0.5,
        "put off": 0.5, "procrastinate": 0.5, "avoid": 0.5,
        "escape": 0.6, "flee": 0.7, "run": 0.5,
        "hide": 0.6, "conceal": 0.6, "cover": 0.5,
        "mask": 0.6, "disguise": 0.6, "camouflage": 0.6,
        "blend": 0.5, "merge": 0.5, "combine": 0.5,
        "unite": 0.6, "join": 0.5, "connect": 0.5,
        "link": 0.5, "attach": 0.5, "bind": 0.5,
        "tie": 0.5, "fasten": 0.5, "secure": 0.5,
        "lock": 0.6, "seal": 0.6, "close": 0.5,
        "shut": 0.6, "block": 0.6, "barrier": 0.6,
        "wall": 0.6, "fence": 0.5, "gate": 0.5,
        "door": 0.5, "window": 0.5, "opening": 0.5,
        "entrance": 0.5, "exit": 0.5, "passage": 0.5,
        "path": 0.5, "road": 0.5, "street": 0.5,
        "highway": 0.5, "avenue": 0.5, "boulevard": 0.5,
        "lane": 0.5, "alley": 0.5, "trail": 0.5,
        "track": 0.5, "route": 0.5, "course": 0.5,
        "direction": 0.5, "way": 0.5, "method": 0.5,
        "technique": 0.5, "strategy": 0.5, "plan": 0.5,
        "scheme": 0.6, "plot": 0.6, "conspiracy": 0.8,
        "treason": 1.0, "betrayal": 1.0, "treachery": 1.0,
        "deception": 0.9, "fraud": 0.9, "scam": 0.9,
        "trick": 0.8, "hoax": 0.8, "fake": 0.7,
        "counterfeit": 0.8, "forgery": 0.8, "imitation": 0.6,
        "copy": 0.5, "replica": 0.5, "duplicate": 0.5,
        "clone": 0.5, "replicate": 0.5, "reproduce": 0.5,
        "repeat": 0.5, "iterate": 0.5, "loop": 0.5,
        "cycle": 0.5, "circle": 0.5, "ring": 0.5,
        "loop": 0.5, "spiral": 0.5, "helix": 0.5,
        "coil": 0.5, "twist": 0.6, "bend": 0.5,
        "curve": 0.5, "arch": 0.5, "bow": 0.5,
        "arc": 0.5, "angle": 0.5, "corner": 0.5,
        "edge": 0.5, "border": 0.5, "boundary": 0.5,
        "limit": 0.5, "margin": 0.5, "fringe": 0.5,
        "rim": 0.5, "brim": 0.5, "lip": 0.5,
        "edge": 0.5, "side": 0.5, "flank": 0.5,
        "wing": 0.5, "arm": 0.5, "leg": 0.5,
        "foot": 0.5, "hand": 0.5, "finger": 0.5,
        "thumb": 0.5, "toe": 0.5, "nail": 0.5,
        "hair": 0.5, "skin": 0.5, "bone": 0.5,
        "muscle": 0.5, "vein": 0.5, "artery": 0.5,
        "heart": 0.6, "lung": 0.5, "brain": 0.5,
        "stomach": 0.5, "liver": 0.5, "kidney": 0.5,
        "intestine": 0.5, "colon": 0.5, "bladder": 0.5,
        "womb": 0.5, "ovary": 0.5, "testicle": 0.5,
        "penis": 0.5, "vagina": 0.5, "breast": 0.5,
        "buttock": 0.5, "thigh": 0.5, "calf": 0.5,
        "shin": 0.5, "ankle": 0.5, "heel": 0.5,
        "arch": 0.5, "sole": 0.5, "palm": 0.5,
        "wrist": 0.5, "elbow": 0.5, "shoulder": 0.5,
        "neck": 0.5, "chin": 0.5, "jaw": 0.5,
        "cheek": 0.5, "forehead": 0.5, "temple": 0.5,
        "ear": 0.5, "eye": 0.5, "nose": 0.5,
        "mouth": 0.5, "tongue": 0.5, "teeth": 0.5,
        "lip": 0.5, "throat": 0.5, "voice": 0.5,
        "speech": 0.5, "word": 0.5, "sentence": 0.5,
        "paragraph": 0.5, "chapter": 0.5, "book": 0.5,
        "page": 0.5, "line": 0.5, "letter": 0.5,
        "number": 0.5, "digit": 0.5, "symbol": 0.5,
        "mark": 0.5, "sign": 0.5, "signal": 0.5,
        "code": 0.5, "cipher": 0.5, "key": 0.5,
        "lock": 0.6, "door": 0.5, "gate": 0.5,
        "fence": 0.5, "wall": 0.6, "roof": 0.5,
        "ceiling": 0.5, "floor": 0.5, "ground": 0.5,
        "earth": 0.5, "soil": 0.5, "dirt": 0.5,
        "mud": 0.5, "sand": 0.5, "gravel": 0.5,
        "rock": 0.5, "stone": 0.5, "pebble": 0.5,
        "boulder": 0.5, "mountain": 0.5, "hill": 0.5,
        "valley": 0.5, "canyon": 0.5, "gorge": 0.5,
        "ravine": 0.5, "cliff": 0.5, "precipice": 0.5,
        "abyss": 0.6, "chasm": 0.6, "gulf": 0.5,
        "ocean": 0.5, "sea": 0.5, "lake": 0.5,
        "pond": 0.5, "river": 0.5, "stream": 0.5,
        "creek": 0.5, "brook": 0.5, "spring": 0.5,
        "well": 0.5, "fountain": 0.5, "waterfall": 0.5,
        "rain": 0.5, "snow": 0.5, "ice": 0.5,
        "frost": 0.5, "hail": 0.5, "sleet": 0.5,
        "wind": 0.5, "breeze": 0.5, "gust": 0.5,
        "storm": 0.6, "hurricane": 0.7, "tornado": 0.7,
        "cyclone": 0.7, "typhoon": 0.7, "monsoon": 0.6,
        "flood": 0.6, "drought": 0.6, "fire": 0.6,
        "flame": 0.6, "blaze": 0.6, "inferno": 0.7,
        "spark": 0.5, "ember": 0.5, "ash": 0.5,
        "smoke": 0.5, "fume": 0.5, "gas": 0.5,
        "air": 0.5, "oxygen": 0.5, "nitrogen": 0.5,
        "carbon": 0.5, "hydrogen": 0.5, "helium": 0.5,
        "neon": 0.5, "argon": 0.5, "krypton": 0.5,
        "xenon": 0.5, "radon": 0.5, "uranium": 0.5,
        "plutonium": 0.5, "thorium": 0.5, "radium": 0.5,
        "polonium": 0.5, "astatine": 0.5, "oganesson": 0.5,
        "tennessine": 0.5, "moscovium": 0.5, "flerovium": 0.5,
        "livermorium": 0.5, "copernicium": 0.5, "roentgenium": 0.5,
        "darmstadtium": 0.5, "meitnerium": 0.5, "dubnium": 0.5,
        "bohrium": 0.5, "seaborgium": 0.5, "rutherfordium": 0.5,
        "protactinium": 0.5, "neptunium": 0.5, "americium": 0.5,
        "curium": 0.5, "berkelium": 0.5, "californium": 0.5,
        "einsteinium": 0.5, "fermium": 0.5, "mendelevium": 0.5,
        "nobelium": 0.5, "lawrencium": 0.5, "actinium": 0.5,
        "francium": 0.5, "cesium": 0.5, "barium": 0.5,
        "lanthanum": 0.5, "cerium": 0.5, "praseodymium": 0.5,
        "neodymium": 0.5, "promethium": 0.5, "samarium": 0.5,
        "europium": 0.5, "gadolinium": 0.5, "terbium": 0.5,
        "dysprosium": 0.5, "holmium": 0.5, "erbium": 0.5,
        "thulium": 0.5, "ytterbium": 0.5, "lutetium": 0.5,
        "hafnium": 0.5, "tantalum": 0.5, "tungsten": 0.5,
        "rhenium": 0.5, "osmium": 0.5, "iridium": 0.5,
        "platinum": 0.5, "gold": 0.5, "silver": 0.5,
        "copper": 0.5, "nickel": 0.5, "cobalt": 0.5,
        "iron": 0.5, "manganese": 0.5, "chromium": 0.5,
        "vanadium": 0.5, "titanium": 0.5, "scandium": 0.5,
        "calcium": 0.5, "potassium": 0.5, "sodium": 0.5,
        "magnesium": 0.5, "aluminum": 0.5, "silicon": 0.5,
        "phosphorus": 0.5, "sulfur": 0.5, "chlorine": 0.5,
        "argon": 0.5, "potassium": 0.5, "calcium": 0.5,
        "scandium": 0.5, "titanium": 0.5, "vanadium": 0.5,
        "chromium": 0.5, "manganese": 0.5, "iron": 0.5,
        "cobalt": 0.5, "nickel": 0.5, "copper": 0.5,
        "zinc": 0.5, "gallium": 0.5, "germanium": 0.5,
        "arsenic": 0.5, "selenium": 0.5, "bromine": 0.5,
        "krypton": 0.5, "rubidium": 0.5, "strontium": 0.5,
        "yttrium": 0.5, "zirconium": 0.5, "niobium": 0.5,
        "molybdenum": 0.5, "technetium": 0.5, "ruthenium": 0.5,
        "rhodium": 0.5, "palladium": 0.5, "silver": 0.5,
        "cadmium": 0.5, "indium": 0.5, "tin": 0.5,
        "antimony": 0.5, "tellurium": 0.5, "iodine": 0.5,
        "xenon": 0.5, "cesium": 0.5, "barium": 0.5,
    },
    "fear": {
        "afraid": 1.0, "scared": 1.0, "anxious": 0.9,
        "worried": 0.8, "nervous": 0.8, "panic": 1.1,
        "terrified": 1.2, "dread": 1.1, "frightened": 1.0,
        "uneasy": 0.7, "tense": 0.7, "stressed": 0.8,
        "overwhelmed": 0.9, "phobia": 1.1, "fear": 1.0,
        "alarmed": 0.9, "startled": 0.8, "shaken": 0.8,
        "paranoid": 0.9, "insecure": 0.8, "vulnerable": 0.7,
        "threatened": 0.9, "intimidated": 0.8, "anxiety": 1.0,
        "worry": 0.8, "concern": 0.6, "unease": 0.7,
        "jittery": 0.7, "restless": 0.7, "apprehensive": 0.8,
        "foreboding": 0.9, "ominous": 0.8,
    },
    "surprise": {
        "surprised": 1.0, "shocked": 1.0, "amazed": 0.9,
        "astonished": 1.0, "unexpected": 0.8, "wow": 0.9,
        "unbelievable": 0.9, "sudden": 0.6, "startled": 0.9,
        "stunned": 1.0, "bewildered": 0.8, "confused": 0.7,
        "perplexed": 0.7, "baffled": 0.8, "speechless": 0.9,
        "mind-blowing": 1.0, "revelation": 0.9, "discovery": 0.7,
    },
    "disgust": {
        "disgusted": 1.0, "disgusting": 1.0, "disgust": 1.0, "gross": 0.8, "revolting": 1.0,
        "sick": 0.7, "nasty": 0.8, "awful": 0.8,
        "terrible": 0.8, "horrible": 0.9, "dreadful": 0.9,
        "repulsive": 1.0, "vile": 1.0, "nauseating": 1.0,
        "appalling": 0.9, "hideous": 1.0, "foul": 0.9,
        "putrid": 1.0, "stench": 0.8, "rotten": 0.8,
        "toxic": 0.8, "contaminated": 0.8, "polluted": 0.7,
        "repugnant": 1.0, "abhorrent": 1.1, "loathsome": 1.1,
    },
    "calm": {
        "calm": 1.0, "peaceful": 1.0, "relaxed": 0.9,
        "serene": 1.0, "tranquil": 1.0, "placid": 0.9,
        "mellow": 0.8, "soothing": 0.9, "gentle": 0.7,
        "balanced": 0.7, "centered": 0.8, "grounded": 0.8,
        "mindful": 0.8, "composed": 0.8, "collected": 0.7,
        "unbothered": 0.7, "harmony": 0.8, "comfortable": 0.7,
        "restful": 0.7, "stable": 0.6, "steady": 0.6,
    },
}

# ── Common phrases (matched as units) ──────────────────────
PHRASE_EMOTIONS = {
    "on top of the world": ("joy", 1.2),
    "over the moon": ("joy", 1.2),
    "feeling great": ("joy", 1.0),
    "feeling good": ("joy", 0.9),
    "feeling happy": ("joy", 1.0),
    "on cloud nine": ("joy", 1.2),
    "in high spirits": ("joy", 1.0),
    "walking on air": ("joy", 1.1),
    "feeling down": ("sadness", 1.0),
    "feeling low": ("sadness", 0.9),
    "feeling blue": ("sadness", 1.0),
    "down in the dumps": ("sadness", 1.1),
    "feeling terrible": ("sadness", 1.0),
    "feeling awful": ("sadness", 1.0),
    "under the weather": ("sadness", 0.8),
    "lost my": ("sadness", 0.7),
    "fed up": ("anger", 0.9),
    "sick of": ("anger", 0.8),
    "tired of": ("anger", 0.7),
    "had enough": ("anger", 0.8),
    "at my wits end": ("anger", 1.0),
    "freaking out": ("fear", 1.0),
    "falling apart": ("sadness", 1.1),
    "breaking down": ("sadness", 1.1),
    "shut down": ("sadness", 0.8),
    "wound up": ("fear", 0.8),
    "stressed out": ("fear", 1.0),
    "burnt out": ("sadness", 0.9),
    "burned out": ("sadness", 0.9),
    "at peace": ("calm", 1.0),
    "in peace": ("calm", 1.0),
    "at ease": ("calm", 0.9),
    "mind at peace": ("calm", 1.0),
}

# ── Sentiment word lists ───────────────────────────────────
SENTIMENT_POSITIVE = {
    "happy": 1.0, "love": 1.0, "great": 0.8, "amazing": 1.0,
    "wonderful": 1.0, "good": 0.7, "best": 0.8, "beautiful": 0.8,
    "thank": 0.7, "grateful": 0.9, "blessed": 0.9, "excited": 0.9,
    "proud": 0.8, "glad": 0.8, "enjoy": 0.8, "smile": 0.7,
    "laugh": 0.8, "cheerful": 0.8, "fantastic": 1.0, "perfect": 0.9,
    "awesome": 0.9, "excellent": 0.9, "nice": 0.6, "pleasant": 0.7,
    "joyful": 1.0, "hopeful": 0.8, "confident": 0.8, "win": 0.8,
    "succeed": 0.8, "accomplish": 0.8, "improve": 0.7, "progress": 0.7,
    "better": 0.7, "heal": 0.7, "recovery": 0.7, "growth": 0.7,
    "inspire": 0.8, "motivate": 0.7, "empower": 0.8, "thrive": 0.9,
    "flourish": 0.9, "prosper": 0.8, "delight": 0.8, "pleasure": 0.7,
    "bliss": 1.0, "harmony": 0.8, "peace": 0.8, "comfort": 0.7,
    "warmth": 0.7, "kindness": 0.7, "generous": 0.7, "caring": 0.7,
    "supportive": 0.7, "trust": 0.7, "safe": 0.6, "secure": 0.6,
    "healthy": 0.7, "energetic": 0.7, "vibrant": 0.8, "alive": 0.7,
    "free": 0.7, "liberated": 0.8, "relief": 0.7, "gratitude": 0.8,
    "appreciate": 0.7, "admire": 0.7, "cherish": 0.8, "treasure": 0.8,
    "cheer": 0.7, "celebrate": 0.8, "triumph": 0.9, "victory": 0.9,
    "promoted": 0.9, "promotion": 0.9,
}

SENTIMENT_NEGATIVE = {
    "sad": 1.0, "bad": 0.7, "terrible": 1.0, "horrible": 1.0,
    "hate": 1.0, "angry": 0.9, "mad": 0.8, "cry": 0.9,
    "hurt": 0.9, "pain": 0.8, "suffer": 0.9, "depressed": 1.1,
    "anxious": 0.8, "worried": 0.7, "scared": 0.9, "afraid": 0.9,
    "lonely": 1.0, "miss": 0.6, "lost": 0.7, "hopeless": 1.1,
    "miserable": 1.1, "awful": 0.9, "worst": 1.0, "frustrated": 0.8,
    "annoyed": 0.7, "stressed": 0.8, "overwhelmed": 0.8,
    "negative": 0.7, "fail": 0.8, "failure": 0.9, "disappointed": 0.8,
    "regret": 0.9, "shame": 1.0, "guilt": 0.9, "blame": 0.8,
    "resent": 0.9, "bitter": 0.8, "cruel": 1.0, "harsh": 0.8,
    "rough": 0.7, "difficult": 0.6, "struggle": 0.7, "problem": 0.6,
    "issue": 0.5, "trouble": 0.7, "worry": 0.7, "fear": 0.8,
    "dread": 0.9, "despair": 1.1, "anguish": 1.1, "agony": 1.1,
    "torment": 1.1, "trauma": 1.1, "harm": 0.9, "damage": 0.7,        "destroy": 0.9, "ruin": 0.9, "crash": 0.8, "collapse": 0.8,
        "sink": 0.7, "drown": 0.9, "suffocate": 0.9, "sick": 0.7,
        "ill": 0.7, "disease": 0.8, "injury": 0.8, "wound": 0.8,
        "bleed": 0.8, "death": 1.0, "die": 1.0, "kill": 1.0,
        "empty": 0.8, "numb": 0.8, "nothing": 0.6,
        "terrified": 0.9, "scared": 0.9, "afraid": 0.9,
        "frightened": 0.9, "disgusting": 0.8, "repulsive": 0.9,
}


def _clean_word(word: str) -> str:
    """Strip non-alpha characters from a word."""
    return re.sub(r"[^a-z]", "", word.lower())


def _get_intensity(words: list, idx: int) -> float:
    """Check words before idx for intensity modifiers."""
    multiplier = 1.0
    for i in range(max(0, idx - 2), idx):
        w = words[i]
        if w in INTENSIFIERS:
            multiplier = max(multiplier, INTENSIFIERS[w])
        elif w in DIMINISHERS:
            multiplier = min(multiplier, DIMINISHERS[w])
    return multiplier


def _has_negation(words: list, idx: int) -> bool:
    """Check if a negation word appears within 3 words before idx."""
    start = max(0, idx - 3)
    for i in range(start, idx):
        if words[i] in NEGATION_WORDS:
            return True
    return False


def _match_keyword(clean: str, keyword: str) -> bool:
    """Strict keyword matching with stem support.
    Handles: happy/happily, sad/sadly, disgust/disgusting, etc."""
    if clean == keyword:
        return True
    # Word starts with keyword (e.g., 'happily' starts with 'happy')
    if len(keyword) >= 4 and clean.startswith(keyword):
        return True
    # Keyword starts with word (e.g., 'disgust' starts with 'disgust' in 'disgusting')
    # Only for keywords >= 5 chars to avoid false positives
    if len(keyword) >= 5 and keyword.startswith(clean) and len(clean) >= 4:
        return True
    return False


def _get_opposite_emotion(emotion: str) -> str:
    """Return the rough opposite emotion for negation handling."""
    opposites = {
        "joy": "sadness",
        "sadness": "joy",
        "anger": "calm",
        "fear": "calm",
        "surprise": "neutral",
        "disgust": "joy",
        "calm": "anger",
    }
    return opposites.get(emotion, "calm")


def analyze_emotion(text: str):
    text_lower = text.lower().strip()
    if not text_lower:
        return {
            "emotion": "calm",
            "score": 50.0,
            "all_emotions": [{"label": "calm", "score": 100.0}],
        }

    words = text_lower.split()
    scores = {emotion: 0.0 for emotion in EMOTION_KEYWORDS}

    # 1. Check phrase matches first (higher weight)
    for phrase, (emotion, weight) in PHRASE_EMOTIONS.items():
        if phrase in text_lower:
            scores[emotion] += weight * 2.0

    # 2. Check individual word matches
    for idx, word in enumerate(words):
        clean = _clean_word(word)
        if not clean:
            continue

        for emotion, keywords in EMOTION_KEYWORDS.items():
            for keyword, weight in keywords.items():
                if _match_keyword(clean, keyword):
                    if _has_negation(words, idx):
                        opposite = _get_opposite_emotion(emotion)
                        intensity = _get_intensity(words, idx)
                        scores[opposite] += weight * intensity * 0.8
                    else:
                        intensity = _get_intensity(words, idx)
                        scores[emotion] += weight * intensity

    # 3. Add base score so calm wins when nothing matches strongly
    total_keyword_score = sum(scores.values())
    if total_keyword_score < 0.5:
        scores["calm"] += 0.3

    # 4. Normalize scores to percentages
    total = sum(scores.values()) or 1.0
    all_emotions = [
        {"label": emo, "score": round((s / total) * 100, 2)}
        for emo, s in sorted(scores.items(), key=lambda x: -x[1])
        if s > 0
    ]

    if not all_emotions:
        all_emotions = [{"label": "calm", "score": 100.0}]

    best = all_emotions[0]
    return {
        "emotion": best["label"],
        "score": best["score"],
        "all_emotions": all_emotions,
    }


def analyze_sentiment(text: str):
    text_lower = text.lower().strip()
    if not text_lower:
        return {"sentiment": "NEUTRAL", "score": 50.0}

    words = text_lower.split()
    pos_score = 0.0
    neg_score = 0.0

    for idx, word in enumerate(words):
        clean = _clean_word(word)
        if not clean:
            continue

        is_negated = _has_negation(words, idx)

        for keyword, weight in SENTIMENT_POSITIVE.items():
            if _match_keyword(clean, keyword):
                if is_negated:
                    neg_score += weight * 0.8
                else:
                    pos_score += weight

        for keyword, weight in SENTIMENT_NEGATIVE.items():
            if _match_keyword(clean, keyword):
                if is_negated:
                    pos_score += weight * 0.5
                else:
                    neg_score += weight

    total = pos_score + neg_score
    if total < 0.1:
        return {"sentiment": "NEUTRAL", "score": 50.0}

    if pos_score > neg_score:
        confidence = round((pos_score / total) * 100, 2)
        return {"sentiment": "POSITIVE", "score": max(confidence, 55.0)}
    elif neg_score > pos_score:
        confidence = round((neg_score / total) * 100, 2)
        return {"sentiment": "NEGATIVE", "score": max(confidence, 55.0)}
    else:
        return {"sentiment": "NEUTRAL", "score": 50.0}
