import requests
from state import state

class APIClient:
    def get_url(self, endpoint):
        base = state.api_url.rstrip("/")
        path = endpoint.lstrip("/")
        return f"{base}/{path}"

    def login(self, username, password):
        url = self.get_url("/auth/login")
        try:
            resp = requests.post(url, json={"username": username, "password": password}, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                state.user = data
                return True, "Login OK"
            elif resp.status_code == 401:
                return False, "Usuario o contraseña incorrectos"
            else:
                return False, f"Server Error: {resp.status_code}"
        except Exception as e:
            return False, f"Connection Error: {e}"

    def post_overtime(self, fecha, motivo, cliente, horas, total, tipo):
        if not state.user: return False, "No logged in"
        
        url = self.get_url("/technicians/overtime")
        payload = {
            "fecha": fecha,
            "motivo": motivo,
            "cliente": cliente,
            "horas": float(horas),
            "total": float(total),
            "tipo": tipo,
            "usuario": state.user["username"]
        }
        
        try:
            resp = requests.post(url, json=payload, timeout=5)
            if resp.status_code == 200:
                return True, resp.json()
            else:
                return False, f"Error {resp.status_code}: {resp.text}"
        except Exception as e:
            return False, str(e)

    def post_expense(self, fecha, tipo, detalle, importe):
        if not state.user: return False, "No logged in"
        
        url = self.get_url("/technicians/expenses")
        payload = {
            "fecha": fecha,
            "tipo": tipo,
            "detalle": detalle,
            "importe": float(importe),
            "usuario": state.user["username"]
        }
        
        try:
            resp = requests.post(url, json=payload, timeout=5)
            if resp.status_code == 200:
                return True, resp.json()
            else:
                return False, f"Error {resp.status_code}: {resp.text}"
        except Exception as e:
            return False, str(e)

api = APIClient()
