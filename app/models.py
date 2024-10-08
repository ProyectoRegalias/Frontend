import os
import pandas as pd

USERS_EXCEL_FILE = 'user_data.xlsx'
HISTORIAL_EXCEL_FILE = 'historial_data.xlsx'

def cargar_usuarios():
    usuarios = {}
    if os.path.exists(USERS_EXCEL_FILE):
        try:
            df = pd.read_excel(USERS_EXCEL_FILE, sheet_name='Usuarios')
            usuarios = pd.Series(df.password.values, index=df.username).to_dict()
        except FileNotFoundError:
            pass
    return usuarios

def guardar_usuario(username, password):
    new_user = {'username': username, 'password': password}
    new_df = pd.DataFrame([new_user])
    if os.path.exists(USERS_EXCEL_FILE):
        with pd.ExcelWriter(USERS_EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            if 'Usuarios' in writer.book.sheetnames:
                existing_df = pd.read_excel(USERS_EXCEL_FILE, sheet_name='Usuarios')
                df = pd.concat([existing_df, new_df], ignore_index=True)
                del writer.book['Usuarios']
            else:
                df = new_df
            df.to_excel(writer, sheet_name='Usuarios', index=False)
    else:
        with pd.ExcelWriter(USERS_EXCEL_FILE, engine='openpyxl') as writer:
            new_df.to_excel(writer, sheet_name='Usuarios', index=False)

def cargar_historial_usuario(username):
    historial = []
    if os.path.exists(HISTORIAL_EXCEL_FILE):
        try:
            with pd.ExcelWriter(HISTORIAL_EXCEL_FILE, engine='openpyxl', mode='a') as writer:
                if username in writer.book.sheetnames:
                    df = pd.read_excel(HISTORIAL_EXCEL_FILE, sheet_name=username)
                    historial = df.to_dict('records')
        except PermissionError:
            print("Error: Archivo en uso.")
    return historial

def guardar_datos_usuario(username, pregunta, respuesta):
    new_data = {'Pregunta': pregunta, 'Respuesta': respuesta}
    new_df = pd.DataFrame([new_data])
    if os.path.exists(HISTORIAL_EXCEL_FILE):
        try:
            with pd.ExcelWriter(HISTORIAL_EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                if username in writer.book.sheetnames:
                    existing_df = pd.read_excel(HISTORIAL_EXCEL_FILE, sheet_name=username)
                    df = pd.concat([existing_df, new_df], ignore_index=True)
                    del writer.book[username]
                else:
                    df = new_df
                df.to_excel(writer, sheet_name=username, index=False)
        except PermissionError:
            print("Error: Archivo en uso.")
    else:
        with pd.ExcelWriter(HISTORIAL_EXCEL_FILE, engine='openpyxl') as writer:
            new_df.to_excel(writer, sheet_name=username, index=False)
