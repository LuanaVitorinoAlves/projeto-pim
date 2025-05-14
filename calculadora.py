import streamlit as st

st.title("Calculadora Simples")
op1 = st.number_input("Operando 1:", value=0.0)
op2= st.number_input("Operando 2:", value=0.0)

def calcular(op, a, b):
    if op == '+':
        return a+b
    if op == "-":
        return a-b
    if op == '*':
        return a*b
    if op == '/':
        return a/b
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("\+"):
            resultado = calcular('+', op1, op2)
            st.sucess(f"Resultado: {resultado}")

    with col2:
        if st.button("\-"):
            resultado = calcular('-', op1, op2)
            st.sucess(f"Resultado: {resultado}")

    with col3:
        if st.button("\*"):
            resultado = calcular('*', op1, op2)
            st.sucess(f"Resultado: {resultado}")

    with col4:
        if st.button("/"):
            resultado = calcular('/', op1, op2)
            st.sucess(f"Resultado: {resultado}")
