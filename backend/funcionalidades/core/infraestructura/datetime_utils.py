"""
Utilidades para manejo de fechas y horas
"""
from datetime import datetime
import pytz


def get_local_now():
    """
    Obtener la fecha y hora actual en la zona horaria local
    
    Returns:
        datetime: Fecha y hora actual en zona horaria local
    """
    # Obtener la zona horaria local del sistema
    local_tz = pytz.timezone('America/Mexico_City')  # Ajustar según la zona horaria deseada
    return datetime.now(local_tz)


def get_local_now_naive():
    """
    Obtener la fecha y hora actual en la zona horaria local sin información de zona horaria
    
    Returns:
        datetime: Fecha y hora actual en zona horaria local (naive)
    """
    return datetime.now()


def utc_to_local(utc_datetime):
    """
    Convertir datetime UTC a zona horaria local
    
    Args:
        utc_datetime (datetime): Fecha y hora en UTC
        
    Returns:
        datetime: Fecha y hora en zona horaria local
    """
    if utc_datetime is None:
        return None
    
    # Si ya tiene información de zona horaria, convertir
    if utc_datetime.tzinfo is not None:
        local_tz = pytz.timezone('America/Mexico_City')
        return utc_datetime.astimezone(local_tz)
    
    # Si es naive, asumir que es UTC y convertir
    utc_tz = pytz.UTC
    local_tz = pytz.timezone('America/Mexico_City')
    utc_datetime = utc_tz.localize(utc_datetime)
    return utc_datetime.astimezone(local_tz)


def local_to_utc(local_datetime):
    """
    Convertir datetime local a UTC
    
    Args:
        local_datetime (datetime): Fecha y hora en zona horaria local
        
    Returns:
        datetime: Fecha y hora en UTC
    """
    if local_datetime is None:
        return None
    
    # Si ya tiene información de zona horaria, convertir
    if local_datetime.tzinfo is not None:
        return local_datetime.astimezone(pytz.UTC)
    
    # Si es naive, asumir que es local y convertir
    local_tz = pytz.timezone('America/Mexico_City')
    utc_tz = pytz.UTC
    local_datetime = local_tz.localize(local_datetime)
    return local_datetime.astimezone(utc_tz)


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
        local_tz = pytz.timezone('America/Mexico_City')
        dt = local_tz.localize(dt)
    
    return dt.isoformat()


def parse_datetime_from_api(dt_string):
    """
    Parsear datetime desde API
    
    Args:
        dt_string (str): Fecha en formato ISO
        
    Returns:
        datetime: Fecha parseada
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
