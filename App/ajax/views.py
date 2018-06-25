from flask import render_template, redirect, request, url_for, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from . import ajax
from model.model import *


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


@ajax.route('/visitor', methods=['POST', 'GET'])
@login_required
def get_visitor():
    if current_user and current_user.email == "voterlin@foxmail.com":
        visitor = Visitor().select(oderby="member_since", isasc=False)
        return jsonify(visitor)
    return "None Info"


@ajax.route('/account', methods=['POST', 'GET'])
@login_required
def get_account():
    if current_user.email == "voterlin@foxmail.com":
        account = Account().select(oderby="timestamp", isasc=False)
        return jsonify(account)
    return "None Info"


@ajax.route('/table', methods=['GET'])
def get_table():
    # 0 one_day / 1 top_word / 2 one_word
    type = request.args.get('type', 0, type=int)
    if type is 0:
        time = now(1)
        fre = Frequency(time=time).select(oderby='times', isasc=False, limit=20)
        return jsonify(day_search_result(fre))
    elif type is 1:
        web = Website().select(oderby='time', isasc=False, limit=20)
        return jsonify(top_word_result(web))
    elif type is 3:
        web = Website().select(oderby='time', isasc=False, limit=20)
        return jsonify(one_day_news_result(web))
    elif type is 2:
        word = request.args.get('word', '', type=str)
        fre = Frequency(word=word).select(oderby='time', isasc=True, limit=20)
        return jsonify(word_search_result(fre))


def one_day_news_result(web):
    data = []
    lables = []
    for w in web:
        data.append(w.news_count)
        lables.append(str(w.time))
    return {'data': data, 'labels': lables}


def top_word_result(web):
    data = []
    lables = []
    for w in web:
        data.append(w.top_word_count)
        lables.append(w.top_word)
    return {'data': data, 'labels': lables}


def day_search_result(fre):
    data = []
    lables = []
    for f in fre:
        data.append(f.times)
        lables.append(f.word)
    return {'data': data, 'labels': lables}


def word_search_result(fre):
    data = []
    lables = []
    for f in fre:
        data.append(f.times)
        lables.append(str(f.time))
    return {'data': data, 'labels': lables}
