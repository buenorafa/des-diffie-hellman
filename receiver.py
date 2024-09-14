import socket
from diffie_hellman import DiffieHellman
from des import DES

# Configuração do servidor
host = 'localhost'
port = 5001

# Parâmetros públicos (g e p)
g = 5
p = 972633691296 

# Inicializando o receiver (servidor) Diffie-Hellman
receiver = DiffieHellman(g, p)

# Cria uma comunicação via socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host, port)) 
    server_socket.listen(1)
    print(f"Aguardando conexão na porta {port}...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"Conectado a: {addr}")
        
        # Recebe a chave pública de Sender
        sender_public_key = int(conn.recv(1024).decode())
        print(f"Chave pública do sender recebida: {sender_public_key}")

        # Envia a chave pública de Receiver para Sender
        conn.sendall(str(receiver.public_key).encode())
        print(f"Chave pública do receiver enviada: {receiver.public_key}")

        # Calcula a chave compartilhada
        shared_key = str(receiver.generate_shared_key(sender_public_key))
        # Utiliza a chave comum Diffie Hellman como a chave do DES
        des = DES(shared_key)
        # Recebe a mensagem criptografada
        encrypted_msg = conn.recv(1024).decode()
        print(encrypted_msg)
        input('Pressione enter para descriptografar a mensagem ')
    print(f"Mensagem descriptografada: {des.decrypt(encrypted_msg)}")
        