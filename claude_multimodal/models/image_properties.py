from typing import List, Optional
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from utils.enums import EntityType, Colors, ToneOfVoice, TaglineType, ValueProposition


class ImageProperties(BaseModel):
    """
    Pydantic model to define the structure of properties extracted from image summaries.
    """

    entity: Optional[List[EntityType]] = Field(
        default_factory=list, description="Unique types of entities"
    )
    color: Optional[List[Colors]] = Field(
        default_factory=list,
        description="Primary, secondary, and tertiary colors in the image",
    )
    tagline: Optional[str] = Field(
        None, description="The main text tag line used in the image"
    )
    tagline_type: Optional[TaglineType] = Field(
        None, description="Categorisation of the tagline"
    )
    tone_of_voice: Optional[List[ToneOfVoice]] = Field(
        default_factory=list, description="Tone of voice of the text"
    )
    value_proposition: Optional[List[ValueProposition]] = Field(
        default_factory=list,
        description="The core value proposition mentioned in the image",
    )
    cta_element: Optional[List[str]] = Field(
        default_factory=list, description="Call-to-actions present in the image"
    )
    language: Optional[List[str]] = Field(
        default_factory=list, description="Language of the text in the image"
    )

    # Normalize all outputs to lowercase
    _normalize_to_lowercase = validator("*", pre=True, allow_reuse=True)(
        lambda v: v.lower() if isinstance(v, str) else v
    )

    @validator("entity", pre=True, each_item=True)
    def validate_entity(cls, v):
        try:
            return EntityType(v)
        except ValueError:
            return EntityType.DEFAULT

    @validator("tone_of_voice", pre=True, each_item=True)
    def validate_tone_of_voice(cls, v):
        try:
            return ToneOfVoice(v)
        except ValueError:
            return ToneOfVoice.DEFAULT

    @validator("tagline_type", pre=True, each_item=True)
    def validate_tagline_type(cls, v):
        try:
            return TaglineType(v)
        except ValueError:
            return TaglineType.DEFAULT

    @validator("value_proposition", pre=True, each_item=True)
    def validate_value_proposition(cls, v):
        try:
            return ValueProposition(v)
        except ValueError:
            return ValueProposition.DEFAULT