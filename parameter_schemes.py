from pydantic import BaseModel

from fastapi import Query


class DataBase(BaseModel):
    """
    Конфигурация Базы Данных
    """
    user: str
    password: str
    db_name: str
    host: str
    port: int


class Config(BaseModel):
    DataBase: DataBase


class Authorization(BaseModel):
    email: str = Query(description='Почта пользователя')
    password: str = Query(description='Пароль для входа в приложение')
    dev: bool = Query(default=False, description='Профиль разработчика')


class Registration(BaseModel):
    mail: str = Query(description='Почта пользователя')
    password: str = Query(description='Пароль для входа')
    password_repeat: str = Query(description='Подтверждение введенного пароля')
    first_name: str = Query(description='Имя пользователя')
    last_name: str = Query(description='Фамилия пользователя')
    dev: bool = Query(default=False, description='Профиль разработчика')


class CodeReg(BaseModel):
    code: str = Query(description='Код подтверждения регистрации')
    public_key: str = Query(description='Открытый ключ')
    private_key: str = Query(description='Закрытый ключ')


class CodeAut(BaseModel):
    code: str = Query(description='Код подтверждения регистрации')


class Folder(BaseModel):
    newFolderName: str = Query(description='Название папки')
    folderParentName: str = Query(default=None, description='Название родительной папки')


class FolderRename(BaseModel):
    newFolderName: str = Query(description='Новое название папки')
    outFolderName: str = Query(description='Старое название папки')


class CodeConfirmation(BaseModel):
    email: str = Query(description='Почта пользователя')
    dev: bool = Query(default=False, description='Профиль разработчика')


class AddNewFile(BaseModel):
    fileName:  str = Query(description='Названия файла')
    content:  str = Query(description='Наполнение файла')
    folderName: str = Query(description='Название папки сохранения')


class FileRename(BaseModel):
    newFileName: str = Query(description='Новое название файла')
    outFileName: str = Query(description='Старое название файла')


class UpdataContent(BaseModel):
    id_file: int = Query(description='Id необходимого файла')
    id_folder: int = Query(description='Id необходимой папки')
    content: str = Query(description='Обновление содержимого файла')


class Settings(BaseModel):
    language: str = Query(default='en')
