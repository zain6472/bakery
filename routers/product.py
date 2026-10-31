from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.product import  Product
from schemas.product import (ProductCreate,ProductResponse)

router = APIRouter(prefix="/products",tags=["Products"])


@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):

    products = db.query(Product).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int,db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    return product


@router.post("/", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,db: Session = Depends(get_db)):

    new_product = Product(
        name=product_data.name,
        price=product_data.price,
        stock=product_data.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int,product_data: ProductCreate,db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")

    product.name = product_data.name
    product.price = product_data.price
    product.stock = product_data.stock

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int,db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}