# RenanBarber — Sistema de Gestão e Agendamentos

![RenanBarber](public/image/logo_renanbarber.svg)

> Gestão de barbeiros, serviços, horários e agendamentos em uma única plataforma.

## Sobre o projeto

O **RenanBarber** é um sistema web desenvolvido para organizar a operação de uma barbearia e facilitar a experiência dos clientes. A plataforma reúne autenticação, agendamentos, gerenciamento de profissionais, disponibilidade de horários, serviços e acompanhamento financeiro em uma interface responsiva inspirada na identidade visual da marca.

A aplicação possui áreas distintas para clientes e barbeiros. O cliente pode criar sua conta, conhecer os serviços, escolher o profissional de sua preferência e reservar um horário disponível. Já a equipe acompanha a agenda diária, administra serviços e profissionais, bloqueia períodos e consulta indicadores de faturamento e desempenho.

## Objetivo

O projeto foi estruturado para centralizar tarefas que normalmente ficam espalhadas entre mensagens, agendas pessoais e controles manuais. O sistema conduz cada usuário para a área adequada após o login e oferece recursos específicos para seu perfil:

- Cadastro e autenticação segura por e-mail e senha;
- Separação entre as áreas de cliente e barbeiro;
- Catálogo de serviços com preço, descrição e duração;
- Escolha do barbeiro durante o agendamento;
- Consulta de horários disponíveis conforme a agenda do profissional;
- Prevenção de conflitos e reservas duplicadas;
- Controle de expediente e períodos bloqueados;
- Acompanhamento financeiro e desempenho da equipe;
- Interface adaptada para computadores, tablets e celulares.

## Funcionalidades

### Autenticação e perfis

O acesso utiliza o sistema de autenticação do Django. Clientes podem criar uma conta diretamente pela tela inicial, enquanto barbeiros são cadastrados por usuários autorizados no painel da equipe.

Após a autenticação, cada usuário é encaminhado automaticamente para sua área. As rotas internas também verificam o perfil no servidor, impedindo que clientes acessem ferramentas administrativas.

### Área do cliente

A página inicial apresenta o próximo atendimento e o histórico recente. O cliente também pode consultar o catálogo, acompanhar todos os seus agendamentos, remarcar ou cancelar horários e avaliar atendimentos concluídos.

### Agendamentos e escolha do barbeiro

Durante o agendamento, o cliente escolhe o serviço, o barbeiro, a data e o horário. A disponibilidade é consultada dinamicamente e considera:

- Expediente semanal do profissional;
- Duração do serviço escolhido;
- Agendamentos já confirmados;
- Períodos bloqueados pelo barbeiro;
- Horários passados ou fora do funcionamento.

As mesmas regras são validadas novamente pelo backend antes da confirmação, evitando conflitos mesmo quando dois usuários tentam reservar horários próximos.

### Gestão de barbeiros

O painel permite adicionar profissionais com nome, e-mail, telefone, senha inicial e percentual de comissão. Cada novo barbeiro recebe uma configuração semanal padrão, que pode ser personalizada posteriormente.

Também é possível ativar ou desativar o acesso de um profissional sem apagar seu histórico de atendimentos.

### Serviços

Barbeiros podem cadastrar, editar e remover serviços do catálogo. Cada serviço possui nome, descrição, preço, duração e status. A remoção é lógica: o serviço deixa de aparecer para novos agendamentos, mas permanece associado aos registros anteriores.

### Agenda e disponibilidade

A equipe pode filtrar os atendimentos por data e profissional, remarcar ou cancelar reservas e marcar um serviço como concluído. Na área de horários, cada barbeiro possui expediente próprio para os dias da semana e pode adicionar bloqueios específicos para compromissos, pausas ou ausências.

### Financeiro e desempenho

O painel administrativo calcula os indicadores diretamente a partir dos atendimentos concluídos. Ele apresenta faturamento, ganhos do dia, comissões, quantidade de horários pendentes, avaliações e desempenho individual de cada profissional.

Os dados podem ser filtrados por período e barbeiro, facilitando o acompanhamento da operação e da produtividade da equipe.

## Tecnologias utilizadas

- **Python** como linguagem principal do backend;
- **Django** para autenticação, rotas, formulários, regras de negócio e administração;
- **SQLite** como banco de dados padrão para desenvolvimento;
- **Django Templates** para integração entre interface e dados do servidor;
- **HTML5** para a estrutura semântica das páginas;
- **CSS3** para identidade visual, responsividade e componentes;
- **JavaScript puro** para abas, navegação mobile e consulta dinâmica de horários;
- **Google Fonts** para a família tipográfica Montserrat.

## Estrutura do repositório

```text
.
├── public/
│   ├── image/                         # Logo e ícones da interface
│   └── styles/
│       ├── pages/                     # Estilos das áreas e da autenticação
│       └── style.css                  # Arquivo central de estilos
├── src/
│   ├── backend/
│   │   ├── apps/
│   │   │   ├── agendamentos/          # Reservas, conflitos e avaliações
│   │   │   ├── barbeiros/             # Equipe, expedientes e bloqueios
│   │   │   ├── dashboard/             # Indicadores das duas áreas
│   │   │   ├── servicos/              # Catálogo e gerenciamento de serviços
│   │   │   └── usuarios/              # Usuários, autenticação e permissões
│   │   ├── config/config/              # Configurações e URLs principais
│   │   └── manage.py                   # Utilitário de administração Django
│   └── frontend/
│       ├── pages/                      # Templates das telas do sistema
│       └── scripts/                    # Interações da interface
├── requirements.txt                   # Dependências Python
└── README.md
```

## Próximas evoluções

- Integração com pagamentos online e confirmação de transações;
- Notificações de agendamento por WhatsApp e e-mail;
- Recuperação de senha por e-mail;
- Relatórios financeiros exportáveis;
- Cadastro de fotos e portfólio de cada barbeiro;
- Cupons, planos recorrentes e programa de fidelidade;
- Migração do banco de produção para PostgreSQL;
- Implantação com domínio próprio e monitoramento.

---

Desenvolvido para a **RenanBarber**. 💈
