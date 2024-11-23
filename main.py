from fastapi import FastAPI
from controllers.user_controller import router as item_router
from controllers.chat_controller import router as chat_router
from controllers.search_controller import router as search_router

from config import get_config
config = get_config()

app = FastAPI()
app.title = config.app_name
app.version = "0.0.1"
app.include_router(item_router)
app.include_router(chat_router)
app.include_router(search_router)