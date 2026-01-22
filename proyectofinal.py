# ========== SISTEMA TERMINAL DE BUSES ========== #
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

# ========== CONFIGURACIONES GLOBALES ========== #
fuente_titulo = ("Arial", 16, "bold")
fuente_subtitulo = ("Arial", 12, "bold")
fuente = ("Arial", 10)
fuente_pequena = ("Arial", 8)


COLOR_FONDO = "#051018"
COLOR_FONDO_SECUNDARIO = "#0f1f2e"
COLOR_PRIMARIO = "#1a4d73"
COLOR_PRIMARIO_CLARO = "#1f5f99"
COLOR_SECUNDARIO = "#0088b8"
COLOR_ACENTO = "#00a8cc"
COLOR_TEXTO = "#ffffff"
COLOR_TEXTO_SECUNDARIO = "#e8f4f8"
COLOR_EXITO = "#00ff88"
COLOR_ERROR = "#ff4444"
COLOR_ASIENTO_LIBRE = "#00d966"
COLOR_ASIENTO_OCUPADO = "#ff6666"
COLOR_BORDE = "#00d4ff"

# ========== ESTRUCTURAS DE DATOS ========== #
cooperativas = {
    "Coop. Panamericana": ["Quito", "Ambato"],
    "Coop. Flota Imbabura": ["Guayaquil", "Ambato"],
    "Coop. Loja": ["Cuenca"],
    "Coop. Reina del Camino": ["Manta"],
    "Coop. Trans Esmeraldas": ["Portoviejo"]
}

# Matriz de rutas bidireccionales (origen: {destino: horas})
rutas_matriz = {
    "Quito": {"Guayaquil": 8, "Cuenca": 6, "Ambato": 2},
    "Guayaquil": {"Quito": 8, "Manta": 4, "Portoviejo": 5},
    "Cuenca": {"Quito": 6, "Ambato": 3},
    "Ambato": {"Quito": 2, "Cuenca": 3},
    "Manta": {"Guayaquil": 4},
    "Portoviejo": {"Guayaquil": 5},
    "Loja": {"Guayaquil": 5}
}

# Datos para clientes (precios y horarios)
rutas_cliente = {
    "Quito": {"precio": 10, "cooperativa": "Coop. Panamericana", "horarios": ["08:00", "12:00", "18:00"]},
    "Guayaquil": {"precio": 12, "cooperativa": "Coop. Flota Imbabura", "horarios": ["07:00", "13:00", "19:00"]},
    "Cuenca": {"precio": 8, "cooperativa": "Coop. Loja", "horarios": ["09:00", "14:00"]},
    "Manta": {"precio": 8, "cooperativa": "Coop. Reina del Camino", "horarios": ["10:00", "16:00"]},
    "Portoviejo": {"precio": 9, "cooperativa": "Coop. Trans Esmeraldas", "horarios": ["11:00", "17:00"]},
    "Ambato": {"precio": 8, "cooperativa": "Coop. Flota Imbabura", "horarios": ["06:00", "15:00"]},
    "Loja": {"precio": 8, "cooperativa": "Coop. Flota Imbabura", "horarios": ["06:00", "15:00"]}
}

clientes = []  # lista de clientes: [nombre, cédula]
boletos = []   # [cliente_nombre, cedula, destino, precio, cooperativa, horario, fecha]
asientos_por_ruta = {}

# LISTA DE USUARIOS (por ahora en memoria) -> cada usuario: [nombre, cedula, password]
usuarios = []

# ========== FUNCIONES PARA GUARDAR Y CARGAR DATOS EN JSON ========== #
def cargar_usuarios_desde_json():
    """Carga los usuarios registrados desde el archivo usuarios.json"""
    global usuarios
    try:
        with open("usuarios.json", "r") as f:
            usuarios = json.load(f)
    except:
        usuarios = []

def guardar_usuarios_en_json():
    """Guarda la lista de usuarios en el archivo usuarios.json"""
    with open("usuarios.json", "w") as f:
        json.dump(usuarios, f, indent=2)

def guardar_todos_datos_en_json():
    """Guarda todos los datos del sistema en archivos JSON"""
    # Guardar usuarios
    with open("usuarios.json", "w") as f:
        json.dump(usuarios, f, indent=2)
    
    # Guardar cooperativas
    with open("cooperativas.json", "w") as f:
        json.dump(cooperativas, f, indent=2)
    
    # Guardar rutas
    with open("rutas.json", "w") as f:
        json.dump(rutas_matriz, f, indent=2)
    
    # Guardar rutas_cliente
    with open("rutas_cliente.json", "w") as f:
        json.dump(rutas_cliente, f, indent=2)
    
    # Guardar clientes
    with open("clientes.json", "w") as f:
        json.dump(clientes, f, indent=2)
    
    # Guardar boletos
    with open("boletos.json", "w") as f:
        json.dump(boletos, f, indent=2)
    
    # Guardar asientos (estructura especial porque es de 2D arrays)
    asientos_para_guardar = {}
    for ruta, matriz in asientos_por_ruta.items():
        asientos_para_guardar[ruta] = matriz
    with open("asientos.json", "w") as f:
        json.dump(asientos_para_guardar, f, indent=2)

def cargar_todos_datos_desde_json():
    """Carga todos los datos del sistema desde los archivos JSON"""
    global usuarios, cooperativas, rutas_matriz, rutas_cliente, clientes, boletos, asientos_por_ruta
    
    # Cargar usuarios
    try:
        with open("usuarios.json", "r") as f:
            usuarios = json.load(f)
    except:
        usuarios = []
    
    # Cargar cooperativas
    try:
        with open("cooperativas.json", "r") as f:
            cooperativas = json.load(f)
    except:
        pass
    
    # Cargar rutas
    try:
        with open("rutas.json", "r") as f:
            rutas_matriz = json.load(f)
    except:
        pass
    
    # Cargar rutas_cliente
    try:
        with open("rutas_cliente.json", "r") as f:
            rutas_cliente = json.load(f)
    except:
        pass
    
    # Cargar clientes
    try:
        with open("clientes.json", "r") as f:
            clientes = json.load(f)
    except:
        clientes = []
    
    # Cargar boletos
    try:
        with open("boletos.json", "r") as f:
            boletos = json.load(f)
    except:
        boletos = []
    
    # Cargar asientos
    try:
        with open("asientos.json", "r") as f:
            asientos_cargados = json.load(f)
            asientos_por_ruta = asientos_cargados
    except:
        asientos_por_ruta = {}
