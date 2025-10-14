"""
Modelo SQLAlchemy para documentos
"""
from datetime import datetime
from funcionalidades.core.infraestructura.database import db


class DocumentoModel(db.Model):
    """Modelo de base de datos para documentos"""
    
    __tablename__ = 'documentos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    embeddings = db.Column(db.JSON, nullable=True)  # Almacenar como JSON
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Documento {self.nombre}>'
