Este bot escanea distintas fuentes rss en busca de contenido. Si encuentra novedades en alguna de ellas, publicará su título y su URL de acceso como toot en la cuenta de Mastodon correspondiente.

## Instalación

El proceso de instalación es muy simple.

1. Instala Python y Pip. Este proceso es sencillo en la mayoría de distribuciones Linux. De hecho, puede que ya los tengas instalados.
2. Clona este repositorio o descarga su contenido en una carpeta y navega hacia ella.
3. Instala los requisitos con un comando como este: `pip install -r requirements.txt`
4. Edita el archivo `bot.py` y modifica la variable `mastodon_url` indicando la URL de tu instancia.
5. Crea tantas cuentas de usuario como necesites, y autoriza la aplicación en todas ellas ejecutando el script `authorize.py`. Deberás conservar los tokens de acceso.
6. Crea un fichero `feeds.json`. En la siguiente sección se indica el formato que debe seguir.
7. Ejecuta el bot: `python bot.py`
8. Si todo funciona bien, configura una tarea Cron que lo ejecute por ti periódicamente.

## El fichero `feeds.json`

Este archivo contiene toda la información de los feeds que el bot debe analizar. Se debe situar en la misma carpeta que el archivo `bot.py`. En los distintos objetos JSON se guarda la siguiente información:

* Nombre identificativo de la cuenta.
* Token de acceso.
* Lista de fuentes RSS asociadas. Cada una contiene la URL de la fuente y la fecha de publicación de la última entrada, si se ha analizado ya con anterioridad.

Ten en cuenta que el bot modificará el contenido del fichero al finalizar su ejecución.

A continuación se ofrece un archivo de ejemplo:

```
[
	"usuario1": {
		"access_token": "token1",
		"feeds": [
			{
				"url": "https://ejemplo1.com/feed",
				"last_date": null
			}
		]
	}
]
```

## Licencia y Copyright

El código fuente de este proyecto se publica bajo los términos de la GNU General Public License, versión 2 o posterior. Puedes redistribuir y crear copias modificadas de este proyecto, siempre que dejes su código a disposición del público, indiques la fuente de procedencia y utilices esta misma licencia.
