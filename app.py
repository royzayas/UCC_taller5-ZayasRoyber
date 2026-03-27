import os
import json
import cherrypy
import mysql.connector

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
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
                        <option value="Especialista - Cardiologo">Especialista - Cardiólogo</option>
                        <option value="Especialista - Neumologo">Especialista - Neumólogo</option>
                        <option value="Especialista - Neurologo">Especialista - Neurólogo</option>
                        <option value="Cirujano">Cirujano</option>
                        <option value="Anestesiologo">Anestesiólogo</option>
                        <option value="Internista">Internista</option>
                        <option value="Ortopedista">Ortopedista</option>
                        <option value="Psiquiatra">Psiquiatra</option>
                        <option value="Endocrinologo">Endocrinólogo</option>
                        <option value="Gastroenterologo">Gastroenterólogo</option>
                        <option value="Fisioterapeuta">Fisioterapeuta</option>
                        <option value="Dermatologo">Dermatólogo</option>
                        <option value="Oftalmologo">Oftalmólogo</option>
                        <option value="Odontologo">Odontólogo</option>
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

        os.makedirs(DATA_DIR, exist_ok=True)

        paciente = {
            "id_paciente": id_paciente,
            "nombre": nombre_paciente,
            "fecha_nacimiento": fecha_nacimiento,
            "genero": genero_paciente
        }

        visita = {
            "id_visita": id_visita,
            "id_paciente": id_paciente,
            "fecha_visita": fecha_visita,
            "nombre_medico": nombreMedico,
            "genero_medicos": generoMedicos,
            "cargo_medico": cargoMedico,
            "recibio_medicamento": recibio,
            "recetaronmedicamentos": recetaron
        }

        with open(os.path.join(DATA_DIR, "pacientes.json"), "a", encoding="utf-8") as f:
            f.write(json.dumps(paciente, ensure_ascii=False) + "\n")

        with open(os.path.join(DATA_DIR, "visitas.json"), "a", encoding="utf-8") as f:
            f.write(json.dumps(visita, ensure_ascii=False) + "\n")

        with open(os.path.join(DATA_DIR, "pacientes.txt"), "a", encoding="utf-8") as f:
            f.write(
                f"Paciente: {nombre_paciente} | ID: {id_paciente} | "
                f"Fecha Nac: {fecha_nacimiento} | Genero: {genero_paciente}\n"
            )

        with open(os.path.join(DATA_DIR, "visitas.txt"), "a", encoding="utf-8") as f:
            f.write(
                f"Visita: {id_visita} | Paciente: {nombre_paciente} | "
                f"Fecha Visita: {fecha_visita} | Medico: {nombreMedico}\n"
            )

        return """
        <h2>Guardado correctamente</h2>
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