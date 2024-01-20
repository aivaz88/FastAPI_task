from typing import Dict, List
from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from my_shop.my_models import UserIn, User, OrderIn, Order, Login, Product, database, metadata, engine, user, product, order, login


app = FastAPI()
templates = Jinja2Templates(directory="my_shop/templates")
app.mount("/my_shop/static", StaticFiles(directory="my_shop/static"), name="static")
# app.mount("/static", StaticFiles(directory="C://Users/Asus/Desktop/GeekBrains/FastAPI/my_shop/static"), name="static")
# DATABASE_URL = "sqlite:///my_shop/instance/mydatabase.db"
# database = databases.Database(DATABASE_URL)
metadata.create_all(engine)

# engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/', response_class=HTMLResponse)
async def main(request: Request):
    name = request.cookies.get('user_name')
    return templates.TemplateResponse('main.html', {"request": request, 'cookie_name': name})


@app.get('/about/', response_class=HTMLResponse)
async def about(request: Request):
    name = request.cookies.get('user_name')
    return templates.TemplateResponse('about.html', {"request": request, 'cookie_name': name})


@app.get('/contacts/', response_class=HTMLResponse)
async def contacts(request: Request):
    name = request.cookies.get('user_name')
    return templates.TemplateResponse('contacts.html', {"request": request, 'cookie_name': name})


@app.get('/clothes/', response_class=HTMLResponse)
async def clothes(request: Request):
    name = request.cookies.get('user_name')
    query = product.select().where(product.c.product_type == "clothes")
    clothes = await database.fetch_all(query)
    return templates.TemplateResponse('products.html', {"request": request, 'cookie_name': name, 'products': clothes})


@app.get('/shoes/', response_class=HTMLResponse)
async def shoes(request: Request):
    name = request.cookies.get('user_name')
    query = product.select().where(product.c.product_type == "shoes")
    shoes = await database.fetch_all(query)
    return templates.TemplateResponse('products.html', {"request": request, 'cookie_name': name, 'products': shoes})


@app.get('/accessories/', response_class=HTMLResponse)
async def accessories(request: Request):
    name = request.cookies.get('user_name')
    query = product.select().where(product.c.product_type == "accessories")
    accessories = await database.fetch_all(query)
    return templates.TemplateResponse('products.html', {"request": request, 'cookie_name': name, 'products': accessories})


@app.get('/item_card/{x}/', response_class=HTMLResponse)
async def item_card(request: Request, x):
    name = request.cookies.get('user_name')
    query = product.select().where(product.c.id == int(x))
    item = await database.fetch_all(query)
    return templates.TemplateResponse('item_card.html', {"request": request, 'cookie_name': name, "products": item})


@app.get('/login/', response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})


@app.post('/login/', response_class=HTMLResponse, response_model=Login)
async def post_login(request: Request, my_user: Login):
    print(my_user.email)
    print(my_user.password)
    return templates.TemplateResponse('login.html', {"request": request})


# @app.route('/greeting/', methods=['GET', 'POST'])
# @csrf.exempt
# def greeting():
#     if request.method == 'POST':
#         response = make_response(redirect('/login/'))
#         response.set_cookie('user_name', '')
#         response.set_cookie('user_surname', '')
#         response.set_cookie('user_email', '')
#         return response
#     cookie_data = []
#     name = request.cookies.get('user_name')
#     email = request.cookies.get('user_email')
#     cookie_data.append(name)
#     cookie_data.append(email)
#     content = {'cookie_data': cookie_data}
#     return render_template('greeting.html', **content)
#
#
# @app.route('/registration/', methods=['GET', 'POST'])
# def registration():
#     form = RegistrationForm()
#     if request.method == 'POST' and form.validate():
#         name = form.username.data
#         surname = form.user_surname.data
#         email = form.email.data
#         password = form.password.data
#         checking = True
#         users = User.query.all()
#         for user in users:
#             if user.email == email:
#                 checking = False
#         if checking:
#             response = make_response(redirect('/greeting/'))
#             response.set_cookie('user_name', name)
#             response.set_cookie('user_surname', surname)
#             response.set_cookie('user_email', email)
#             user = User(name=name, surname=surname, email=email, password=password)
#             db.session.add(user)
#             db.session.commit()
#             return response
#         else:
#             return render_template('registration.html', form=form)
#     return render_template('registration.html', form=form)

