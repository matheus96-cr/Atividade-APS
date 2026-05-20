"""
Camada de Domínio - Entidade Usuario e regras de negócio puras.

Responsabilidades:
- Definir a estrutura da entidade Usuario
- Implementar validações de domínio
- Encapsular comportamentos da entidade
- Garantir invariantes do domínio

NÃO deve conter:
- Dependências de outras camadas
- Código de infraestrutura (banco de dados, APIs)
- Lógica de apresentação
- Detalhes de persistência
"""

import re
from dataclasses import dataclass
from typing import Optional


class UsuarioInvalidoError(Exception):
    """Exceção lançada quando dados do usuário são inválidos."""
    pass


@dataclass
class Usuario:
    """
    Entidade de domínio representando um usuário do sistema.
    
    Invariantes (regras que sempre devem ser verdadeiras):
    - Nome não pode ser vazio e deve ter entre 2 e 100 caracteres
    - Email deve ser válido e único no sistema
    - ID é gerado pelo banco de dados (None antes de persistir)
    - Usuário é criado como ativo por padrão
    """
    
    nome: str
    email: str
    id: Optional[int] = None
    ativo: bool = True
    telefone: Optional[str] = None
    
    def __post_init__(self):
        """
        Valida os dados após inicialização.
        Garante que invariantes sejam respeitadas.
        """
        self._validar_nome(self.nome)
        self._validar_email(self.email)
        if self.telefone is not None:
            self._validar_telefone(self.telefone)

    @staticmethod
    def _validar_nome(nome: str) -> None:
        """
        Valida o nome do usuário.
        
        Regras:
        - Não pode ser vazio ou apenas espaços
        - Deve ter entre 2 e 100 caracteres
        
        Args:
            nome: Nome a ser validado
        
        Raises:
            UsuarioInvalidoError: Se nome é inválido
        """
        if not nome or not nome.strip():
            raise UsuarioInvalidoError("Nome não pode ser vazio")
        
        nome_limpo = nome.strip()
        
        if len(nome_limpo) < 2:
            raise UsuarioInvalidoError("Nome deve ter pelo menos 2 caracteres")
        
        if len(nome_limpo) > 100:
            raise UsuarioInvalidoError("Nome deve ter no máximo 100 caracteres")
    
    @staticmethod
    def _validar_email(email: str) -> None:
        """
        Valida o formato do email.
        
        Regras:
        - Não pode ser vazio
        - Deve ter formato válido (regex simples)
        - Deve ter no máximo 255 caracteres
        
        Args:
            email: Email a ser validado
        
        Raises:
            UsuarioInvalidoError: Se email é inválido
        """
        if not email or not email.strip():
            raise UsuarioInvalidoError("Email não pode ser vazio")
        
        email_limpo = email.strip().lower()
        
        if len(email_limpo) > 255:
            raise UsuarioInvalidoError("Email deve ter no máximo 255 caracteres")
        
        # Regex simples para validação de email
        padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(padrao_email, email_limpo):
            raise UsuarioInvalidoError("Formato de email inválido")
    
    @staticmethod
    def _validar_telefone(telefone: str) -> None:
        digitos = re.sub(r'\D', '', telefone)
        if len(digitos) not in (10, 11):
            raise UsuarioInvalidoError("Telefone deve ter 10 ou 11 dígitos")
    
    def atualizar_nome(self, novo_nome: str) -> None:
        """
        Atualiza o nome do usuário com validação.
        
        Args:
            novo_nome: Novo nome do usuário
        
        Raises:
            UsuarioInvalidoError: Se novo nome é inválido
        """
        self._validar_nome(novo_nome)
        self.nome = novo_nome.strip()
    
    def atualizar_email(self, novo_email: str) -> None:
        """
        Atualiza o email do usuário com validação.
        
        Args:
            novo_email: Novo email do usuário
        
        Raises:
            UsuarioInvalidoError: Se novo email é inválido
        """
        self._validar_email(novo_email)
        self.email = novo_email.strip().lower()
    
    def ativar(self) -> None:
        """Ativa o usuário."""
        self.ativo = True
    
    def desativar(self) -> None:
        """Desativa o usuário (soft delete)."""
        self.ativo = False
    
    def esta_ativo(self) -> bool:
        """
        Verifica se o usuário está ativo.
        
        Returns:
            bool: True se ativo, False caso contrário
        """
        return self.ativo
    
    def __str__(self) -> str:
        """Representação em string do usuário."""
        status = "ativo" if self.ativo else "inativo"
        return f"Usuario(id={self.id}, nome='{self.nome}', email='{self.email}', {status})"
    
    def __repr__(self) -> str:
        """Representação técnica do usuário."""
        return (f"Usuario(id={self.id}, nome='{self.nome}', "
                f"email='{self.email}', ativo={self.ativo})")
    
    def __eq__(self, other) -> bool:
        """
        Compara dois usuários por ID.
        Dois usuários são iguais se têm o mesmo ID.
        """
        if not isinstance(other, Usuario):
            return False
        return self.id is not None and self.id == other.id
    
    def __hash__(self) -> int:
        """Hash baseado no ID para uso em sets e dicts."""
        return hash(self.id) if self.id else hash((self.nome, self.email))