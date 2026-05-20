"""
Camada de Dados - Gerenciamento de conexão com banco de dados.

Responsabilidades:
- Gerenciar conexão com o banco de dados
- Implementar singleton de conexão
- Criar estrutura do banco (tabelas)
- Fornecer conexão para o repositório

NÃO deve conter:
- Lógica de negócio
- Operações CRUD específicas
- Regras de domínio
- Lógica de apresentação
"""

import sqlite3
from typing import Optional


# Variável global para armazenar a conexão (Singleton)
_conexao: Optional[sqlite3.Connection] = None


def obter_conexao() -> sqlite3.Connection:
    """
    Obtém a conexão com o banco de dados (Singleton).
    
    Implementa o padrão Singleton para garantir uma única conexão
    durante o ciclo de vida da aplicação.
    
    Returns:
        sqlite3.Connection: Conexão ativa com o banco
    """
    global _conexao
    
    if _conexao is None:
        # Criar nova conexão
        _conexao = sqlite3.connect(
            'layered_project.db',
            check_same_thread=False  # Permitir uso em múltiplas threads
        )
        
        # Configurar conexão
        _conexao.row_factory = sqlite3.Row  # Acesso por nome de coluna
        
        print("Conexão com banco de dados estabelecida")
    
    return _conexao


def fechar_conexao() -> None:
    """
    Fecha a conexão com o banco de dados.
    
    Deve ser chamado ao encerrar a aplicação.
    """
    global _conexao
    
    if _conexao is not None:
        _conexao.close()
        _conexao = None
        print("Conexão com banco de dados fechada")


def inicializar_banco() -> None:
    """
    Inicializa o banco de dados criando as tabelas necessárias.
    
    Cria a tabela 'usuarios' se ela não existir.
    Esta função deve ser chamada na inicialização da aplicação.
    """
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        # Criar tabela de usuários
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                telefone TEXT,
                ativo INTEGER NOT NULL DEFAULT 1,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        
        # Criar índice no email para buscas rápidas
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_usuarios_email
            ON usuarios(email)
            """
        )
        
        # Criar índice no status ativo
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_usuarios_ativo
            ON usuarios(ativo)
            """
        )
        
        conexao.commit()
        print("Banco de dados inicializado com sucesso")
        
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {str(e)}")
        raise
    finally:
        cursor.close()


def limpar_banco() -> None:
    """
    Limpa todos os dados do banco (útil para testes).
    
    ATENÇÃO: Esta operação é irreversível!
    """
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("DELETE FROM usuarios")
        conexao.commit()
        print("Banco de dados limpo")
        
    except Exception as e:
        print(f"Erro ao limpar banco de dados: {str(e)}")
        raise
    finally:
        cursor.close()


def resetar_banco() -> None:
    """
    Reseta o banco de dados (drop e recria tabelas).
    
    ATENÇÃO: Esta operação é irreversível!
    Útil para desenvolvimento e testes.
    """
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        # Dropar tabela existente
        cursor.execute("DROP TABLE IF EXISTS usuarios")
        
        conexao.commit()
        print("Tabelas removidas")
        
        # Recriar estrutura
        inicializar_banco()
        
    except Exception as e:
        print(f"Erro ao resetar banco de dados: {str(e)}")
        raise
    finally:
        cursor.close()


def obter_estatisticas_banco() -> dict:
    """
    Obtém estatísticas sobre o banco de dados.
    
    Returns:
        dict: Dicionário com estatísticas
    """
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    try:
        # Contar total de usuários
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        # Contar usuários ativos
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE ativo = 1")
        usuarios_ativos = cursor.fetchone()[0]
        
        # Contar usuários inativos
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE ativo = 0")
        usuarios_inativos = cursor.fetchone()[0]
        return {
            "total_usuarios": total_usuarios,
            "usuarios_ativos": usuarios_ativos,
            "usuarios_inativos": usuarios_inativos
        }
        
    finally:
        cursor.close()