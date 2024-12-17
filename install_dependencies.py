import subprocess
import sys

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencias instaladas correctamente.")
    except subprocess.CalledProcessError as e:
        print("Error al instalar las dependencias:", e)

if __name__ == "__main__":
    install_requirements()