import uvicorn
from fastapi import Depends, FastAPI

from api.dependencies import get_db
from api.users import router_user, router_users
from api.pets import router_pet, router_pets
from db.database import engine
from db.database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Тестовое API",
    description="Пятая версия приложения",
    version="0.0.5",
    license_info={
        "name": "Допустим под лицензией Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
    dependencies=[Depends(get_db)]
)

app.include_router(router_user)
app.include_router(router_users)
app.include_router(router_pet)
app.include_router(router_pets)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8006)
