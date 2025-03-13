#!/bin/bash

# Adicionando o agente
eval "$(ssh-agent -s)" && ssh-add ~/.ssh/tperons_rsa

# Adicionando os requirements
pip freeze > requirements.txt

# Solicita uma mensagem de commit
echo "Digite a mensagem do commit:"
read commit_message

# Adiciona todas as alterações ao stage
git add .

# Faz o commit com a mensagem digitada
git commit -m "$commit_message"

# Envia para o repositório remoto
git push -u origin main

echo "Push realizado com sucesso"