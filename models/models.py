from sqlalchemy import Integer, String, ForeignKey, DateTime, func,Text,DECIMAL,Float
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase            
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime


class Base(DeclarativeBase):
    pass

class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
# Supplier-Product Table
supplier_product_association = ('supplier_product_association',
    Base.metadata,
    mapped_column('supplier_id', Integer, ForeignKey('supplier.id')),
    mapped_column('product_id', Integer, ForeignKey('product.id'))  )  
    
class User(Base, BaseModel):
    __tablename__ = 'user'
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username:Mapped[str] = mapped_column(String(200), unique=True)
    password:Mapped[str] = mapped_column(String(255))    


    
class product(Base, BaseModel):
    __tablename__= 'product'
    product_id:Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at:Mapped[DateTime]= mapped_column(DateTime,insert_default=func.now())
    product_name:Mapped[str] = mapped_column(String(255))
    description:Mapped[str] = mapped_column(Text)
    price:Mapped[DECIMAL] = mapped_column(DECIMAL(precision=10, scale=2))
    quantity_available:Mapped[int] = mapped_column(Integer)
    category:Mapped[str]= mapped_column(String(255))
    supplier_id:Mapped[int] = mapped_column(Integer, ForeignKey('suppliers.supplier_id'))

class Supplier(Base):
    __tablename__ = 'supplier'
    Supplier_id:Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_name:Mapped[str] = mapped_column(String(255), nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=func.now())

class Transaction(Base):
    __tablename__ = 'transaction'

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id:Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False)
    transaction_type:Mapped[str] = mapped_column(str(TransactionType), nullable=False)
    quantity:Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price:Mapped[float] = mapped_column(Float, nullable=False)
    transaction_date:Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    payment_method:Mapped[str] = mapped_column(String(255), nullable=False)
    customer_name:Mapped[str] = mapped_column(String(255))
    shipping_address:Mapped[str] = mapped_column(String)

