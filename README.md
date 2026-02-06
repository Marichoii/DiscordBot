# 🐕 Bot da Kuma

Bot do Discord da Kuma, uma Spitz Alemã caótica e divertida! Este bot simula a personalidade de uma cachorra com humor baseado no horário, sistema de memória, aprendizado de palavras e muito mais.

## ✨ Funcionalidades

### 🧠 Inteligência Artificial Canina
- **Sistema de Aprendizado**: A Kuma aprende palavras automaticamente das conversas
- **Memória de Usuários**: Lembra a última palavra que cada usuário disse
- **Humor Dinâmico**: Muda de humor baseado na hora do dia (cansada, hiper, normal)
- **Persistência de Dados**: Salva automaticamente memórias e palavras aprendidas

### 😱 Sistema de Emoções
- **Medos**: Reage com medo a aspirador, fogos, banho e veterinário
- **Sistema de Ofensa**: Fica ofendida quando é xingada e para de responder
- **Modo Moderador**: Pode ativar modo moderador temporário para deletar mensagens

### 🎲 Comportamentos Aleatórios
- Surtos de latidos aleatórios
- Respostas confusas e engraçadas
- Reações especiais a menções
- Instintos caninos (comida, passeio, gatos, bola)

## 📋 Comandos

| Comando | Descrição |
|---------|-----------|
| `/kuma` | Invoca a Kuma |
| `/humor` | Mostra o humor atual da Kuma |
| `/petisco` | Dá um petisco para a Kuma |
| `/carinho` | Faz carinho na Kuma |
| `/passear` | Convida a Kuma para passear |
| `/truque` | Pede para a Kuma fazer um truque |
| `/medos` | Lista os medos da Kuma |
| `/vocabulario` | Mostra quantas palavras a Kuma aprendeu |
| `/latir` | Faz a Kuma latir |
| `/status` | Mostra o status completo da Kuma |
| `/desculpa` | Pede desculpas para a Kuma |
| `/salvar` | Salva manualmente os dados da Kuma |
| `/ajuda` | Lista todos os comandos |

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Conta no Discord
- Bot criado no [Discord Developer Portal](https://discord.com/developers/applications)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/Marichoii/DiscordBot.git
cd DiscordBot
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure o token do bot**

Crie um arquivo `.env` na raiz do projeto:
```env
DISCORD_TOKEN=seu_token_aqui
```

Para obter o token:
- Acesse o [Discord Developer Portal](https://discord.com/developers/applications)
- Selecione seu bot
- Vá em "Bot" no menu lateral
- Clique em "Reset Token" e copie o token
- Cole no arquivo `.env`

4. **Configure as permissões do bot**

No Discord Developer Portal, em "OAuth2 > URL Generator":
- **Scopes**: `bot`, `applications.commands`
- **Bot Permissions**:
  - Read Messages/View Channels
  - Send Messages
  - Manage Messages (para deletar mensagens no modo moderador)
  - Use Slash Commands

5. **Execute o bot**
```bash
python bot.py
```

## 🏗️ Estrutura do Projeto

```
DiscordBot/
├── bot.py                 # Arquivo principal do bot
├── brain/                 # Módulos de inteligência
│   ├── __init__.py
│   ├── fear.py           # Sistema de medos
│   ├── learning.py       # Sistema de aprendizado
│   ├── memory.py         # Sistema de memória
│   ├── moderator.py      # Modo moderador
│   ├── moods.py          # Sistema de humor
│   ├── offended.py       # Sistema de ofensa
│   ├── persistence.py    # Persistência de dados
│   ├── responses.py      # Respostas e frases
│   └── rules.py          # Regras de processamento
├── requirements.txt       # Dependências Python
├── .env                   # Configurações (não versionado)
├── .gitignore            # Arquivos ignorados pelo Git
├── kuma.log              # Log do bot (gerado automaticamente)
└── kuma_data.json        # Dados salvos (gerado automaticamente)
```

## 🔧 Configuração Avançada

### Sistema de Logging
O bot gera logs em dois lugares:
- **Console**: Saída padrão para monitoramento em tempo real
- **Arquivo**: `kuma.log` para histórico completo

### Salvamento Automático
Os dados são salvos automaticamente a cada 5 minutos e também:
- Quando o bot é encerrado normalmente
- Manualmente com o comando `/salvar`

### Variáveis de Ambiente (opcional)
Você pode ajustar comportamentos no `.env`:
- `BOT_PREFIX` (padrão `!`)
- `AUTOSAVE_MINUTES` (padrão `5`)
- `MOD_DURATION_SECONDS` (padrão `10`)
- `OFFENDED_DURATION_SECONDS` (padrão `45`)
- `RESPOND_TO_BOTS_CHANCE` (padrão `0.3`)
- `BARK_BURST_CHANCE` (padrão `0.01`)
- `BRAINROT_CHANCE` (padrão `0.02`)
- `KUMA_WRONG_CHANCE` (padrão `0.2`)
- `KUMA_EMOJI_CHANCE` (padrão `0.3`)
- `KUMA_RECALL_WRONG_CHANCE` (padrão `0.3`)
- `KUMA_LEARNED_CHANCE` (padrão `0.1`)
- `MSG_USER_COOLDOWN` (padrão `1.5`)
- `MSG_CHANNEL_COOLDOWN` (padrão `0.4`)
- `SLASH_USER_COOLDOWN` (padrão `2.0`)

### Personalização

Você pode personalizar as respostas editando os arquivos em `brain/`:
- `responses.py`: Frases e respostas
- `fear.py`: Lista de medos
- `moods.py`: Comportamento baseado em humor
- `learning.py`: Critérios de aprendizado

## 🐛 Solução de Problemas

### Bot não inicia
- Verifique se o token está correto no `.env`
- Confirme que as dependências estão instaladas: `pip install -r requirements.txt`

### Comandos não aparecem
- Aguarde alguns minutos após iniciar o bot (sincronização com Discord)
- Verifique se o bot tem permissão `applications.commands`

### Bot não deleta mensagens
- Verifique se o bot tem permissão "Manage Messages"
- O bot precisa ter cargo superior ao usuário que postou a mensagem

### Dados não são salvos
- Verifique permissões de escrita na pasta do bot
- Confira o arquivo `kuma.log` para erros

## 📝 Licença

Este projeto é de código aberto. Sinta-se livre para usar, modificar e distribuir.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 👥 Créditos

Bot criado com ❤️ para a Kuma, a Spitz Alemã mais caótica do Discord!

---

**Nota**: Este bot foi criado para fins de entretenimento e aprendizado. Certifique-se de seguir os [Termos de Serviço do Discord](https://discord.com/terms) ao usar bots.

