#Saudação
def saudacao (nome):
    print (f"Olá {nome}!")
nome = input ("Digite seu nome:")
saudacao (nome)

#Soma simples
def somar (a,b):
    return a + b
a = float(input("Digite o primeiro número: "))
b = float (input("Digite o segundo número:"))
soma = somar (a,b)
print (f"O resultado é {soma}")

#Número maior
def maior_de_dois(a, b):
    if a > b:
       return a
    elif b > a:
       return b

a = (input("Digite o 1º número:"))
b = (input("Digite o 2º número:"))

maior = maior_de_dois(a, b)
print(f"O maior número é {maior}")


#Verfificação de par
def eh_par (numero):
    if numero % 2 == 0:
        return True
    else:
        return False   
    
numero = int(input("Digite um número: "))
if eh_par(numero):
    print(f"{numero} é par.")
else:
    print(f"{numero} é ímpar.")


#Caucular área de retângulo
def calcular_area_retangulo(base, altura):
    return base * altura

base = float(input("Digite a base do retângulo: "))
altura = float(input("Digite a altura do retângulo: "))
area = calcular_area_retangulo(base, altura)
print(f"A área do retângulo é {area}")




    