from flask import render_template, redirect, request, url_for, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from . import ajax
from Model.model import *


@ajax.route('/thumb', methods=['POST', 'GET'])
@login_required
def thumb():
    is_del = request.args.get('del', 0, type=int)
    operand = request.args.get('oper', 0, type=int)
    operand_id = request.args.get('id', 0, type=int)
    oper = OPERAND[operand](id=operand_id).select(getone=True)
    is_thumb = oper.is_thumb(current_user.id)
    if is_del and is_thumb:
        oper.del_thumb(current_user.id)
    elif not is_thumb:
        oper.set_thumb(current_user.id)
    return True


@ajax.route('/collect', methods=['POST', 'GEt'])
@login_required
def collect():
    is_del = request.args.get('del', 0, type=int)
    operand = request.args.get('oper', 0, type=int)
    operand_id = request.args.get('id', 0, type=int)
    oper = OPERAND[operand](id=operand_id).select(getone=True)
    is_collect = oper.is_collect(current_user.id)
    if is_del and is_collect:
        oper.del_collect(current_user.id)
    elif not is_collect:
        oper.set_collect(current_user.id)
    return True


@ajax.route('/follow', methods=['POST', 'GET'])
@login_required
def follow():
    user_id = request.args.get('id', -1, type=int)
    print(user_id, current_user.id)
    user = Account(id=user_id).select(getone=True)
    if user_id is -1:
        return False
    if current_user.is_follow(user):
        current_user.unfollow(user)
        result = -1
    else:
        current_user.follow(user)
        result = 1
    return jsonify({'f': result})