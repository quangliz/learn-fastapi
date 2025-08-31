from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# @app.get("/ping")
# def ping():
#     return {"message": "ping"}

# # quey params
# @app.get("/sum")
# def sum(a: int, b: int):
#     return a+b


# # path params
# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     return {
#         "user_id": user_id,
#         "message": f"User {user_id} details"
#     }

    
    
# class Item(BaseModel):
#     name: str
#     price: float

# # request body
# @app.post("/items")
# def create_item(item: Item):
#     return {
#         "item": item.name,
#         "price": item.price
#     }
    

# # practise
# @app.get("/hello/{username}")
# def greeting(username: str):
#     return {
#         "message": f"Hello {username}"
#     }
    
    
# @app.get("/calc")
# def calc(a: float, b: float):
#     return {
#         "a": a,
#         "b": b,
#         "sum": a+b,
#         "sub": a-b,
#         "mul": a*b,
#         "div": a/b
#     }

# class Product(BaseModel):
#     name: str
#     price: float
#     in_stock: bool
    
# @app.post("/product")
# def create_product(product: Product):
#     return {
#         "name": product.name,
#         "price": product.price,
#         "in_stock": product.in_stock,
#         "status": "received"
#     }
    

# practise 2
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id,
        "message": f"This is user {id}"
    }

@app.get("/users")
def is_active(active:bool = False):
    if active == True: return {"filter": "active=true"}
    return {"filter": "none"}

class User(BaseModel):
    name:str
    age:int
    email:str
    
@app.post("/users")
def create_user(user:User):
    return {
        "name": user.name,
        "age": user.age,
        "email": user.email,
        "status": "created"
    }