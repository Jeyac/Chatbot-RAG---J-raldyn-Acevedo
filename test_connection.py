#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión entre frontend y backend
"""

import requests
import json

def test_backend_connection():
    """Probar conexión con el backend"""
    print("🔍 Probando conexión con el backend...")
    
    try:
        # Probar endpoint principal
        response = requests.get('http://localhost:5000/')
        if response.status_code == 200:
            print("✅ Backend conectado correctamente")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Error en backend: {response.status_code}")
            return False
            
        # Probar endpoint de salud
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("✅ Health check exitoso")
            health_data = response.json()
            print(f"   Estado: {health_data}")
        else:
            print(f"❌ Error en health check: {response.status_code}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend en http://localhost:5000")
        print("   Asegúrate de que el backend esté ejecutándose")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def test_frontend_connection():
    """Probar conexión con el frontend"""
    print("\n🔍 Probando conexión con el frontend...")
    
    try:
        response = requests.get('http://localhost:3000/')
        if response.status_code == 200:
            print("✅ Frontend conectado correctamente")
            return True
        else:
            print(f"❌ Error en frontend: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al frontend en http://localhost:3000")
        print("   Asegúrate de que el frontend esté ejecutándose")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de conexión...\n")
    
    backend_ok = test_backend_connection()
    frontend_ok = test_frontend_connection()
    
    print("\n📊 Resumen de pruebas:")
    print(f"   Backend: {'✅ OK' if backend_ok else '❌ FALLO'}")
    print(f"   Frontend: {'✅ OK' if frontend_ok else '❌ FALLO'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 ¡Todas las conexiones funcionan correctamente!")
        print("\n📋 Próximos pasos:")
        print("   1. Abre http://localhost:3000 en tu navegador")
        print("   2. Sube un documento PDF")
        print("   3. Procesa el documento")
        print("   4. Haz preguntas en el chat")
    else:
        print("\n⚠️  Hay problemas de conexión que resolver")
        if not backend_ok:
            print("   - Ejecuta: cd backend && python app.py")
        if not frontend_ok:
            print("   - Ejecuta: cd frontend && npm run dev")

if __name__ == "__main__":
    main()
