# 📱 Atividade APS - Arquitetura em Camadas (Gerenciamento de Usuários)

## 📁 Estrutura do Projeto


* `apresentacao/` - Contém as rotas da API REST (`rotas_usuario.py`)
* `servico/` - Orquestração de negócio e regras operacionais (`servico_usuario.py`)
* `dominio/` - Entidades e validações de negócio fundamentais (`usuario.py`)
* `repositorio/` - Camada que faz a ponte entre o Python e o banco SQL (`repositorio_usuario.py`)
* `dados/` - Scripts de inicialização e estrutura do banco de dados (`db.py`)
* `docs/` - Documentações e guias de suporte do projeto.

---

## 🛠️ Etapas do Desenvolvimento (Camadas)

A implementação seguiu estritamente a ordem de dependência técnica[cite: 24, 25]:

### 1. Camada de Dados (`dados/db.py`)
* **Responsabilidade:** Fundação de persistência do sistema[cite: 38].
* **Implementação:** Inclusão da coluna `telefone TEXT` na tabela `usuarios` dentro da função `inicializar_banco()`[cite: 41].

### 2. Camada de Domínio (`dominio/usuario.py`)
* **Responsabilidade:** Definição da estrutura e validações da entidade de negócio[cite: 61].
* **Implementação:** Adicionado o campo opcional `telefone: Optional[str] = None` ao `@dataclass Usuario` [cite: 65, 68, 75], com regra de validação para aceitar apenas formatos válidos de 10 ou 11 dígitos[cite: 67].

### 3. Camada de Repositório (`repositorio/repositorio_usuario.py`)
* **Responsabilidade:** Tradução de dados entre queries SQL e objetos Python[cite: 80].
* **Implementação:** Atualização do método `salvar()` (INSERT) [cite: 87], mapeamento nos métodos de busca (SELECT) [cite: 88] e extração na função `_converter_linha_para_usuario()`[cite: 89].

### 4. Camada de Serviço (`servico/servico_usuario.py`)
* **Responsabilidade:** Coordenação dos fluxos de negócio e comunicação com repositórios[cite: 91].
* **Implementação:** Alteração da assinatura do método `criar_usuario()` para receber o parâmetro opcional e repassá-lo na instanciação do objeto `Usuario`[cite: 94, 95, 96, 102, 108].

### 5. Camada de Apresentação (`apresentacao/rotas_usuario.py`)
* **Responsabilidade:** Interface externa e exposição dos endpoints da API REST[cite: 110].
* **Implementação:** Atualização das rotas `POST /api/usuarios` e `GET /api/usuarios` para capturar e responder os dados de telefone no formato JSON[cite: 114, 115, 116, 118, 119, 121].

---

## 🚀 Como Executar e Testar

### Instalação
1. Clone o repositório:
   ```bash
   git clone [https://github.com/matheus96-cr/Atividade-APS.git](https://github.com/matheus96-cr/Atividade-APS.git)
   cd Atividade-APS
