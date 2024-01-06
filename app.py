import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from database.connection_db import JobDb
from database.sql_requests import *

from views import servis_router
from settings import HOST, PORT


app = FastAPI(
    title='Сервис заметок',
    version='0.0.1'
)

@app.on_event("startup")
async def on_startup():
    '''Функция подключени базы данных на старте приложения'''
    await JobDb().create_pool()
    async with JobDb() as pool:
        await pool.execute(PROFILE_TABLE)
        await pool.execute(SESSION_TABLE)
        await pool.execute(USER_DATA_PUBLIC_KEYS_TABLE)
        await pool.execute(USER_FILE_TABLE)
        await pool.execute(USER_FOLDER_TABLE)
        await pool.execute(CONFIRM_CODE_TABLE)



@app.on_event('shutdown')
async def shutdown_event():
    '''Функция отключения базы данных по окончанию работы'''
    await JobDb().close_pool()



origins = [
    "http://0.0.0.0:3000",
    "http://localhost:1420",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8082",
    "http://127.0.0.1:8083",
    "https://smtp.yandex.com:465"

]

app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")
app.include_router(servis_router)

if __name__ == '__main__':
    uvicorn.run(
        app,
        host=HOST,
        port=PORT
    )
