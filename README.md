# 📤 Sistema de Envio de Mensagens - Rocket Send

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


### Interface do Sistema
### Tela Login
![WhatsApp Image 2025-11-06 at 20 54 44](https://github.com/user-attachments/assets/36da265b-d55f-41d8-af9f-f4f04be95af6)
:

### Listagem de Campanhas
![WhatsApp Image 2025-11-06 at 20 55 46](https://github.com/user-attachments/assets/72a51686-369e-4c0b-bff0-dfc828d07cc3)

### Criar Campanha
![WhatsApp Image 2025-11-06 at 20 55 49](https://github.com/user-attachments/assets/5975505f-785a-4ae2-a48a-abe229b6bf23)

### Mensagens

![WhatsApp Image 2025-11-06 at 20 56 05](https://github.com/user-attachments/assets/247bac37-3ad2-4af1-8a2a-2800251fc87a)

### Editar ou Criar Mensagens

![WhatsApp Image 2025-11-06 at 20 56 40](https://github.com/user-attachments/assets/a6eccb69-e23a-4afe-bc21-4e3e92d5d252)

### Listagem de Leads
![WhatsApp Image 2025-11-06 at 20 57 06](https://github.com/user-attachments/assets/e8a365eb-0495-4a0c-973f-82363f1c558c)

### Cadastro de Leads por CSV
![WhatsApp Image 2025-11-06 at 20 57 24](https://github.com/user-attachments/assets/671cf517-1142-4d9d-bba7-734de29834ab)

### Dashboard em Realtime
![WhatsApp Image 2025-11-06 at 20 57 40](https://github.com/user-attachments/assets/3cc8ffc7-1174-436f-b220-b36cee2bd016)

### Relatório de campanha com gráfico e download de csv.

![WhatsApp Image 2025-11-06 at 20 58 07](https://github.com/user-attachments/assets/2486d4ad-a09d-41d0-a254-6897c1ad3592)
