from models.client_model import Client

class ClientController:
    
    def __init__(self):
        self.clientes = []
        
    def add_client(self, id, nombre, email):
        client = Client(id, nombre, email)
        self.clientes.append(client)

    def modify_client(self, id, new_nombre, new_email):
        for client in self.clientes:
            if client.id == id:
                client.nombre = new_nombre
                client.email = new_email
                break

    def delete_client(self, id):
        self.clientes = [client for client in self.clientes if client.id != id]

    def get_client_by_id(self, id):
        for client in self.clientes:
            if client.id == id:
                return client

    def get_clients(self):
        return self.clientes
