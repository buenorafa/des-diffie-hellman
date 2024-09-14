import socket
from diffie_hellman import DiffieHellman
from des import DES

# Configuração do cliente
host = 'localhost'
port = 5001

# Parâmetros públicos (g e p)
g = 5
p = 972633691296

# Inicializando o sender (cliente) Diffie-Hellman
sender = DiffieHellman(g, p)

# Criando socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

    client_socket.connect((host, port))
    print(f"Conectado ao servidor {host}:{port}")

    # Envia a chave pública do sender para o receiver
    client_socket.sendall(str(sender.public_key).encode())
    print(f"Chave pública do sender enviada: {sender.public_key}")

    # Recebe a chave pública do receiver
    receiver_public_key = int(client_socket.recv(1024).decode())
    print(f"Chave pública do receiver recebida: {receiver_public_key}")

    # Calcula a chave compartilhada
    shared_key = str(sender.generate_shared_key(receiver_public_key))
    # Utiliza a chave comum Diffie Hellman como a chave do DES
    des = DES(shared_key)
    # Enviar mensagem criptografada
    message = input("Enviar mensagem: ")
    encrypted_msg = des.encrypt(message)
    client_socket.sendall(encrypted_msg.encode())
    input('Pressione enter ver a mensagem criptografada ')
print(encrypted_msg)
    
    