from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Produto_Pedido

router = APIRouter()

@router.post("/produto_pedido")
async def criar_produto_pedido(produto_pedido: Produto_Pedido):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Produto_Pedido (ID_PEDIDO, ID_PRODUTO, QUANT_PEDIDO_PRODUTO) VALUES (%s, %s, %s)",
            (produto_pedido.id_pedido, produto_pedido.id_produto, produto_pedido.quant_pedido_produto)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar Produto_Pedido")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Produto_Pedido criado com sucesso!"}

@router.get("/produto_pedido", response_model=list[Produto_Pedido])
async def listar_produto_pedido():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PEDIDO, ID_PRODUTO, QUANT_PEDIDO_PRODUTO FROM Produto_Pedido")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        Produto_Pedido(
            id_pedido=p[0],
            id_produto=p[1],
            quant_pedido_produto=p[2]
        ) for p in rows
    ]

@router.get("/produto_pedido/{id_pedido}/{id_produto}", response_model=Produto_Pedido)
async def get_produto_pedido(id_pedido: int, id_produto: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PEDIDO, ID_PRODUTO, QUANT_PEDIDO_PRODUTO FROM Produto_Pedido WHERE ID_PEDIDO = %s AND ID_PRODUTO = %s", (id_pedido, id_produto))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Produto_Pedido(
            id_pedido=row[0],
            id_produto=row[1],
            quant_pedido_produto=row[2]
        )
    raise HTTPException(status_code=404, detail="Produto_Pedido não encontrado")

@router.patch("/produto_pedido/{id_pedido}/{id_produto}")
async def atualizar_produto_pedido(id_pedido: int, id_produto: int, produto_pedido: Produto_Pedido):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PEDIDO, ID_PRODUTO FROM Produto_Pedido WHERE ID_PEDIDO = %s AND ID_PRODUTO = %s", (id_pedido, id_produto))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Produto_Pedido não encontrado")
    try:
        cur.execute(
            "UPDATE Produto_Pedido SET QUANT_PEDIDO_PRODUTO = %s WHERE ID_PEDIDO = %s AND ID_PRODUTO = %s",
            (produto_pedido.quant_pedido_produto, id_pedido, id_produto)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao atualizar Produto_Pedido")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Produto_Pedido atualizado com sucesso"}

@router.delete("/produto_pedido/{id_pedido}/{id_produto}")
async def deletar_produto_pedido(id_pedido: int, id_produto: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PEDIDO, ID_PRODUTO FROM Produto_Pedido WHERE ID_PEDIDO = %s AND ID_PRODUTO = %s", (id_pedido, id_produto))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Produto_Pedido não encontrado")
    try:
        cur.execute("DELETE FROM Produto_Pedido WHERE ID_PEDIDO = %s AND ID_PRODUTO = %s", (id_pedido, id_produto))
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao deletar Produto_Pedido")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Produto_Pedido deletado com sucesso"}
