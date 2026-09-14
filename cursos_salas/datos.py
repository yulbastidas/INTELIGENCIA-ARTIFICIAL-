"""Datos fijos: IDs coinciden con posiciones en las listas, desde cero."""

FRANJAS = ["08:00 - 10:00", "10:00 - 12:00", "14:00 - 16:00",
           "16:00 - 18:00", "18:00 - 20:00"]

CURSOS = [
    {"id": 0, "nombre": "Programación", "cantidad_estudiantes": 30,
     "requiere_computadores": True, "software_requerido": ["Python"],
     "recurso_especial": "proyector", "franjas_bloqueadas": [4]},
    {"id": 1, "nombre": "Bases de Datos", "cantidad_estudiantes": 28,
     "requiere_computadores": True, "software_requerido": ["MySQL"],
     "recurso_especial": None, "franjas_bloqueadas": []},
    {"id": 2, "nombre": "Diseño Multimedia", "cantidad_estudiantes": 24,
     "requiere_computadores": True, "software_requerido": ["GIMP"],
     "recurso_especial": "tabletas gráficas", "franjas_bloqueadas": []},
    {"id": 3, "nombre": "Modelado 3D", "cantidad_estudiantes": 22,
     "requiere_computadores": True, "software_requerido": ["Blender"],
     "recurso_especial": "GPU", "franjas_bloqueadas": [0]},
    {"id": 4, "nombre": "Análisis de Datos", "cantidad_estudiantes": 26,
     "requiere_computadores": True, "software_requerido": ["R"],
     "recurso_especial": "proyector", "franjas_bloqueadas": []},
    {"id": 5, "nombre": "Inteligencia Artificial", "cantidad_estudiantes": 28,
     "requiere_computadores": True, "software_requerido": ["Python"],
     "recurso_especial": "GPU", "franjas_bloqueadas": [4]},
    {"id": 6, "nombre": "Redes", "cantidad_estudiantes": 20,
     "requiere_computadores": True, "software_requerido": ["Packet Tracer"],
     "recurso_especial": "equipos de red", "franjas_bloqueadas": []},
    {"id": 7, "nombre": "Ética Profesional", "cantidad_estudiantes": 20,
     "requiere_computadores": False, "software_requerido": [],
     "recurso_especial": "proyector", "franjas_bloqueadas": [0]},
]

SALAS = [
    {"id": 0, "nombre": "Sala Desarrollo", "capacidad": 40, "cantidad_computadores": 35,
     "software_disponible": ["Python", "MySQL", "R"], "recursos": ["proyector"],
     "franjas_bloqueadas": [4]},
    {"id": 1, "nombre": "Sala Multimedia", "capacidad": 25, "cantidad_computadores": 25,
     "software_disponible": ["GIMP", "Blender", "Python"],
     "recursos": ["proyector", "tabletas gráficas", "GPU"], "franjas_bloqueadas": [2]},
    {"id": 2, "nombre": "Sala Analítica", "capacidad": 30, "cantidad_computadores": 30,
     "software_disponible": ["Python", "R", "MySQL"], "recursos": ["proyector", "GPU"],
     "franjas_bloqueadas": [0]},
    {"id": 3, "nombre": "Sala Redes", "capacidad": 24, "cantidad_computadores": 20,
     "software_disponible": ["Packet Tracer", "Python"],
     "recursos": ["proyector", "equipos de red"], "franjas_bloqueadas": [1]},
]
