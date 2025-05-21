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

def register_user(admin=False):
    admin_str = 'ADMIN ' if admin else ''
    print(f"\n=== Cadastro de Usuário ===")
    if admin:
        print("USUÁRIO ADMINISTRADOR")

    print("\nPolítica de Privacidade:")
    print("Este sistema armazena seus dados localmente apenas para fins educacionais.")
    print("Nenhuma informação será compartilhada com terceiros.")
    print("Você pode solicitar a exclusão de seus dados a qualquer momento.")

    aceite = input("Você aceita os termos da política de privacidade? (S/N): ").strip().lower()
    if aceite != 's':
        print("Cadastro cancelado. É necessário aceitar a política de privacidade.")
        return

    nome = input(f"{admin_str}Nome: ")
    idade = int(input(f"{admin_str}Idade: "))
    email = input(f"{admin_str}Email: ")
    senha = input(f"{admin_str}Senha: ")
    pergunta = input(f"Digite uma pergunta de segurança (ex: Nome da sua mãe?): ")
    resposta = input(f"Resposta: ")
    
    usuario = {
        "id": len(usuarios) + 1,
        "nome": nome,
        "idade": idade,
        "email": email,
        "senha": hash_password(senha),
        "pergunta": pergunta,
        "resposta": hash_password(resposta.lower().strip()),
        "notas": [],
        "aceite_politica": True,
        "admin": admin
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
                if usuario.get("admin"):
                    menu_admin(usuario)
                else:
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

def menu_admin(usuario):
    while True:
        print(f"\nBem-vindo(a) ADMIN, {usuario['nome']}")
        print("1. Ver Estatísticas da Plataforma")
        print("2. Logout")
        op = input("Escolha uma opção: ")

        if op == "1":
            mostrar_estatisticas_globais()
        elif op == "2":
            break
        else:
            print("Opção inválida.")

def mostrar_estatisticas_globais():
    print("\n=== Estatísticas da Plataforma ===")
    if not usuarios:
        print("Nenhum dado para exibir.")
        return

    idades = [u["idade"] for u in usuarios]
    todas_notas = [nota for u in usuarios for nota in u["notas"]]

    print(f"Usuários cadastrados: {len(usuarios)}")
    print(f"Idade média: {statistics.mean(idades):.1f}")

    faixa_etaria = {"0-17": 0, "18-25": 0, "26-40": 0, "41+": 0}
    for idade in idades:
        if idade <= 17:
            faixa_etaria["0-17"] += 1
        elif idade <= 25:
            faixa_etaria["18-25"] += 1
        elif idade <= 40:
            faixa_etaria["26-40"] += 1
        else:
            faixa_etaria["41+"] += 1
    print("Distribuição por faixa etária:")
    for faixa, total in faixa_etaria.items():
        print(f"  {faixa}: {total} usuário(s)")

    if todas_notas:
        print(f"\nTotal de notas registradas: {len(todas_notas)}")
        print(f"Média geral das notas: {statistics.mean(todas_notas):.2f}")
        print(f"Mediana das notas: {statistics.median(todas_notas):.2f}")
        try:
            print(f"Moda das notas: {statistics.mode(todas_notas):.2f}")
        except statistics.StatisticsError:
            print("Moda das notas: Sem valor único dominante.")

        # Histograma textual
        print("\nHistograma de notas:")
        faixas = {"0-4": 0, "5-6": 0, "7-8": 0, "9-10": 0}
        for nota in todas_notas:
            if nota < 5:
                faixas["0-4"] += 1
            elif nota <= 6:
                faixas["5-6"] += 1
            elif nota <= 8:
                faixas["7-8"] += 1
            else:
                faixas["9-10"] += 1
        for faixa, contagem in faixas.items():
            print(f"  {faixa}: {'*' * contagem}")
    else:
        print("Nenhuma nota registrada ainda.")

# Execução
usuarios = load_data(USERS_FILE)
if not usuarios:
    print("Nenhum usuário encontrado. Cadastro inicial obrigatório (admin).")
    register_user(admin=True)
menu_principal()
