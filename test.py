import tweepy
import os
import dotenv
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

# === Carregar variáveis de ambiente ===
dotenv.load_dotenv()
client_id = os.environ["client_id"]
redirect_uri = os.environ["redirect_uri"]
scopes = ["tweet.write", "tweet.read", "users.read", "offline.access"]

# === Inicializa o handler do OAuth 2.0 com PKCE ===
oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=client_id,
    redirect_uri=redirect_uri,
    scope=scopes
)

# === Gera URL de autorização ===
auth_url = oauth2_user_handler.get_authorization_url()
print("🔗 Autorize seu app no navegador:", auth_url)
webbrowser.open(auth_url)

# === Servidor local para capturar o código ===
class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if "/callback" in self.path:
            code = self.path.split("code=")[-1].split("&")[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"✅ Autenticado! Pode voltar ao terminal.")
            self.server.auth_code = code

httpd = HTTPServer(("localhost", 8080), OAuthCallbackHandler)
httpd.handle_request()

# === Troca o código por access_token ===
token = oauth2_user_handler.fetch_token(httpd.auth_code)

# === Cria cliente com o token ===
client = tweepy.Client(access_token=token['access_token'])

# === Testa postagem de tweet ===
tweet = "🌤️ Post de teste via OAuth 2.0 atualizado! #OAuth2 #TwitterAPI"
response = client.create_tweet(text=tweet)
print("✅ Tweet postado:", response)
