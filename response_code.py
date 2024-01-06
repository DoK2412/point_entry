from typing import Any

response_ru = {
    1: 'Успешное выполнение запроса.',
    2: 'Ошибка на стороне сервера.',
    3: 'Отказ в доступе со стороны сервера.'
}

response_en = {
    1: 'Successful completion of the request.',
    2: 'Server side error.',
    3: 'Server access denied.'
}


data_ru = {
    # общие ошибки сервисов
    "notСonfirmed":                 "Аккаунт пользователя не подтвержден.",
    "internalError":                "Внутренняя ошибка выполнения запроса.",
    # сервис login_authorization
    "newCode":                      "Код подтверждения отправлен на вашу почту.",
    "registrationOk":               "Регистрация  успешно завершена.",
    "authorizationOK":              "Авторизация  успешно завершена.",
    "mailError":                    "Введенная почта не является почтовым адресом.",
    "passwordErrorValid":           "Пароль должен содержать 8 символов, буквы в верхнем и нижнем регистре и цифр.",
    "passwordError":                "Введенные пароли не совпадают.",
    "nameError":                    "Имя не соответствует стандарту, использовано смешивание алфавитов.",
    "surnameError":                 "Фамилия не соответствует стандарту, использовано смешивание алфавитов.",
    "userError":                    "Пользователь под данным эмейлом уже есть в базе данных.",
    "codeError":                    "Получен не активный либо не существующий код.",
    "logPassError":                 "Неверный логин или пароль.",
    "accountError":                 "Аккаунт пользователя не подтвержден.",
    "userNot":                      "Пользователь не найдей в базе данных.",
    # сервис file_data
    "folderOk":                     "Папка успешно создана",
    "fileOk":                       "Файл успешно создан",
    "renameFolderOk":               "Папка успешно переименована.",
    "renameFileOk":                 "Файл успешно переименован.",
    "deleteFileOk":                 "Файл успешно удален.",
    "updateСontentFileOK":          "Данные в файле обнослены.",
    "availabilityFolderError":      "У пользователя есть папка с таким именем.",
    "notFolderError":               "У пользователя нет папки с таким именем.",
    "notParameterError":            "В запрос не передан обязательный параметр.",
    "availabilityFileError":        "У аользователя уже есть файл с таким именем.",
    "notFileError":                 "У пользователя нет файла с таким именем.",
    # сервис point_entry
    "settingsOk":                   "Настройки успешно изменены.",
    "loggedOk":                     "Пользователь вышел из приложения.",
    "sessionNotError":              "Cессия отсуттсвует, авторизуйтесь.",
    "sessionActiveError":           "У пользователя есть активная сессия.",
    "": "",
}

data_en = {
    # общие ошибки сервисов
    "notСonfirmed":                 "User account not verified.",
    # сервис login_authorization
    "newCode":                      "A new code has been sent to your email.",
    "registrationOk":               "Registration successfully completed.",
    "authorizationOK":              "Authorization completed successfully.",
    "internalError":                "Internal request execution error.",
    "mailError":                    "The entered email is not a postal address.",
    "passwordErrorValid":           "Password must contain 8 characters, upper and lower case letters and numbers.",
    "passwordError":                "The entered passwords do not match.",
    "nameError":                    "The name does not correspond to the standard, alphabets are mixed.",
    "surnameError":                 "The surname does not correspond to the standard, alphabets are mixed.",
    "userError":                    "The user under this email is already in the database.",
    "codeError":                    "An inactive or non-existent code was received.",
    "logPassError":                 "Wrong login or password.",
    "accountError":                 "User account not verified.",
    "userNot":                      "User not found in database.",
    # сервис file_data
    "folderOk":                     "Folder created successfully",
    "fileOk":                       "File created successfully.",
    "renameFolderOk":               "The folder has been successfully renamed.",
    "renameFileOk":                 "The file has been successfully renamed.",
    "deleteFileOk":                 "The file was successfully deleted.",
    "updateСontentFileOK":          "The data in the file has been updated.",
    "availabilityFolderError":      "The user has a folder with this name.",
    "notFolderError":               "The user does not have a folder with this name.",
    "notParameterError":            "A required parameter was not passed to the request.",
    "availabilityFileError":        "The user already has a file with the same name.",
    "notFileError":                 "The user does not have a file with this name.",
    # сервис point_entry
    "settingsOk":                   "Settings successfully changed.",
    "loggedOk":                     "The user has logged out of the application.",
    "sessionNotError":              "No session, log in",
    "sessionActiveError":           "The user has an active session.",

}


class ResponseCode():
    def __init__(self, code, data=None):
        self.answercode: int = code
        self.answer: str = response_en[code]
        self.data: Any = data

    def give_answer(self, request):
        if request.session.get('language') is None or request.session['language'] == 'en':
            if isinstance(self.data, dict) or isinstance(self.data, list):
                return {
                    'answercode': self.answercode,
                    'answer': response_en[self.answercode],
                    'data': self.data
                }
            if self.data in data_en:
                self.data = data_en[self.data]
            return {
                    'answercode': self.answercode,
                    'answer': response_en[self.answercode],
                    'data': self.data
                    }
        else:
            if isinstance(self.data, dict) or isinstance(self.data, list):
                return {
                    'answercode': self.answercode,
                    'answer': response_ru[self.answercode],
                    'data': self.data
                }
            if self.data in data_ru:
                self.data = data_ru[self.data]
            return {
                    'answercode': self.answercode,
                    'answer': response_ru[self.answercode],
                    'data': self.data
                    }

