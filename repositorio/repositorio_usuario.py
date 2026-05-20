"""
Camada de Repositório - Acesso a dados de usuários.

Responsabilidades:
- Abstrair acesso ao banco de dados
- Implementar operações CRUD
- Converter entre entidades de domínio e registros de BD
- Executar queries SQL

NÃO deve conter:
- Lógica de negócio
- Regras de validação de domínio
- Formatação de respostas HTTP
- Lógica de orquestração
"""

from typing import Optional, List
from dominio.usuario import Usuario
from dados.db import obter_conexao


class RepositorioUsuario:
    """
    Repositório responsável pela persistência de usuários.
    Implementa o padrão Repository para abstrair acesso ao banco.
    """
    
    def salvar(self, usuario: Usuario) -> Usuario:
        """
        Salva um novo usuário no banco de dados.
        
        Args:
            usuario: Entidade Usuario a ser salva
        
        Returns:
            Usuario: Usuário com ID gerado pelo banco
        
        Raises:
            Exception: Se houver erro na persistência
        """
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        try:
            # Executar INSERT
            cursor.execute(
                """
                INSERT INTO usuarios (nome, email, telefone, ativo)
                VALUES (?, ?, ?, ?)
                """,
                (usuario.nome, usuario.email, usuario.telefone, usuario.ativo)
            )
            
            # Obter ID gerado
            usuario_id = cursor.lastrowid
            
            # Commit da transação
            conexao.commit()
            
            # Retornar usuário com ID
            usuario.id = usuario_id
            return usuario
            
        except Exception as e:
            conexao.rollback()
            raise Exception(f"Erro ao salvar usuário: {str(e)}")
        finally:
            cursor.close()
    
    def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """
        Busca um usuário por ID.
        
        Args:
            usuario_id: ID do usuário
        
        Returns:
            Usuario: Usuário encontrado ou None
        """
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        try:
            cursor.execute(
                """
                SELECT id, nome, email, telefone, ativo
                FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,)
            )
            
            linha = cursor.fetchone()
            
            if linha:
                return self._converter_linha_para_usuario(linha)
            
            return None
            
        finally:
            cursor.close()
    
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """
        Busca um usuário por email.
        
        Args:
            email: Email do usuário
        
        Returns:
            Usuario: Usuário encontrado ou None
        """
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        try:
            cursor.execute(
                """
                SELECT id, nome, email, telefone, ativo
                FROM usuarios
                WHERE email = ?
                """,
                (email.lower(),)
            )
            
            linha = cursor.fetchone()
            
            if linha:
                return self._converter_linha_para_usuario(linha)
            
            return None
            
        finally:
            cursor.close()
    
    def listar_todos(self) -> List[Usuario]:
        """
        Lista todos os usuários do sistema.
        
        Returns:
            List[Usuario]: Lista de usuários
        """
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        try:
            cursor.execute(
                """
                SELECT id, nome, email, telefone, ativo
                FROM usuarios
                ORDER BY nome
                """
            )
            
            linhas = cursor.fetchall()
            
            return [self._converter_linha_para_usuario(linha) for linha in linhas]
            
        finally:
            cursor.close()
    
    def atualizar(self, usuario: Usuario) -> Usuario:
        """
        Atualiza um usuário existente.
        
        Args:
            usuario: Entidade Usuario com dados atualizados
        
        Returns:
            Usuario: Usuário atualizado
        
        Raises:
            Exception: Se houver erro na atualização
        """
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        try:
            cursor.execute(
                """
                UPDATE usuarios
                SET nome = ?, email = ?, ativo = ?
                WHERE id = ?
                """,
                (usuario.nome, usuario.email, usuario.ativo, usuario.id)
            )
            
            conexao.commit()
            
            return usuario
            
        except Exception as e:
            conexao.rollback()
            raise Exception(f"Erro ao atualizar usuário: {str(e)}")
        finally:
            cursor.close()
    
    def deletar(self, usuario_id: int) -> bool:
        """
        Deleta fisicamente um usuário do banco.
        
        Nota: Na prática, preferimos soft delete (desativar).
        Este método existe para casos específicos.
        
        Args:
            usuario_id: ID do usuário
        
        Returns:
            bool: True se deletado, False se não encontrado
        """
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        try:
            cursor.execute(
                """
                DELETE FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,)
            )
            
            linhas_afetadas = cursor.rowcount
            conexao.commit()
            
            return linhas_afetadas > 0
            
        except Exception as e:
            conexao.rollback()
            raise Exception(f"Erro ao deletar usuário: {str(e)}")
        finally:
            cursor.close()
    
    @staticmethod
    def _converter_linha_para_usuario(linha: tuple) -> Usuario:
        
        # Adicione o telefone aqui:
        usuario_id, nome, email, telefone, ativo = linha
        
        usuario = Usuario(
            nome=nome,
            email=email,
            telefone=telefone, # <- E repasse o telefone aqui
            ativo=bool(ativo)
        )
        usuario.id = usuario_id
        
        return usuario