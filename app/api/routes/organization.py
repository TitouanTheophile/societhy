from flask import Blueprint, Response, render_template, request, jsonify, make_response

from core import base_orga, sales_platform

from models.organization import organizations
from api import requires_auth, ensure_fields, populate_user

router = Blueprint('orga', __name__)

@router.route('/getOrganization', methods=['POST'])
@populate_user
def getOrgaDocument(user):
	if 'id' in request.json:
		ret = base_orga.getOrgaDocument(user, _id=request.json.get('id'))
		return make_response(jsonify(ret.get('data')), ret.get('status'))
	elif 'name' in request.json:
		ret = base_orga.getOrgaDocument(user, name=request.json.get('name'))
		return make_response(jsonify(ret.get('data')), ret.get('status'))
	else:
		return make_response("Wrong request format", 400)

@router.route('/getAllOrganizations', methods=['GET'])
def getAllOrganizations():
	ret = base_orga.getAllOrganizations()
	return make_response(jsonify(ret.get('data')), ret.get('status'))

@router.route('/createOrga', methods=['POST'])
@requires_auth
def createOrga(user):
	if ensure_fields(['password', 'socketid', {'newOrga': ["name", "description", "accessibility", "gov_model", "quorum", "majority"]}], request.json):
		ret = base_orga.createOrga(user, request.json.get('password'), request.json.get('newOrga'))
		return make_response(jsonify(ret.get('data')), ret.get('status'))
	else:
		return make_response("Wrong request format", 400)

@router.route('/addOrgaProfilePicture', methods=['POST'])
@requires_auth
def addOrgaProfilePicture(user):
	orga_id = request.form.get("orga_id")
	pic_type = request.form.get("type")
	pic = request.files.get("pic")
	ret = base_orga.addOrgaProfilePicture(user, orga_id, pic, pic_type)
	#todo : gerer le retour
	return make_response("ok", 200)

@router.route('/addOrgaDocuments', methods=['POST'])
@requires_auth
def addOrgaDocuments(user):
	orga_id = request.form.get("orga_id")
	doc = request.files.get("doc")
	name = request.form.get("name")
	doc_type = request.form.get("type")
	ret = base_orga.addOrgaDocuments(user, orga_id, doc, name, doc_type)
	return make_response("ok", 200)

@router.route('/getOrgaUploadedDocument/<doc_id>/<doc_name>', methods=['GET'])
@requires_auth
def getOrgaUploadedDocument(user, doc_id, doc_name):
	ret = base_orga.getOrgaUploadedDocument(user, doc_id, doc_name)
	return ret

@router.route('/joinOrga', methods=['POST'])
@requires_auth
def joinOrga(user):
	if ensure_fields(['password', 'socketid', 'orga_id', 'tag'], request.json):
		ret = base_orga.joinOrga(user, request.json.get('password'), request.json.get('orga_id'), request.json.get('tag'))
		return make_response(jsonify(ret.get('data')), ret.get('status'))
	else:
		return make_response("Wrong request format", 400)

@router.route('/getOrgaMemberList/<orga_id>', methods=['GET'])
@populate_user
def getOrgaMemberList(user, orga_id):
	if orga_id:
		ret = base_orga.getOrgaMemberList(orga_id)
		return make_response(jsonify(ret.get('data')), ret.get('status'))
	else:
		return make_response("Wrong request format", 400)

@router.route('/makeDonation', methods=['POST'])
@requires_auth
def makeDonation(user):
	if ensure_fields(['password', 'socketid', 'orga_id', 'donation'], request.json):
		ret = base_orga.donateToOrga(user, request.json.get('password'), request.json.get('orga_id'), request.json.get('donation'))
		return make_response(jsonify(ret.get('data')), ret.get('status'))
	else:
		return make_response("Wrong request format", 400)

@router.route('/createProjectFromOrga', methods=['POST'])
@requires_auth
def createProjectFromOrga(user):
	if ensure_fields(['password', 'socketid', 'orga_id', 'newProject'], request.json):
		ret = base_orga.createProjectFromOrga(user, request.json.get('password'), request.json.get('orga_id'), request.json.get('newProject'))
		return make_response(jsonify(ret.get('data')), ret.get('status'))
	else:
		return make_response("Wrong request format", 400)

@router.route('/leaveOrga', methods=['POST'])
@requires_auth
def leaveOrga(user):
	if ensure_fields(['password', 'socketid', 'orga_id'], request.json):
		ret = base_orga.leaveOrga(user, request.json.get('password'), request.json.get('orga_id'))
		return make_response(jsonify(ret.get('data')), ret.get('status'))
	else:
		return make_response("Wrong request format", 400)

@router.route('/addNewProduct', methods=['POST'])
@requires_auth
def addProductOrga(user):
    if ensure_fields(['name', 'owner', 'description', 'price', 'paymentMode', 'isDigital', 'shippingMode', 'stock'], request.json):
        ret = sales_platform.addProduct(request.json)
        return make_response(jsonify(ret.get('data')), ret.get('status'))
    else:
        return make_response('Something went wrong', 400)

@router.route('/getOrgaProducts/<orga_id>', methods=['GET'])
def getOrgaProducts(orga_id):
    products = sales_platform.getProductsByOwner(orga_id)
    return make_response(jsonify(products.get('data')), products.get('status'))

@router.route('/getOrgaHisto', methods=['POST'])
def getOrgaHisto():
	ret = base_orga.getHisto(request.json.get('password'), request.json.get('orga_id'), request.json.get('date'))
	return make_response(jsonify(ret.get('data')), ret.get('status'))
