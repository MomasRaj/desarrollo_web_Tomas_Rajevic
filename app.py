from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from utils.validations import validate_form, validate_nombre, validate_coment
from database import db
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os
import uuid
import random
from datetime import datetime, timedelta
import time
from flask_cors import cross_origin
from jinja2 import TemplateNotFound

UPLOAD_FOLDER = 'static/Listado_avisos/Animales_aviso'

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# --- Auth routes ---

@app.route('/')
def inicio():
    avisos = db.get_ultimo_avisos(limit=5)
    return render_template('index.html', avisos=avisos)


@app.route('/form', methods=['Get','POST'])
def agregar_aviso():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        numero = request.form.get("numero")
        region = int(request.form.get("region"))
        comuna = request.form.get("comuna")
        sector = request.form.get("sector")
        tipo = request.form.get("tipo")
        cantidad = int(request.form.get("cantidad"))
        edad = int(request.form.get("edad"))
        unidad = request.form.get("unidad")
        fecha = request.form.get("fecha")
        descripcion = request.form.get("descripcion")
        contacto = request.form.get("contacto")
        contactar_por = request.form.get("contactar")
        fotos = request.files.getlist("foto[]")
        formulario = {
            "nombre": nombre,
            "email": email,
            "numero": numero,
            "region": region,
            "comuna": comuna,
            "sector": sector,
            "tipo": tipo,
            "cantidad": cantidad,
            "edad": edad,
            "unidad": unidad,
            "fecha": fecha,
            "descripcion": descripcion,
            "contacto": contacto,
            "fotos": fotos
        }
        if(validate_form(formulario)):
            session = db.SessionLocal()
            if(unidad == "meses"):
                unidad = "m"
            else:
                unidad = "a"
            aviso=db.crear_aviso(comuna, sector, nombre, email, numero, tipo, cantidad, edad, unidad, fecha, descripcion)
            session.close()
            for f in fotos:
                if f.filename:
                    filename = secure_filename(f.filename)
                    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                    f.save(path)
                    db.agregar_foto(aviso.id, path, filename)
            if contacto and contactar_por:
                db.agregar_contacto(aviso.id, contactar_por, contacto)
            return redirect(url_for('inicio'))
        else:
            return render_template('form.html', error="Por favor corrija los campos inválidos.", form=formulario)
    return render_template('form.html')
        


    

@app.route('/list')
def list():
    session = None
    try:
        try:
            page = int(request.args.get("page", 1))
        except Exception:
            page = 1
        per_page = 5
        if page < 1:
            page = 1
        offset = (page - 1) * per_page

        total = db.count_avisos()
        total_pages = max(1, (int(total) + per_page - 1) // per_page)

        avisos = db.get_avisos_paginated(limit=per_page, offset=offset)

        return render_template(
            'Animales/listado.html',
            avisos=avisos,
            page=page,
            total_pages=total_pages,
            per_page=per_page,
            total=total
        )
    except Exception as e:
        print("list error:", e)
        return render_template('Animales/listado.html', avisos=[])
    finally:
        if session:
            session.close()


@app.route('/aviso/<int:aid>')
def aviso_detail(aid):
    aviso = db.get_aviso_detail_dict(aid)
    comentarios = db.get_comentarios_por_aviso(aid)
    return render_template('Animales/animal.html', aviso=aviso, comentarios=comentarios)


@app.route('/aviso/<int:aid>/comentarios', methods=['GET', 'POST'])
def aviso_comentarios(aid):
    if request.method == 'GET':
        rows = db.get_comentarios_por_aviso(aid)
        return jsonify(rows), 200
    if request.method == "POST":
        data = request.get_json() or {}
        nombre = data.get("nombre")
        comentario = data.get("comentario_box")
        if validate_nombre(nombre) and validate_coment(comentario):
            db.add_comment_to_aviso(aid, nombre, comentario)
        else:
            error = "Por favor corrija los campos inválidos."
            aviso = db.get_aviso_detail_dict(aid)
            return render_template('Animales/animal.html', aviso=aviso, error=error)
    return redirect(url_for('aviso_detail', aid=aid))


@app.route('/stats', methods=["GET"])
def stats():
    return render_template('estadisticas.html')



@app.route("/get-stats-data", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def get_stats_data():
    data = db.get_stats_data_from_db()
    if data:
        return jsonify(data)


@app.route("/get-stats-type", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def get_stats_type():
    rows = db.get_stats_type_from_db()
    data = [{"type": r["type"], "count": int(r["count"])} for r in rows] if rows else []
    if data:
        return jsonify(data)



@app.route("/get-stats-monthly-type", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def get_stats_monthly_type():
    data = db.get_stats_monthly_type_from_db()
    if data:
        return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
