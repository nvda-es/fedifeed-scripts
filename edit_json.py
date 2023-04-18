import json
import os

class Usuario:
	def __init__(self, access_token, feeds):

		self.access_token = access_token
		self.feeds = feeds

	def agregar_feed(self, url, last_date):
		self.feeds.append({"url": url, "last_date": last_date})

	def editar_feed(self, index, url):
		self.feeds[index]["url"] = url

	def eliminar_feed(self, index):
		del self.feeds[index]

	def to_dict(self):
		return {"access_token": self.access_token, "feeds": self.feeds}

# Función para imprimir los usuarios en pantalla
def imprimir_usuarios(usuarios):
	""" Podemos dar más info en esta función a mostrar"""
	for i, u in enumerate(usuarios):
		print(f"\t{i+1}: Usuario{i+1}")

# Abrir el archivo JSON y cargarlo en una lista de objetos Usuario
try:
	with open('feeds.json', 'r') as f:
		data = json.load(f)
		usuarios = [Usuario(u["access_token"], u["feeds"]) for u in data.values()]
except FileNotFoundError:
	print("No se encontró el archivo feeds.json. Creando nuevo archivo.")
	usuarios = []

# Ciclo while para el menú de opciones
while True:
	# Borra consola en Windows
	try:
		os.system('cls')
	except:
		os.system('clear')

	# Imprimir el menú de opciones
	print("Selecciona una opción:")
	print("1. Agregar usuario")
	print("2. Editar usuario")
	print("3. Eliminar usuario")
	print("4. Salir")
	opcion = input("Opción: ")

	try:
		# Opción 1: Agregar usuario
		if opcion == "1":
			access_token = input("Ingrese el access token del nuevo usuario: ")
			url = input("Ingrese la URL del feed del nuevo usuario: ")
			last_date = input("Ingrese la última fecha del feed en formato yyyy-mm-ddThh:mm:ss+hh:mm (deje en blanco para omitir): ")
			if last_date.strip() == "":
				last_date = None
			nuevo_usuario = Usuario(access_token, [{"url": url, "last_date": last_date}])
			usuarios.append(nuevo_usuario)
			print(f"Usuario {access_token} agregado exitosamente.")
			input("Presione cualquier tecla para continuar...")
		# Opción 2: Editar usuario
		elif opcion == "2":
			if not usuarios:
				print("No hay usuarios para editar.")
				input("Presione cualquier tecla para continuar...")
				continue
			imprimir_usuarios(usuarios)
			indice = int(input("Ingrese el índice del usuario que desea editar: "))
			if indice < 1 or indice > len(usuarios):
				print("Índice inválido.")
				input("Presione cualquier tecla para continuar...")
				continue
			usuario = usuarios[indice-1]
			access_token = input(f"Ingrese el nuevo access token ({usuario.access_token}): ").strip() or usuario.access_token
			feeds = []
			for i, f in enumerate(usuario.feeds):
				url = input(f"Ingrese la URL del feed {i+1} ({f['url']}): ").strip() or f["url"]
				last_date = input(f"Ingrese la última fecha del feed {i+1} en formato yyyy-mm-ddThh:mm:ss+hh:mm ({f['last_date']}): ").strip() or f["last_date"]
				feeds.append({"url": url, "last_date": last_date})
				while True:
					mas_feeds = input(f"Desea agregar otra entrada de feed para el usuario {usuario.access_token}? (s/n): ").lower()
					if mas_feeds not in ("s", "n"):
						print("Opción inválida. Por favor, ingrese 's' para sí o 'n' para no.")
					elif mas_feeds == "s":
						url = input(f"Ingrese la URL del feed {len(feeds)+1}: ")
						last_date = input(f"Ingrese la última fecha del feed {len(feeds)+1} en formato yyyy-mm-ddThh:mm:ss+hh:mm (deje en blanco para omitir): ")
						if last_date.strip() == "":
							last_date = None
						feeds.append({"url": url, "last_date": last_date})
					else:
						break
			usuarios[indice-1] = Usuario(access_token, feeds)
			print(f"Usuario {access_token} editado exitosamente.")
			input("Presione cualquier tecla para continuar...")
		# Opción 3: Eliminar usuario
		elif opcion == "3":
			if not usuarios:
				print("No hay usuarios para eliminar.")
				input("Presione cualquier tecla para continuar...")
				continue
			imprimir_usuarios(usuarios)
			indice = int(input("Ingrese el índice del usuario que desea eliminar: "))
			if indice < 1 or indice > len(usuarios):
				print("Índice inválido.")
				continue
			del usuarios[indice-1]
			print(f"Usuario {indice} eliminado exitosamente.")
			input("Presione cualquier tecla para continuar...")
		# Opción 4: Salir
		elif opcion == "4":
			break

		# Opción inválida
		else:
			print("Opción inválida. Por favor, ingrese una opción válida.")
			input("Presione cualquier tecla para continuar...")
			continue

	except ValueError:
		print("Error: el valor ingresado es inválido.")
		input("Presione cualquier tecla para continuar...")
	except KeyError:
		print("Error: el campo ingresado no existe.")
		input("Presione cualquier tecla para continuar...")
	except IndexError:
		print("Error: el índice ingresado está fuera de rango.")
		input("Presione cualquier tecla para continuar...")
	except Exception as e:
		print("Error:", e)
		input("Presione cualquier tecla para continuar...")

# Convertir los objetos Usuario a un diccionario y guardarlos en el archivo JSON
data = {f"usuario{i+1}": u.to_dict() for i, u in enumerate(usuarios)}
with open('feeds.json', 'w') as f:
	json.dump(data, f, indent='\t')
	print("Datos guardados exitosamente en archivo JSON.")