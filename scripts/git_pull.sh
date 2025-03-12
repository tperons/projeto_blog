#!/bin/bash

# Adicionando o agente
eval "$(ssh-agent -s)" && ssh-add ~/.ssh/tperons_rsa

# Puxa as atualizações do repositório remoto
git pull origin main

echo "Pull realizado com sucesso"

# Verifica se a venv está ativada
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Virtual environment não está ativa. Ativando..."
    source ~/python/projeto_blog/venv/bin/activate
else
    echo "Virtual environment já está ativa."
fi

# Instalando os requirements
pip install -r requirements.txt

# Fazendo as migrações
python manage.py makemigrations
python manage.py migrate