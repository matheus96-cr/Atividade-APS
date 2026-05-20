"""
Ponto de entrada da aplicação.
Inicializa o servidor Flask e registra as rotas.
"""

from flask import Flask
from apresentacao.rotas_usuario import usuario_bp
from dados.db import inicializar_banco

def criar_app():
    """
    Factory function para criar e configurar a aplicação Flask.
    
    Returns:
        Flask: Instância configurada da aplicação
    """
    app = Flask(__name__)
    
    # Configurações da aplicação
    app.config['JSON_AS_ASCII'] = False  # Suporte a caracteres UTF-8
    
    # Inicializar banco de dados
    inicializar_banco()
    
    # Registrar blueprints (rotas)
    app.register_blueprint(usuario_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = criar_app()
    #print("Servidor iniciado em http://localhost:5000")
    #print("Documentação: http://localhost:5000/api/usuarios")
    app.run(debug=True, host='0.0.0.0', port=5000)