import uvicorn
from fastapi import FastAPI, Path, Request, HTTPException
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')
users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get('/')
async def home_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})

@app.get('/users/{user.id}')
async def get_users(request: Request,
                    user_id: Annotated[int, Path(ge=1, le=100, description='Enter your id', example='1')]
                    ) -> HTMLResponse:
    for user in users:
        if int(user.id) == user_id:
            return templates.TemplateResponse('users.html', {'request': request, 'users': users})
    raise HTTPException(status_code=404, detail='User was not found')

@app.post("/user/{username}/{age}")
async def create_users(
        username: Annotated[str, Path(min_length=5, max_length=20,
                                      description="Enter username", example="UrbanUser")],
        age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]) -> User:
    if len(users) == 0:
        user_id = 1
    else:
        user_id = len(users) + 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter your id', example='1')],
                      username: Annotated[
                          str, Path(max_length=20, min_length=5, description='Enter username', example='UrbanUser')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> str:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")


# if __name__ == '__main__':
#     uvicorn.run('module_16_5:app')
