# Desafio de Criptografia Simétrica: DES e Diffie-Hellman

Este projeto foi desenvolvido como parte da disciplina de **Segurança de Dados** no curso de **Sistemas para Internet do Instituto Federal da Paraíba (IFPB)**. A implementação aborda os algoritmos **DES (Data Encryption Standard)** e o **Mecanismo de Troca de Chaves Diffie-Hellman**.

O objetivo do projeto é simular a comunicação segura entre duas partes (sender e receiver) por meio de um canal inseguro, utilizando o protocolo Diffie-Hellman para gerar uma chave secreta compartilhada. Essa chave compartilhada é então usada no algoritmo DES para criptografar e descriptografar as mensagens trocadas entre as partes, proporcionando segurança na comunicação.

## Requisitos do Projeto

### 1. **Implementação do DES**

O algoritmo **DES** é um dos mais conhecidos para criptografia simétrica e opera com chaves de 56 bits, criptografando blocos de dados de 64 bits.

Para mais detalhes sobre a implementação, acesse: [https://github.com/buenorafa/des-python](https://github.com/buenorafa/des-python).

### 2. **Troca de Chaves Diffie-Hellman**

O protocolo **Diffie-Hellman** permite que duas partes, sem uma chave previamente compartilhada, estabeleçam uma chave secreta comum. A troca de chaves ocorre da seguinte forma:

- As duas partes escolhem parâmetros públicos `g` e `p` (base e número primo).
- Ambas geram suas chaves privadas e calculam suas chaves públicas.
- As chaves públicas são trocadas e, a partir delas, é gerada a chave secreta compartilhada.

## Requisitos de Implementação

- **Linguagem**: Python
- **Bibliotecas externas para criptografia**: Não é permitido o uso de bibliotecas auxiliares para criptografia.
- **Arquivos separados**: O código foi separado em `sender.py` (emissor) e `receiver.py` (receptor), conforme especificado no desafio.

## Diffie-Hellman

O algoritmo funciona com base em dois números primos públicos: uma **base** (`g`) e um **módulo** (`p`). Ambos são conhecidos por todas as partes envolvidas. Cada parte gera uma **chave privada** secreta e calcula sua **chave pública** usando os números públicos. Em seguida, as chaves públicas são trocadas. Com base na chave pública recebida e na chave privada gerada, cada parte pode calcular uma **chave compartilhada**.

### Passos Gerais:

1. Ambas as partes escolhem um número primo `g` (base) e um número primo `p` (módulo).
2. Cada parte gera uma **chave privada**.
3. Usando a chave privada e os números públicos `g` e `p`, cada parte calcula sua **chave pública**.
4. As partes trocam suas chaves públicas.
5. Cada parte usa a chave pública recebida e sua chave privada para calcular a **chave compartilhada**.

### Fórmulas:

- Chave Pública: `public key` = `g`^ `privatekey` mod `p`
- Chave Compartilhada: `shared key` = `public key other`^`private key` mod `p`

## Estrutura da Classe

A classe `DiffieHellman` implementa o processo de geração de chaves privadas e públicas, bem como a geração da chave compartilhada com base na chave pública da outra parte.

### Código:

```python
import util

class DiffieHellman:
    def __init__(self, g, p) -> None:
        self.__g = g  # Base pública (g)
        self.__p = p  # Módulo público (p)
        self.__private_key = self.__generate_private_key()  # Gera a chave privada
        self.public_key = self.__generate_public_key()  # Calcula a chave pública

    def __generate_private_key(self):
        return util.generate_random_prime(2, 3333)  # Gera uma chave privada aleatória

    def __generate_public_key(self):
        # Calcula a chave pública usando g^private_key mod p
        return (self.__g**self.__private_key) % self.__p

    def generate_shared_key(self, public_key_other):
        # Calcula a chave compartilhada usando public_key_other^private_key mod p
        return (public_key_other**self.__private_key) % self.__p
```

## Receiver e do Sender

### Receiver (Servidor)

O **receiver** é responsável por escutar a conexão do cliente (sender) e iniciar o processo de troca de chaves Diffie-Hellman. Ele gera uma chave pública a partir de uma chave privada e troca a chave pública com o sender. Após receber a chave pública do sender, o receiver calcula a chave secreta compartilhada e a utiliza para descriptografar mensagens enviadas, usando o algoritmo DES.

#### Código do Receiver:

```python
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

# Cria um server e fica esperando o Sender
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
        des = DES(shared_key)
        # Recebe e descriptografa a mensagem
        encrypted_msg = conn.recv(1024).decode()
        input('Pressione enter para descriptografar a mensagem ')
    print(f"Mensagem descriptografada: {des.decrypt(encrypted_msg)}")
```

### Sender (Cliente)

O **sender** se conecta ao receiver, gera sua chave pública e a troca com o receiver. Após a troca de chaves, o sender calcula a chave secreta compartilhada e a usa para criptografar a mensagem antes de enviá-la ao receiver.

#### Código do Sender:

```python
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
    des = DES(shared_key)
    # Envia a mensagem criptografada
    message = input("Enviar mensagem: ")
    encrypted_msg = des.encrypt(message)
    client_socket.sendall(encrypted_msg.encode())
    input('Pressione enter ver a mensagem criptografada ')
print(encrypted_msg)
```

## Como Executar

### 1. Clonar o Repositório

```bash
git clone https://github.com/buenorafa/des-diffie-hellman.git
cd des-diffie-hellman
```

### 2. Executar o Receiver (Servidor)

```bash
python3 des_diffie_hellman/receiver.py
```

O receiver vai aguardar a conexão do sender.

### 3. Executar o Sender (Cliente)

Em uma nova janela de terminal, execute:

```bash
python3 des_diffie_hellman/sender.py
```

O sender vai se conectar ao receiver, trocar as chaves públicas, calcular a chave secreta compartilhada e enviar uma mensagem criptografada usando o algoritmo DES.

### 4. Comunicação

- O sender enviará uma chave pública para o receiver.
- O receiver retornará sua chave pública.
- A chave compartilhada será calculada e utilizada para criptografar a mensagem enviada pelo sender.
- O receiver descriptografará a mensagem e exibirá o resultado.

## Exemplos de Saída

```bash
# Receiver (servidor)
Aguardando conexão na porta 5001...
Conectado a: ('127.0.0.1', 49531)
Chave pública do sender recebida: 10361
Chave pública do receiver enviada: 25013
70d92fd02a3ffcd2
Pressione enter para descriptografar a mensagem
Mensagem descriptografada: teste

# Sender (cliente)
Conectado ao servidor localhost:5001
Chave pública do sender enviada: 10361
Chave pública do receiver recebida: 25013
Enviar mensagem: teste
Pressione enter ver a mensagem criptografada
70d92fd02a3ffcd2
```
