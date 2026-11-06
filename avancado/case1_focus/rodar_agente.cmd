@echo off
REM Case 1 - Termometro do Focus
REM Wrapper usado pela tarefa agendada do Windows ("Termometro do Focus").
REM Roda o agente semanal e acumula a saida em saida\agente.log.
REM Para rodar a mao, e so dar duplo clique neste arquivo.

set "PASTA=%~dp0"
set "LOG=%PASTA%saida\agente.log"
set "PYTHON=C:\Users\leost\AppData\Local\Programs\Python\Python312\python.exe"

REM A etapa 4 chama "claude" pelo PATH. Garantimos a pasta aqui para a tarefa
REM agendada nao depender do PATH do ambiente que a disparou.
set "PATH=%USERPROFILE%\.local\bin;%PATH%"

if not exist "%PASTA%saida" mkdir "%PASTA%saida"

echo. >> "%LOG%"
echo ================================================== >> "%LOG%"
echo Execucao iniciada em %DATE% %TIME% >> "%LOG%"
echo ================================================== >> "%LOG%"

"%PYTHON%" "%PASTA%agente_semanal.py" >> "%LOG%" 2>&1
set CODIGO=%ERRORLEVEL%

echo. >> "%LOG%"
echo Terminou em %DATE% %TIME% com codigo %CODIGO% >> "%LOG%"

exit /b %CODIGO%
