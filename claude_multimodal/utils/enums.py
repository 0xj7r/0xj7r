from enum import Enum
from langchain_core.pydantic_v1 import BaseModel, validator


class ToneOfVoice(Enum):
    FORMAL = "formal"
    INFORMAL = "informal"
    FRIENDLY = "friendly"
    SERIOUS = "serious"
    PLAYFUL = "playful"
    PROFESSIONAL = "professional"
    AUTHORITATIVE = "authoritative"
    INSPIRATIONAL = "inspirational"
    CONVERSATIONAL = "conversational"
    EDUCATIONAL = "educational"
    EMPATHETIC = "empathetic"
    HUMOROUS = "humorous"
    SINCERE = "sincere"
    PERSUASIVE = "persuasive"
    DEFAULT = "other"


class EntityType(Enum):
    ORGANIZATION = "organization"
    ANIMAL = "animal"
    PEOPLE = "people"
    INDIVIDUAL = "individual"
    OBJECT = "object"
    PRODUCT = "product"
    EVENT = "event"
    LOCATION = "location"
    MOVEMENT = "movement"
    TECHNOLOGY = "technology"
    CONCEPT = "concept"
    DEFAULT = "other"


class Entity(BaseModel):
    category: EntityType
    name: str

    @validator("category", pre=True)
    def validate_entity_type(cls, v):
        try:
            return EntityType(v)
        except ValueError:
            return EntityType.DEFAULT


class HTMLColor(Enum):
    ALICE_BLUE = "alice blue"
    ANTIQUE_WHITE = "antique white"
    AQUA = "aqua"
    AQUAMARINE = "aquamarine"
    AZURE = "azure"
    BEIGE = "beige"
    BISQUE = "bisque"
    BLACK = "black"
    BLANCHED_ALMOND = "blanched almond"
    BLUE = "blue"
    BLUE_VIOLET = "blue violet"
    BROWN = "brown"
    BURLY_WOOD = "burly wood"
    CADET_BLUE = "cadet blue"
    CHARTREUSE = "chartreuse"
    CHOCOLATE = "chocolate"
    CORAL = "coral"
    CORNFLOWER_BLUE = "cornflower blue"
    CORNSILK = "cornsilk"
    CRIMSON = "crimson"
    CYAN = "cyan"
    DARK_BLUE = "dark blue"
    DARK_CYAN = "dark cyan"
    DARK_GOLDEN_ROD = "dark golden rod"
    DARK_GRAY = "dark gray"
    DARK_GREEN = "dark green"
    DARK_KHAKI = "dark khaki"
    DARK_MAGENTA = "dark magenta"
    DARK_OLIVE_GREEN = "dark olive green"
    DARK_ORANGE = "dark orange"
    DARK_ORCHID = "dark orchid"
    DARK_RED = "dark red"
    DARK_SALMON = "dark salmon"
    DARK_SEA_GREEN = "dark sea green"
    DARK_SLATE_BLUE = "dark slate blue"
    DARK_SLATE_GRAY = "dark slate gray"
    DARK_TURQUOISE = "dark turquoise"
    DARK_VIOLET = "dark violet"
    DEEP_PINK = "deep pink"
    DEEP_SKY_BLUE = "deep sky blue"
    DIM_GRAY = "dim gray"
    DODGER_BLUE = "dodger blue"
    FIRE_BRICK = "fire brick"
    FLORAL_WHITE = "floral white"
    FOREST_GREEN = "forest green"
    FUCHSIA = "fuchsia"
    GAINSBORO = "gainsboro"
    GHOST_WHITE = "ghost white"
    GOLD = "gold"
    GOLDEN_ROD = "golden rod"
    GRAY = "gray"
    GREEN = "green"
    GREEN_YELLOW = "green yellow"
    HONEY_DEW = "honey dew"
    HOT_PINK = "hot pink"
    INDIAN_RED = "indian red"
    INDIGO = "indigo"
    IVORY = "ivory"
    KHAKI = "khaki"
    LAVENDER = "lavender"
    LAVENDER_BLUSH = "lavender blush"
    LAWN_GREEN = "lawn green"
    LEMON_CHIFFON = "lemon chiffon"
    LIGHT_BLUE = "light blue"
    LIGHT_CORAL = "light coral"
    LIGHT_CYAN = "light cyan"
    LIGHT_GOLDEN_ROD_YELLOW = "light golden rod yellow"
    LIGHT_GRAY = "light gray"
    LIGHT_GREEN = "light green"
    LIGHT_PINK = "light pink"
    LIGHT_SALMON = "light salmon"
    LIGHT_SEA_GREEN = "light sea green"
    LIGHT_SKY_BLUE = "light sky blue"
    LIGHT_SLATE_GRAY = "light slate gray"
    LIGHT_STEEL_BLUE = "light steel blue"
    LIGHT_YELLOW = "light yellow"
    LIME = "lime"
    LIME_GREEN = "lime green"
    LINEN = "linen"
    MAGENTA = "magenta"
    MAROON = "maroon"
    MEDIUM_AQUA_MARINE = "medium aqua marine"
    MEDIUM_BLUE = "medium blue"
    MEDIUM_ORCHID = "medium orchid"
    MEDIUM_PURPLE = "medium purple"
    MEDIUM_SEA_GREEN = "medium sea green"
    MEDIUM_SLATE_BLUE = "medium slate blue"
    MEDIUM_SPRING_GREEN = "medium spring green"
    MEDIUM_TURQUOISE = "medium turquoise"
    MEDIUM_VIOLET_RED = "medium violet red"
    MIDNIGHT_BLUE = "midnight blue"
    MINT_CREAM = "mint cream"
    MISTY_ROSE = "misty rose"
    MOCCASIN = "moccasin"
    NAVAJO_WHITE = "navajo white"
    NAVY = "navy"
    OLD_LACE = "old lace"
    OLIVE = "olive"
    OLIVE_DRAB = "olive drab"
    ORANGE = "orange"
    ORANGE_RED = "orange red"
    ORCHID = "orchid"
    PALE_GOLDEN_ROD = "pale golden rod"
    PALE_GREEN = "pale green"
    PALE_TURQUOISE = "pale turquoise"
    PALE_VIOLET_RED = "pale violet red"
    PAPAYA_WHIP = "papaya whip"
    PEACH_PUFF = "peach puff"
    PERU = "peru"
    PINK = "pink"
    PLUM = "plum"
    POWDER_BLUE = "powder blue"
    PURPLE = "purple"
    REBECCA_PURPLE = "rebecca purple"
    RED = "red"
    ROSY_BROWN = "rosy brown"
    ROYAL_BLUE = "royal blue"
    SADDLE_BROWN = "saddle brown"
    SALMON = "salmon"
    SANDY_BROWN = "sandy brown"
    SEA_GREEN = "sea green"
    SEA_SHELL = "sea shell"
    SIENNA = "sienna"
    SILVER = "silver"
    SKY_BLUE = "sky blue"
    SLATE_BLUE = "slate blue"
    SLATE_GRAY = "slate gray"
    SLATE_GREY = "slate grey"
    SNOW = "snow"
    SPRING_GREEN = "spring green"
    STEEL_BLUE = "steel blue"
    TAN = "tan"
    TEAL = "teal"
    THISTLE = "thistle"
    TOMATO = "tomato"
    TURQUOISE = "turquoise"
    VIOLET = "violet"
    WHEAT = "wheat"
    WHITE = "white"
    WHITE_SMOKE = "white smoke"
    YELLOW = "yellow"
    YELLOW_GREEN = "yellow green"
    DEFAULT = "other"


class ColorCategory(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    DEFAULT = "other"


class Colors(BaseModel):
    category: ColorCategory
    name: HTMLColor

    @validator("category", pre=True)
    def validate_category(cls, v):
        try:
            return ColorCategory(v)
        except ValueError:
            return ColorCategory.DEFAULT

    @validator("name", pre=True)
    def validate_name(cls, v):
        try:
            return HTMLColor[v.replace(" ", "_").upper()]
        except KeyError:
            return HTMLColor.DEFAULT


class TaglineType(Enum):
    COMMAND = "command"
    QUESTION = "question"
    STATEMENT = "statement"
    EXCLAMATION = "exclamation"
    INVITIATION = "invitation"
    QUOTATION = "quotation"
    TESTIMONIAL = "testimonial"
    CHALLENGE = "challenge"
    PROMISE = "promise"
    DEFAULT = "other"


class ValueProposition(Enum):
    PRODUCT_QUALITY = "product quality"
    INNOVATION = "innovation"
    PRICE_VALUE = "price value"
    CONVENIENCE = "convenience"
    CUSTOMER_SERVICE = "customer service"
    SOCIAL_PROOF = "social proof"
    PERSONALISATION = "personalisation"
    EXCLUSIVITY = "exclusivity"
    DEFAULT = "other"


class ContentType(Enum):
    PHOTOGRAPH = "photograph"
    ILLUSTRATION = "illustration"  
    SCREENSHOT = "screenshot"
    COLLAGE = "collage"   
    PRODUCT = "product"
    INFOPRAPHIC = "infographic"  
    CHART = "chart"
    DEFAULT = "other"  