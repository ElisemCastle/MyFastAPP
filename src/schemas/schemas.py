from pydantic import BaseModel, Field
from enum import Enum

# Enum limits the list of allowed values.
# Must pass in string to support json.
class CatBreed(str, Enum):
    # Python attr = jsonvalue
    gray                = "grey"
    tuxedo              = "tuxedo"
    ragdoll             = "ragdoll"
    white               = "white"
    scottish_fold       = "scottish_fold"
    calico              = "calico"
    russian_blue        = "russian_blue"
    gray_tabby          = "gray_tabby"
    main_coon           = "main_coon"
    tabby               = "tabby"
    british_shorthair   = "british_shorthair"
    sphynx              = "sphynx"
    siamese             = "siamese"
    orange_tabby        = "orange_tabby"
    black               = "black"
    persian             = "persian"
    orange              = "orange"
    bengal              = "bengal"


class Cat(BaseModel):
    # Limits the breeds that can be passed in.
    breed: CatBreed
    name: str
    favorite_toy: str
    # Pydantic validation
    age: int = Field(gt=0, le=40)
    # Set None = None to make this Key optional.
    picture: str | None = None
