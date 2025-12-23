import flet as ft
from state import state
from api_client import api
from datetime import datetime


def main(page: ft.Page):
    page.title = "Service ATS Mobile"
    # Mobile friendly dimensions for testing
    page.window.width = 390
    page.window.height = 844
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # --- VIEWS ---
    
    def get_login_view():
        # Inputs
        ip_field = ft.TextField(label="Server Address", value=state.api_url)
        user_field = ft.TextField(label="Usuario", icon=ft.Icons.PERSON)
        pass_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, icon=ft.Icons.LOCK)
        error_txt = ft.Text(color="red")
        
        def login_click(e):
            state.api_url = ip_field.value
            error_txt.value = "Conectando..."
            page.update()
            
            ok, msg = api.login(user_field.value, pass_field.value)
            if ok:
                page.go("/dashboard")
            else:
                error_txt.value = msg
                page.update()

        return ft.View(
            "/",
            [
                ft.AppBar(title=ft.Text("Service ATS"), bgcolor=ft.Colors.BLUE),
                ft.Column(
                    [
                        ft.Image(src="assets/logo.png", width=200, height=200), # Company Logo
                        ft.Text("Iniciar Sesión", size=30, weight="bold"),
                        ft.Divider(height=20, color="transparent"),
                        ip_field,
                        user_field,
                        pass_field,
                        ft.ElevatedButton("Entrar", on_click=login_click, width=200),
                        error_txt
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            padding=20
        )

    def get_dashboard_view():
        # --- TAB: HORAS ---
        date_field = ft.TextField(label="Fecha (YYYY-MM-DD)", value=datetime.now().strftime("%Y-%m-%d"))
        motivo_field = ft.TextField(label="Motivo")
        cliente_field = ft.TextField(label="Cliente")
        horas_field = ft.TextField(label="Horas", keyboard_type=ft.KeyboardType.NUMBER)
        
        def enviar_horas(e):
            if not horas_field.value: return
            # Simple logic for POC: total = horas * 20 (hardcoded price for now)
            # In real app we would fetch price from user config
            total = float(horas_field.value) * 20.0 
            
            ok, msg = api.post_overtime(
                date_field.value, 
                motivo_field.value, 
                cliente_field.value, 
                horas_field.value, 
                total, 
                "Hora Extra"
            )
            if ok:
                page.open(ft.SnackBar(ft.Text("Horas enviadas correctamente!")))
                motivo_field.value = ""
                horas_field.value = ""
                page.update()
            else:
                page.open(ft.SnackBar(ft.Text(f"Error: {msg}")))

        tab_horas = ft.Column([
            ft.Text("Reportar Horas Extras", size=20, weight="bold"),
            date_field,
            motivo_field,
            cliente_field,
            horas_field,
            ft.ElevatedButton("Enviar Horas", on_click=enviar_horas, bgcolor=ft.Colors.BLUE, color="white")
        ], spacing=10, scroll=ft.ScrollMode.AUTO)

        # --- TAB: GASTOS ---
        g_date = ft.TextField(label="Fecha", value=datetime.now().strftime("%Y-%m-%d"))
        g_tipo = ft.Dropdown(label="Tipo", options=[
            ft.dropdown.Option("Material"),
            ft.dropdown.Option("Comida"),
            ft.dropdown.Option("Gasoil"),
            ft.dropdown.Option("Otros")
        ], value="Material")
        g_det = ft.TextField(label="Detalle")
        g_imp = ft.TextField(label="Importe (€)", keyboard_type=ft.KeyboardType.NUMBER)
        
        def enviar_gasto(e):
            if not g_imp.value: return
            ok, msg = api.post_expense(
                g_date.value, g_tipo.value, g_det.value, g_imp.value
            )
            if ok:
                page.open(ft.SnackBar(ft.Text("Gasto enviado!")))
                g_det.value = ""
                g_imp.value = ""
                page.update()
            else:
                page.open(ft.SnackBar(ft.Text(f"Error: {msg}")))

        tab_gastos = ft.Column([
            ft.Text("Reportar Gasto", size=20, weight="bold"),
            g_date, g_tipo, g_det, g_imp,
            ft.ElevatedButton("Enviar Gasto", on_click=enviar_gasto, bgcolor=ft.Colors.ORANGE, color="white")
        ], spacing=10)

        # Tabs Container
        t = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="Horas", content=ft.Container(content=tab_horas, padding=20)),
                ft.Tab(text="Gastos", content=ft.Container(content=tab_gastos, padding=20)),
            ],
            expand=1,
        )

        return ft.View(
            "/dashboard",
            [
                ft.AppBar(
                    title=ft.Text(f"Hola, {state.user['username']}"), 
                    actions=[ft.IconButton(ft.Icons.LOGOUT, on_click=lambda e: page.go("/"))]
                ),
                t
            ]
        )

    def route_change(route):
        page.views.clear()
        page.views.append(get_login_view())
        if page.route == "/dashboard" and state.user:
            page.views.append(get_dashboard_view())
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)
