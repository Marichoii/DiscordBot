import json
import os
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

DATA_FILE = "kuma_data.json"

def save_data(data: Dict[str, Any]) -> None:
    """Salva dados em arquivo JSON."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info("Dados salvos com sucesso")
    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")

def load_data() -> Dict[str, Any]:
    """Carrega dados do arquivo JSON."""
    if not os.path.exists(DATA_FILE):
        logger.info("Arquivo de dados não encontrado, criando novo")
        return {}
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info("Dados carregados com sucesso")
        return data
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}")
        return {}

def export_state() -> Dict[str, Any]:
    """Exporta o estado atual do bot para um dicionário."""
    from kuma.features.learning import learned_words
    from kuma.features.memory import user_memory
    
    return {
        "learned_words": list(learned_words),
        "user_memory": {str(k): v for k, v in user_memory.items()}
    }

def import_state(data: Dict[str, Any]) -> None:
    """Importa o estado do bot de um dicionário."""
    from kuma.features.learning import learned_words
    from kuma.features.memory import user_memory
    
    if "learned_words" in data:
        learned_words.clear()
        learned_words.update(data["learned_words"])
        logger.info(f"Carregadas {len(learned_words)} palavras aprendidas")
    
    if "user_memory" in data:
        user_memory.clear()
        user_memory.update({int(k): v for k, v in data["user_memory"].items()})
        logger.info(f"Carregadas memórias de {len(user_memory)} usuários")

