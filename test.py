from pydantic import BaseModel, Field, ValidationError

class TestModel(BaseModel):
    email: str = Field(..., pattern=r'^\S+@\S+\.\S+$')

try:
    TestModel(email="wrong@outlook.com")
except ValidationError as e:
    print(e)