from sqlalchemy import Column,Integer,String,DateTime
from database.db import Base
from datetime import timedelta,datetime,timezone


class Products(Base):
  __tablename__ ="Product"
  id = Column(Integer,primary_key=True)
  name= Column(String(200),nullable=False)
  stock = Column(Integer,default=1)
  create_at = Column(DateTime,default=datetime.now)