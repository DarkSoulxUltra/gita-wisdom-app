import requests
import json
import math
import random
from collections import defaultdict

VERBOSE = True

VERSE_URL = "https://raw.githubusercontent.com/gita/gita/main/data/verse.json"
TRANSLATION_URL = "https://raw.githubusercontent.com/gita/gita/main/data/translation.json"

def assign_mood(text, chapter_num):
    text = text.lower()
    
    # Chapter 1 Manual Overrides (Arjuna's Despair)
    if chapter_num == 1:
        if "fear" in text or "tremble" in text or "bow" in text:
            return "anxiety"
        if "sin" in text or "grief" in text or "slay" in text:
            return "sad"
        return "lonely"

    # Keyword based for other chapters
    if "anger" in text or "wrath" in text or "fury" in text or "delusion" in text:
        return "anger"
    if "peace" in text or "calm" in text or "tranquil" in text or "serene" in text:
        return "peace"
    if "fear" in text or "anxiety" in text or "worry" in text or "despair" in text:
        return "anxiety"
    if "sorrow" in text or "grief" in text or "lament" in text or "pain" in text:
        return "sad"
    if "lazy" in text or "inaction" in text or "sloth" in text or "sleep" in text:
        return "lazy"
    if "alone" in text or "self" in text or "solitude" in text:
        return "lonely"
    if "protect" in text or "dharma" in text or "righteous" in text or "duty" in text:
        return "protection"
    
    return "happy"

def generate_example(mood):
    examples = {
        "anxiety": [
            {"situation": "You are overthinking results before a big exam or interview.", "insight": "Focus purely on your effort and preparation instead of worrying about the final outcome."},
            {"situation": "You are stressed about a future event you cannot control.", "insight": "Do your best in the present moment and let go of the anxiety over things outside your control."},
            {"situation": "You feel paralyzed by the fear of making a wrong decision.", "insight": "Overthinking clouds your judgement. Act with a clear, calm mind and trust the process."}
        ],
        "anger": [
            {"situation": "Someone just insulted you or cut you off in traffic.", "insight": "Take a deep breath and pause before reacting. A calm response is much stronger than a furious reaction."},
            {"situation": "You are holding a grudge against a friend who wronged you.", "insight": "Anger destroys your own peace of mind. Forgive them, not because they deserve it, but because you deserve peace."},
            {"situation": "You are frustrated because things aren't going your way.", "insight": "Anger clouds logic and leads to delusion. Choose patience and evaluate the situation objectively."}
        ],
        "sad": [
            {"situation": "You recently experienced a failure or lost something important.", "insight": "Loss is a natural, unavoidable part of life. Accept it gracefully, and you will continue to grow."},
            {"situation": "You are feeling down because of a temporary setback.", "insight": "Tough times are temporary. Don't attach your core happiness to temporary worldly outcomes."},
            {"situation": "You miss a phase of your life that has passed.", "insight": "Keep your head up. Every ending is just a new beginning in disguise. The soul's journey continues."}
        ],
        "peace": [
            {"situation": "You are caught in a chaotic, fast-paced work environment.", "insight": "A calm and peaceful mind gives you incredible clarity in your decisions, even in chaos."},
            {"situation": "You are endlessly chasing the next big achievement.", "insight": "True happiness comes from within, not from external achievements. Find stillness inside you."},
            {"situation": "You feel overwhelmed by material desires and trends.", "insight": "Let go of excessive desires and attachments to find deep, lasting inner tranquility."}
        ],
        "lazy": [
            {"situation": "You are procrastinating on an important project because it feels too big.", "insight": "Start with one small step instead of avoiding the work completely. Action cures fear."},
            {"situation": "You feel like skipping your daily responsibilities today.", "insight": "Inaction is also a choice, and it leads to stagnation. Do the work that is required of you without making excuses."},
            {"situation": "You are waiting for the 'perfect moment' to start.", "insight": "Don't let laziness rob you of your true potential. Discipline is the bridge between goals and accomplishment."}
        ],
        "lonely": [
            {"situation": "You feel isolated because you don't fit in with the crowd.", "insight": "You are never truly alone when you are comfortable with yourself. Your true self is already complete."},
            {"situation": "You are spending a weekend completely by yourself.", "insight": "Solitude is a superpower. Use this time to build self-discipline and profound self-awareness."},
            {"situation": "You are constantly seeking validation and company from others.", "insight": "Realize that the divine energy resides within you at all times. Look inward for fulfillment."}
        ],
        "protection": [
            {"situation": "You see someone being treated unfairly but are afraid to speak up.", "insight": "Stand firm for what is right (Dharma), even if you are standing alone."},
            {"situation": "You are tempted to take an unethical shortcut at work.", "insight": "Protect your morals and values, because they are your true wealth. Do your duty honestly."},
            {"situation": "You feel vulnerable and unsure of your path.", "insight": "Have faith. When you walk on the path of truth and righteousness, you are always protected."}
        ],
        "happy": [
            {"situation": "You just achieved a massive goal and feel on top of the world.", "insight": "Stay humble in your happiness. Treat both success and failure with an equal, balanced mind."},
            {"situation": "You are having a wonderful, joyous day.", "insight": "Channel your positive energy into doing good for others. Be a source of light to everyone around you."},
            {"situation": "You feel perfectly content with your life right now.", "insight": "True joy isn't just in celebrating victories, but in living a balanced, purposeful life."}
        ]
    }
    pool = examples.get(mood, examples["happy"])
    return random.choice(pool)

print("Fetching Bhagavad Gita verses and translations...")
try:
    verses_data = requests.get(VERSE_URL).json()
    translations_data = requests.get(TRANSLATION_URL).json()
except Exception as e:
    print("Failed to download dataset.", e)
    exit(1)

# Preferred authors
PREF_ENG = "Shri Purohit Swami"
FALLBACK_ENG = "Swami Sivananda"
PREF_HIN = "Swami Tejomayananda"
FALLBACK_HIN = "Swami Ramsukhdas"

translations_map = defaultdict(lambda: {"english": "", "hindi": ""})

# First pass: map preferred authors
for trans in translations_data:
    v_id = trans.get("verse_id")
    lang = trans.get("lang")
    desc = trans.get("description", "").strip()
    author = trans.get("authorName", "")
    
    if not v_id or not desc: continue
    if "No changes needed" in desc or len(desc) < 10: continue
    
    if lang == "english":
        if author == PREF_ENG:
            translations_map[v_id]["english"] = desc
        elif not translations_map[v_id]["english"] and author == FALLBACK_ENG:
            translations_map[v_id]["english"] = desc
        elif not translations_map[v_id]["english"]:
            translations_map[v_id]["english"] = desc
            
    if lang == "hindi":
        if author == PREF_HIN:
            translations_map[v_id]["hindi"] = desc
        elif not translations_map[v_id]["hindi"] and author == FALLBACK_HIN:
            translations_map[v_id]["hindi"] = desc
        elif not translations_map[v_id]["hindi"]:
            translations_map[v_id]["hindi"] = desc

all_verses = []

for verse in verses_data:
    v_id = verse.get("id")
    chapter_num = verse.get("chapter_number")
    verse_num = verse.get("verse_number")
    sanskrit_text = verse.get("text", "")
    
    eng_trans = translations_map[v_id]["english"]
    hin_trans = translations_map[v_id]["hindi"]
    
    if not eng_trans: eng_trans = "Translation not available."
    if not hin_trans: hin_trans = "अनुवाद उपलब्ध नहीं है।"
        
    mood = assign_mood(eng_trans, chapter_num)
    
    obj = {
        "verse": f"{chapter_num}.{verse_num}",
        "mood": mood,
        "sanskrit": sanskrit_text,
        "hindi": hin_trans,
        "english": eng_trans,
        "example": generate_example(mood)
    }
    
    all_verses.append(obj)

all_verses.sort(key=lambda x: (int(x["verse"].split('.')[0]), int(x["verse"].split('.')[1])))

print(f"Total verses processed: {len(all_verses)}")

chunk_size = math.ceil(len(all_verses) / 7)

for i in range(7):
    chunk = all_verses[i * chunk_size:(i + 1) * chunk_size]
    filename = f"gita_part{i+1}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chunk, f, ensure_ascii=False, indent=2)
        
    print(f"Created {filename} with {len(chunk)} verses")

print("All JSON files generated successfully!")