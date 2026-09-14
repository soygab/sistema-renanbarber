# RenanBarber

Sistema de gestão e agendamento para barbearia, construído com Django e SQLite.

## Executar localmente

No PowerShell, a partir da raiz do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src\backend\manage.py migrate
.\.venv\Scripts\python.exe src\backend\manage.py createsuperuser
.\.venv\Scripts\python.exe src\backend\manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. O superusuário é criado como barbeiro e pode cadastrar os demais profissionais e serviços. Clientes criam suas contas na aba **Cadastrar**.

## Fluxos disponíveis

- autenticação real por e-mail e senha;
- separação e proteção das áreas de cliente e barbeiro;
- cadastro e ativação/desativação de barbeiros;
- cadastro, edição e remoção lógica de serviços;
- escolha de serviço, barbeiro, data e horário pelo cliente;
- detecção de conflitos, disponibilidade e períodos bloqueados;
- remarcação, cancelamento e conclusão de atendimentos;
- indicadores financeiros, comissões e desempenho por profissional.

## Testes

```powershell
.\.venv\Scripts\python.exe src\backend\manage.py test apps.usuarios apps.barbeiros apps.servicos apps.agendamentos
```

Configurações de produção devem definir `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0` e `DJANGO_ALLOWED_HOSTS`.
