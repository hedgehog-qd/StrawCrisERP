__all__ = ()

from quart import render_template, redirect, request, jsonify
from quart import Blueprint, send_file
from quart_cors import cors
from functools import wraps
from blueprints.utils import flash
from quart import session
import fileprocess
import db
import os

apis = Blueprint('apis', __name__)
cors(apis)  # 允许跨域请求


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not session:
            json = {
                "status": "4",
                "text": "Your current user role is not allowed to access this API."
            }
            return jsonify(json)
        if not session['email']:
            json = {
                "status": "4",
                "text": "Your current user role is not allowed to access this API."
            }
            return jsonify(json)
        return await func(*args, **kwargs)

    return wrapper


@apis.route('/')
async def apihome():
    return "Welcome to StrawCris API! Check the document for detailed API information."


@apis.route('/getAllPartData')
@login_required
async def getAllPartData():
    allMaterials = db.getAllMaterials()
    json = {
        "status": "0",
        "result": allMaterials
    }
    return jsonify(json)


@apis.route('/search', methods=['POST'])
async def searchForMaterials():
    data = await request.get_json()
    searchdata = data.get('search', [])
    print(searchdata)
    search_result = db.getInfoMetaSearch(searchdata)
    returndata = {
        'result': search_result
    }
    return jsonify(returndata)


@apis.route('/addNewMaterial', methods=['POST'])
@login_required
async def addNewMaterial():
    data = await request.get_json()
    m_name = data.get('m_name', '(no data)')
    m_class = data.get('m_class', '(no data)')
    footprint = data.get('footprint', '(no data)')
    quantity = data.get('quantity', '(no data)')
    mpn = data.get('mpn', '(no data)')
    manufacture = data.get('manufacture', '(no data)')
    spn = data.get('spn', '(no data)')
    supplier = data.get('supplier', '(no data)')
    position = data.get('position', '(no data)')
    user_comment = data.get('user_comment', '(no data)')
    buy_time = data.get('buy_time', '(no data)')
    if db.checkMaterialExists(mpn) == 1:
        existing_num = db.getMaterialInfowithMPN(mpn)[4]
        db.updateMaterialQuantitywithMPN(mpn, int(existing_num) + int(quantity))
        json = {
            "status": 1,
            "text": "Material already exist"
        }
        return jsonify(json)
    db.addNewMaterial(m_name, m_class, footprint, quantity, mpn, manufacture, spn, supplier, position, user_comment, buy_time)
    json = {
        "status": 0,
        "text": "Successfully added"
    }
    return jsonify(json)


@apis.route('/uploadBOM', methods=['POST'])
@login_required
async def uploadBOM():
    f = (await request.files).get('file')
    print("file: " + f.filename)
    basepath = "./"
    upload_path = os.path.join(basepath, 'uploaded_files', f.filename)
    await f.save(upload_path)
    print("BOM uploaded file saved")
    fileprocess.processUpdateBOMupdateDB(f.filename, upload_path)
    return 'OK'


@apis.route('/getSingleDatawithMPN')
@login_required
async def getSingleDatawithMPN():
    mpn = str(request.args['mpn'])
    if db.checkMaterialExists(mpn) == 0:
        json = {
            "status": 1
        }
        return jsonify(json)
    data = db.getMaterialInfowithMPN(str(mpn))
    json = {
        "status": 0,
        "data": data
    }
    return jsonify(json)


@apis.route('/updateSingleDatawithMPN', methods=['POST'])
@login_required
async def updateSingleDatawithMPN():
    data = await request.get_json()
    m_name = data.get('m_name', '(no data)')
    m_class = data.get('m_class', '(no data)')
    footprint = data.get('footprint', '(no data)')
    quantity = data.get('quantity', '(no data)')
    mpn = data.get('mpn', '(no data)')
    manufacture = data.get('manufacture', '(no data)')
    spn = data.get('spn', '(no data)')
    supplier = data.get('supplier', '(no data)')
    position = data.get('position', '(no data)')
    user_comment = data.get('user_comment', '(no data)')
    buy_time = data.get('buy_time', '(no data)')
    print(buy_time)
    db.updateMaterialInfowithMPN(mpn, m_name, m_class, footprint, quantity, manufacture, spn, supplier, position,
                                 user_comment, buy_time)
    return 'OK'


@apis.route('/checkoutOnetimeUsewithMPN')
@login_required
async def checkoutOnetimeUsewithMPN():
    mpn = str(request.args['mpn'])
    quantity = str(request.args['quantity'])
    if db.checkMaterialExists(mpn) == 0:
        json = {
            "status": 1,
            "text": "The requested mpn does not exist"
        }
        return jsonify(json)
    existing_num = db.getMaterialInfowithMPN(mpn)[4]
    if int(existing_num) < int(quantity):
        json = {
            "status": 2,
            "text": "The amount you request is more than the existing amount",
            "existing_amount": existing_num
        }
        return jsonify(json)
    db.updateMaterialQuantitywithMPN(mpn, int(existing_num) - int(quantity))
    json = {
        "status": 0,
        "text": "OK"
    }
    return jsonify(json)


@apis.route('/checkoutUploadExcel', methods=['POST'])
@login_required
async def checkoutUploadExcel():
    f = (await request.files).get('file')
    print("file: " + f.filename)
    basepath = "./"
    upload_path = os.path.join(basepath, 'uploaded_files', f.filename)
    await f.save(upload_path)
    print("BOM uploaded file saved")
    whatwehave, whatwedonthave = fileprocess.processCompareBOM(f.filename, upload_path)
    json = {
        "status": 0,
        "bill_have": whatwehave,
        "bill_donthave": whatwedonthave
    }
    return jsonify(json)


@apis.route('/checkoutConfirmHave', methods=['POST'])
@login_required
async def checkoutConfirmHave():
    data = await request.get_json()
    have_list = data.get('data', '')
    print(have_list)
    db.checkoutHaveList(have_list)
    return 'OK'
