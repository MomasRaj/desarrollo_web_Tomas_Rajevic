from flask import Flask, request, render_template, redirect, url_for, session
from utils.validations import validate_form
from database import db
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os
import uuid

UPLOAD_FOLDER = 'static/Listado_aviso/Animales_aviso'

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# --- Auth routes ---

@app.route('/')
def inicio():
    avisos = db.get_ultimo_avisos(limit=5)
    return render_template('index.html', avisos=avisos)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/form', methods=['POST'])
def agregar_aviso():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        numero = request.form.get("numero")
        region = request.form.get("region")
        comuna = request.form.get("comuna")
        sector = request.form.get("sector")
        tipo = request.form.get("tipo")
        cantidad = request.form.get("cantidad")
        edad = request.form.get("edad")
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
            aviso=db.crear_aviso(comuna, sector, nombre, email, numero, tipo, cantidad, edad, unidad, fecha, descripcion)
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

        


    

@app.route('/list')
def list():
    return render_template('Animales/listado.html')

@app.route('/stats')
def stats():
    return render_template('estadisticas.html')

if __name__ == "__main__":
    app.run(debug=True)
