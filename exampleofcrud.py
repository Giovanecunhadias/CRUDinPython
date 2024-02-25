import mysql.connector

class ConexaoDB:
    def __init__(self, host='localhost', usuario='seu_usuario', senha='sua_senha', banco='seu_banco'):
        self.host = host
        self.usuario = usuario
        self.senha = senha
        self.banco = banco
        self.conexao = None

    def conectar(self):
        self.conexao = mysql.connector.connect(
            host=self.host,
            user=self.usuario,
            password=self.senha,
            database=self.banco
        )
        return self.conexao

    def fechar_conexao(self):
        if self.conexao:
            self.conexao.close()

class CRUDOperations(ConexaoDB):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_table(self):
        connection = self.conectar()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
            )
        ''')
        connection.commit()
        cursor.close()
        self.fechar_conexao()

    def insert_user(self, nome, email):
        connection = self.conectar()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email))
        connection.commit()
        cursor.close()
        self.fechar_conexao()

    def get_all_users(self):
        connection = self.conectar()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        users = cursor.fetchall()
        cursor.close()
        self.fechar_conexao()
        return users

    def update_user(self, user_id, nome, email):
        connection = self.conectar()
        cursor = connection.cursor()
        cursor.execute("UPDATE usuarios SET nome=%s, email=%s WHERE id=%s", (nome, email, user_id))
        connection.commit()
        cursor.close()
        self.fechar_conexao()

    def delete_user(self, user_id):
        connection = self.conectar()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=%s", (user_id,))
        connection.commit()
        cursor.close()
        self.fechar_conexao()

# Example of Usage
crud = CRUDOperations()

# Create table (execute only once)
crud.create_table()
#insert name for user
name = input('Name for user: ')
email = input('Email for user: ')
# Insert a user
crud.insert_user(name, email)

# Get all users
all_users = crud.get_all_users()
print('All users:', all_users)

# Update a user
crud.update_user(1, 'Updated Name', 'updated.email@example.com')

# Get all users again after update
all_users_after_update = crud.get_all_users()
print('All users after update:', all_users_after_update)

# Delete a user
crud.delete_user(1)

# Get all users after deletion
all_users_after_delete = crud.get_all_users()
print('All users after deletion:', all_users_after_delete)
