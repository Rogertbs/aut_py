#!/bin/bash
set -e

echo "⏳ Aguardando banco de dados em $DB_HOST..."
#until nc -z "$DB_HOST" 3306; do
#  sleep 1
#done
echo "✅ Banco disponível, iniciando Django..."

echo "🚀 Aplicando migrações..."
python3 manage.py migrate

echo "👤 Criando superusuário Django..."
python3 manage.py createsuperuser --noinput \
  --username "$DJANGO_SUPERUSER_USERNAME" \
  --email "$DJANGO_SUPERUSER_EMAIL" || true

echo "🔑 Definindo senha para o superusuário..."
python3 manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(username='${DJANGO_SUPERUSER_USERNAME}')
u.set_password('${DJANGO_SUPERUSER_PASSWORD}')
u.save()
print("✔ Superusuário atualizado com senha.")
END

echo "🎯 Iniciando servidor Django..."
python3 manage.py runserver 0.0.0.0:$DJANGO_PORT

