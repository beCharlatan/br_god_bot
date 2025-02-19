from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# Инициализация приложения с метаданными
app = FastAPI(
    title="BR-Bot API",
    description="""API для взаимодействия с BR-Bot - интеллектуальным помощником для работы с базой знаний.
    
Основные возможности:
* Чат с ботом и управление историей сообщений
* Загрузка и обработка BA и SA документов
    """,
    version="1.0.0",
    contact={
        "name": "BR-Bot Team",
        "email": "support@example.com"
    },
    license_info={
        "name": "Private",
        "url": "https://example.com/license"
    }
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Кастомизация OpenAPI схемы
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=[
            {
                "name": "chat",
                "description": "Эндпоинты для взаимодействия с чат-ботом"
            },
            {
                "name": "documents",
                "description": "Эндпоинты для загрузки и обработки документов"
            }
        ]
    )
    
    # Добавляем дополнительную информацию
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
