__all__ = ()

from quart import render_template, redirect, request, send_file, jsonify, session
from quart import Blueprint
from functools import wraps
from blueprints.utils import flash
import db

frontend = Blueprint('frontend', __name__)


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not session:
            return await flash('error', 'You must be logged in to access that page.', 'login')
        if not session['email']:
            return await flash('error', 'You must be logged in to access that page.', 'login')
        return await func(*args, **kwargs)

    return wrapper


@frontend.route('/')
@frontend.route('/home')
async def home_page():  # put application's code here
    return await render_template('home.html')


@frontend.route('/search')
@login_required
async def search():
    return await render_template('search.html')


@frontend.route('/viewall')
@login_required
async def viewall():
    return await render_template('viewall.html')


@frontend.route('/checkout')
@login_required
async def checkout():
    if session['role_level'] > 1:
        return await flash('ban', 'Your current user role is not allowed to access that page.', 'home')
    return await render_template('checkout.html')


@frontend.route('/addnew')
@login_required
async def addnew():
    if session['role_level'] > 1:
        return await flash('ban', 'Your current user role is not allowed to access that page.', 'home')
    return await render_template('addnew.html')


@frontend.route('/edit')
@login_required
async def edit():
    if session['role_level'] > 1:
        return await flash('ban', 'Your current user role is not allowed to access that page.', 'home')
    return await render_template('edit.html')


@frontend.route('/login', methods=['GET', "POST"])
async def login():
    if request.method == 'GET':
        return await render_template('login.html')
    user = (await request.form).get('email')
    pwd = (await request.form).get('password')
    print("Login User: " + user)
    print("with passwd: " + str(pwd))
    stats = db.checklogin(str(user), str(pwd))
    if stats == 0:
        uid, role_level = db.getuserdata(str(user))
        session['username'] = user
        session['email'] = user
        session['uid'] = uid
        session['role_level'] = role_level
        return await flash('success', 'Successful logged in!', 'home')
    elif stats == 1:
        return await flash('error', 'Wrong username or password.', 'login')
    else:
        return await flash('error', 'User does not exist.', 'login')


@frontend.route('/logout')
async def logout():
    del session['username']
    del session['email']
    return await flash('success', 'Logout successful!', 'login')

