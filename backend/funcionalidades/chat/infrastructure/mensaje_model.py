"""
Modelo SQLAlchemy para mensajes
"""
from datetime import datetime
from funcionalidades.core.infraestructura.database import db


class MensajeModel(db.Model):
    """Modelo de base de datos para mensajes"""
    
    __tablename__ = 'mensajes'
    
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    es_usuario = db.Column(db.Boolean, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'), nullable=True)
    
    def __repr__(self):
        return f'<Mensaje {self.id}: {"Usuario" if self.es_usuario else "Bot"}>'
