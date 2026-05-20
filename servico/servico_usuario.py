"""
Camada de Serviço - Lógica de negócio para gerenciamento de usuários.

Responsabilidades:
- Orquestrar operações de negócio
- Aplicar regras de negócio
- Validar dados de domínio
- Coordenar chamadas ao repositório

NÃO deve conter:
- Código de apresentação (rotas, HTTP)
- Acesso direto ao banco de dados
- Detalhes de infraestrutura
"""

from dominio.usuario import Usuario
from repositorio.repositorio_usuario import RepositorioUsuario


class ServicoUsuario:
    """
    Serviço responsável pela lógica de negócio de usuários.
    """
    
    def __init__(self):
        """Inicializa o serviço com suas dependências."""
        self.repositorio = RepositorioUsuario()
    
    def criar_usuario(self, nome: str, email: str, telefone: str = None) -> Usuario:
        """
        Cria um novo usuário aplicando regras de negócio.
        
        Regras de negócio:
        1. Email deve ser único no sistema
        2. Nome e email devem ser válidos (validado pela entidade)
        3. Usuário é criado como ativo por padrão
        
        Args:
            nome: Nome do usuário
            email: Email do usuário
        
        Returns:
            Usuario: Usuário criado com ID
        
        Raises:
            ValueError: Se email já existe
            UsuarioInvalidoError: Se dados são inválidos
        """
        # Regra de negócio: Email deve ser único
        usuario_existente = self.repositorio.buscar_por_email(email)
        if usuario_existente:
            raise ValueError(f"Email '{email}' já está cadastrado no sistema")
        
        # Criar entidade de domínio (valida dados automaticamente)
        usuario = Usuario(nome=nome, email=email, telefone=telefone)
        
        # Persistir no banco de dados
        usuario_salvo = self.repositorio.salvar(usuario)
        
        return usuario_salvo
    
    def obter_usuario_por_id(self, usuario_id: int) -> Usuario:
        """
        Obtém um usuário por ID.
        
        Args:
            usuario_id: ID do usuário
        
        Returns:
            Usuario: Usuário encontrado ou None
        """
        return self.repositorio.buscar_por_id(usuario_id)
    
    def obter_usuario_por_email(self, email: str) -> Usuario:
        """
        Obtém um usuário por email.
        
        Args:
            email: Email do usuário
        
        Returns:
            Usuario: Usuário encontrado ou None
        """
        return self.repositorio.buscar_por_email(email)
    
    def listar_usuarios(self) -> list[Usuario]:
        """
        Lista todos os usuários ativos.
        
        Returns:
            list[Usuario]: Lista de usuários
        """
        return self.repositorio.listar_todos()
    
    def atualizar_usuario(self, usuario_id: int, nome: str = None, 
                         email: str = None, telefone: str = None) -> Usuario:
        """
        Atualiza dados de um usuário.
        
        Regras de negócio:
        1. Usuário deve existir
        2. Se email for alterado, deve ser único
        3. Dados devem ser válidos
        
        Args:
            usuario_id: ID do usuário
            nome: Novo nome (opcional)
            email: Novo email (opcional)
        
        Returns:
            Usuario: Usuário atualizado ou None se não encontrado
        
        Raises:
            ValueError: Se novo email já existe
            UsuarioInvalidoError: Se dados são inválidos
        """
        # Buscar usuário existente
        usuario = self.repositorio.buscar_por_id(usuario_id)
        if not usuario:
            return None
        
        # Se email está sendo alterado, verificar unicidade
        if email and email != usuario.email:
            usuario_com_email = self.repositorio.buscar_por_email(email)
            if usuario_com_email:
                raise ValueError(f"Email '{email}' já está cadastrado")
        
        # Atualizar dados (validação feita pela entidade)
        if nome:
            usuario.atualizar_nome(nome)
        if email:
            usuario.atualizar_email(email)
        
        # Persistir alterações
        return self.repositorio.atualizar(usuario)
    
    def deletar_usuario(self, usuario_id: int) -> bool:
        """
        Deleta (desativa) um usuário.
        
        Regra de negócio: Usuários não são removidos fisicamente,
        apenas marcados como inativos (soft delete).
        
        Args:
            usuario_id: ID do usuário
        
        Returns:
            bool: True se deletado, False se não encontrado
        """
        usuario = self.repositorio.buscar_por_id(usuario_id)
        if not usuario:
            return False
        
        # Desativar usuário (soft delete)
        usuario.desativar()
        
        # Persistir alteração
        self.repositorio.atualizar(usuario)
        
        return True
    
    def reativar_usuario(self, usuario_id: int) -> bool:
        """
        Reativa um usuário desativado.
        
        Args:
            usuario_id: ID do usuário
        
        Returns:
            bool: True se reativado, False se não encontrado
        """
        usuario = self.repositorio.buscar_por_id(usuario_id)
        if not usuario:
            return False
        
        usuario.ativar()
        self.repositorio.atualizar(usuario)
        
        return True