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

    print("\nPolítica de Privacidade:")
    print("Este sistema armazena seus dados localmente apenas para fins educacionais.")
    print("Nenhuma informação será compartilhada com terceiros.")
    print("Você pode solicitar a exclusão de seus dados a qualquer momento.")

    aceite = input("Você aceita os termos da política de privacidade? (S/N): ").strip().lower()
    if aceite != 's':
        print("Cadastro cancelado. É necessário aceitar a política de privacidade.")
        return

    nome = input("Nome: ")
    idade = int(input("Idade: "))
    email = input("Email: ")
    senha = input("Senha: ")
    pergunta = input("Digite uma pergunta de segurança (ex: Nome da sua mãe?): ")
    resposta = input("Resposta: ")
    
    usuario = {
        "id": len(usuarios) + 1,
        "nome": nome,
        "idade": idade,
        "email": email,
        "senha": hash_password(senha),
        "pergunta": pergunta,
        "resposta": hash_password(resposta.lower().strip()),
        "notas": [],
        "aceite_politica": True
    }
    
    usuarios.append(usuario)
    save_data(USERS_FILE, usuarios)
    print("Usuário cadastrado com sucesso!\n")

def recuperar_senha():
    print("\n=== Recuperação de Senha ===")
    email = input("Email: ")
    for usuario in usuarios:
        if usuario["email"] == email:
            print(f"Pergunta de segurança:\n -- {usuario['pergunta']}")
            resposta = input("Resposta: ").lower().strip()
            if hash_password(resposta) == usuario["resposta"]:
                nova_senha = input("Digite a nova senha: ")
                usuario["senha"] = hash_password(nova_senha)
                save_data(USERS_FILE, usuarios)
                print("Senha atualizada com sucesso!")
                return
            else:
                print("Resposta incorreta.")
                return
    print("Email não encontrado.")


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
        print("3. Recuperar Senha")
        print("4. Sair")
        op = input("Escolha uma opção: ")

        if op == "1":
            register_user()
        elif op == "2":
            usuario = login()
            if usuario:
                menu_usuario(usuario)
        elif op == "3":
            recuperar_senha()
        elif op == "4":
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
