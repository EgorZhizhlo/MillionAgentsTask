import os
import random
import string
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from .database import URLS, async_session_maker, engine
from .schemas import SUrl

app = FastAPI()
templates = Jinja2Templates(directory=os.path.abspath('templates'))


def generate_random_short_url(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


async def generate_unique_short_url():
    async with async_session_maker() as session:
        while True:
            short_url = generate_random_short_url()
            query = select(URLS).filter_by(short_url=short_url)
            result = await session.execute(query)
            if result.scalar_one_or_none() is None:
                return short_url


async def find_url_or_none(**kwargs):
    async with async_session_maker() as session:
        query = select(URLS).filter_by(**kwargs)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def add(**kwargs):
    async with async_session_maker() as session:
        async with session.begin():
            new_instance = URLS(**kwargs)
            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_instance


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(URLS.metadata.create_all)


@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse(
        "base.html", {'request': request}
    )


@app.post('/url')
async def create_short_url(request: Request, url: SUrl = Form(...)):
    original_url_entry = await find_url_or_none(original_url=url.url)
    if original_url_entry:
        return templates.TemplateResponse(
            "base.html",
            {'request': request, 'short_url': original_url_entry.short_url}
        )
    try:
        new_url = await add(
            original_url=url.url,
            short_url=await generate_unique_short_url(),
        )
        return templates.TemplateResponse(
            "base.html",
            {'request': request, 'short_url': new_url.short_url}
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/url/{url}')
async def redirect_to_original(url: str):
    short_url_entry = await find_url_or_none(short_url=url)
    if short_url_entry:
        return RedirectResponse(url=short_url_entry.original_url)
    else:
        return RedirectResponse('/')
