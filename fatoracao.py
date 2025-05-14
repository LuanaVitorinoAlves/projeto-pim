# Fatoração de um número inteiro positivo
numero = int(input ("Digite um número inteiro positivo: "))

fatorial = 1
# Verifica se o número é negativo
if numero < 0:
    print ("digite apenas números positivos")
    fatorial = 1

# Fatoração de um número inteiro positivo
for i in range(1, numero + 1):
    fatorial = fatorial * i
print (fatorial)
