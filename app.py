import os
import cherrypy
import mysql.connector

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")


class App:
    @cherrypy.expose
    def index(self):
        return """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Registro Paciente</title>
            <link rel="stylesheet" href="/static/estilos.css">
        </head>
        <body>
            <div class="container">
                <h1>Registro de Paciente</h1>

                <form action="/guardar" method="POST">
                    <label>Nombre completo</label>
                    <input type="text" name="nombre_paciente" required>

                    <label>Fecha de Nacimiento</label>
                    <input type="date" name="fecha_nacimiento" required>

                    <label>Género</label>
                    <select name="genero_paciente" required>
                        <option value="">Seleccionar</option>
                        <option value="M">Masculino</option>
                        <option value="F">Femenino</option>
                        <option value="O">Otro</option>
                    </select>

                    <label>Fecha de visita</label>
                    <input type="date" name="fecha_visita">

                    <label>Nombre del médico</label>
                    <input type="text" name="nombreMedico">

                    <label>Género del médico</label>
                    <select name="generoMedicos" required>
                        <option value="">Seleccionar</option>
                        <option value="Masculino">Masculino</option>
                        <option value="Femenino">Femenino</option>
                        <option value="Otro">Otro</option>
                    </select>

                    <label>Cargo del médico</label>
                    <select name="cargoMedico">
                        <option value="">Seleccionar</option>
                        <option value="Medico general">Médico general</option>
                        <option value="Especialista - Pediatra">Especialista - Pediatra</option>
                        <option value="Especialista - Ginecologo">Especialista - Ginecólogo</option>
                        <option value="Otro">Otro</option>
                    </select>

                    <label>¿Se recetaron medicamentos?</label>
                    <select name="recetaronMedicamentos">
                        <option value="">Seleccionar</option>
                        <option value="Si">Si</option>
                        <option value="No">No</option>
                    </select>

                    <label>
                        <input type="checkbox" name="recibioMedicamento" value="1">
                        Recibió medicamento
                    </label>

                    <button type="submit">Guardar</button>
                </form>
            </div>
        </body>
        </html>
        """

    @cherrypy.expose
    def guardar(
        self,
        nombre_paciente="",
        fecha_nacimiento="",
        genero_paciente="",
        fecha_visita="",
        nombreMedico="",
        generoMedicos="",
        cargoMedico="",
        recetaronMedicamentos="",
        recibioMedicamento=None
    ):
        recetaron = 1 if recetaronMedicamentos == "Si" else 0
        recibio = 1 if recibioMedicamento else 0

        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sofiaroy",
            database="ESEHLMPL"
        )
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO pacientes (nombre_paciente, fecha_nacimiento, genero_paciente) VALUES (%s, %s, %s)",
            (nombre_paciente, fecha_nacimiento, genero_paciente)
        )
        id_paciente = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO visitas
            (id_paciente, fecha_visita, nombre_medico, genero_medicos, cargo_medico, recibio_medicamento, recetaronmedicamentos)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (id_paciente, fecha_visita, nombreMedico, generoMedicos, cargoMedico, recibio, recetaron)
        )
        id_visita = cursor.lastrowid

        conexion.commit()
        cursor.close()
        conexion.close()

        return f"""
        <h2>Guardado correctamente</h2>
        <p>Paciente ID: {id_paciente}</p>
        <p>Visita ID: {id_visita}</p>
        <a href="/">Volver</a>
        """


if __name__ == "__main__":
    cherrypy.config.update({
        "server.socket_port": 8080,
        "server.socket_host": "127.0.0.1"
    })

    conf = {
        "/static": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": STATIC_DIR
        }
    }

    cherrypy.quickstart(App(), "/", conf)