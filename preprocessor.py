import re

PIDGIN_MAP = [
    (r"\bwater\s+no\s+dey\b", "there is no water"),
    (r"\brain\s+no\s+dey\b", "there is no rain"),
    (r"\bdon\s+spoil\b", "has spoiled"),
    (r"\bdon\s+die\b", "has died"),
    (r"\bdon\s+yellow\b", "has turned yellow"),
    (r"\bdon\s+dry\b", "has dried"),
    (r"\bdon\s+rot\b", "has rotted"),
    (r"\bdon\s+finish\b", "has finished"),
    (r"\bna\s+wetin\b", "what is"),
    (r"\bhow\s+i\s+go\b", "how do I"),
    (r"\bwhich\s+kain\b", "what kind of"),
    (r"\bno\s+dey\b", "is not"),
    (r"\be\s+don\b", "it has"),
    (r"\bwetin\b", "what"),
    (r"\bdey\b", "is"),
    (r"\babeg\b", "please"),
    (r"\bdem\b", "them"),
    (r"\bdis\b", "this"),
    (r"\bdat\b", "that"),
    (r"\bfit\b", "can"),
    (r"\bsabi\b", "know"),
    (r"\bplenty\b", "many"),
    (r"\bwey\b", "that"),
    (r"\buna\b", "you"),
]

WORD_MAP = {
    "tomatoe": "tomato",
    "cassva": "cassava",
    "cassawa": "cassava",
    "fertlizer": "fertilizer",
    "fertliser": "fertilizer",
    "pestside": "pesticide",
    "hervest": "harvest",
    "irigation": "irrigation",
    "okoro": "okra",
    "okro": "okra",
    "ugu": "fluted pumpkin",
    "egusi": "melon seed",
    "ewedu": "jute mallow",
    "ogbono": "bush mango",
    "ata rodo": "scotch bonnet pepper",
    "gbure": "waterleaf",
    "tete": "amaranth",
    "ila": "okra",
    "efo": "leafy vegetable",
    "agbado": "maize",
    "oka": "maize",
    "dawa": "millet",
    "gero": "millet",
    "shinkafa": "rice",
    "iresi": "rice",
    "rogo": "cassava",
}

def preprocess(text):
    # Step 1: Pidgin to English
    for pattern, replacement in PIDGIN_MAP:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    # Step 2: Local names and misspellings to English
    words = text.split()
    processed = []
    for word in words:
        lower = word.lower().strip(".,!?")
        if lower in WORD_MAP:
            processed.append(word + " (" + WORD_MAP[lower] + ")")
        else:
            processed.append(word)
    return " ".join(processed)

if __name__ == "__main__":
    tests = [
        "wetin make my ugu dey yellow",
        "how i go plant egusi dis season",
        "my rogo don rot",
        "abeg which kain fertlizer good for agbado",
        "water no dey, how i go do irigation",
    ]
    for q in tests:
        print(f"IN:  {q}")
        print(f"OUT: {preprocess(q)}")
        print()
