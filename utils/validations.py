import re
import filetype

def validate_name(name):
    if not name:
        return False
    length_valid = len(name.strip()) >= 3 and len(name.strip()) <= 200
    return length_valid

def validate_contact(contact):
    if not contact:
        return True
    length_valid = len(contact.strip()) >= 4 and len(contact.strip()) <= 50
    return length_valid

def validate_sector(sector):
    if not sector:
        return True
    length_valid = len(sector.strip()) <= 100
    return length_valid

def validate_email(email):
    if not email:
        return False
    length_valid = len(email) <= 100
    re_format = re.compile(r'^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$')
    format_valid = bool(re_format.match(email))
    return length_valid and format_valid

def validate_phone_number(phone_number):
    if not phone_number:
        return True
    length_valid = len(phone_number) >= 8
    format_valid = bool(re.match(r'^[0-9]+$', phone_number))
    return length_valid and format_valid

def validate_files(files):
    if not files or len(files) == 0:
        return False
    length_valid = len(files) >= 1 and len(files) <= 5
    type_valid = True
    for f in files:
        ftype_guess = filetype.guess(f)
        if not ftype_guess:
            type_valid = False
            break
        if not (ftype_guess.mime.startswith("image/") or ftype_guess.mime == "application/pdf"):
            type_valid = False
            break
    return length_valid and type_valid

def validate_select(select):
    if not select:
        return False
    return True

def validate_type(select):
    if not select or (select != "perro" and select != "gato"):
        return False
    return True

def validate_unit(select):
    if not select or (select != "meses" and select != "años"):
        return False
    return True

def validate_number(number):
    if number is None:
        return False
    try:
        number = int(number)
    except:
        return False
    if number < 1:
        return False
    return True

def validate_date(date):
    if date is None or date.strip() == "":
        return False
    re_format = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$')
    return bool(re_format.match(date))

def validate_form(form):
    email = form.get("email")
    phone_number = form.get("numero")
    name = form.get("nombre")
    region = form.get("region")
    comuna = form.get("comuna")
    cantidad = form.get("cantidad")
    edad = form.get("edad")
    fecha = form.get("fecha")
    sector = form.get("sector")
    tipo = form.get("tipo")
    unidad = form.get("unidad")
    contacto = form.get("contacto")
    files = form.get("fotos", [])

    invalid_inputs = []
    is_valid = True

    def set_invalid_input(input_name):
        invalid_inputs.append(input_name)

    if not validate_sector(sector):
        set_invalid_input("Sector")
        is_valid = False
    if not validate_name(name):
        set_invalid_input("nombre")
        is_valid = False
    if not validate_email(email):
        set_invalid_input("Email")
        is_valid = False
    if not validate_phone_number(phone_number):
        set_invalid_input("Número")
        is_valid = False
    if not validate_files(files):
        set_invalid_input("Fotos")
        is_valid = False
    if not validate_select(region):
        set_invalid_input("Región")
        is_valid = False
    if not validate_select(comuna):
        set_invalid_input("Comuna")
        is_valid = False
    if not validate_number(cantidad):
        set_invalid_input("Cantidad de mascotas")
        is_valid = False
    if not validate_number(edad):
        set_invalid_input("Edad de la mascota")
        is_valid = False
    if not validate_date(fecha):
        set_invalid_input("Fecha disponible para entrega")
        is_valid = False
    if not validate_type(tipo):
        set_invalid_input("Tipo de animal")
        is_valid = False
    if not validate_unit(unidad):
        set_invalid_input("Unidad de edad")
        is_valid = False
    if not validate_contact(contacto):
        set_invalid_input("Contacto")
        is_valid = False

    return is_valid

# -----------Tarea3------------
def validate_nombre(nombre):
    if not nombre:
        return False
    length_valid = len(nombre.strip()) >= 3 and len(nombre.strip()) <= 80
    return length_valid

def validate_coment(comment):
    if not comment:
        return False
    length_valid = len(comment.strip()) >= 5
    return length_valid

