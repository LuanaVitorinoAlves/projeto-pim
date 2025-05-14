
def menu():
    while True:
        mostrar_menu()
        opcao = input("Digite a opção que deseja\n> ")
        match opcao:
            case "1":
                validar_quantidade_executar(">>> Valor da média: ", calcular_media)
            case "2":
                validar_quantidade_executar(">>> Valor da mediana:", calcular_mediana)
            case "3":
                break
        input("--- Presione ENTER para continuar")

def mostrar_menu():
    print("""
[1] Media
[2] Mediana
[3] Sair
""")

def validar_quantidade_executar(mensagem_saida, funcao):
    while True:
        quantidade = int(input("Digite a quantidade de notas que deseja inserir no sistema\n> "))
        if (quantidade <= 0):
            print("O valor deve ser maior do que zero!")
        else:
            break
    print(mensagem_saida, funcao(quantidade))

def calcular_media(quantidade: int):
    soma = 0
    for i in range(quantidade):
        soma += float(input(f"Digite a {i + 1}ª nota\n> "))
    return soma / quantidade

def calcular_mediana(quantidade: int):
    notas = []
    for i in range(quantidade):
        notas.append(float(input(f"Digite a {i + 1}ª nota\n> ")))
    notas_size = len(notas)
    index = notas_size//2;
    if notas_size == 1:
        return notas[0]
    if notas_size % 2 == 0:
        return notas[index]
    return (notas[index] + notas[index + 1]) / 2
            
menu()

