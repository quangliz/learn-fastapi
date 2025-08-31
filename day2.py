from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

# practise 1
class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=50) # "..." mean mandatory field
    price: float = Field(..., gt=0)
    quantity: int = Field(1, gt=0)
@app.post("/product")
def create_product(product: Product):
    return {
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
        "status": "ok"
    }

# practise 2
class User(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)
@app.post("/register")
def register(user: User):
    return {
        "username": user.username,
        "email": user.email,
        "status": "registered"
    }

# practise 3
class Blog(BaseModel):
    title: str = Field(..., min_length=5)
    content: str = Field(..., min_length=20)
    published: bool = False
    tags: list[str] = []
@app.post("/blog")
def create_blog(blog: Blog):
    return {
        "title": blog.title,
        "content": blog.content,
        "published": blog.published,
        "tags": blog.tags,
        "status": "created"
    }


# class User(BaseModel):
#     name: str
#     age: Optional[int] = 18
#     email: EmailStr
# @app.post("/user")
# def create_user(user:User):
#     return {
#         "name": user.name,
#         "age": user.age,
#         "email": user.email,
#         "msg": f"created user by email: {user.email}"
#     }
    
    
# class Product(BaseModel):
#     name: str = Field(..., min_length=3, max_length=50)
#     price: float = Field(..., gt = 0)
#     in_stock: bool = True
# @app.post("/product")
# def create_product(product:Product):
#     return {
#         "name": product.name,
#         "price": product.price,
#         "in_stock": product.in_stock
#     }