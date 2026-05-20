
##  Exemplo de Uso

### Instalação de Dependências

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências
pip install flask
```

### Executar a Aplicação

```bash
# Executar servidor
python app.py
```

### Testar os Endpoints

#### 1. Criar Usuário

```bash
curl -X POST http://localhost:5000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@email.com"
  }'
```

**Resposta (201 Created):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "ativo": true
}
```

#### 2. Listar Usuários

```bash
curl http://localhost:5000/api/usuarios
```

**Resposta (200 OK):**
```json
{
  "total": 1,
  "usuarios": [
    {
      "id": 1,
      "nome": "João Silva",
      "email": "joao@email.com",
      "ativo": true
    }
  ]
}
```

#### 3. Obter Usuário por ID

```bash
curl http://localhost:5000/api/usuarios/1
```

**Resposta (200 OK):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "ativo": true
}
```

#### 4. Atualizar Usuário

```bash
curl -X PUT http://localhost:5000/api/usuarios/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva Atualizado",
    "email": "joao.novo@email.com"
  }'
```

**Resposta (200 OK):**
```json
{
  "id": 1,
  "nome": "João Silva Atualizado",
  "email": "joao.novo@email.com",
  "ativo": true
}
```

#### 5. Deletar Usuário

```bash
curl -X DELETE http://localhost:5000/api/usuarios/1
```

**Resposta (204 No Content)**

---

