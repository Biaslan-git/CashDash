from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from handlers import routers

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)

for router in routers:
    app.include_router(router=router)
 
  

