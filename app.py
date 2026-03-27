import os
import cherrypy

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

                    <button type="submit">Guardar</button>
                </form>
            </div>
        </body>
        </html>
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