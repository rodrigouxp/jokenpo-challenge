#!/bin/bash
# Roda este script no macOS ou Linux, dentro da pasta do projeto,
# com o ambiente virtual ja ativado e as dependencias instaladas
# (pip install -r requirements.txt)

pyinstaller --onefile --windowed --name JokenpoChallenge --add-data "data:data" main.py

echo ""
echo "Pronto! O executavel esta em dist/JokenpoChallenge"
echo "Copie o arquivo e mande para seus amigos (mesmo sistema operacional)."
echo "Nao precisa instalar Python nem pygame."
