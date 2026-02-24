from pydantic import BaseModel, Field

# Was going to add enum to validate breed, but ran out of time
# class CatBreed(str, Enum):
#     siamese = "siamese"
#     maine_coon = "maine_coon"
#     ragdoll = "ragdoll"
#     sphynx = "sphynx"
#     bengal = "bengal"


class Cat(BaseModel):
    # Set None = None to make this Key optional.
    breed: str | None = None
    name: str
    favorite_toy: str
    # Pydantic validation
    age: int = Field(gt=0, le=40)
    picture: str
