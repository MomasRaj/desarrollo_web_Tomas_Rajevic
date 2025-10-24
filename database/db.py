from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, Enum, Text, DateTime, case
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
from sqlalchemy.sql import func
from datetime import datetime
import json


DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# --- Models ---

class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)

    comunas = relationship('Comuna', back_populates='region')


class Comuna(Base):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    region = relationship('Region', back_populates='comunas')
    avisos = relationship('AvisoAdopcion', back_populates='comuna')


class AvisoAdopcion(Base):
    __tablename__ = 'aviso_adopcion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(DateTime, nullable=False, server_default=func.now())
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100))
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15))
    tipo = Column(Enum('gato', 'perro'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    unidad_medida = Column(Enum('a', 'm'), nullable=False)  #
    fecha_entrega = Column(DateTime, nullable=False)
    descripcion = Column(Text(500))

    comuna = relationship('Comuna', back_populates='avisos')
    fotos = relationship('Foto', back_populates='aviso', cascade="all, delete-orphan")
    contactos = relationship('ContactarPor', back_populates='aviso', cascade="all, delete-orphan")
    comentarios = relationship('Comentario', back_populates='aviso', cascade="all, delete-orphan")


class Foto(Base):
    __tablename__ = 'foto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey('aviso_adopcion.id'), nullable=False)

    aviso = relationship('AvisoAdopcion', back_populates='fotos')


class ContactarPor(Base):
    __tablename__ = 'contactar_por'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey('aviso_adopcion.id'), nullable=False)

    aviso = relationship('AvisoAdopcion', back_populates='contactos')


class Comentario(Base):
    __tablename__ = 'comentario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)
    texto = Column(String(300), nullable=False)
    fecha = Column(DateTime, nullable=False, server_default=func.now())
    aviso_id = Column(Integer, ForeignKey('aviso_adopcion.id'), nullable=False)

    aviso = relationship('AvisoAdopcion', back_populates='comentarios')
    
# --- Database Functions ---

def get_all_regiones():
    session = SessionLocal()
    regiones = session.query(Region).all()
    session.close()
    return regiones

def get_comunas_by_region(region_id):
    session = SessionLocal()
    comunas = session.query(Comuna).filter_by(region_id=region_id).all()
    session.close()
    return comunas


def get_ultimo_avisos(limit=5):
    session = SessionLocal()
    #pequeño fix usando cosas de metodologias
    try:
        avisos = session.query(AvisoAdopcion).join(Comuna).join(Region).options(joinedload(AvisoAdopcion.fotos),joinedload(AvisoAdopcion.comuna).joinedload(Comuna.region)).order_by(AvisoAdopcion.fecha_ingreso.desc()).limit(limit).all()
        
        result = []
        for aviso in avisos:
            # fuerza carga de relaciones
            _ = aviso.fotos
            comuna_nombre = aviso.comuna.nombre if aviso.comuna else None

            # tomar primera foto si existe
            foto_path = None
            if aviso.fotos and len(aviso.fotos) > 0:
                foto_path = aviso.fotos[0].ruta_archivo

            result.append({
                "id": aviso.id,
                "nombre": aviso.nombre,
                "tipo": aviso.tipo,
                "cantidad": aviso.cantidad,
                "edad": aviso.edad,
                "unidad_medida": aviso.unidad_medida,
                "descripcion": aviso.descripcion,
                "fecha": aviso.fecha_ingreso.strftime("%Y-%m-%d") if aviso.fecha_ingreso else None,
                "comuna": comuna_nombre,
                "foto": foto_path,
            })

        return result
    finally:
        session.close()

def get_aviso_by_id(aviso_id):
    session = SessionLocal()
    aviso = session.query(AvisoAdopcion).filter_by(id=aviso_id).first()
    session.close()
    return aviso

def crear_aviso(comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion):
    session = SessionLocal()
    nuevo_aviso = AvisoAdopcion(
        fecha_ingreso=datetime.now(),
        comuna_id=comuna_id,
        sector=sector,
        nombre=nombre,
        email=email,
        celular=celular,
        tipo=tipo,
        cantidad=cantidad,
        edad=edad,
        unidad_medida=unidad_medida,
        fecha_entrega=fecha_entrega,
        descripcion=descripcion
    )
    session.add(nuevo_aviso)
    session.commit()
    session.refresh(nuevo_aviso)
    session.close()
    return nuevo_aviso


def agregar_foto(aviso_id, ruta_archivo, nombre_archivo):
    session = SessionLocal()
    nueva_foto = Foto(
        actividad_id=aviso_id,
        ruta_archivo=ruta_archivo,
        nombre_archivo=nombre_archivo
    )
    session.add(nueva_foto)
    session.commit()
    session.close()

def get_fotos_por_aviso(aviso_id):
    session = SessionLocal()
    fotos = session.query(Foto).filter_by(actividad_id=aviso_id).all()
    session.close()
    return fotos

def get_comuna_by_id(comuna_id):
    session = SessionLocal()
    try:
        comuna = session.query(Comuna).filter_by(id=comuna_id).first()
        return comuna
    finally:
        session.close()

def agregar_contacto(aviso_id, nombre, identificador):
    session = SessionLocal()
    contacto = ContactarPor(
        actividad_id=aviso_id,
        nombre=nombre,
        identificador=identificador
    )
    session.add(contacto)
    session.commit()
    session.close()

def get_contactos_por_aviso(aviso_id):
    session = SessionLocal()
    contactos = session.query(ContactarPor).filter_by(actividad_id=aviso_id).all()
    session.close()
    return contactos


# ------- nuevas funciones para la tarea3(y cosas que faltaban) -------

def count_avisos():
    session = SessionLocal()
    return int(session.query(AvisoAdopcion).count())

def get_stats_type_from_db():
    session = SessionLocal()
    rows = session.query(
                AvisoAdopcion.tipo.label("type"),
                func.count(AvisoAdopcion.id).label("count"),
            ) \
            .group_by(AvisoAdopcion.tipo) \
            .all()

    result = [{"type": r.type, "count": int(r.count)} for r in rows]
    session.close()
    return result

def get_stats_monthly_type_from_db():
    session = SessionLocal()
    month_expr = func.date_format(AvisoAdopcion.fecha_ingreso, "%Y-%m")
    perro_sum = func.sum(case((AvisoAdopcion.tipo == 'perro', 1), else_=0)).label("perro")
    gato_sum = func.sum(case((AvisoAdopcion.tipo == 'gato', 1), else_=0)).label("gato")

    rows = session.query(
                month_expr.label("month"),
                perro_sum,
                gato_sum,
            ) \
            .group_by(month_expr) \
            .order_by(month_expr) \
            .all()

    result = []
    for r in rows:
        result.append({"month": r.month, "perro": int(r.perro or 0), "gato": int(r.gato or 0)})
    session.close()
    return result

def get_stats_data_from_db():
    session = SessionLocal()
    rows = session.query(
        func.date(AvisoAdopcion.fecha_ingreso).label("date"),
        func.count(AvisoAdopcion.id).label("count"),
    ).group_by(func.date(AvisoAdopcion.fecha_ingreso)) \
    .order_by(func.date(AvisoAdopcion.fecha_ingreso)) \
    .all()

    result = []
    for r in rows:
        d = r.date
        date_str = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
        result.append({"date": date_str, "count": int(r.count)})
    session.close()
    return result


def get_aviso_detail_dict(aviso_id):
    session = SessionLocal()
    aviso = session.query(AvisoAdopcion) \
        .options(joinedload(AvisoAdopcion.fotos), joinedload(AvisoAdopcion.comuna)) \
        .filter(AvisoAdopcion.id == aviso_id) \
        .first()

    if not aviso:
        session.close()
        return None

    comuna_nombre = aviso.comuna.nombre if aviso.comuna else None
    fotos = [f.ruta_archivo for f in aviso.fotos] if aviso.fotos else []

    result = {
        "id": aviso.id,
        "nombre": aviso.nombre,
        "tipo": aviso.tipo,
        "cantidad": aviso.cantidad,
        "edad": aviso.edad,
        "unidad_medida": aviso.unidad_medida,
        "sector": aviso.sector,
        "descripcion": aviso.descripcion,
        "fecha": aviso.fecha_ingreso.strftime("%Y-%m-%d") if aviso.fecha_ingreso else None,
        "comuna": comuna_nombre,
        "email": aviso.email,
        "celular": aviso.celular,
        "fotos": fotos,
    }
    session.close()
    return result

def get_avisos_paginated(limit=5, offset=0):
    session = SessionLocal()
    q = (
        session.query(AvisoAdopcion)
        .options(joinedload(AvisoAdopcion.fotos), joinedload(AvisoAdopcion.comuna))
        .order_by(AvisoAdopcion.fecha_ingreso.desc())
        .limit(limit)
        .offset(offset)
    )
    avisos = q.all()

    result = []
    for aviso in avisos:
        comuna_nombre = aviso.comuna.nombre if aviso.comuna else None
        foto_path = aviso.fotos[0].ruta_archivo if aviso.fotos else None
        result.append({
            "id": aviso.id,
            "nombre": aviso.nombre,
            "tipo": aviso.tipo,
            "cantidad": aviso.cantidad,
            "edad": aviso.edad,
            "unidad_medida": aviso.unidad_medida,
            "sector": aviso.sector,
            "descripcion": aviso.descripcion,
            "fecha": aviso.fecha_ingreso.strftime("%Y-%m-%d") if aviso.fecha_ingreso else None,
            "comuna": comuna_nombre,
            "foto": foto_path,
        })

    session.close()
    return result

def add_comment_to_aviso(aviso_id, nombre, comentario):
    session = SessionLocal()
    new_comment = Comentario(
        nombre=nombre,
        texto=comentario,
        fecha=datetime.now(),
        aviso_id=aviso_id
    )
    session.add(new_comment)
    session.commit()        
    session.refresh(new_comment)
    result = {
        "id": new_comment.id,
        "nombre": new_comment.nombre,
        "texto": new_comment.texto,
        "fecha": new_comment.fecha.strftime("%Y-%m-%d %H:%M:%S") if new_comment.fecha else None,
        "aviso_id": new_comment.aviso_id,
    }
    session.close()
    return result


def get_comentarios_por_aviso(aviso_id):
    session = SessionLocal()
    comentarios = session.query(Comentario).filter_by(aviso_id=aviso_id).order_by(Comentario.fecha.asc()).all()
    result = []
    for c in comentarios:
        result.append({
            "id": c.id,
            "nombre": c.nombre,
            "texto": c.texto,
            "fecha": c.fecha.strftime("%Y-%m-%d %H:%M:%S") if c.fecha else None,
        })
    session.close()
    return result