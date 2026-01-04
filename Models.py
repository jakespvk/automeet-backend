# from typing import List, Optional, Annotated
from pydantic import BaseModel, EmailStr


class Subscription(BaseModel):
    email: EmailStr
    price: int
    column_limit: int
    row_limit: int
    poll_frequency: int
