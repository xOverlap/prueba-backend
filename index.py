from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse
from controller.client_controler import ClientController

cliente = ClientController()

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)

        if path == "/":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            clientes = cliente.get_clients()

            html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de clientes</title>
</head>
<body>
<h1>Lista de clientes</h1>
<ul>
"""
            for cl in clientes:
                html_content += (
                    f"<li>{cl.id} - {cl.nombre} - {cl.email}"
                    f" [<a href='/modify?id={cl.id}'>Modificar</a>] "
                    f" [<a href='/delete?id={cl.id}'>Eliminar</a>]</li>"
                )
            html_content += "</ul>"

            html_form = """
                        <h2>Agregar Nuevos Clientes</h2><br>
                        <form method="POST" action="/">
                            <label>Nombre: </label><br>
                                <input type="text" id="nombre" name="nombre"><br>
                            <label>Correo: </label><br>
                                <input type="text" id="email" name="email"><br>
                            <input type="submit" value="Agregar_Clientes"><br>
                        </form>
                        """
            html_form += "</body></html>"
            html_content += html_form

            self.wfile.write(html_content.encode())
            return

        elif path == "/modify":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            modify_id = int(query.get('id', [''])[0])
            client_to_modify = cliente.get_client_by_id(modify_id)
            
            html_form = """
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de clientes</title>
</head>
<body>
"""
            if client_to_modify:
                html_form += f"""
                            <h2>Modificar Cliente</h2><br>
                            <form method="POST" action="/">
                                <input type="hidden" name="modify_id" value="{modify_id}">
                                <label>Nombre: </label><br>
                                    <input type="text" id="new_nombre" name="new_nombre" value="{client_to_modify.nombre}"><br>
                                <label>Correo: </label><br>
                                    <input type="text" id="new_email" name="new_email" value="{client_to_modify.email}"><br>
                                <input type="submit" value="Modificar"><br>
                            </form>
                            """
            else:
                html_form += "Cliente no encontrado."
                
            html_form += "</body></html>"
            self.wfile.write(html_form.encode())

        elif path == "/delete":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            delete_id = int(query.get('id', [''])[0])
            client_to_delete = cliente.get_client_by_id(delete_id)

            html_form = """
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de clientes</title>
</head>
<body>
"""
            if client_to_delete:
                html_form += f"""
                            <h2>Eliminar Cliente</h2><br>
                            <form method="POST" action="/">
                                <input type="hidden" name="delete_id" value="{delete_id}">
                                <p>¿Está seguro de eliminar al cliente {client_to_delete.nombre}?</p>
                                <input type="submit" value="Eliminar"><br>
                            </form>
                            """
                            
            else:
                html_form += "Cliente no encontrado."
                
            html_form += "</body></html>"
            self.wfile.write(html_form.encode())
                

        else:
            self.send_error(404, "Página no encontrada")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        parsed_data = urllib.parse.parse_qs(post_data)

        nombre = parsed_data['nombre'][0]
        email = parsed_data['email'][0]

        cliente.add_client(len(cliente.get_clients()) + 1, nombre, email)

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        parsed_data = urllib.parse.parse_qs(post_data)

        if 'modify_id' in parsed_data:
            modify_id = int(parsed_data['modify_id'][0])
            new_nombre = parsed_data['new_nombre'][0]
            new_email = parsed_data['new_email'][0]

            cliente.modify_client(modify_id, new_nombre, new_email)

        elif 'delete_id' in parsed_data:
            delete_id = int(parsed_data['delete_id'][0])
            cliente.delete_client(delete_id)

        else:
            nombre = parsed_data['nombre'][0]
            email = parsed_data['email'][0]

            cliente.add_client(len(cliente.get_clients()) + 1, nombre, email)

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()


PORT = 8000

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

with HTTPServer(("",PORT),MyHandler) as httpd:
    print(f"Servidor en el puerto {PORT}")
    httpd.serve_forever()