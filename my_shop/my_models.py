import databases
import sqlalchemy
from sqlalchemy import create_engine, ForeignKey
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime



DATABASE_URL = "sqlite:///my_shop/instance/mydatabase.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

login = sqlalchemy.Table(
    "login",
    metadata,
    sqlalchemy.Column("email", sqlalchemy.String(120)),
    sqlalchemy.Column("password", sqlalchemy.String(15)),
)

user = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(80)),
    sqlalchemy.Column("surname", sqlalchemy.String(80)),
    sqlalchemy.Column("email", sqlalchemy.String(120)),
    sqlalchemy.Column("password", sqlalchemy.String(15)),
)

product = sqlalchemy.Table(
    "product",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("product_name", sqlalchemy.String(80)),
    sqlalchemy.Column("product_type", sqlalchemy.String(15)),
    sqlalchemy.Column('photo', sqlalchemy.String(300)),
    sqlalchemy.Column('content', sqlalchemy.Text),
    sqlalchemy.Column('color', sqlalchemy.String(15)),
    sqlalchemy.Column('price', sqlalchemy.Integer),
    sqlalchemy.Column('count', sqlalchemy.Integer),
)

order = sqlalchemy.Table(
    "order",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user", ForeignKey('user.id')),
    sqlalchemy.Column("product", ForeignKey('product.id')),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column('status', sqlalchemy.Boolean),
)


class Login(BaseModel):
    email: EmailStr = Field(..., title="Email", max_length=120)
    password: str = Field(..., title="Password", min_length=6)


class UserIn(BaseModel):
    name: str = Field(..., title="Name", max_length=80)
    surname: str = Field(..., title="Surname", max_length=80)
    email: EmailStr = Field(..., title="Email", max_length=120)
    password: str = Field(..., title="Password", min_length=6)


class User(BaseModel):
    id: int
    name: str = Field(..., title="Name", max_length=80)
    surname: str = Field(..., title="Surname", max_length=80)
    email: EmailStr = Field(..., title="Email", max_length=120)
    password: str = Field(..., title="Password", min_length=6)


class Product(BaseModel):
    id: int
    product_name: str = Field(..., title="Product_name", max_length=80)
    product_type: str = Field(..., title="Product_type", max_length=15)
    photo: str = Field(title="Photo", max_length=300)
    content: str = Field(..., title="Content")
    color: str = Field(title="Color", max_length=15)
    price: int = Field(..., title="Price", gt=0)
    count: int = Field(0, title="Count", ge=0)


class OrderIn(BaseModel):
    user: User = Field(..., title="User")
    product: list[Product] = Field(..., title="Product")
    created_at: datetime = Field(datetime.utcnow(), title="Created_at")
    status: bool = Field(True, title="Status")


class Order(BaseModel):
    id: int
    user: User = Field(..., title="User")
    product: list[Product] = Field(..., title="Product")
    created_at: datetime = Field(datetime.utcnow(), title="Created_at")
    status: bool = Field(True, title="Status")
