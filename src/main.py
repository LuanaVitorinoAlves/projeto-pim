import json
import hashlib
import statistics
import os

from crypto import load_key, encrypt_data, decrypt_data

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "usuarios.json")
COURSES_FILE = os.path.join(DATA_DIR, "cursos.json")
key = load_key()

# === Função para garantir a criação da pasta ===
def ensure_data_directory():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

# === Leitura com Descriptografia ===
def load_data(file):
    ensure_data_directory()
    if not os.path.exists(file):
        return []
    with open(file, 'r') as f:
        encrypted_data = f.read()
        decrypted_data = decrypt_data(encrypted_data, key)
        return json.loads(decrypted_data)

def save_data(file, data):
    ensure_data_directory()
    with open(file, 'w') as f:
        json_data = json.dumps(data, indent=4)
        encrypted_data = encrypt_data(json_data, key)
        f.write(encrypted_data)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    print("\n=== Cadastro de Usuário ===")
    nome = input("Nome: ")
    idade = int(input("Idade: "))
    email = input("Email: ")
    senha = input("Senha: ")
    
    usuario = {
        "id": len(usuarios) + 1,
        "nome": nome,
        "idade": idade,
        "email": email,
        "senha": hash_password(senha),
        "notas": []
    }
    
    usuarios.append(usuario)
    save_data(USERS_FILE, usuarios)
    print("Usuário cadastrado com sucesso!\n")

def login():
    print("\n=== Login ===")
    email = input("Email: ")
    senha = input("Senha: ")

    for u in usuarios:
        if u["email"] == email and u["senha"] == hash_password(senha):
            print("Login bem-sucedido!\n")
            return u
    print("Credenciais inválidas.\n")
    return None

def adicionar_nota(usuario):
    print("\n=== Adicionar Nota ===")
    try:
        nota = float(input("Digite a nota do curso (0 a 10): "))
        if 0 <= nota <= 10:
            usuario["notas"].append(nota)
            save_data(USERS_FILE, usuarios)
            print("Nota registrada com sucesso!")
        else:
            print("Nota inválida.")
    except ValueError:
        print("Digite um número válido.")

def exibir_desempenho(usuario):
    print("\n=== Desempenho ===")
    if not usuario["notas"]:
        print("Sem notas registradas.")
        return
    notas: list[float] = usuario["notas"]
    print(f"Notas: {', '.join(map(str, notas))}")
    print(f"Média: {statistics.mean(notas):.2f}")
    print(f"Moda: {statistics.mode(notas):.2f}")
    print(f"Mediana: {statistics.median(notas):.2f}")

def menu_principal():
    while True:
        print("\n1. Cadastrar Usuário")
        print("2. Login")
        print("3. Sair")
        op = input("Escolha uma opção: ")

        if op == "1":
            register_user()
        elif op == "2":
            usuario = login()
            if usuario:
                menu_usuario(usuario)
        elif op == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

def menu_usuario(usuario):
    while True:
        print(f"\nBem-vindo(a), {usuario['nome']}")
        print("1. Adicionar Nota")
        print("2. Ver Desempenho")
        print("3. Logout")
        op = input("Escolha uma opção: ")

        if op == "1":
            adicionar_nota(usuario)
        elif op == "2":
            exibir_desempenho(usuario)
        elif op == "3":
            break
        else:
            print("Opção inválida.")

# Execução
usuarios = load_data(USERS_FILE)
menu_principal()
