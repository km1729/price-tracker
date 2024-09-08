import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from typing import List, Union, Dict, Annotated, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

import models 
from database import engine, get_db
import price_tracker.chemistwarehouse as cw

from pydantic import BaseModel

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PriceOut(BaseModel):
    price: float
    updated_on: datetime

class ProductOut(BaseModel):
    id: int
    brand_name: Optional[str] 
    product_name: str
    product_id: str
    supplier: Optional[str] 
    url: str
    prices: List[PriceOut] 

    class Config:
        from_attributes = True

@app.get("/")
def greet():
    return {'message':'hello price-tracker'}

@app.post("/products")
def add_products(url:str, db: Session = Depends(get_db)):
    company, product_name, price, product_id, supplier = cw.extract(url)

    # Check if the product already exists in the database
    existing_product = db.query(models.Product).filter_by(url=url).first()
    
    if existing_product:
        # If the product exists, update the price with the existing product's ID
        price_entry = models.Price(price=price, product_id=existing_product.id)
        db.add(price_entry)
        db.commit()
        return {"product_id": existing_product.id, "price_id": price_entry.id, "message": "Price updated for existing product"}
    
    # If the product does not exist, add the new product and its price
    product_entry = models.Product(url=url, brand_name=company, product_name =product_name, product_id=product_id, supplier=supplier)
    db.add(product_entry)
    db.commit()
    db.refresh(product_entry)
    
    price_entry = models.Price(price=price, product_id=product_entry.id)
    db.add(price_entry)
    db.commit()

    return {"product_id": product_entry.id, "price_id": price_entry.id, "message": "Product and price added successfully"}

@app.get("/products/", response_model=List[ProductOut])
def product_list(db: Session = Depends(get_db), product_id: Optional[int] = None):
    if product_id:
        result = db.query(models.Product).options(joinedload(models.Product.prices)).filter(models.Product.id == product_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Product not found")
        return [result]  # 단일 객체를 리스트로 감싸서 반환
    else:
        result = db.query(models.Product).options(joinedload(models.Product.prices)).all()
    return result  # 리스트 형태로 반환

if __name__ == '__main__':
     # This part should ideally be done in a testing environment or in a script.
    from sqlalchemy.orm import Session
    from database import SessionLocal

    def run_test():
        db = SessionLocal()
        try:
            # url = 'https://www.chemistwarehouse.com.au/buy/56237/healthy-care-royal-jelly-1000mg-365-capsules'
            # add_products(url, db)
            result = product_list(db)
            for product in result:
                print(f"Product ID: {product.id}, Product Name: {product.product_name}, Brand Name: {product.brand_name}")
                for price in product.prices:
                    print(f"  Price: ${price.price}, Updated On: {price.updated_on}")
        finally:
            db.close()

    run_test()