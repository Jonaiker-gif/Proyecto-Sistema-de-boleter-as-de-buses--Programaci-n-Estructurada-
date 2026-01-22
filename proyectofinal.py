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
# ========== FUNCIONES PARA GESTIONAR HORARIOS ========== #
def gestionar_horarios():
    """Función para que el admin vea y gestione horarios por ciudad"""
    ventana = tk.Toplevel()
    ventana.title("Gestionar Horarios")
    ventana.geometry("400x300")
    
    tk.Label(ventana, text="Seleccione una ciudad:", font=fuente).pack(pady=10)
    
    # Lista de ciudades disponibles
    lista_ciudades = tk.Listbox(ventana, width=40, height=8, font=fuente)
    for ciudad in rutas_cliente:
        horarios = ', '.join(rutas_cliente[ciudad]["horarios"])
        lista_ciudades.insert(tk.END, f"{ciudad} ({horarios})")
    lista_ciudades.pack(pady=10)
    
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)
    
    def agregar_horario():
        seleccion = lista_ciudades.curselection()
        if not seleccion:
            messagebox.showwarning("Error", "Seleccione una ciudad")
            return
        
        ciudad = list(rutas_cliente.keys())[seleccion[0]]
        ventana_agregar_horario(ciudad, ventana)
        refrescar_lista()
    
    def eliminar_horario():
        seleccion = lista_ciudades.curselection()
        if not seleccion:
            messagebox.showwarning("Error", "Seleccione una ciudad")
            return
        
        ciudad = list(rutas_cliente.keys())[seleccion[0]]
        ventana_eliminar_horario(ciudad, ventana)
        refrescar_lista()
    
    def refrescar_lista():
        lista_ciudades.delete(0, tk.END)
        for ciudad in rutas_cliente:
            horarios = ', '.join(rutas_cliente[ciudad]["horarios"])
            lista_ciudades.insert(tk.END, f"{ciudad} ({horarios})")
    
    tk.Button(frame_botones, text="Agregar Horario", command=agregar_horario, font=fuente).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botones, text="Eliminar Horario", command=eliminar_horario, font=fuente).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botones, text="Refrescar", command=refrescar_lista, font=fuente).pack(side=tk.LEFT, padx=5)

def ventana_agregar_horario(ciudad, ventana_padre):
    """Ventana para agregar un nuevo horario a una ciudad"""
    ventana = tk.Toplevel(ventana_padre)
    ventana.title(f"Agregar Horario - {ciudad}")
    ventana.geometry("300x200")
    
    tk.Label(ventana, text=f"Ciudad: {ciudad}", font=("Times New Roman", 12)).pack(pady=10)
    tk.Label(ventana, text="Nuevo horario:", font=fuente).pack()
    
    entry_horario = tk.Entry(ventana, width=15, font=fuente)
    entry_horario.pack(pady=5)
    
    tk.Label(ventana, text="Formato: HH:MM (ej: 14:30)", font=("Times New Roman", 8), fg="gray").pack()
    
    def guardar_horario():
        horario = entry_horario.get().strip()
        
        if not horario:
            messagebox.showerror("Error", "Ingrese un horario")
            return
        
        # Validar formato básico
        if len(horario) != 5 or horario[2] != ':':
            messagebox.showerror("Error", "Formato incorrecto. Use HH:MM")
            return
        
        try:
            horas, minutos = horario.split(':')
            if not (0 <= int(horas) <= 23 and 0 <= int(minutos) <= 59):
                raise ValueError
        except:
            messagebox.showerror("Error", "Horario inválido")
            return
        
        # Verificar si ya existe
        if horario in rutas_cliente[ciudad]["horarios"]:
            messagebox.showerror("Error", "El horario ya existe")
            return
        
        # Agregar horario
        rutas_cliente[ciudad]["horarios"].append(horario)
        rutas_cliente[ciudad]["horarios"].sort()  # Ordenar horarios
        
        # Crear asientos para todas las rutas que involucren esta ciudad
        crear_asientos_nuevo_horario(ciudad, horario)
        
        messagebox.showinfo("Éxito", f"Horario {horario} agregado a {ciudad}")
        ventana.destroy()
    
    tk.Button(ventana, text="Guardar", command=guardar_horario, font=fuente).pack(pady=15)

def ventana_eliminar_horario(ciudad, ventana_padre):
    """Ventana para eliminar un horario de una ciudad"""
    ventana = tk.Toplevel(ventana_padre)
    ventana.title(f"Eliminar Horario - {ciudad}")
    ventana.geometry("300x250")
    
    tk.Label(ventana, text=f"Ciudad: {ciudad}", font=("Times New Roman", 12)).pack(pady=10)
    tk.Label(ventana, text="Seleccione horario a eliminar:", font=fuente).pack()
    
    lista_horarios = tk.Listbox(ventana, width=25, height=6, font=fuente)
    for horario in rutas_cliente[ciudad]["horarios"]:
        lista_horarios.insert(tk.END, horario)
    lista_horarios.pack(pady=10)
    
    def eliminar():
        seleccion = lista_horarios.curselection()
        if not seleccion:
            messagebox.showwarning("Error", "Seleccione un horario")
            return
        
        horario = lista_horarios.get(seleccion[0])
        
        # Verificar que no sea el último horario
        if len(rutas_cliente[ciudad]["horarios"]) <= 1:
            messagebox.showerror("Error", "No puede eliminar el último horario")
            return
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno("Confirmar", f"¿Eliminar horario {horario}?\n\nSe perderán todos los asientos vendidos en este horario.")
        if not respuesta:
            return
        
        # Eliminar horario
        rutas_cliente[ciudad]["horarios"].remove(horario)
        
        # Eliminar asientos asociados
        eliminar_asientos_horario(ciudad, horario)
        
        messagebox.showinfo("Éxito", f"Horario {horario} eliminado de {ciudad}")
        ventana.destroy()
    
    tk.Button(ventana, text="Eliminar", command=eliminar, font=fuente, bg="red", fg="white").pack(pady=10)

def crear_asientos_nuevo_horario(ciudad, horario):
    """Crea asientos para un nuevo horario en todas las rutas que involucren la ciudad"""
    # Para rutas donde la ciudad es origen
    if ciudad in rutas_matriz:
        for destino in rutas_matriz[ciudad]:
            clave = f"{ciudad}-{destino}-{horario}"
            if clave not in asientos_por_ruta:
                asientos_por_ruta[clave] = generar_matriz_asientos()
    
    # Para rutas donde la ciudad es destino
    for origen in rutas_matriz:
        if ciudad in rutas_matriz[origen]:
            clave = f"{origen}-{ciudad}-{horario}"
            if clave not in asientos_por_ruta:
                asientos_por_ruta[clave] = generar_matriz_asientos()

def eliminar_asientos_horario(ciudad, horario):
    """Elimina todos los asientos asociados a un horario específico"""
    claves_a_eliminar = []
    
    for clave in list(asientos_por_ruta.keys()):
        if horario in clave and ciudad in clave:
            claves_a_eliminar.append(clave)
    
    for clave in claves_a_eliminar:
        del asientos_por_ruta[clave]

def ver_todos_horarios():
    """Función para ver todos los horarios por ciudad"""
    if not rutas_cliente:
        messagebox.showinfo("Horarios", "No hay ciudades registradas")
        return
    
    texto = "HORARIOS POR CIUDAD:\n\n"
    for ciudad, datos in rutas_cliente.items():
        horarios = ', '.join(sorted(datos['horarios']))
        cooperativa = datos['cooperativa']
        precio = datos['precio']
        texto += f"{ciudad}\n"
        texto += f"   Cooperativa: {cooperativa}\n"
        texto += f"   Precio: ${precio}\n"
        texto += f"   Horarios: {horarios}\n\n"
    
    messagebox.showinfo("Todos los Horarios", texto)

def agregar_cooperativa():
    """Función para que el admin agregue nuevas cooperativas"""
    ventana = tk.Toplevel()
    ventana.title("Agregar Cooperativa")
    ventana.geometry("400x300")
    
    tk.Label(ventana, text="Nombre de la Cooperativa:", font=fuente).pack(pady=5)
    entry_nombre = tk.Entry(ventana, width=40, font=fuente)
    entry_nombre.pack(pady=5)
    
    tk.Label(ventana, text="Ciudades que cubre (separadas por comas):", font=fuente).pack(pady=5)
    entry_ciudades = tk.Entry(ventana, width=40, font=fuente)
    entry_ciudades.pack(pady=5)
    
    tk.Label(ventana, text="Ejemplo: Quito, Guayaquil, Cuenca", font=("Times New Roman", 8), fg="gray").pack()

    def guardar_cooperativa():
        nombre = entry_nombre.get().strip()
        ciudades_str = entry_ciudades.get().strip()
        
        if not nombre or not ciudades_str:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if nombre in cooperativas:
            messagebox.showerror("Error", "La cooperativa ya existe")
            return
        
        # Procesar ciudades
        ciudades = [ciudad.strip() for ciudad in ciudades_str.split(",")]
        ciudades = [ciudad for ciudad in ciudades if ciudad]  # Filtrar vacíos
        
        if not ciudades:
            messagebox.showerror("Error", "Debe ingresar al menos una ciudad")
            return
        
        # Verificar que las ciudades existan en el sistema
        ciudades_no_existentes = [ciudad for ciudad in ciudades if ciudad not in rutas_matriz]
        if ciudades_no_existentes:
            messagebox.showerror("Error", f"Las siguientes ciudades no existen en el sistema: {', '.join(ciudades_no_existentes)}")
            return
        
        cooperativas[nombre] = ciudades
        guardar_todos_datos_en_json()
        messagebox.showinfo("Éxito", f"Cooperativa '{nombre}' agregada correctamente")
        ventana.destroy()

    tk.Button(ventana, text="Guardar Cooperativa", command=guardar_cooperativa, font=fuente).pack(pady=15)

def ver_cooperativas():
    """Función para ver todas las cooperativas registradas"""
    if not cooperativas:
        messagebox.showinfo("Cooperativas", "No hay cooperativas registradas")
        return
    
    texto = ""
    for coop, ciudades in cooperativas.items():
        texto += f"{coop}: {', '.join(ciudades)}\n"
    
    messagebox.showinfo("Cooperativas Registradas", texto)

def gestionar_asientos_ruta():
    """Función para que el admin vea y modifique asientos por ruta y horario"""
    ventana = tk.Toplevel()
    ventana.title("Gestionar Asientos por Ruta")
    ventana.geometry("350x250")
    
    tk.Label(ventana, text="Ciudad Origen:", font=fuente).pack()
    entry_origen = tk.Entry(ventana, font=fuente)
    entry_origen.pack()
    
    tk.Label(ventana, text="Ciudad Destino:", font=fuente).pack()
    entry_destino = tk.Entry(ventana, font=fuente)
    entry_destino.pack()
    
    tk.Label(ventana, text="Horario:", font=fuente).pack()
    entry_horario = tk.Entry(ventana, font=fuente)
    entry_horario.pack()
    
    tk.Label(ventana, text="Ejemplo: 08:00", font=("Times New Roman", 8), fg="gray").pack()

    def mostrar_asientos():
        origen = entry_origen.get().strip()
        destino = entry_destino.get().strip()
        horario = entry_horario.get().strip()
        
        if not origen or not destino or not horario:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if origen not in rutas_matriz or destino not in rutas_matriz.get(origen, {}):
            messagebox.showerror("Error", "La ruta no existe")
            return
        
        ventana.destroy()
        mostrar_matriz_asientos_admin(origen, destino, horario)

    tk.Button(ventana, text="Ver Asientos", command=mostrar_asientos, font=fuente).pack(pady=10)

def mostrar_matriz_asientos_admin(origen, destino, horario):
    """Muestra la matriz de asientos para administrador con opción de liberar asientos"""
    clave_ruta = f"{origen}-{destino}-{horario}"
    if clave_ruta not in asientos_por_ruta:
        asientos_por_ruta[clave_ruta] = generar_matriz_asientos()
    
    ventana = tk.Toplevel()
    ventana.title(f"Asientos: {origen} → {destino} - {horario}")
    ventana.geometry("500x500")
    
    tk.Label(ventana, text=f"Bus: {origen} → {destino}", font=("Times New Roman", 12)).pack(pady=5)
    tk.Label(ventana, text=f"Horario: {horario}", font=("Times New Roman", 10)).pack(pady=5)
    
    frame_asientos = tk.Frame(ventana)
    frame_asientos.pack()
    
    # Crear botones para cada asiento
    for fila in range(4):
        for columna in range(4):
            estado = "ocupado" if asientos_por_ruta[clave_ruta][fila][columna] else "libre"
            bg_color = "red" if estado == "ocupado" else "green"
            
            def toggle_asiento(f=fila, c=columna):
                # Cambiar estado del asiento
                asientos_por_ruta[clave_ruta][f][c] = not asientos_por_ruta[clave_ruta][f][c]
                ventana.destroy()
                mostrar_matriz_asientos_admin(origen, destino, horario)  # Refrescar vista
            
            boton = tk.Button(
                frame_asientos,
                text=f"F{fila+1}C{columna+1}\n({estado})",
                width=8,
                height=3,
                bg=bg_color,
                command=toggle_asiento
            )
            boton.grid(row=fila, column=columna, padx=5, pady=5)
    
    # Botón para resetear todos los asientos
    def resetear_asientos():
        asientos_por_ruta[clave_ruta] = generar_matriz_asientos()
        messagebox.showinfo("Éxito", "Todos los asientos han sido liberados")
        ventana.destroy()
        mostrar_matriz_asientos_admin(origen, destino, horario)
    
    tk.Button(ventana, text="Liberar Todos los Asientos", command=resetear_asientos, font=fuente, bg="orange").pack(pady=10)
    
    # Información adicional
    ocupados = sum(sum(fila) for fila in asientos_por_ruta[clave_ruta])
    libres = 16 - ocupados
    tk.Label(ventana, text=f"Asientos ocupados: {ocupados} | Asientos libres: {libres}", font=fuente).pack(pady=5)

def ver_estado_todos_asientos():
    """Función para ver el estado de asientos de todas las rutas y horarios"""
    if not asientos_por_ruta:
        messagebox.showinfo("Estado de Asientos", "No hay rutas con asientos configurados")
        return
    
    texto = "ESTADO DE ASIENTOS POR BUS (RUTA + HORARIO):\n\n"
    for ruta_horario, matriz in asientos_por_ruta.items():
        ocupados = sum(sum(fila) for fila in matriz)
        libres = 16 - ocupados
        # Separar ruta de horario para mejor presentación
        partes = ruta_horario.split('-')
        if len(partes) >= 3:
            origen = partes[0]
            destino = partes[1] 
            horario = '-'.join(partes[2:])  # Por si el horario tiene guiones
            texto += f"{origen} → {destino} ({horario}): {ocupados}/16 ocupados, {libres}/16 libres\n"
        else:
            texto += f"{ruta_horario}: {ocupados}/16 ocupados, {libres}/16 libres\n"
    
    messagebox.showinfo("Estado General de Asientos", texto)

# ========== MÓDULO ADMINISTRADOR ========== #
def ventana_login_admin():
    win = tk.Tk()
    win.title("Login Administrador - Terminal de Buses")
    win.geometry("500x400")
    win.config(bg=COLOR_FONDO)
    
    # Header
    frame_header = tk.Frame(win, bg=COLOR_PRIMARIO_CLARO, height=120)
    frame_header.pack(fill=tk.X, pady=0)
    frame_header.pack_propagate(False)
    
    tk.Label(frame_header, text="ACCESO ADMINISTRADOR", font=("Arial", 18, "bold"), bg=COLOR_PRIMARIO_CLARO, fg=COLOR_TEXTO).pack(pady=10)
    
    # Línea decorativa
    frame_linea = tk.Frame(win, bg=COLOR_ACENTO, height=2)
    frame_linea.pack(fill=tk.X, pady=10)
    frame_linea.pack_propagate(False)
    
    # Contenido
    frame = tk.Frame(win, bg=COLOR_FONDO)
    frame.pack(pady=40, padx=40, fill=tk.BOTH, expand=True)
    
    tk.Label(frame, text="ID Administrador:", font=("Arial", 12, "bold"), bg=COLOR_FONDO, fg=COLOR_ACENTO).pack(anchor=tk.W, pady=(10, 10))
    entry_id = tk.Entry(frame, width=30, font=("Arial", 12), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO, relief=tk.FLAT, bd=5, show="*")
    entry_id.pack(pady=10, fill=tk.X)

    tk.Label(frame, text="Ingresa tu ID de administrador para continuar", font=("Arial", 9), bg=COLOR_FONDO, fg=COLOR_TEXTO_SECUNDARIO).pack(pady=10)

    def verificar():
        if entry_id.get() == "admin123":
            win.destroy()
            panel_admin()
        else:
            messagebox.showerror("Error", " ID incorrecto. Intenta de nuevo.")
            entry_id.delete(0, tk.END)

    btn = tk.Button(
        frame,
        text="INGRESAR",
        command=verificar,
        font=("Arial", 12, "bold"),
        bg=COLOR_PRIMARIO_CLARO,
        fg=COLOR_TEXTO,
        relief=tk.RAISED,
        bd=3,
        padx=20,
        pady=12,
        activebackground=COLOR_ACENTO,
        activeforeground=COLOR_FONDO,
        cursor="hand2"
    )
    btn.pack(pady=20, fill=tk.X)

def panel_admin():
    win = tk.Tk()
    win.title("Panel Administrador - Terminal de Buses")
    win.geometry("700x800")
    win.config(bg=COLOR_FONDO)
    
    # Header
    frame_header = tk.Frame(win, bg=COLOR_PRIMARIO_CLARO, height=100)
    frame_header.pack(fill=tk.X, pady=0)
    frame_header.pack_propagate(False)
    
    tk.Label(frame_header, text="PANEL ADMINISTRADOR", font=("Arial", 20, "bold"), bg=COLOR_PRIMARIO_CLARO, fg=COLOR_TEXTO).pack(pady=10)
    
    # Línea decorativa
    frame_linea = tk.Frame(win, bg=COLOR_ACENTO, height=2)
    frame_linea.pack(fill=tk.X, pady=5)
    frame_linea.pack_propagate(False)
    
    # Canvas con Scrollbar para los botones
    canvas = tk.Canvas(win, bg=COLOR_FONDO, highlightthickness=0)
    scrollbar = tk.Scrollbar(win, orient=tk.VERTICAL, command=canvas.yview)
    frame_botones = tk.Frame(canvas, bg=COLOR_FONDO)
    frame_botones.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame_botones, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Permitir scroll con rueda del mouse
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    botones = [
        ("Ver rutas y precios", ver_rutas_admin, COLOR_PRIMARIO),
        ("Ver rutas más baratas", lambda: mostrar_rutas_por_tipo("barata", "Rutas Más Baratas"), COLOR_PRIMARIO),
        ("Ver rutas más cortas", lambda: mostrar_rutas_por_tipo("corta", "Rutas Más Cortas"), COLOR_PRIMARIO),
        ("Ver rutas más largas", lambda: mostrar_rutas_por_tipo("larga", "Rutas Más Largas"), COLOR_PRIMARIO),
        ("Buscar rutas entre ciudades", buscar_ruta_dfs, COLOR_SECUNDARIO),
        ("Agregar nueva ciudad", agregar_ciudad, COLOR_SECUNDARIO),
        ("Agregar nueva ruta", agregar_ruta, COLOR_SECUNDARIO),
        ("Gestionar horarios", gestionar_horarios, COLOR_PRIMARIO_CLARO),
        ("Ver todos los horarios", ver_todos_horarios, COLOR_PRIMARIO_CLARO),
        ("Agregar cooperativa", agregar_cooperativa, COLOR_PRIMARIO_CLARO),
        ("Ver cooperativas", ver_cooperativas, COLOR_PRIMARIO_CLARO),
        ("Gestionar asientos por ruta", gestionar_asientos_ruta, COLOR_PRIMARIO),
        ("Ver estado de todos los asientos", ver_estado_todos_asientos, COLOR_PRIMARIO),
        ("Ver facturas", ver_facturas, COLOR_SECUNDARIO),
        ("Cerrar sesión", lambda: [win.destroy(), ventana_principal()], "#555555")
    ]

    for texto, comando, color in botones:
        btn = tk.Button(
            frame_botones, 
            text=texto, 
            width=45,
            command=comando, 
            font=("Arial", 10),
            bg=color,
            fg=COLOR_TEXTO,
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=8,
            activebackground=COLOR_ACENTO,
            activeforeground=COLOR_FONDO,
            cursor="hand2"
        )
        btn.pack(pady=4, anchor="center")

    # Footer
    frame_footer = tk.Frame(win, bg=COLOR_PRIMARIO, height=50)
    frame_footer.pack(fill=tk.X, side=tk.BOTTOM)
    frame_footer.pack_propagate(False)
    tk.Label(frame_footer, text="Gestiona la terminal con seguridad y precisión", font=("Arial", 9), bg=COLOR_PRIMARIO, fg=COLOR_TEXTO).pack(pady=15)

def ver_rutas_admin():
    texto = ""
    for origen in rutas_matriz:
        for destino, tiempo in rutas_matriz[origen].items():
            precio = tiempo * 1.5
            texto += f"{origen} -> {destino} | {tiempo}h | ${precio:.2f}\n"
    messagebox.showinfo("Rutas Disponibles", texto)

def agregar_ciudad():
    ciudad = simpledialog.askstring("Agregar Ciudad", "Nombre de la nueva ciudad:")
    if ciudad and ciudad not in rutas_matriz:
        rutas_matriz[ciudad] = {}
        # Agregar datos básicos para clientes
        rutas_cliente[ciudad] = {
            "precio": 10,  # Precio por defecto
            "cooperativa": "Nueva Cooperativa",
            "horarios": ["08:00", "16:00"]  # Horarios por defecto
        }
        guardar_todos_datos_en_json()
        messagebox.showinfo("Éxito", f"Ciudad {ciudad} agregada correctamente")
    elif ciudad in rutas_matriz:
        messagebox.showerror("Error", "La ciudad ya existe")

def agregar_ruta():
    ventana = tk.Toplevel()
    ventana.title("Agregar Ruta")
    ventana.geometry("300x250")
    
    tk.Label(ventana, text="Ciudad Origen:", font=fuente).pack()
    entry_origen = tk.Entry(ventana, font=fuente)
    entry_origen.pack()
    
    tk.Label(ventana, text="Ciudad Destino:", font=fuente).pack()
    entry_destino = tk.Entry(ventana, font=fuente)
    entry_destino.pack()
    
    tk.Label(ventana, text="Tiempo de viaje (horas):", font=fuente).pack()
    entry_tiempo = tk.Entry(ventana, font=fuente)
    entry_tiempo.pack()

    def guardar_ruta():
        origen = entry_origen.get().strip()
        destino = entry_destino.get().strip()
        tiempo = entry_tiempo.get().strip()
        
        if not origen or not destino or not tiempo:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            tiempo = float(tiempo)
        except ValueError:
            messagebox.showerror("Error", "El tiempo debe ser un número")
            return
        
        if origen not in rutas_matriz or destino not in rutas_matriz:
            messagebox.showerror("Error", "Una o ambas ciudades no existen")
            return
        
        # Agregar ruta bidireccional
        rutas_matriz[origen][destino] = tiempo
        rutas_matriz[destino][origen] = tiempo
        
        # Actualizar asientos para cada horario disponible
        if destino in rutas_cliente:
            for horario in rutas_cliente[destino]["horarios"]:
                clave_ida = f"{origen}-{destino}-{horario}"
                clave_vuelta = f"{destino}-{origen}-{horario}"
                if clave_ida not in asientos_por_ruta:
                    asientos_por_ruta[clave_ida] = generar_matriz_asientos()
                if clave_vuelta not in asientos_por_ruta:
                    asientos_por_ruta[clave_vuelta] = generar_matriz_asientos()
        
        guardar_todos_datos_en_json()
        messagebox.showinfo("Éxito", "Ruta agregada correctamente")
        ventana.destroy()

    tk.Button(ventana, text="Guardar Ruta", command=guardar_ruta, font=fuente).pack(pady=15)

def buscar_ruta_dfs():
    ventana = tk.Toplevel()
    ventana.title("Buscar Ruta")
    ventana.geometry("300x200")
    
    tk.Label(ventana, text="Ciudad Origen:", font=fuente).pack()
    entry_origen = tk.Entry(ventana, font=fuente)
    entry_origen.pack()
    
    tk.Label(ventana, text="Ciudad Destino:", font=fuente).pack()
    entry_destino = tk.Entry(ventana, font=fuente)
    entry_destino.pack()

    def buscar():
        origen = entry_origen.get().strip()
        destino = entry_destino.get().strip()
        if not origen or not destino:
            messagebox.showerror("Error", "Ambos campos son obligatorios")
            return
        
        buscar_rutas_entre_ciudades(origen, destino)
        ventana.destroy()

    tk.Button(ventana, text="Buscar", command=buscar, font=fuente).pack(pady=10)

def ver_facturas():
    try:
        with open("facturas.json", "r") as f:
            facturas = json.load(f)
    except:
        facturas = []
    
    if not facturas:
        messagebox.showinfo("Facturas", "No hay registros")
        return
    
    texto = "\n".join(
        f"{f['cliente']} | {f['destino']} | ${f['precio']} | {f['fecha']}" 
        for f in facturas
    )
    messagebox.showinfo("Historial de Facturas", texto)
