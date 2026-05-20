
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
        
        return self.repositorio.buscar_por_id(usuario_id)
    
    def obter_usuario_por_email(self, email: str) -> Usuario:
       
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
