
import streamlit as st
import sqlite3
import secrets

st.set_page_config(
    page_title="Mi Entrada Digital",
    page_icon="🎟️",
    layout="centered"
)

# Base de datos
def conectar():
    return sqlite3.connect("usuarios.db")

def preparar_db():
    with conectar() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL UNIQUE,
                codigo TEXT NOT NULL UNIQUE
            )
        """)

preparar_db()

# Generar código único
def generar_codigo():
    with conectar() as db:
        while True:
            codigo = str(secrets.randbelow(90000000) + 10000000)
            existe = db.execute(
                "SELECT id FROM usuarios WHERE codigo=?",
                (codigo,)
            ).fetchone()
            if not existe:
                return codigo

# Título
st.title("🎟️ Mi Entrada Digital")
st.write("Regístrate o ingresa utilizando tu código personal.")

opcion = st.radio(
    "Selecciona una opción:",
    ["Registrarse", "Ingresar con código"],
    horizontal=True
)

if opcion == "Registrarse":

    st.subheader("📝 Registro de usuario")

    with st.form("registro"):
        nombre = st.text_input("Nombre completo")
        correo = st.text_input("Correo electrónico")
        guardar = st.form_submit_button(
            "Registrarme",
            use_container_width=True
        )

    if guardar:
        nombre = nombre.strip()
        correo = correo.strip().lower()

        if not nombre or "@" not in correo:
            st.warning("Completa correctamente tus datos.")
        else:
            codigo = generar_codigo()

            try:
                with conectar() as db:
                    db.execute(
                        """INSERT INTO usuarios
                        (nombre, correo, codigo)
                        VALUES (?, ?, ?)""",
                        (nombre, correo, codigo)
                    )

                st.success("¡Registro exitoso!")
                st.write("Guarda tu código personal:")
                st.code(codigo)
                st.info("Lo necesitarás para volver a ingresar.")

            except sqlite3.IntegrityError:
                st.error("Este correo ya está registrado.")

else:

    st.subheader("🔐 Ingreso de usuario")

    codigo = st.text_input(
        "Ingresa tu código de 8 dígitos",
        max_chars=8
    )

    if st.button("Ingresar", use_container_width=True):

        with conectar() as db:
            usuario = db.execute(
                "SELECT nombre, correo FROM usuarios WHERE codigo=?",
                (codigo.strip(),)
            ).fetchone()

        if usuario:
            st.success("✅ Acceso autorizado")
            st.balloons()
            st.subheader(f"¡Bienvenido, {usuario[0]}!")
            st.write(f"📧 Correo: {usuario[1]}")
            st.write("🎟️ Tu entrada es válida.")
        else:
            st.error("Código incorrecto o no registrado.")
