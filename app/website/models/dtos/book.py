from pydantic import BaseModel, Field

class BookFilterInputModel(BaseModel):
    keyword: str
    category: list[str] = []
    min_price_input: float = Field(default=0)
    max_price_input: float
    min_rate_input: int = Field(ge=0, le=5)
    max_rate_input: int = Field(ge=0, le=5)
    sort_by: str