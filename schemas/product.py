from pydantic import BaseModel, Field


class ClientCreate(BaseModel):
    name: str
    phone: str
    city: str


class ClientResponse(BaseModel):
    id: int
    name: str
    phone: str
    city: str

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int

    model_config = {"from_attributes": True}



class OrderCreate(BaseModel):
    client_id: int
    product_id: int
    quantity: int = Field(gt=0)


class OrderResponse(BaseModel):
    id: int
    client_id: int
    product_id: int
    quantity: int

    model_config = {"from_attributes": True}