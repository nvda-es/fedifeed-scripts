from mastodon import Mastodon

print("Rellena la información necesaria para obtener tu token de acceso.")
instance_url = input("URL de la instancia: ")
client_id, client_secret = Mastodon.create_app("Fedifeed", api_base_url=instance_url, website="https://fedifeed.net")
temporary_api = Mastodon(client_id=client_id, client_secret=client_secret, api_base_url=instance_url, user_agent="Fedifeed/1.0")
auth_url = temporary_api.auth_request_url()
print("Genial, parece que todo ha ido bien. Ahora, visita esta URL en tu navegador web y autoriza la app en tu cuenta")
print(auth_url)
code = input("Introduce el código devuelto por la web: ")
access_token = temporary_api.log_in(code=code)
print("Token de acceso: "+access_token)
