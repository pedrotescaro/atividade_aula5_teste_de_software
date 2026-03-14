@echo off
chcp 65001
setlocal

:: Define o diretório do ambiente virtual
set "VENV_DIR=venv"
set "REQUIREMENTS_FILE=requirements.txt"

:: Alterar a política de execução do PowerShell para permitir scripts (apenas se necessário)
echo Alterando a política de execução do PowerShell para 'RemoteSigned'...
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force" >nul 2>&1
if %errorlevel% neq 0 (
    echo Falha ao alterar a política de execução do PowerShell. Continuando sem alterar.
) else (
    echo Política de execução alterada para 'RemoteSigned'.
)

:: Verifica se o ambiente virtual já existe
if not exist "%VENV_DIR%" (
    echo Criando ambiente virtual...
    python -m venv "%VENV_DIR%"
) else (
    echo Limpando ambiente virtual antigo...
    rmdir /S /Q "%VENV_DIR%"
    echo Ambiente virtual antigo removido.
    echo Criando novo ambiente virtual...
    python -m venv "%VENV_DIR%"
)

:: Verifica se o script de ativação existe
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Erro: O arquivo de ativação do ambiente virtual não foi encontrado!
    exit /b 1
)

:: Ativa o ambiente virtual
echo Ativando ambiente virtual...
call "%VENV_DIR%\Scripts\activate.bat"

:: Instala pacotes do requirements.txt, se existir
if exist "%REQUIREMENTS_FILE%" (
    echo Instalando pacotes do %REQUIREMENTS_FILE%...
    pip install -r "%REQUIREMENTS_FILE%"
) else (
    echo %REQUIREMENTS_FILE% não encontrado, pulando a instalação de dependências.
)

:: Verifica se o arquivo test_soma_interface.py existe e executa
if exist "test_soma_interface.py" (
    echo Iniciando test_soma_interface.py...
    python test_soma_interface.py

) else (
    echo Erro: printer.py não encontrado!
)

echo Ambiente virtual pronto!

:: Mantém a janela aberta após a execução
cmd /k
