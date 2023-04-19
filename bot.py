#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from email.utils import parsedate_to_datetime
import feedparser
import json
from mastodon import Mastodon
from datetime import datetime
import sys
import time

# URL de la instancia de Mastodon donde se publicarán los estados
mastodon_url = 'https://fedifeed.net'

# Ruta del archivo JSON donde se almacenarán las URLs de los feeds de noticias y las credenciales de acceso a Mastodon
feeds_file_path = 'feeds.json'

# Leer las URLs de los feeds de noticias y las credenciales de acceso a Mastodon del archivo JSON
try:
	with open(feeds_file_path, 'r') as f:
		feeds_data = json.load(f)
except FileNotFoundError:
	feeds_data = None

# Si no hay ninguna URL de feed de noticias o credencial de acceso a Mastodon, salir del script
if not feeds_data:
	print('No se encontraron feeds de noticias o credenciales de acceso a Mastodon.')
	sys.exit(1)

# Iterar sobre cada usuario y sus respectivos feeds de noticias y credenciales de acceso a Mastodon
for user_key, user_data in feeds_data.items():
	account_name = user_key
	feed_urls = user_data['feeds']
	mastodon_token = user_data['access_token']
	# Inicializar el cliente de Mastodon
	mastodon = Mastodon(
		access_token = mastodon_token,
		api_base_url = mastodon_url
	)

	# Iterar sobre las URLs de los feeds de noticias del usuario actual
	for feed_url in feed_urls:
		# Obtener los datos del feed de noticias
		feed_data = feedparser.parse(feed_url['url'])

		# Leer la última fecha de publicación, si existe
		try:
			last_published_date = datetime.fromisoformat(feed_url['last_date'])
		except:
			last_published_date = None

		# Iterar sobre las entradas del feed de noticias
		max_date = last_published_date
		for entry in feed_data.entries:
			# Obtener el título, la URL y la fecha de la entrada
			title = entry.title
			url = entry.link
			entry_date = parsedate_to_datetime(entry.published)

			# Si la fecha de la entrada es posterior a la última fecha de publicación,
			# publicar la entrada en Mastodon y actualizar la última fecha de publicación
			if last_published_date is None or entry_date > last_published_date:
				# Crear el texto del estado de Mastodon
				status_text = f'{title}\n\n{url}'

				# Publicar el estado en Mastodon
				mastodon.status_post(status_text, visibility="unlisted")
				time.sleep(1)

				# Actualizar la última fecha de publicación si es necesario
				if max_date is None or entry_date > max_date:
					max_date = entry_date

		# Guardar la última fecha de publicación
		if max_date is not None:
			feed_url['last_date'] = max_date.isoformat()

# Guardar las últimas fechas de publicación de cada usuario
with open(feeds_file_path, 'w') as f:
	json.dump(feeds_data, f, indent=0)
