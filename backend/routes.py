from flask import request, Response, jsonify, make_response, send_file
from time import strftime, time
import os
from shutil import copyfile
from uuid import uuid4
from random import randint
from backend.dbquery import DBSQLite
import mysql.connector, io
from base64 import b64decode,b64encode
from zipfile import ZipFile
from datetime import datetime
from . import app

@app.route("/create_room", methods=['POST'])
def create_room():
    data = request.get_json()
    dbr = DBSQLite('chatbot.sqlite')
    cursorObj = dbr.conn.cursor()

    try:
        if data['privilege'] == 'penjual':
            cursorObj.execute('''
                INSERT INTO chatbot(uuid, privilege, amount_seller, username_seller, username_buyer)
                VALUES(?, ?, ?, ?, ?)''', (
                data['uuid'],
                data['privilege'],
                data['amount'],
                data['username'],
                'none'
            ))
            msg = f"[SYSTEM] HELLO INI INITIAL MESSAGE DARI \"{data['username']}\", HARAP SELESAIKAN PEMBAYARAN SENILAI Rp.{data['amount']:,} KE REKENING KAMI DI 13371337 BCA A/N RekBerSama"
            cursorObj.execute('''
                INSERT INTO chatroom(uuid, msg_iter, msg_text)
                VALUES(?, ?, ?)''', (
                data['uuid'],
                0,
                msg
            ))

        elif data['privilege'] == 'pembeli':
            cursorObj.execute('''
                UPDATE chatbot SET username_buyer = ?
                WHERE uuid = ?''', (
                data['username'],
                data['uuid']
            ))
            msg = f"[SYSTEM] USER \"{data['username']}\" TELAH MASUK KEDALAM CHATBOT ..."
            cursorObj.execute('''
                INSERT INTO chatroom(uuid, msg_iter, msg_text)
                VALUES(?, ?, ?)''', (
                data['uuid'],
                0,
                msg
            ))

        dbr.conn.commit()
        dbr.conn.close()

        return jsonify({
            "status": "success",
            "message": f"Room '{data['uuid']}' created successfully"
        }), 200

    except Exception as e:
        dbr.conn.rollback()
        dbr.conn.close()
        return jsonify({"status": "error", "message": str(e)}), 400
    

@app.route("/get_message", methods=['POST'])
def get_message():
    if request.method == 'POST':
        data = request.get_json()
        dbr = DBSQLite('chatbot.sqlite')
        cursorObj=dbr.conn.cursor()
        cursorObj.execute('SELECT msg_text FROM chatroom WHERE uuid = ?', (
                data['uuid'],
            )
        )
        rows = cursorObj.fetchall()
        dbr.conn.commit()
        dbr.conn.close()
        return jsonify({
                "status": "success",
                "message": rows
            }), 200 


@app.route("/send_message", methods=['POST'])
def send_message():
    if request.method == 'POST':
        data = request.get_json()
        dbr = DBSQLite('chatbot.sqlite')
        cursorObj=dbr.conn.cursor()
        cursorObj.execute('''
            INSERT INTO chatroom(uuid, msg_text)
            VALUES(?, ?)''', (
            data['uuid'],
            data['msg']
        ))
        dbr.conn.commit()
        dbr.conn.close()
        return jsonify({
                "status": "success",
                "message": "send message success full"
            }), 200 


@app.errorhandler(404)
def page_404(e):
    resp = make_response(jsonify({"msg":request.headers.get('User-Agent')}), 404)
    resp.headers = {
        'Date': strftime("%a, %d %b %Y %H:%M:%S UTC"),#'Tue, 06 Apr 2021 21:37:44 GMT',
        "Accept-Ranges": "bytes",
        "Content-Type": "application/json",
        "X-Frame-Options": "SAMEORIGIN",
        "Content-Security-Policy": "frame-ancestors 'self'",
        "X-XSS-Protection": "1; mode=block",
        "X-Content-Type-Options": "nosniff",
    }
    return resp