from pydantic import BaseModel
from typing import Optional
from datetime import date

class Clientes(BaseModel):
    id_cliente: int
    nome_cliente: str
    email: str
    telefone: int

class ClientesUpdate(BaseModel):
    id_cliente: int
    nome_cliente: str
    email: str
    telefone: int

class Produto(BaseModel):
    id_produto: int
    nome_produto: str
    valor_produto: float 
    estoque_produto: int

class ProdutoUpdate(BaseModel):
    id_produto: int
    nome_produto: str
    valor_produto: float 
    estoque_produto: int

class Pedido(BaseModel):
    id_pedido: int
    id_cliente: int
    status_pedido: str
    valor_pedido: float
    data_hora_pedido: date

class PedidoUpdate(BaseModel):
    id_pedido: int
    id_cliente: int
    status_pedido: str
    valor_pedido: float
    data_hora_pedido: date

class Produto_Pedido(BaseModel):
    id_pedido: int
    id_produto: int
    quant_pedido_produto: int

class Historico(BaseModel):
    id_pedido: int
    id_historico: int
    status_antigo: str
    status_novo: Optional[str] = None
    data_hora_alteracao: date
    
class HistoricoUpdate(BaseModel):
    id_pedido: int
    id_historico: int
    status_antigo: str = "Pedente"
    status_novo: Optional[str] = None
    data_hora_alteracao: date
    
class EnderecoCliente(BaseModel):
    id_cliente: int
    rua: str
    numero: str
    bairro: str
    cidade: str

class EnderecoClienteUpdate(BaseModel):
    id_cliente: int
    rua: str
    numero: str
    bairro: str
    cidade: str