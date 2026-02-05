# 🧠 Brain - Módulos de Inteligência da Kuma

Este diretório contém os módulos que compõem a "inteligência" da Kuma.

## Módulos

### `fear.py` - Sistema de Medos
Define os medos da Kuma e verifica se uma mensagem contém algo assustador.

**Medos padrão**: aspirador, fogos, banho, veterinário

### `learning.py` - Sistema de Aprendizado
Aprende palavras automaticamente das conversas (palavras com 4+ caracteres).

**Funções**:
- `learn(word)`: Adiciona uma palavra ao vocabulário
- `random_learned()`: Retorna uma palavra aleatória aprendida

### `memory.py` - Sistema de Memória
Lembra a última palavra dita por cada usuário, com sistema de cooldown.

**Funções**:
- `remember(user, msg)`: Salva a última palavra do usuário
- `recall_user(user)`: Recupera a lembrança do usuário
- `can_recall(user)`: Verifica se pode usar lembrança (cooldown de 60s)

### `moderator.py` - Modo Moderador
Sistema temporário de moderação que permite deletar mensagens.

**Funções**:
- `activate_mod(seconds)`: Ativa modo moderador por X segundos
- `is_mod()`: Verifica se o modo está ativo

### `moods.py` - Sistema de Humor
Define o humor da Kuma baseado na hora do dia.

**Humores**:
- **Cansada** (0h-6h): Adiciona "..." nas respostas
- **Hiper** (7h-12h, 19h-23h): Adiciona "!!!" nas respostas
- **Normal** (13h-18h): Respostas normais

### `offended.py` - Sistema de Ofensa
Controla quando a Kuma está ofendida e não quer conversar.

**Funções**:
- `offend(seconds)`: Define que está ofendida por X segundos
- `is_offended()`: Verifica se está ofendida

### `persistence.py` - Persistência de Dados
Salva e carrega dados do bot em arquivo JSON.

**Funções**:
- `save_data(data)`: Salva dados em arquivo
- `load_data()`: Carrega dados do arquivo
- `export_state()`: Exporta estado atual do bot
- `import_state(data)`: Importa estado para o bot

### `responses.py` - Respostas e Frases
Contém todas as listas de respostas e frases da Kuma.

**Categorias**:
- Instintos (comida, passeio, gato, bola)
- Respostas genéricas (não sei, brainrot, erradas)
- Emojis e latidos
- Lembranças (certas e erradas)

### `rules.py` - Regras de Processamento
Funções auxiliares para processamento de mensagens.

**Funções**:
- `contains(msg, palavras)`: Verifica se mensagem contém alguma palavra da lista

## Arquitetura

Todos os módulos são **stateful** e mantêm estado em memória. O módulo `persistence.py` é responsável por salvar e carregar esse estado entre execuções do bot.

## Extensibilidade

Para adicionar novas funcionalidades:

1. Crie um novo arquivo `.py` no diretório `brain/`
2. Implemente as funções necessárias com type hints
3. Importe no `bot.py`
4. Se precisar persistência, adicione em `persistence.py`
