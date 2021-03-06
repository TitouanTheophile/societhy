from api import requires_auth, ensure_fields, populate_user
from core import base_orga, sales_platform
from flask import Blueprint, request, jsonify, make_response, send_file
from models.clients import blockchain_watcher as bw

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
    if ensure_fields(['password', 'socketid', {'newOrga': ["name", "description", "rules", "gov_model"]}], request.json):
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
    size = request.form.get("size")
    privacy = request.form.get("privacy")
    privacy = privacy.split(",")
    print(privacy)
    ret = base_orga.addOrgaDocuments(user, orga_id, doc, name, doc_type, size, privacy)
    return make_response(jsonify(ret.get('data')), ret.get('status'))

@router.route('/getOrgaUploadedDocument/<doc_id>/<doc_name>', methods=['GET'])
def getOrgaUploadedDocument(doc_id, doc_name):
    ret = base_orga.getOrgaUploadedDocument(doc_id, doc_name)
    return make_response(send_file(ret, attachment_filename=doc_name, as_attachment=True), 200)

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

@router.route('/payMembership', methods=['POST'])
@requires_auth
def payMembership(user):
    if ensure_fields(['password', 'socketid', 'orga_id', 'donation'], request.json):
        ret = base_orga.donateToOrga(user, request.json.get('password'), request.json.get('orga_id'), request.json.get('donation'))
        if ret.get('status') == 200:
            bw.waitTx(ret.get("data"))
            ret = base_orga.joinOrga(user, request.json.get('password'), request.json.get('orga_id'), request.json.get('tag'))
        return make_response("dsadsa", ret.get('status'))
    else:
        return make_response("Wrong request format", 400)

@router.route('/createProjectFromOrga', methods=['POST'])
@requires_auth
def createProjectFromOrga(user):
    if ensure_fields(['password', 'socketid', 'orga_id', {'newProject': ['name', 'description', 'campaign']}], request.json):
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

@router.route('/removeMember', methods=['POST'])
@requires_auth
def removeMember(user):
    if ensure_fields(['password', 'socketid', 'orga_id'], request.json):
        ret = base_orga.removeMember(user, request.json.get('account'), request.json.get('password'), request.json.get('orga_id'))
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
        return make_response('Wrong request format', 400)

@router.route('/productImageUpload', methods=['POST'])
@requires_auth
def addProductImage(user):
	prod_id = request.form.get("prod_id")
	type = request.form.get("type")
	pic = request.files.get("prodImg")
	ret = sales_platform.addProductImage(prod_id, pic, type)
	return make_response(jsonify(ret.get('data')), ret.get('status'))

@router.route('/getProductImages/<prod_id>', methods=['GET'])
def getProductImages(prod_id):
    images = sales_platform.getProductImages(prod_id)
    return make_response(jsonify(images.get('data')), images.get('status'))

@router.route('/getOrgaProducts/<orga_id>', methods=['GET'])
def getOrgaProducts(orga_id):
    products = sales_platform.getProductsByOwner(orga_id)
    return make_response(jsonify(products.get('data')), products.get('status'))

@router.route('/addReviewToProduct/<product_id>', methods=['POST'])
@requires_auth
def addReview(user, product_id):
    ret = sales_platform.addReviewToProduct(product_id, request.json)
    return make_response(jsonify(ret.get('data')), ret.get('status'))

@router.route('/getOrgaHisto', methods=['POST'])
def getOrgaHisto():
    ret = base_orga.getHisto(request.json.get('password'), request.json.get('orga_id'), request.json.get('date'))
    return make_response(jsonify(ret.get('data')), ret.get('status'))

@router.route('/updateOrgaRights', methods=['POST'])
@requires_auth
def updateOrgaRights(user):
    ret = base_orga.updateOrgaRights(user, request.json.get('orga_id'), request.json.get('rights'))
    return make_response(jsonify(ret.get('data')), ret.get('status'))

@router.route('/updateMemberTag', methods=['POST'])
@requires_auth
def updateMembertag(user):
    ret = base_orga.updateMemberTag(user, request.json.get('orga_id'), request.json.get('addr'), request.json.get('tag'))
    return make_response(jsonify(ret.get('data')), ret.get('status'))

@router.route('/inviteUsersToOrga', methods=["POST"])
@requires_auth
def inviteUsersToOrga(user):
    if ensure_fields(['orga_id', 'invited_users', 'socketid'], request.json):
        ret = base_orga.inviteUsers(user, request.json.get('orga_id'), request.json.get('invited_users'))
        return make_response(jsonify(ret.get('data')), ret.get('status'))
    else:
        return make_response("Wrong request format", 400)

@router.route('/createOffer', methods=["POST"])
@requires_auth
def createOffer(user):
    if ensure_fields(['password', 'socketid', 'orga_id', {'offer': ['name', 'client', 'contractor', 'initialWithdrawal', 'isPermanent', 'isRecurrent', 'duration', 'type', 'description']}], request.json):
        ret = base_orga.createOffer(user, request.json.get('password'), request.json.get('orga_id'), request.json.get('offer'))
        return make_response(jsonify(ret.get('data')), ret.get('status'))
    else:
        return make_response("Wrong request format", 400)

@router.route('/cancelOffer', methods=["POST"])
@requires_auth
def cancelOffer(user, orga_id, offer_id):
    if ensure_fields(['password', 'socketid', 'orga_id', 'offer_id'], request.json):
        ret = base_orga.cancelOffer(user, request.json.get('password'), request.json.get('orga_id'), request.json.get('offer_id'))
        return make_response(jsonify(ret.get('data')), ret.get('status'))
    else:
        return make_response("Wrong request format", 400)

@router.route('/createProposal', methods=["POST"])
@requires_auth
def createProposal(user):
    if ensure_fields(['password', 'socketid', 'orga_id', 'offer'], request.json):
        ret = base_orga.createProposal(user, request.json.get('password'), request.json.get('orga_id'), request.json.get('offer'), request.json.get('duration'))
        return make_response(jsonify(ret.get('data')), ret.get('status'))
    else:
        return make_response("Wrong request format", 400)

@router.route('/voteForProposal', methods=["POST"])
@requires_auth
def voteForProposal(user):
    if ensure_fields(['password', 'socketid', 'orga_id', 'proposal_id', 'vote'], request.json):
        ret = base_orga.voteForProposal(user, request.json.get('password'), request.json.get('orga_id'), request.json.get('proposal_id'), request.json.get('vote'))
        return make_response(jsonify(ret.get('data')), ret.get('status'))
    else:
        return make_response("Wrong request format", 400)

@router.route('/refreshProposals/<orga_id>')
def refreshProposals(orga_id):
    ret = base_orga.refreshProposals(orga_id)
    return make_response(jsonify(ret.get('data')), ret.get('status'))

@router.route('/executeProposal', methods=["POST"])
@requires_auth
def executeProposal(user):
    if ensure_fields(['password', 'socketid', 'orga_id', 'proposal_id'], request.json):
        ret = base_orga.executeProposal(user, request.json.get('password'), request.json.get('orga_id'), request.json.get('proposal_id'))
        return make_response(jsonify(ret.get('data')), ret.get('status'))
    else:
        return make_response("Wrong request format", 400)

@router.route('/withdrawFundsFromOffer', methods=["POST"])
@requires_auth
def withdrawFundsFromOffer(user):
    if ensure_fields(['password', 'socketid', 'orga_id', 'offer_id'], request.json):
        ret = base_orga.withdrawFundsFromOffer(user, request.json.get('password'), request.json.get('orga_id'), request.json.get('offer_id'))
        return make_response(jsonify(ret.get('data')), ret.get('status'))
    else:
        return make_response("Wrong request format", 400)


@router.route('/getOrgaTransaction/<orga_id>', methods=['GET'])
@requires_auth
def getOrgaTransaction(user, orga_id):
    if orga_id:
        ret = base_orga.getOrgaTransaction(user)
        return make_response(jsonify(ret.get('data')), ret.get('status'))
    else:
        return make_response("Wrong request format", 400)

@router.route('/getGovernanceRights', methods=["GET"])
def getRights():
    ret = base_orga.getGovernanceRights()
    return make_response(jsonify(ret.get('data')), ret.get('status'))
    if ensure_fields('socketid', request.json):
        ret = base_orga.getGovernanceRights()
        return make_response(jsonify(ret.get('data')), ret.get('status'))
    else:
        return make_response("Wrong request format", 400)

#### NEWS ###


@router.route('/publish_news', methods=["POST"])
@requires_auth
def publish_news(user):
    if ensure_fields(['title', 'text', 'orga_id'], request.json):
        ret = base_orga.publishNews(user, request.json.get("title"), request.json.get("text"), request.json.get("orga_id"), request.json.get("yt_url"))
        return make_response(jsonify(ret.get('data')), ret.get('status'))
    else:
        return make_response("Wrong request format", 400)


@router.route('/publish_news_photo', methods=["POST"])
@requires_auth
def publish_news_photo(user):
    ret = base_orga.publishNewsPhoto(user,
                                     request.form.get("orga_id"),
                                     request.form.get("news_key"),
                                     request.files.get("pic"),
                                     request.form.get("name"),
                                     request.form.get("type"))
    return make_response(jsonify(ret.get('data')), ret.get('status'))


@router.route('/get_news_photo', methods=["POST"])
def get_news_photo():
    ret = base_orga.getNewsPhoto(request.json.get("orga_id"), request.json.get("news_key"))
    return make_response(jsonify(ret.get('data')), ret.get('status'))
