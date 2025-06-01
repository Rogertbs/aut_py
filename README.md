# 📤 Sistema de Envio de Mensagens - Active Unify Talk

Este projeto é uma plataforma web desenvolvida em **Python (Django)** para criação e gerenciamento de campanhas de envio de mensagens personalizadas via **WhatsApp**, com suporte a múltiplas instâncias, importação de leads e controle de tempo de envio (time frame).

---

## 🚀 Funcionalidades Principais

- ✅ Cadastro e edição de campanhas
- 📅 Definição de janelas de envio (dias e horários permitidos)
- 📥 Importação de leads por CSV
- 💬 Criação de mensagens personalizadas por campanha
- 🔁 Envio programado e envio em massa
- 📊 Relatórios e dashboards de campanhas
- 🔄 Suporte a múltiplas instâncias conectadas via QR Code (WhatsApp Web)
- 🛡️ Controle de ativação/desativação de campanhas

---

## 🧰 Tecnologias Utilizadas

- **Back-end:** Python 3.9, Django 4.2
- **Front-end:** Bootstrap 5.3 + HTML5
- **Banco de Dados:** PostgreSQL ou SQLite (desenvolvimento)
- **Outros:** jQuery, AJAX, Docker (opcional)

---

## 📦 Instalação

### 1. Clone o repositório:

git clone https://github.com/seuusuario/seu-repo.git
cd seu-repo

2. Crie o ambiente virtual e ative:

python3 -m venv venv
source venv/bin/activate

3. Instale as dependências:

pip install -r requirements.txt

4. Aplique as migrações:

python manage.py migrate

5. Crie o superusuário:

python manage.py createsuperuser

6. Rode o servidor:

python manage.py runserver

🖼️ Screenshots
Lista de Campanhas	Edição de Campanha

🔐 Autenticação
O sistema possui autenticação embutida (login/logout). O painel só é acessível por usuários autenticados.

📁 Estrutura
csharp
Copiar
Editar
├── activeut/              # Aplicação principal
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   └── views.py
├── manage.py
└── requirements.txt
📄 Licença
Este projeto é distribuído sob a licença MIT. Sinta-se à vontade para usá-lo, melhorar ou contribuir.

🤝 Contribuições
Pull requests são bem-vindos! Para mudanças maiores, abra uma issue primeiro para discutir o que você gostaria de modificar.
