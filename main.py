import json
# Importo esta librería para poder hacer los emparejamientos de una manera mas optima
from itertools import combinations
# Importo esta librería para generar los goles de manera aleatoria
import random

def cargar_datos(ruta):
  with open(ruta) as contenido:
    resultados = json.load(contenido)
    teams = resultados.get("teams", None)
    if teams:
        return teams
    else:
        print("La clave 'teams' no se encontró en el JSON.")
        return []

def creacion_grupos(teams):
    # Aqui se crean grupos vacios dentro de un objeto o diccionario
    grupos = {'A': [], 'B': [], 'C': [], 'D': []}

    # Iteramos los datos traidos por la funcion cargar_datos
    for team in teams:
      # Seteamos a 0 todos los datos para evitar inconsistencias en los datos
      team['pro_goals'] = 0
      team['ag_goal'] = 0
      team['games_played'] = 0
      team['points'] = 0

      # Buscamos y almacenamos los datos que tengan una clave group
      grupo = team.get("group")
      # Si el grupo pertenece o hace match con algun grupo dentro de los objetos
      # dentro de grupos continua la ejecucion
      if grupo in grupos:
        # Agregamos cada equipo al grupo correspondiente
        grupos[grupo].append(team)
      else:
        print("Error grupo inexistente")

    return grupos

def generar_enfrentamientos(grupo, nombre_grupo):
    # Creamos un arreglo vacio
    enfrentamientos = []
    # Esta linea almacena en la variable combinaciones una lista iterada dentro de cada grupo con
    # dos elementos del grupo
    combinaciones = list(combinations(grupo, 2))
    # Iteramos dentro de esas combinaciones de dos equipos dentro del grupo
    for partido in combinaciones:
        equipo1 = partido[0]
        equipo2 = partido[1]
        # Aqui se generan de manera aleatoria los goles para los dos equipos dentro del enfrentamiento
        goles1 = random.randint(0, 3)
        goles2 = random.randint(0, 3)

        # Actualizar goles y partidos jugados
        equipo1['pro_goals'] += goles1
        equipo1['ag_goal'] += goles2
        equipo1['games_played'] += 1

        equipo2['pro_goals'] += goles2
        equipo2['ag_goal'] += goles1
        equipo2['games_played'] += 1

        # Actualizar los puntos según el resultado del partido
        if goles1 > goles2:
          equipo1['points'] += 3
        elif goles2 > goles1:
          equipo2['points'] += 3
        else:
          equipo1['points'] += 1
          equipo2['points'] += 1

        # Creacion del enfrentamiento para mostrarlo en el Json
        enfrentamiento = {
            'grupo': nombre_grupo,
            'equipo1': equipo1['name'],
            'goles1': goles1,
            'equipo2': equipo2['name'],
            'goles2': goles2
        }
        enfrentamientos.append(enfrentamiento)
    return enfrentamientos

def guardar_enfrentamientos(enfrentamientos, ruta_salida):
  with open(ruta_salida, 'w') as archivo_salida:
    # Convierte el diccionario de Python a un Json
    json.dump(enfrentamientos, archivo_salida, indent=4)

def guardar_datos_equipos(teams, ruta_salida):
  with open(ruta_salida, 'w') as archivo_salida:
    # Convierte el diccionario de Python a un Json
    json.dump(teams, archivo_salida, indent=4)

if __name__ == "__main__":
    ruta = "./copa-america.json"
    teams = cargar_datos(ruta)
    # Si Equipos existe ejecuta todo el bloque de codigo
    if teams:
        # Almacena en la variable grupos el resultado de la funcion creación grupos
        grupos = creacion_grupos(teams)
        # Crea un arreglo vacio
        todos_enfrentamientos = []
        # Itera dentro de los grupos previamente creados y de allí trae los datos de los enfrentamientos
        # Como los enfrentamientos se generan entre grupos saldrían 4 grupos, por esto se usa el metodo .extend
        # Para combinar en un solo grupo todos los 4 grupos de enfrentamientos
        for nombre_grupo, grupo in grupos.items():
            enfrentamientos = generar_enfrentamientos(grupo, nombre_grupo)
            todos_enfrentamientos.extend(enfrentamientos)
        
        # Exportar los resultados de los enfrentamientos a un archivo JSON
        # Definimos la ruta de salida del Json
        ruta_salida_enfrentamientos = "./resultados-enfrentamientos-copa-america.json"
        # Ejecutamos la funcion guardar_entrentamientos y le pasamos los parametros para su ejecucion
        guardar_enfrentamientos(todos_enfrentamientos, ruta_salida_enfrentamientos)
        print(f"Los resultados de los enfrentamientos se han guardado en {ruta_salida_enfrentamientos}")
        
        # Exportar los datos actualizados de los equipos a un archivo JSON
        ruta_salida_teams = "./resultados-equipos-copa-america.json"

        # Ejecutamos la funcion guardar_datos_equipos y le pasamos los parametros para su ejecucion
        guardar_datos_equipos(teams, ruta_salida_teams)
        print(f"Los datos actualizados de los equipos se han guardado en {ruta_salida_teams}")
