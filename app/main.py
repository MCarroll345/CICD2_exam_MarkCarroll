# app/main.py
from typing import Optional

from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import engine, SessionLocal
from app.models import Base, CustomerDB, OrdersDB
from app.schemas import CustomerCreate, CustomerRead, CustomerPatch, OrderCreate, OrderRead

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (dev/exam). Prefer Alembic in production.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


# ---- Health ----
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/customers", response_model = CustomerRead, status_code = status.HTTP_201_CREATED)
def add_customer(payload: CustomerCreate, db:Session = Depends(get_db)):
    customer = CustomerDB(**payload.model_dump())
    db.add(customer)
    try:
        db.commit()
        db.refresh(customer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="User already exists")
    return customer

@app.get("/api/customers", response_model = list[CustomerRead])
def get_all_customers(db:Session = Depends(get_db)):
    stmt = select(CustomerDB).order_by(CustomerDB.id)
    result = db.execute(stmt)
    customers = result.scalars().all()
    return customers 

@app.get("/api/customers/{id}", response_model = CustomerRead)
def get_customer(id = int, db:Session = Depends(get_db)):
    customer = db.get(CustomerDB, id)
    if not customer:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    return customer

@app.put("/api/customers/{cust_id}", response_model = CustomerRead, status_code = status.HTTP_201_CREATED)
def update_customer(payload:CustomerCreate, cust_id = int, db:Session = Depends(get_db)):
    customer = db.get(CustomerDB, cust_id)
    if not customer:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    customer = CustomerDB(**payload.model_dump())
    try:
        stmt = update(CustomerDB).where(CustomerDB.id==cust_id).values(id=customer.id,name=customer.name,email=customer.email,customer_since=customer.customer_since)
        db.execute(stmt)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="User already exists")
    return customer

@app.patch("/api/customers/{cust_id}", response_model = CustomerPatch, status_code = status.HTTP_201_CREATED)
def patch_customer(payload:CustomerPatch, cust_id = int, db:Session = Depends(get_db)):
    customer_details = payload.model_dump(exclude_unset=True)
    customer = db.get(CustomerDB, cust_id)
    if not customer:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    try:
        stmt = update(CustomerDB).where(CustomerDB.id==cust_id).values(**customer_details)
        db.execute(stmt)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="User already exists")
    return customer_details

@app.delete("/api/customers/{cust_id}", response_model = CustomerRead)
def get_customer(id = int, db:Session = Depends(get_db)):
    customer = db.get(CustomerDB, id)
    if not customer:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    try:
        stmt = delete(CustomerDB).where(CustomerDB.id==cust_id)
        db.execute(stmt)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Error")
    return customer

@app.post("/api/orders", response_model = OrderRead, status_code = status.HTTP_201_CREATED)
def add_order(payload: OrderCreate, db:Session = Depends(get_db)):
    order = OrdersDB(**payload.model_dump())
    customer = db.get(CustomerDB, order.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    db.add(order)
    try:
        db.commit()
        db.refresh(order)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Order already exists")
    return order
    
@app.get("/api/orders", response_model = list[OrderRead])
def get_all_orders(db:Session = Depends(get_db)):
    stmt = select(OrderRead).order_by(OrderRead.id)
    result = db.execute(stmt)
    orders = result.scalars().all()
    return orders 

@app.post("/api/orders", response_model = OrderRead, status_code = status.HTTP_201_CREATED)
def add_order(payload: OrderCreate, db:Session = Depends(get_db)):
    order = OrdersDB(**payload.model_dump())
    customer = db.get(CustomerDB, order.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    db.add(order)
    try:
        db.commit()
        db.refresh(order)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Order already exists")
    return order