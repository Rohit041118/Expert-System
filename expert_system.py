"""
expert_system.py
================
Fashion Recommendation Expert System
- Knowledge Base: IF-THEN rules
- Inference Engine: Forward Chaining
- Explanation Facility: Traces fired rules
"""

# ─────────────────────────────────────────────────────────────────────────────
# DATA STRUCTURES
# ─────────────────────────────────────────────────────────────────────────────

class Rule:
    """Represents a single IF–THEN rule in the knowledge base."""

    def __init__(self, rule_id, conditions, outfit, accessories, explanation):
        self.rule_id = rule_id          # Unique rule identifier
        self.conditions = conditions    # dict of {attribute: value}
        self.outfit = outfit            # Primary outfit recommendation
        self.accessories = accessories  # List of suggested accessories
        self.explanation = explanation  # Human-readable explanation string

    def matches(self, facts):
        """
        Forward chaining check: Does this rule's conditions match the given facts?
        Returns True only when ALL conditions are satisfied.
        """
        for attr, expected_val in self.conditions.items():
            if attr not in facts:
                return False
            actual = facts[attr].strip().lower()
            if isinstance(expected_val, list):
                if actual not in [v.lower() for v in expected_val]:
                    return False
            else:
                if actual != expected_val.lower():
                    return False
        return True


# ─────────────────────────────────────────────────────────────────────────────
# KNOWLEDGE BASE
# ─────────────────────────────────────────────────────────────────────────────

KNOWLEDGE_BASE = [

    # ── PARTY rules ──────────────────────────────────────────────────────────
    Rule(
        rule_id="R01",
        conditions={"occasion": "party", "style": "trendy", "gender": "male"},
        outfit="🎽 Graphic Tee + Slim-fit Jeans + White Sneakers",
        accessories=["Silver chain necklace", "Leather belt", "Minimalist watch"],
        explanation="For a trendy male party look, a graphic tee paired with slim-fit jeans and clean sneakers delivers a relaxed yet stylish vibe."
    ),
    Rule(
        rule_id="R02",
        conditions={"occasion": "party", "style": "trendy", "gender": "female"},
        outfit="👗 Off-shoulder Crop Top + High-waist Skirt + Block Heels",
        accessories=["Hoop earrings", "Sling bag", "Statement ring"],
        explanation="A trendy female party outfit — off-shoulder crop top with a high-waist skirt creates a chic, fashionable silhouette ideal for parties."
    ),
    Rule(
        rule_id="R03",
        conditions={"occasion": "party", "style": "formal", "gender": "male"},
        outfit="🕴️ Blazer + Turtleneck + Tailored Trousers + Chelsea Boots",
        accessories=["Pocket square", "Dress watch", "Leather belt"],
        explanation="A formal party look for males combines a sleek blazer with a turtleneck — sophisticated yet party-ready."
    ),
    Rule(
        rule_id="R04",
        conditions={"occasion": "party", "style": "formal", "gender": "female"},
        outfit="👠 Cocktail Dress + Strappy Heels",
        accessories=["Pearl necklace", "Clutch purse", "Subtle perfume"],
        explanation="A cocktail dress with strappy heels is the timeless formal party choice for females — elegant and refined."
    ),
    Rule(
        rule_id="R05",
        conditions={"occasion": "party", "style": "sporty"},
        outfit="🧢 Jogger Pants + Oversized Hoodie + Fresh Sneakers",
        accessories=["Cap", "Backpack", "Sports watch"],
        explanation="A sporty party outfit keeps things comfortable and street-smart with joggers and a hoodie — perfect for casual social events."
    ),
    Rule(
        rule_id="R06",
        conditions={"occasion": "party", "style": "classic"},
        outfit="👔 Dark Jeans + Oxford Shirt + Loafers",
        accessories=["Analog watch", "Leather belt", "Simple bracelet"],
        explanation="Classic party style — dark jeans with a clean Oxford shirt and loafers never goes out of fashion."
    ),

    # ── OFFICE / WORK rules ──────────────────────────────────────────────────
    Rule(
        rule_id="R07",
        conditions={"occasion": "office", "style": "formal", "gender": "male"},
        outfit="👔 Formal Shirt + Dress Trousers + Derby Shoes + Tie",
        accessories=["Leather briefcase", "Cufflinks", "Belt to match shoes"],
        explanation="Classic office formal for males — a crisp dress shirt with tailored trousers and Derby shoes projects professionalism."
    ),
    Rule(
        rule_id="R08",
        conditions={"occasion": "office", "style": "formal", "gender": "female"},
        outfit="💼 Pencil Skirt + Blouse + Court Heels",
        accessories=["Structured handbag", "Stud earrings", "Silk scarf"],
        explanation="The pencil skirt and blouse combination is a power-dressing staple for females in formal office environments."
    ),
    Rule(
        rule_id="R09",
        conditions={"occasion": "office", "style": "classic"},
        outfit="🧥 Chinos + Button-down Shirt + Loafers",
        accessories=["Watch", "Minimal bag", "Leather belt"],
        explanation="A classic office look — chinos with a button-down shirt balances professional and comfortable for everyday work."
    ),
    Rule(
        rule_id="R10",
        conditions={"occasion": "office", "style": "trendy", "gender": "female"},
        outfit="👗 Wide-leg Trousers + Fitted Blazer + Pointed Flats",
        accessories=["Statement earrings", "Tote bag", "Minimalist watch"],
        explanation="Wide-leg trousers with a fitted blazer is the modern, trendy take on office wear for females — polished and on-trend."
    ),
    Rule(
        rule_id="R11",
        conditions={"occasion": "office", "style": "trendy", "gender": "male"},
        outfit="🧥 Smart Joggers + Polo Shirt + Clean Leather Sneakers",
        accessories=["Slim watch", "Minimalist backpack", "No-show socks"],
        explanation="Modern office trend for males — smart joggers with a polo shirt bridges comfort and contemporary professional style."
    ),

    # ── CASUAL rules ─────────────────────────────────────────────────────────
    Rule(
        rule_id="R12",
        conditions={"occasion": "casual", "weather": "hot", "gender": "male"},
        outfit="🩳 Shorts + Plain T-Shirt + Slip-on Sandals",
        accessories=["Sunglasses", "Cap", "Minimal wristband"],
        explanation="Hot-weather casual for males — shorts and a tee with sandals keep you cool and relaxed all day."
    ),
    Rule(
        rule_id="R13",
        conditions={"occasion": "casual", "weather": "hot", "gender": "female"},
        outfit="👙 Sundress + Flat Sandals",
        accessories=["Straw hat", "Tote bag", "Sunglasses"],
        explanation="A light sundress with flat sandals is breezy and perfect for hot casual days for females."
    ),
    Rule(
        rule_id="R14",
        conditions={"occasion": "casual", "weather": "cold", "gender": "male"},
        outfit="🧣 Jeans + Thermal Innerwear + Pullover Sweater + Boots",
        accessories=["Beanie hat", "Scarf", "Woolen socks"],
        explanation="Cold-weather casual for males — layered with a thermal base and a cozy sweater over jeans with boots."
    ),
    Rule(
        rule_id="R15",
        conditions={"occasion": "casual", "weather": "cold", "gender": "female"},
        outfit="🧥 Corduroy Pants + Turtleneck + Long Cardigan + Ankle Boots",
        accessories=["Beanie", "Crossbody bag", "Warm scarf"],
        explanation="Cold-weather casual for females — corduroy and a cozy cardigan over a turtleneck is both stylish and warm."
    ),
    Rule(
        rule_id="R16",
        conditions={"occasion": "casual", "weather": "rainy"},
        outfit="🌧️ Waterproof Jacket + Dark Jeans + Rubber-sole Boots",
        accessories=["Compact umbrella", "Waterproof backpack", "Waterproof watch"],
        explanation="Rainy casual weather calls for a waterproof jacket and sturdy boots to stay dry while looking put-together."
    ),
    Rule(
        rule_id="R17",
        conditions={"occasion": "casual", "style": "sporty"},
        outfit="🏃 Track Pants + Moisture-wick Tee + Running Shoes",
        accessories=["Sports cap", "Gym bag", "Fitness tracker"],
        explanation="A sporty casual look — track pants and a breathable tee with running shoes keep you ready for active days."
    ),

    # ── WEDDING rules ────────────────────────────────────────────────────────
    Rule(
        rule_id="R18",
        conditions={"occasion": "wedding", "style": "formal", "gender": "male"},
        outfit="🤵 Three-piece Suit + Dress Shirt + Tie + Oxford Shoes",
        accessories=["Pocket square", "Cufflinks", "Dress watch"],
        explanation="A three-piece suit is the pinnacle of male wedding formal wear — timeless, distinguished, and appropriate."
    ),
    Rule(
        rule_id="R19",
        conditions={"occasion": "wedding", "style": "formal", "gender": "female"},
        outfit="👘 Anarkali Gown OR Evening Gown + Stilettos",
        accessories=["Statement necklace", "Clutch", "Chandelier earrings"],
        explanation="An elegant evening gown or Anarkali with stilettos is the quintessential formal wedding look for females."
    ),
    Rule(
        rule_id="R20",
        conditions={"occasion": "wedding", "style": "classic"},
        outfit="💍 Sherwani (male) / Saree (female) + Traditional Footwear",
        accessories=["Traditional jewelry", "Ethnic clutch", "Matching dupatta"],
        explanation="Classic wedding style — traditional ethnic wear like Sherwani or Saree always fits perfectly at weddings."
    ),
    Rule(
        rule_id="R21",
        conditions={"occasion": "wedding", "style": "trendy", "gender": "female"},
        outfit="✨ Lehenga Choli + Embellished Heels",
        accessories=["Maang tikka", "Jhumka earrings", "Potli bag"],
        explanation="A trendy wedding look for females — a modern Lehenga with embellished heels strikes the perfect balance of tradition and trend."
    ),
    Rule(
        rule_id="R22",
        conditions={"occasion": "wedding", "style": "trendy", "gender": "male"},
        outfit="🎩 Indo-western Suit + Jodhpuri Pants + Mojari Shoes",
        accessories=["Brooch", "Pocket square", "Traditional watch"],
        explanation="Indo-western fusion for males at weddings — Jodhpuri pants with a modern suit jacket is a sophisticated trending choice."
    ),

    # ── COLOR-SPECIFIC overrides ─────────────────────────────────────────────
    Rule(
        rule_id="R23",
        conditions={"color": "dark", "style": "formal"},
        outfit="🖤 Charcoal / Navy Suit + White Dress Shirt + Dark Shoes",
        accessories=["Dark tie", "Leather belt", "Watch with dark strap"],
        explanation="Dark colors in a formal setting exude authority and professionalism — charcoal or navy are the gold standard."
    ),
    Rule(
        rule_id="R24",
        conditions={"color": "light", "occasion": "casual"},
        outfit="🤍 Pastel Shirt + Cream Chinos + White Sneakers",
        accessories=["Light canvas bag", "Minimal jewelry", "Nude sandals"],
        explanation="Light pastel tones for casual wear create a fresh, airy, effortless look — ideal for daytime outings."
    ),
    Rule(
        rule_id="R25",
        conditions={"color": "bright", "occasion": "party"},
        outfit="🌈 Color-block Outfit + Bold Accessories",
        accessories=["Statement piece", "Contrasting shoes", "Bold bag"],
        explanation="Bright colors at a party scream confidence and fun — color-blocking makes you unforgettable on the dance floor."
    ),
    Rule(
        rule_id="R26",
        conditions={"color": "neutral", "occasion": "office"},
        outfit="🤎 Beige Blazer + White Shirt + Brown Trousers + Tan Shoes",
        accessories=["Tan leather bag", "Gold watch", "Minimal earrings"],
        explanation="Neutral tones in the office project calm professionalism — beige and tan combinations are timeless and versatile."
    ),

    # ── WEATHER overrides ────────────────────────────────────────────────────
    Rule(
        rule_id="R27",
        conditions={"weather": "cold"},
        outfit="🧥 Layered Outfit: Base layer + Mid layer (Fleece/Sweater) + Outer layer (Coat/Parka)",
        accessories=["Thermal gloves", "Woolen scarf", "Insulated boots"],
        explanation="Cold weather demands layering — a base thermal layer, a warm mid-layer, and a wind-resistant outer coat keeps you comfortable."
    ),
    Rule(
        rule_id="R28",
        conditions={"weather": "rainy", "occasion": "office"},
        outfit="☔ Trench Coat + Formal Outfit Underneath + Waterproof Brogues",
        accessories=["Compact umbrella", "Waterproof briefcase cover", "Extra socks"],
        explanation="For rainy office days, a classic trench coat protects your formal wear while keeping the professional look intact."
    ),
    Rule(
        rule_id="R29",
        conditions={"weather": "hot", "occasion": "office"},
        outfit="🌤️ Linen Shirt + Breathable Trousers + Light Loafers",
        accessories=["Lightweight watch", "Minimal bag", "Handkerchief"],
        explanation="Hot office weather calls for breathable linen — light colors and natural fabrics keep you cool during long work hours."
    ),

    # ── SPORTY special ───────────────────────────────────────────────────────
    Rule(
        rule_id="R30",
        conditions={"style": "sporty", "weather": "hot"},
        outfit="🏋️ Compression Shorts + Dry-fit Tee + Athletic Shoes",
        accessories=["Sports water bottle", "Sweat-wicking headband", "Fitness tracker"],
        explanation="Hot sporty days need performance wear — compression shorts and a dry-fit tee with athletic shoes maximize comfort and performance."
    ),
    Rule(
        rule_id="R31",
        conditions={"style": "sporty", "weather": "cold"},
        outfit="🏂 Thermal Base + Fleece Joggers + Athletic Jacket + High-top Sneakers",
        accessories=["Beanie", "Gloves", "Insulated gym bag"],
        explanation="Cold sporty weather — layer a thermal base with fleece joggers and an athletic jacket to stay warm without sacrificing mobility."
    ),

    # ── WEDDING + SPORTY rules ───────────────────────────────────────────────
    Rule(
        rule_id="R32",
        conditions={"occasion": "wedding", "style": "sporty", "gender": "male"},
        outfit="🏅 Smart Kurta Pajama + Clean White Sneakers + Minimal Accessories",
        accessories=["Simple bracelet", "Analog watch", "Light cologne"],
        explanation="For a sporty male attending a wedding, a smart Kurta Pajama with clean white sneakers blends cultural appropriateness with a relaxed, athletic sensibility."
    ),
    Rule(
        rule_id="R33",
        conditions={"occasion": "wedding", "style": "sporty", "gender": "female"},
        outfit="🌸 Palazzo Pants + Embroidered Crop Top + Wedge Sandals",
        accessories=["Stud earrings", "Potli bag", "Delicate bracelet"],
        explanation="Palazzo pants with an embroidered crop top offer a sporty yet festive wedding look for females — comfortable, elegant, and on-trend."
    ),

    # ── FALLBACK rule ────────────────────────────────────────────────────────
    Rule(
        rule_id="R00",
        conditions={},  # Matches anything — used as fallback
        outfit="👕 Smart Casual: Plain T-shirt + Jeans + Clean Sneakers",
        accessories=["Watch", "Belt", "Minimal bag"],
        explanation="Based on your unique combination of preferences, a clean smart-casual look is always a safe and stylish choice for any occasion."
    ),
]


# ─────────────────────────────────────────────────────────────────────────────
# INFERENCE ENGINE (Forward Chaining)
# ─────────────────────────────────────────────────────────────────────────────

class InferenceEngine:
    """
    Forward Chaining Inference Engine.
    
    Working Memory = user's confirmed facts (gender, occasion, weather, style, color).
    The engine scans ALL rules, fires those whose conditions match the facts,
    and returns the BEST match (most conditions matched first) + explanation.
    """

    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def infer(self, facts):
        """
        Run forward chaining over the knowledge base.
        Returns the best-matching rule (or fallback R00).
        """
        matched_rules = []

        for rule in self.kb:
            if rule.rule_id == "R00":
                continue  # Skip fallback during primary search
            if rule.matches(facts):
                matched_rules.append(rule)

        if not matched_rules:
            # Fire fallback rule
            fallback = next(r for r in self.kb if r.rule_id == "R00")
            return fallback, ["R00"]

        # Sort by specificity: more conditions matched = higher priority
        matched_rules.sort(key=lambda r: len(r.conditions), reverse=True)
        primary = matched_rules[0]
        fired_ids = [r.rule_id for r in matched_rules]
        return primary, fired_ids

    def build_explanation(self, rule, fired_ids, facts):
        """
        Explanation Facility: Returns a clean, user-friendly explanation.
        """
        return rule.explanation


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

engine = InferenceEngine(KNOWLEDGE_BASE)


def get_recommendation(facts: dict) -> dict:
    """
    Main entry point.
    Input:  facts = {gender, occasion, weather, style, color}
    Output: dict with outfit, accessories, explanation, fired_rules
    """
    rule, fired_ids = engine.infer(facts)
    explanation_html = engine.build_explanation(rule, fired_ids, facts)

    return {
        "outfit": rule.outfit,
        "accessories": rule.accessories,
        "explanation": explanation_html,
        "fired_rules": fired_ids,
        "rule_id": rule.rule_id,
    }
