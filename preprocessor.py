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
    words = text.split()
    processed = []
    for word in words:
        lower = word.lower().strip(".,!?")
        if lower in WORD_MAP:
            processed.append(word + " (" + WORD_MAP[lower] + ")")
        else:
            processed.append(word)
    return " ".join(processed)
