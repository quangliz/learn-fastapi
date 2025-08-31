import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.routers import user, todo

# Tạo bảng trong DB (nếu chưa có)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Đăng ký router
app.include_router(user.router)
app.include_router(todo.router)

@app.get("/")
def root():
    return {"message": "Hello FastAPI with PostgreSQL"}

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tạm cho tất cả domain, sau này chỉ frontend mình
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"{request.method} {request.url} completed in {process_time:.4f}s")
    return response