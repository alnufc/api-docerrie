from fastapi import FastAPI
from crud_cliente import router as cliente_router
from crud_historico import router as historico_router
from crud_produto import router as produto_router
from crud_pedido import router as pedido_router
from crud_produto_pedido import router as produto_pedido_router
from crud_endereco_cliente import router as endereco_cliente_router

app = FastAPI(
    title="Api Docerrie",
    version="1.0"
)

app.include_router(cliente_router, prefix="/clientes", tags = ["Clientes"])
app.include_router(historico_router, prefix="/historico", tags=["Histórico"])
app.include_router(produto_router, prefix="/produtos", tags=["Produtos"])
app.include_router(pedido_router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(produto_pedido_router, prefix="/produto_pedido", tags=["Produto_Pedido"])
app.include_router(endereco_cliente_router, prefix="/enderecos", tags=["Endereços Clientes"])

