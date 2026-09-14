"""Quince objetos fijos. Peso y valor expresados en unidades académicas."""

OBJETOS = [
    {"id": 0, "nombre": "Laptop", "peso": 8, "valor": 100},
    {"id": 1, "nombre": "Cámara", "peso": 4, "valor": 65},
    {"id": 2, "nombre": "Tablet", "peso": 5, "valor": 70},
    {"id": 3, "nombre": "Botiquín", "peso": 3, "valor": 45},
    {"id": 4, "nombre": "Carpa", "peso": 12, "valor": 90},
    {"id": 5, "nombre": "Agua", "peso": 7, "valor": 50},
    {"id": 6, "nombre": "Alimentos", "peso": 6, "valor": 55},
    {"id": 7, "nombre": "Linterna", "peso": 2, "valor": 25},
    {"id": 8, "nombre": "Radio", "peso": 4, "valor": 40},
    {"id": 9, "nombre": "Abrigo", "peso": 5, "valor": 35},
    {"id": 10, "nombre": "Batería", "peso": 3, "valor": 48},
    {"id": 11, "nombre": "Herramientas", "peso": 9, "valor": 60},
    {"id": 12, "nombre": "GPS", "peso": 2, "valor": 42},
    {"id": 13, "nombre": "Saco de dormir", "peso": 10, "valor": 75},
    {"id": 14, "nombre": "Cuaderno", "peso": 1, "valor": 12},
]
CAPACIDADES = (30, 45)
# Mayor que la suma de todos los valores. Con pesos/capacidades enteros,
# todo exceso es al menos 1 y cualquier individuo inválido tiene fitness < 0.
FACTOR_PENALIZACION = sum(o["valor"] for o in OBJETOS) + 1
