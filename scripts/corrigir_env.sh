#!/bin/bash
# Script para corrigir arquivo .env com senha que contém caracteres especiais

echo "============================================================"
echo "  CORRIGIR ARQUIVO .env - Senha com caracteres especiais"
echo "============================================================"
echo ""

if [ ! -f ".env" ]; then
    echo "ERRO: Arquivo .env não encontrado!"
    exit 1
fi

echo "Arquivo .env atual:"
grep DATABASE_URL_PERSONAL .env
echo ""

read -p "Digite a senha do banco de dados (será codificada automaticamente): " -s DB_PASSWORD
echo ""

# Função para codificar senha para URL
url_encode() {
    local string="${1}"
    local strlen=${#string}
    local encoded=""
    local pos c o

    for (( pos=0 ; pos<strlen ; pos++ )); do
        c=${string:$pos:1}
        case "$c" in
            [-_.~a-zA-Z0-9] ) o="${c}" ;;
            * ) printf -v o '%%%02x' "'$c" ;;
        esac
        encoded+="${o}"
    done
    echo "${encoded}"
}

# Codificar senha
DB_PASSWORD_ENCODED=$(url_encode "$DB_PASSWORD")

echo ""
echo "Senha original: $DB_PASSWORD"
echo "Senha codificada: $DB_PASSWORD_ENCODED"
echo ""

# Atualizar .env
sed -i "s|postgresql://personal_agent_user:[^@]*@localhost|postgresql://personal_agent_user:$DB_PASSWORD_ENCODED@localhost|g" .env

echo "Arquivo .env atualizado!"
echo ""
echo "Nova URL:"
grep DATABASE_URL_PERSONAL .env
echo ""
echo "Teste a conexão com: python3 scripts/test_connection.py"
