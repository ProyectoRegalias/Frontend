from app import create_app
import webbrowser

# Función para abrir el navegador
def open_browser():
    # La URL generada por Flask (por defecto en localhost:5000)
    webbrowser.open("http://127.0.0.1:5000")

app = create_app()

if __name__ == '__main__':
    open_browser()
    app.run(debug=True, use_reloader=False)