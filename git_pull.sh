#!/bin/bash

# Adicionando o agente
eval "$(ssh-agent -s)" && ssh-add ~/.ssh/tperons_rsa

# Puxa as atualizações do repositório remoto
git pull -u origin main

echo "Pull realizado com sucesso"