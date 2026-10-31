
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.product import Client, Order, Product
from schemas.product import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):

    orders = db.query(Order).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.post("/", response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):

    client = db.query(Client).filter(Client.id == order_data.client_id).first()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    product = db.query(Product).filter(Product.id == order_data.product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    new_order = Order(
        client_id=order_data.client_id,
        product_id=order_data.product_id,
        quantity=order_data.quantity
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_data: OrderCreate, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    client = db.query(Client).filter(Client.id == order_data.client_id).first()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    product = db.query(Product).filter(Product.id == order_data.product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    order.client_id = order_data.client_id
    order.product_id = order_data.product_id
    order.quantity = order_data.quantity

    db.commit()
    db.refresh(order)

    return order


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()

    return {"message": "Order deleted successfully"}
