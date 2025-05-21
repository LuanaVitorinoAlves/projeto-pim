@echo off
echo Criando ambiente python...
python -m venv venv
echo Criado com sucesso
echo Ativando ambiente python...
call venv\Scripts\activate
echo Ativado com sucesso
echo Instalando bibliotecas...
python -m pip install -r requirements.txt
echo Configurado com sucesso!
pause
