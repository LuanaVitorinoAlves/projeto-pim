# src/crypto_utils.py

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

KEY_FILE = "key.key"
SALT = b'\x92\x93\x13\x1d\xd4\xe4\x91\xf3'  # Salt fixo para derivação de chave

# === Geração de chave baseada em senha ===
def generate_key(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# === Função para salvar a chave ===
def save_key(key):
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

# === Função para carregar a chave ===
def load_key():
    if not os.path.exists(KEY_FILE):
        password = input("Defina uma senha mestra para proteger os dados: ")
        key = generate_key(password)
        save_key(key)
        print("Chave gerada e salva com sucesso!")
    else:
        password = input("Digite a senha mestra para acessar os dados: ")
        key = generate_key(password)
    return key

# === Função para criptografar dados ===
def encrypt_data(data, key):
    iv = os.urandom(16)  # Vetor de inicialização aleatório
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Preenchimento (Padding)
    padded_data = data + ' ' * (16 - len(data) % 16)
    encrypted = encryptor.update(padded_data.encode()) + encryptor.finalize()

    # Salva o IV junto com os dados criptografados
    return urlsafe_b64encode(iv + encrypted).decode()

# === Função para descriptografar dados ===
def decrypt_data(encrypted_data, key):
    raw_data = urlsafe_b64decode(encrypted_data)
    iv, encrypted = raw_data[:16], raw_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Remove o preenchimento (Padding)
    decrypted = decryptor.update(encrypted) + decryptor.finalize()
    return decrypted.decode().strip()
