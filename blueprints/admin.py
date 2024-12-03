__all__ = ()

from quart import Blueprint, session, render_template, request, jsonify
from functools import wraps
from blueprints.utils import flash
import db

admin = Blueprint('admin', __name__)


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not session:
            return await flash('error', 'You must be logged in to access that page.', 'login')
        if session['role_level'] != 0:
            return await flash('error', 'Your user role is not Admin', 'login')
        return await func(*args, **kwargs)

    return wrapper


@admin.route('/')
@login_required
async def adminhome():
    return await render_template("/admin/editAccounts.html")


@admin.route('/getAllUsers')
@login_required
async def getAllUsers():
    allUsers = db.getUserList()
    json = {
        "result": allUsers
    }
    return jsonify(json)


@admin.route('/deleteUser')
@login_required
async def deleteUser():
    uid = str(request.args['uid'])
    db.deleteUser(uid)
    return 'OK'


@admin.route('/addUser')
@login_required
async def addUser():
    user_name = str(request.args['uname'])
    passwd = str(request.args['passwd'])
    role = str(request.args['role'])
    status = db.addUser(user_name, passwd, role)
    json = {
        "get_status": status
    }
    return jsonify(json)


@admin.route('/updateUser')
@login_required
async def updateUser():
    uid = str(request.args['uid'])
    user_name = str(request.args['uname'])
    passwd = str(request.args['passwd'])
    role = str(request.args['role'])
    db.updateUser(uid, user_name, passwd, role)
    return 'OK'
