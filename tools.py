from fastapi import FastAPI,Form,Depends
from sqlalchemy.orm import Session
from database.db import Base,SessionLocal,engine
from models.product import Products
from langchain.tools import tool



app = FastAPI()

@tool
async def insert_items(name:str=Form,stock:int=Form(...))->str:
  """Insert the item when user give but must ensure that all filed are required when one filed are missed recognize the user  about the fields"""
  db = SessionLocal()
  try:
    item = db.query(Products).filter(Products.name == name).first()

    if  item:
      item.stock+=stock
      db.commit()
      db.refresh(item)
      return f"{item.stock}is update"

    new_item = Products(
      name=name,
      stock=stock
    ) 
    db.add(new_item)
    db.commit() 
    db.refresh(new_item)
    return {
        "items":item,
        "message":f"{name},{stock} are successfully added"
      }  
  finally:
    db.close()

  


@tool
async def deleted_product(name:str=Form(...))->str:
  """Deleted the  items when user said  search the name from database table then deleted the item the.
    Return the message . 
  
  """

  db=SessionLocal()
  try:
    item = db.query(Products).filter(Products.name == name).first()

    if not item:
      return{
        "message":"Product not Found"
      }
    db.delete(item)
    db.commit()
    return{
      "message":f"{item} is successfully delete"
    }

  finally:
    db.close()



@tool
async def search_all(name:str=Form(...),stock:int=Form(...)):
  """ Search the items by name and return the details about it like stock based on  the information store on  database table"""

  
  db=SessionLocal()
  try:
    item = db.query(Products).filter(Products.name == name).first()
    if not item:
          return{
            "message":"Product not Found"
          }

  
    return{
      "message":f"Product {item.name} stock{item.stock}  "
    }
  finally:
    db.close()  

  






