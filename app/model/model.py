from app.utils.utils import db


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    proyectos = db.relationship('Proyecto', back_populates='usuario')

    def __init__(self, username, password):
        self.username = username
        self.password = password


# Modelo para Proyecto
class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nombre_proyecto = db.Column(db.String, nullable=False)
    objetivo_general = db.Column(db.String, nullable=False)

    usuario = db.relationship('Usuario', back_populates='proyectos')
    arbol_problema = db.relationship('ArbolProblema', back_populates='proyecto', uselist=False)
    arbol_objetivo = db.relationship('ArbolObjetivo', back_populates='proyecto', uselist=False)

    def __init__(self, id_usuario, nombre_proyecto, objetivo_general):
        self.id_usuario = id_usuario
        self.nombre_proyecto = nombre_proyecto
        self.objetivo_general = objetivo_general


# Modelo para ArbolProblema
class ArbolProblema(db.Model):
    __tablename__ = 'arbol_problemas'
    id = db.Column(db.Integer, primary_key=True)
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)

    proyecto = db.relationship('Proyecto', back_populates='arbol_problema')
    causas = db.relationship('Causa', back_populates='arbol_problema')
    efectos = db.relationship('Efecto', back_populates='arbol_problema')

    def __init__(self, id_proyecto):
        self.id_proyecto = id_proyecto


# Modelo para Causa
class Causa(db.Model):
    __tablename__ = 'causas'
    id_causa = db.Column(db.Integer, primary_key=True)
    id_arbol_problema = db.Column(db.Integer, db.ForeignKey('arbol_problemas.id'), nullable=False)
    tipo = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)

    arbol_problema = db.relationship('ArbolProblema', back_populates='causas')

    def __init__(self, id_arbol_problema, tipo, descripcion):
        self.id_arbol_problema = id_arbol_problema
        self.tipo = tipo
        self.descripcion = descripcion


# Modelo para Efecto
class Efecto(db.Model):
    __tablename__ = 'efectos'
    id_efecto = db.Column(db.Integer, primary_key=True)
    id_arbol_problema = db.Column(db.Integer, db.ForeignKey('arbol_problemas.id'), nullable=False)
    tipo = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)

    arbol_problema = db.relationship('ArbolProblema', back_populates='efectos')

    def __init__(self, id_arbol_problema, tipo, descripcion):
        self.id_arbol_problema = id_arbol_problema
        self.tipo = tipo
        self.descripcion = descripcion


# Modelo para ArbolObjetivo
class ArbolObjetivo(db.Model):
    __tablename__ = 'arbol_objetivos'
    id = db.Column(db.Integer, primary_key=True)
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)

    proyecto = db.relationship('Proyecto', back_populates='arbol_objetivo')
    especificos = db.relationship('Especifico', back_populates='arbol_objetivo')
    generales = db.relationship('General', back_populates='arbol_objetivo')

    def __init__(self, id_proyecto):
        self.id_proyecto = id_proyecto


# Modelo para Especifico
class Especifico(db.Model):
    __tablename__ = 'especificos'
    id_es = db.Column(db.Integer, primary_key=True)
    id_arbol_objetivo = db.Column(db.Integer, db.ForeignKey('arbol_objetivos.id'), nullable=False)
    descripcion = db.Column(db.String, nullable=False)

    arbol_objetivo = db.relationship('ArbolObjetivo', back_populates='especificos')

    def __init__(self, id_arbol_objetivo, descripcion):
        self.id_arbol_objetivo = id_arbol_objetivo
        self.descripcion = descripcion


# Modelo para General
class General(db.Model):
    __tablename__ = 'generales'
    id_ge = db.Column(db.Integer, primary_key=True)
    id_arbol_objetivo = db.Column(db.Integer, db.ForeignKey('arbol_objetivos.id'), nullable=False)
    descripcion = db.Column(db.String, nullable=False)

    arbol_objetivo = db.relationship('ArbolObjetivo', back_populates='generales')
    directos = db.relationship('Directo', back_populates='general')
    indirectos = db.relationship('Indirecto', back_populates='general')

    def __init__(self, id_arbol_objetivo, descripcion):
        self.id_arbol_objetivo = id_arbol_objetivo
        self.descripcion = descripcion


# Modelo para Fin
class Fin(db.Model):
    __tablename__ = 'fines'
    id = db.Column(db.Integer, primary_key=True)
    id_arbol_objetivo = db.Column(db.Integer, db.ForeignKey('arbol_objetivos.id'), nullable=False)
    tipo = db.Column(db.String, nullable=False)

    def __init__(self, id_arbol_objetivo, tipo):
        self.id_arbol_objetivo = id_arbol_objetivo
        self.tipo = tipo


# Modelo para Directo
class Directo(db.Model):
    __tablename__ = 'directos'
    id_de = db.Column(db.Integer, primary_key=True)
    id_ge = db.Column(db.Integer, db.ForeignKey('generales.id'), nullable=False)
    descripcion = db.Column(db.String, nullable=False)

    general = db.relationship('General', back_populates='directos')

    def __init__(self, id_ge, descripcion):
        self.id_ge = id_ge
        self.descripcion = descripcion


# Modelo para Indirecto
class Indirecto(db.Model):
    __tablename__ = 'indirectos'
    id_ie = db.Column(db.Integer, primary_key=True)
    id_ge = db.Column(db.Integer, db.ForeignKey('generales.id'), nullable=False)
    descripcion = db.Column(db.String, nullable=False)

    general = db.relationship('General', back_populates='indirectos')

    def __init__(self, id_ge, descripcion):
        self.id_ge = id_ge
        self.descripcion = descripcion


# Modelo para Bot_IA
class BotIA(db.Model):
    __tablename__ = 'bot_ia'
    id = db.Column(db.Integer, primary_key=True)
    nombre_proyecto = db.Column(db.String, nullable=False)

    def __init__(self, nombre_proyecto):
        self.nombre_proyecto = nombre_proyecto
