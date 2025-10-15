"""
Modelo SQLAlchemy para documentos
"""
from datetime import datetime
from funcionalidades.core.infraestructura.database import db
from funcionalidades.core.infraestructura.datetime_utils import get_local_now_naive


class DocumentoModel(db.Model):
    """Modelo de base de datos para documentos"""
    
    __tablename__ = 'documentos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    embeddings = db.Column(db.JSON, nullable=True)  # Almacenar como JSON
    fecha_creacion = db.Column(db.DateTime, default=get_local_now_naive, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, default=get_local_now_naive, onupdate=get_local_now_naive, nullable=False)
    
    def __repr__(self):
        return f'<Documento {self.nombre}>'
