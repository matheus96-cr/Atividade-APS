"""
Camada de Apresentação - Rotas HTTP para gerenciamento de usuários.

Responsabilidades:
- Receber requisições HTTP
- Validar formato de entrada
- Chamar a camada de Serviço
- Retornar respostas HTTP formatadas

NÃO deve conter:
- Lógica de negócio
- Acesso direto ao banco de dados
- Regras de validação complexas
"""

from flask import Blueprint, request, jsonify
from servico.servico_usuario import ServicoUsuario
from dominio.usuario import UsuarioInvalidoError

# Criar blueprint para rotas de usuário
usuario_bp = Blueprint('usuario', __name__)

# Instanciar serviço
servico_usuario = ServicoUsuario()


@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    """
    Endpoint para criar um novo usuário.
    
    Request Body:
        {
            "nome": "João Silva",
            "email": "joao@email.com"
        }
    
    Returns:
        201: Usuário criado com sucesso
        400: Dados inválidos
        409: Email já cadastrado
        500: Erro interno
    """
    try:
        # Extrair dados da requisição
        dados = request.get_json()
        
        # Validação básica de entrada
        if not dados:
            return jsonify({"erro": "Corpo da requisição vazio"}), 400
        
        nome = dados.get('nome')
        email = dados.get('email')
        telefone = dados.get('telefone')
        
        if not nome or not email:
            return jsonify({"erro": "Nome e email são obrigatórios"}), 400
        
        # Chamar camada de serviço
        usuario = servico_usuario.criar_usuario(nome, email, telefone)
        
        # Retornar resposta formatada
        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "ativo": usuario.ativo
        }), 201
        
    except UsuarioInvalidoError as e:
        return jsonify({"erro": str(e)}), 400
    except ValueError as e:
        return jsonify({"erro": str(e)}), 409
    except Exception as e:
        return jsonify({"erro": "Erro interno do servidor", "detalhe": str(e)}), 500


@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obter_usuario(usuario_id):
    """
    Endpoint para obter um usuário por ID.
    
    Args:
        usuario_id: ID do usuário
    
    Returns:
        200: Usuário encontrado
        404: Usuário não encontrado
        500: Erro interno
    """
    try:
        usuario = servico_usuario.obter_usuario_por_id(usuario_id)
        
        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        
        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone,   
            "ativo": usuario.ativo
        }), 200
        
    except Exception as e:
        return jsonify({"erro": "Erro interno do servidor"}), 500


@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    """
    Endpoint para listar todos os usuários.
    
    Returns:
        200: Lista de usuários
        500: Erro interno
    """
    try:
        usuarios = servico_usuario.listar_usuarios()
        
        return jsonify({
            "total": len(usuarios),
            "usuarios": [
                {
                    "id": u.id,
                    "nome": u.nome,
                    "email": u.email,
                    "telefone": u.telefone,
                    "ativo": u.ativo
                }
                for u in usuarios
            ]
        }), 200
        
    except Exception as e:
        return jsonify({"erro": "Erro interno do servidor"}), 500


@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    """
    Endpoint para atualizar um usuário.
    
    Args:
        usuario_id: ID do usuário
    
    Request Body:
        {
            "nome": "João Silva Atualizado",
            "email": "joao.novo@email.com"
        }
    
    Returns:
        200: Usuário atualizado
        400: Dados inválidos
        404: Usuário não encontrado
        500: Erro interno
    """
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify({"erro": "Corpo da requisição vazio"}), 400
        
        nome = dados.get('nome')
        email = dados.get('email')
        telefone = dados.get('telefone')
        
        usuario = servico_usuario.atualizar_usuario(usuario_id, nome, email)
        
        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        
        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "ativo": usuario.ativo
        }), 200
        
    except UsuarioInvalidoError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro interno do servidor"}), 500


@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def deletar_usuario(usuario_id):
    """
    Endpoint para deletar (desativar) um usuário.
    
    Args:
        usuario_id: ID do usuário
    
    Returns:
        204: Usuário deletado
        404: Usuário não encontrado
        500: Erro interno
    """
    try:
        sucesso = servico_usuario.deletar_usuario(usuario_id)
        
        if not sucesso:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        
        return '', 204
        
    except Exception as e:
        return jsonify({"erro": "Erro interno do servidor"}), 500