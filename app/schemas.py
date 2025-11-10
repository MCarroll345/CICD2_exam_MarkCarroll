from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict

NameStr = Annotated[str, StringConstraints(min_length=1, max_length=100)]
EmailStr = Annotated[str, StringConstraints(min_length=1, max_length=100)]
CustSinceInt = Annotated[int, range(2000 - 2100)]
OrderNumInt = Annotated[int, range(3 - 20)]
TotalCentInt = Annotated[int, range(1 - 1000000)]

class CustomerCreate(BaseModel) :
    name : NameStr
    email : EmailStr
    customer_since : CustSinceInt
    
class CustomerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int 
    name : NameStr
    email : EmailStr
    customer_since : CustSinceInt

class CustomerPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name : Optional[NameStr] = None
    email : Optional[EmailStr] = None
    customer_since : Optional[CustSinceInt] = None

class OrderCreate(BaseModel):
    order_number : OrderNumInt
    total_cents : TotalCentInt
    customer_id : int 

class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    order_number : OrderNumInt
    total_cents : TotalCentInt
    customer_id : int 

class OrdersCust(OrderRead):
    customer: Optional["Customer"] = None