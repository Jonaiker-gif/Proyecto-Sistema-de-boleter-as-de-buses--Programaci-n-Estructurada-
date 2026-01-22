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
# ========== FUNCIONES AUXILIARES (VALIDACIONES) ========== #
def validar_cedula_ecuador(cedula: str) -> bool:
    """
    Valida cédula ecuatoriana (10 dígitos).
    Algoritmo:
    - 10 dígitos
    - dos primeros: código de provincia (01-24)
    - tercer dígito < 6 para personas naturales
    - coeficientes [2,1,2,1,2,1,2,1,2], sumar dígitos (si >9 restar 9)
    - dígito verificador: 10 - (suma % 10) (si suma%10 == 0 -> 0)
    """
    if not cedula.isdigit() or len(cedula) != 10:
        return False
    prov = int(cedula[:2])
    if prov < 1 or prov > 24:
        return False
    tercer = int(cedula[2])
    if tercer >= 6:
        return False
    coef = [2,1,2,1,2,1,2,1,2]
    suma = 0
    for i in range(9):
        val = int(cedula[i]) * coef[i]
        if val >= 10:
            val = val - 9
        suma += val
    verificador = int(cedula[9])
    resto = suma % 10
    digito_calc = 0 if resto == 0 else 10 - resto
    return verificador == digito_calc

def nombre_valido(nombre: str) -> bool:
    """Permite letras y espacios (al menos 2 caracteres no vacíos)."""
    if not nombre or len(nombre.strip()) < 2:
        return False
    return all(p.isalpha() or p.isspace() for p in nombre)


# ========== FUNCIONES COMPARTIDAS ========== #
def seleccionar_asiento(origen, destino, horario):
    clave_ruta = f"{origen}-{destino}-{horario}"
    if clave_ruta not in asientos_por_ruta:
        asientos_por_ruta[clave_ruta] = generar_matriz_asientos()
    
    ventana = tk.Toplevel()
    ventana.title("Seleccionar Asiento - Terminal de Buses")
    ventana.geometry("500x550")
    ventana.config(bg=COLOR_FONDO)
    
    # Header
    frame_header = tk.Frame(ventana, bg=COLOR_PRIMARIO, height=80)
    frame_header.pack(fill=tk.X, pady=0)
    frame_header.pack_propagate(False)
    
    tk.Label(frame_header, text="SELECCIONAR ASIENTO", font=("Arial", 16, "bold"), bg=COLOR_PRIMARIO, fg=COLOR_TEXTO).pack(pady=8)
    tk.Label(frame_header, text=f"{origen} → {destino} ({horario})", font=("Arial", 9), bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_SECUNDARIO).pack(pady=2)
    
    # Línea decorativa
    frame_linea = tk.Frame(ventana, bg=COLOR_ACENTO, height=2)
    frame_linea.pack(fill=tk.X, pady=5)
    frame_linea.pack_propagate(False)
    
    # Contenedor de asientos
    frame_contenedor = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_contenedor.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)
    
    frame_asientos = tk.Frame(frame_contenedor, bg=COLOR_FONDO)
    frame_asientos.pack(pady=10)
    
    asiento_seleccionado = [None]
    
    for fila in range(4):
        for columna in range(4):
            estado = "ocupado" if asientos_por_ruta[clave_ruta][fila][columna] else "libre"
            bg_color = COLOR_ASIENTO_OCUPADO if estado == "ocupado" else COLOR_ASIENTO_LIBRE
            boton = tk.Button(
                frame_asientos,
                text=f"F{fila+1}C{columna+1}",
                width=8,
                height=3,
                bg=bg_color,
                fg=COLOR_TEXTO,
                state="disabled" if estado == "ocupado" else "normal",
                command=lambda f=fila, c=columna: [asiento_seleccionado.__setitem__(0, (f, c)), ventana.destroy()],
                font=("Arial", 9, "bold"),
                relief=tk.RAISED,
                bd=2,
                disabledforeground="#999999",
                activebackground=COLOR_ACENTO
            )
            boton.grid(row=fila, column=columna, padx=5, pady=5)
    
    # Leyenda
    frame_leyenda = tk.Frame(frame_contenedor, bg=COLOR_FONDO)
    frame_leyenda.pack(pady=15, fill=tk.X)
    
    tk.Label(frame_leyenda, text="●", font=("Arial", 12), bg=COLOR_FONDO, fg=COLOR_ASIENTO_LIBRE).pack(side=tk.LEFT, padx=20)
    tk.Label(frame_leyenda, text="Libre", font=("Arial", 10), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side=tk.LEFT, padx=5)
    
    tk.Label(frame_leyenda, text="●", font=("Arial", 12), bg=COLOR_FONDO, fg=COLOR_ASIENTO_OCUPADO).pack(side=tk.LEFT, padx=20)
    tk.Label(frame_leyenda, text="Ocupado", font=("Arial", 10), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side=tk.LEFT, padx=5)
    
    ventana.wait_window()
    return asiento_seleccionado[0]

def generar_matriz_asientos():
    return [[False for _ in range(4)] for _ in range(4)]

def inicializar_asientos():
    for origen in rutas_matriz:
        for destino in rutas_matriz[origen]:
            # Crear asientos para cada horario disponible
            if destino in rutas_cliente:
                for horario in rutas_cliente[destino]["horarios"]:
                    clave = f"{origen}-{destino}-{horario}"
                    if clave not in asientos_por_ruta:
                        asientos_por_ruta[clave] = generar_matriz_asientos()

def guardar_factura_json(cliente, destino, precio, fecha):
    factura = {"cliente": cliente, "destino": destino, "precio": precio, "fecha": fecha}
    try:
        with open("facturas.json", "r") as f:
            data = json.load(f)
    except:
        data = []
    data.append(factura)
    with open("facturas.json", "w") as f:
        json.dump(data, f, indent=2)

# DFS mejorado para rutas bidireccionales
def encontrar_rutas_dfs(origen, destino, visitado=None, camino=None):
    if visitado is None: visitado = set()
    if camino is None: camino = []
    visitado.add(origen)
    camino.append(origen)
    
    if origen == destino:
        return [list(camino)]
    
    rutas = []
    # Busca en ambas direcciones (ida y vuelta)
    vecinos = set(rutas_matriz.get(origen, {}).keys())
    for ciudad in rutas_matriz:
        if origen in rutas_matriz[ciudad]:
            vecinos.add(ciudad)
    
    for vecino in vecinos:
        if vecino not in visitado:
            rutas.extend(encontrar_rutas_dfs(vecino, destino, visitado.copy(), camino.copy()))
    return rutas

def obtener_rutas_con_info():
    """Obtiene todas las rutas posibles con su tiempo y precio"""
    lista_rutas = []
    ciudades = list(rutas_matriz.keys())
    
    for i in range(len(ciudades)):
        for j in range(len(ciudades)):
            if i != j:
                origen = ciudades[i]
                destino = ciudades[j]
                rutas = encontrar_rutas_dfs(origen, destino)
                for ruta in rutas:
                    tiempo_total = sum(
                        rutas_matriz[ruta[k]][ruta[k+1]]
                        for k in range(len(ruta)-1)
                        if ruta[k+1] in rutas_matriz[ruta[k]]
                    )
                    precio_total = tiempo_total * 1.5
                    lista_rutas.append((" -> ".join(ruta), tiempo_total, precio_total))
    
    # Eliminar duplicados
    rutas_unicas = []
    vistas = set()
    for ruta, tiempo, precio in lista_rutas:
        if ruta not in vistas:
            rutas_unicas.append((ruta, tiempo, precio))
            vistas.add(ruta)
    
    return rutas_unicas

def mostrar_rutas_por_tipo(tipo, titulo):
    rutas = obtener_rutas_con_info()
    
    if tipo == "barata":
        rutas.sort(key=lambda x: x[2])
    elif tipo == "corta":
        rutas.sort(key=lambda x: x[1])
    elif tipo == "larga":
        rutas.sort(key=lambda x: -x[1])
    
    texto = "\n".join([f"{r} | {t}h | ${p:.2f}" for r, t, p in rutas])
    messagebox.showinfo(titulo, texto)

def buscar_rutas_entre_ciudades(origen, destino):
    rutas = encontrar_rutas_dfs(origen, destino)
    if not rutas:
        messagebox.showinfo("Resultado", "No hay rutas disponibles")
    else:
        texto = "\n".join([" → ".join(r) for r in rutas])
        messagebox.showinfo("Rutas Encontradas", texto)
