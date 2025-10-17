"""
Utilidades para manejo de fechas y horas
"""
from datetime import datetime
import pytz

# Zona horaria de Guatemala (constante para evitar repetición)
GUATEMALA_TZ = pytz.timezone('America/Guatemala')


def get_local_now():
    """
    Obtener la fecha y hora actual en la zona horaria de Guatemala
    
    Returns:
        datetime: Fecha y hora actual en zona horaria de Guatemala
    """
    return datetime.now(GUATEMALA_TZ)


def get_local_now_naive():
    """
    Obtener la fecha y hora actual en la zona horaria de Guatemala sin información de zona horaria
    
    Returns:
        datetime: Fecha y hora actual en zona horaria de Guatemala (naive)
    """
    return datetime.now()


def utc_to_local(utc_datetime):
    """
    Convertir datetime UTC a zona horaria de Guatemala
    
    Args:
        utc_datetime (datetime): Fecha y hora en UTC
        
    Returns:
        datetime: Fecha y hora en zona horaria de Guatemala
    """
    if utc_datetime is None:
        return None
    
    # Si ya tiene información de zona horaria, convertir
    if utc_datetime.tzinfo is not None:
        return utc_datetime.astimezone(GUATEMALA_TZ)
    
    # Si es naive, asumir que es UTC y convertir
    utc_tz = pytz.UTC
    utc_datetime = utc_tz.localize(utc_datetime)
    return utc_datetime.astimezone(GUATEMALA_TZ)


def local_to_utc(local_datetime):
    """
    Convertir datetime de Guatemala a UTC
    
    Args:
        local_datetime (datetime): Fecha y hora en zona horaria de Guatemala
        
    Returns:
        datetime: Fecha y hora en UTC
    """
    if local_datetime is None:
        return None
    
    # Si ya tiene información de zona horaria, convertir
    if local_datetime.tzinfo is not None:
        return local_datetime.astimezone(pytz.UTC)
    
    # Si es naive, asumir que es de Guatemala y convertir
    local_datetime = GUATEMALA_TZ.localize(local_datetime)
    return local_datetime.astimezone(pytz.UTC)


def format_datetime_for_api(dt):
    """
    Formatear datetime para API (ISO format con zona horaria)
    
    Args:
        dt (datetime): Fecha y hora a formatear
        
    Returns:
        str: Fecha formateada en ISO format
    """
    if dt is None:
        return None
    
    # Asegurar que tenga información de zona horaria
    if dt.tzinfo is None:
        dt = GUATEMALA_TZ.localize(dt)
    
    return dt.isoformat()


def parse_datetime_from_api(dt_string):
    """
    Parsear datetime desde API
    
    Args:
        dt_string (str): Fecha en formato ISO
        
    Returns:
        datetime: Fecha parseada en zona horaria de Guatemala
    """
    if not dt_string:
        return None
    
    try:
        # Intentar parsear con información de zona horaria
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return utc_to_local(dt)
    except ValueError:
        # Si falla, intentar parsear como naive y asumir UTC
        dt = datetime.fromisoformat(dt_string)
        return utc_to_local(dt)

