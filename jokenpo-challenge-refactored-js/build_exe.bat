@echo off
REM Roda este script no Windows, dentro da pasta do projeto,
REM com o ambiente virtual ja ativado e as dependencias instaladas
REM (pip install -r requirements.txt)

python -m PyInstaller --onefile --windowed --name JokenpoChallenge --add-data "data;data" main.py

echo.
echo Pronto! O executavel esta em dist\JokenpoChallenge.exe
echo Copie a pasta "dist" inteira (ou so o .exe, que ja embute tudo)
echo e mande para seus amigos. Nao precisa instalar Python nem pygame.
pause
