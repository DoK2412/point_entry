from fastapi import APIRouter, Request, Query, Cookie, Response

from proxy_client import RegistrationServise, SessionServise, DataServise
import json


from typing import Union

from urls import *
from parameter_schemes import *

from response_code import ResponseCode

servis_router = APIRouter()


async def sessions(request: Request, response: Response, id=None, email=None, uid_session=None):

    if request.session.get('moi'):
        params = {
            "user_id": request.session['moi']['user_id']
            if 'moi' in request.session else None,
            "email": request.session['moi']['email']
            if 'moi' in request.session else None,
            "uid_session": request.session['moi']['uid_session']
            if 'moi' in request.session else None
        }
    else:
        params = {
            'user_id': id,
            'email': email,
            "uid_session": uid_session
        }

    async with SessionServise() as client:
        responses = await client.request(
            'POST',
            '/new',
            params=params,
            headers={"user-agent": request.headers.get('user-agent', 'None')}
        )
        print(responses.json()['uid_session'])
        response.set_cookie(key="session", value=responses.json()['uid_session'], samesite=None)
        request.session['moi'] = responses.json()
        if request.session.get('session') is None:
            request.session['session'] = 'active'
        else:
            request.session['session'] == 'confirmed'


@servis_router.post(SETTING, tags=['point_entry'])
async def setting(request: Request,
                  setting: Settings):
    request.session['language'] = setting.language
    return ResponseCode(1, 'settingsOk').give_answer(request)


@servis_router.post(REGISTRATION, tags=['registration'])
async def registration(request: Request,
                       response: Response,
                       user: Registration
                       ):
    if request.session:
        return ResponseCode(2, 'sessionActiveError').give_answer(request)
    params = dict(user)
    async with RegistrationServise() as client:
        responses = await client.request(
            request.method,
            request.url.path,
            json=params)
        responses = responses.json()
    if responses['answercode'] == 1:
        await sessions(request, response, id=int(responses['data']))
        return ResponseCode(responses['answercode'], 'newCode').give_answer(request)
    elif responses['answercode'] == 15:
        await sessions(request, id=int(responses['data']))
        return ResponseCode(responses['answercode'], responses['data']).give_answer(request)

    return ResponseCode(responses['answercode'], responses['data']).give_answer(request)


@servis_router.post(CONFIRM_REGISTRATION, tags=['registration'])
async def confirm(request: Request,
                  code: CodeReg):
    if request.session.get('session') and request.session['session'] == 'active':
        params = dict(code)
        await sessions(request)
        async with RegistrationServise() as client:
            response = await client.request(
                request.method,
                request.url.path,
                json=params,
                cookies={"user_id": str(request.session['moi']['user_id'])
                if 'moi' in request.session else None}
            )
            response = response.json()
        if response['answercode'] == 1:
            request.session['session'] = 'confirmed'
        return ResponseCode(response['answercode'], response['data']).give_answer(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)


@servis_router.post(AUTHORIZATION, tags=['registration'])
async def authorization(request: Request):
    params_valid = await request.body()
    param = json.loads(params_valid.decode())
    if request.session:
        return ResponseCode(2, 'sessionActiveError').give_answer(request)
    params = dict()
    print(request)
    await sessions(request, email=param['data']['email'])
    async with RegistrationServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            json=params,
        )
        response = response.json()
        if response['answercode'] != 1:
            await logout(request)
        return ResponseCode(response['answercode'], response['data']).give_answer(request)


@servis_router.post(CODE_REPETITION, tags=['registration'])
async def codeRepetition(request: Request, email: CodeConfirmation):
    params = dict(email)
    if request.session:
        await sessions(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)

    async with RegistrationServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            json=params,
            cookies={"user_id": str(request.session['moi']['user_id'])
            if 'moi' in request.session else None}
        )
        response = response.json()
        return ResponseCode(response['answercode'],  response['data']).give_answer(request)


@servis_router.post(CONFIRM_AUTHORIZATIOH, tags=['registration'])
async def confirm(request: Request,
                  code: CodeAut):
    if request.session.get('session') and request.session['session'] == 'active':
        params = dict(code)
        await sessions(request)

        async with RegistrationServise() as client:
            response = await client.request(
                request.method,
                request.url.path,
                json=params,
            )
        response = response.json()
        data = response.get('data', None)
        if data is not None:
            if len(response['data']) == 32:
                request.session['uid'] = response['data']
                request.session['session'] = 'confirmed'
                return ResponseCode(response['answercode'], 'authorizationOK').give_answer(request)
            else:
                return ResponseCode(response['answercode'], response['data']).give_answer(request)
        else:
            return ResponseCode(response['answercode'], response['data']).give_answer(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)


@servis_router.get(LOGOUT, tags=['point_entry'])
async def logout(request: Request):
    request.session.clear()
    request.cookies.clear()
    return ResponseCode(1, 'loggedOk').give_answer(request)


@servis_router.post(NEW_FOLDER, tags=['file_data'])
async def createFolder(request: Request,
                       folder: Folder):
    if request.session.get('session') and request.session['session'] == 'confirmed':
        await sessions(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)

    params = dict(folder)
    async with DataServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            json=params,
            cookies={"user_id": str(request.session['moi']['user_id'])
            if 'moi' in request.session else None}
        )
    response = response.json()
    return ResponseCode(response['answercode'], response['data']).give_answer(request)


@servis_router.post(RENAME_FOLDER, tags=['file_data'])
async def createFolder(request: Request,
                       folder: FolderRename):
    if request.session.get('session') and request.session['session'] ==  'confirmed':
        await sessions(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)
    params = dict(folder)
    async with DataServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            json=params,
            cookies={"user_id": str(request.session['moi']['user_id'])
            if 'moi' in request.session else None}
        )
    response = response.json()
    return ResponseCode(response['answercode'], response['data']).give_answer(request)


@servis_router.get(GET_PROFILE, tags=['registration'])
async def profile(request: Request):
    if request.session.get('session') and request.session['session'] == 'confirmed':
        await sessions(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)

    async with RegistrationServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            cookies={"user_uid": str(request.session['moi']['uid_session'])}
                )
    response = response.json()
    return response


@servis_router.get(GET_FOLDERS, tags=['file_data'])
async def get_folder(request: Request):
    if request.session.get('session') and request.session['session'] == 'confirmed':
        await sessions(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)

    async with DataServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            cookies={"user_id": str(request.session['moi']['user_id'])
            if 'moi' in request.session else None}
        )
    response = response.json()
    return ResponseCode(response['answercode'], response['data']).give_answer(request)


@servis_router.get(GET_FOLDER, tags=['file_data'])
async def get_folder(request: Request,
                     id_folder: int = Query(None, description="Id необходимой папки")):
    if request.session.get('session') and request.session['session'] == 'confirmed':
        await sessions(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)

    params = {'id_folder': id_folder}

    async with DataServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            params=params,
            cookies={"user_id": str(request.session['moi']['user_id'])
            if 'moi' in request.session else None}
        )
    response = response.json()
    return ResponseCode(response['answercode'], response['data']).give_answer(request)


@servis_router.get(DELETE_FOLDER, tags=['file_data'])
async def delete_folder(request: Request,
                        id_folder: int = Query(None, description="Id удаляемой папки")):
    if request.session.get('session') and request.session['session'] == 'confirmed':
        await sessions(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)
    params = {'id_folder': id_folder}

    async with DataServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            params=params,
            cookies={"user_id": str(request.session['moi']['user_id'])
            if 'moi' in request.session else None}
        )
    response = response.json()
    return ResponseCode(response['answercode'], response['data']).give_answer(request)



@servis_router.post(ADD_FILES, tags=['file_data'])
async def add_file(request: Request,
                   addFales: AddNewFile):
    if request.session.get('session') and request.session['session'] == 'confirmed':
        await sessions(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)
    params = dict(addFales)
    async with DataServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            json=params,
            cookies={"user_id": str(request.session['moi']['user_id'])
            if 'moi' in request.session else None}
        )
    response = response.json()
    return ResponseCode(response['answercode'], response['data']).give_answer(request)

@servis_router.post(RENAME_FILE, tags=['file_data'])
async def rename_file(request: Request,
                   renameFales: FileRename):
    if request.session.get('session') and request.session['session'] == 'confirmed':
        await sessions(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)
    params = dict(renameFales)
    async with DataServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            json=params,
            cookies={"user_id": str(request.session['moi']['user_id'])
            if 'moi' in request.session else None}
        )
    response = response.json()
    return ResponseCode(response['answercode'], response['data']).give_answer(request)


@servis_router.get(DELETE_FILE, tags=['file_data'])
async def rename_file(request: Request,
                      id_file: int = Query(None, description="Id удаляемого файла")):
    if request.session.get('session') and request.session['session'] == 'confirmed':
        await sessions(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)
    params = {'id_file': id_file}
    async with DataServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            params=params,
            cookies={"user_id": str(request.session['moi']['user_id'])
            if 'moi' in request.session else None}
        )
    response = response.json()
    return ResponseCode(response['answercode'], response['data']).give_answer(request)



@servis_router.get(GET_FILE, tags=['file_data'])
async def get_file(request: Request,
                      id_file: int = Query(None, description="Id удаляемого файла")):
    if request.session.get('session') and request.session['session'] == 'confirmed':
        await sessions(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)
    params = {'id_file': id_file}
    async with DataServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            params=params,
            cookies={"user_id": str(request.session['moi']['user_id'])
            if 'moi' in request.session else None}
        )
    response = response.json()
    return ResponseCode(response['answercode'], response['data']).give_answer(request)


@servis_router.get(GET_FILE_FOLDER, tags=['file_data'])
async def get_file(request: Request,
                      id_folder: int = Query(None, description="Id необходимой папки")):
    if request.session.get('session') and request.session['session'] == 'confirmed':
        await sessions(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)
    params = {'id_folder': id_folder}
    async with DataServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            params=params,
            cookies={"user_id": str(request.session['moi']['user_id'])
            if 'moi' in request.session else None}
        )
    response = response.json()
    return ResponseCode(response['answercode'], response['data']).give_answer(request)


@servis_router.post(UPDATA_FILE_CONTETN, tags=['file_data'])
async def updata_file(request: Request, content: UpdataContent):
    if request.session.get('session') and request.session['session'] == 'confirmed':
        await sessions(request)
    else:
        return ResponseCode(2, 'sessionNotError').give_answer(request)
    params = dict(content)
    async with DataServise() as client:
        response = await client.request(
            request.method,
            request.url.path,
            json=params,
            cookies={"user_id": str(request.session['moi']['user_id'])
            if 'moi' in request.session else None}
        )
    response = response.json()
    return ResponseCode(response['answercode'], response['data']).give_answer(request)


@servis_router.get('/test/cookie')
async def add_cookies(response: Response,
                      request: Request):
    response.set_cookie(key="session", value="6a0bb0f1-3a8b-4c90-a174-28aeb9d16275", samesite=None)
    request.session['moi'] = 'Проверка'
    return {'Кука установлена'}
    # return {'session_cookies':  request.cookies.get('session', None)}

@servis_router.get('/test/cookie/delete')
async def getCookie(request: Request):
    request.cookies.clear()
    return {'session_cookies': request.cookies.get('session', None)}


@servis_router.get('/test')
async def test(response: Response,
               request: Request,
               session: str | None = Cookie(default=None)):
    print(session)
    if session == None:
        return {"message": "Это ваш первый визит на сайт"}
    else:
        return {"message": f"установленная кука: {session}"}
