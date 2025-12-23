class AppState:
    api_url: str = "http://127.0.0.1:8000"  # Default for testing
    user: dict = None
    token: str = None  # Future use

state = AppState()
