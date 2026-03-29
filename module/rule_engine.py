import json
import os
import re
from database.database import get_connection

RULES_FILE = "rules.json"

# LOAD RULES
def load_rules():

    if not os.path.exists(RULES_FILE):
        return {}, None, {}, {}

    with open(RULES_FILE, "r") as f:
        data = json.load(f)

    word_map = {}
    words = []

    word_categories = ["positive_words", "negative_words", "spam"]

    for category in word_categories:
        for word, score in data.get(category, {}).items():

            word_lower = word.lower()

            word_map[word_lower] = {
                "score": float(score),
                "category": category
            }

            words.append(re.escape(word_lower))

    pattern = re.compile(r"\b(" + "|".join(words) + r")\b") if words else None

    phrases = {
        **data.get("positive_phrases", {}),
        **data.get("negative_phrases", {})
    }

    patterns = data.get("rule_patterns", {})

    intensifiers = data.get("intensifiers", {})
    negators = data.get("negators", {})

    return word_map, pattern, phrases, patterns, intensifiers, negators



# APPLY RULES TO CHUNKS
def apply_rules():

    word_map, pattern, phrases, patterns, intensifiers, negators = load_rules()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, chunk FROM chunks")
    rows = cursor.fetchall()

    updates = []

    for chunk_id, text in rows:

        text_lower = text.lower()

        score = 0
        matched_words = []
        categories = []

        # WORD MATCHING
        if pattern:
            matches = pattern.findall(text_lower)

            for word in set(matches):

                rule = word_map[word]

                score += rule["score"]
                matched_words.append(word)
                categories.append(rule["category"])

        # PHRASE MATCHING
        for phrase, val in phrases.items():
            if phrase in text_lower:
                score += float(val)
                matched_words.append(phrase)
                categories.append("phrase")

        # INTENSIFIERS 
        words = text_lower.split()
        for w in words:
            if w in intensifiers:
                score *= float(intensifiers[w])
                matched_words.append(w)

        # NEGATORS
        for w in words:
            if w in negators:
                score *= -1
                matched_words.append(w)

        # REGEX PATTERNS 
        for name, obj in patterns.items():
            pattern_str = obj.get("pattern", "")
            val = obj.get("score", 0)

            try:
                found = re.findall(pattern_str, text)
                if found:
                    score += len(found) * float(val)
                    matched_words.append(name)
                    categories.append("pattern")
            except:
                pass

        # SENTIMENT 
        if score > 0:
            sentiment = "Positive"
        elif score < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        updates.append(
            (
                score,
                ",".join(set(matched_words)),
                ",".join(set(categories)),
                sentiment,
                chunk_id
            )
        )

        if len(updates) >= 5000:

            cursor.executemany("""
            UPDATE chunks
            SET score=?,
                matched_rules=?,
                rule_category=?,
                sentiment=?
            WHERE id=?
            """, updates)

            updates = []

    if updates:
        cursor.executemany("""
        UPDATE chunks
        SET score=?,
            matched_rules=?,
            rule_category=?,
            sentiment=?
        WHERE id=?
        """, updates)

    conn.commit()
    conn.close()