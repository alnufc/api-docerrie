from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Produto, ProdutoUpdate
from pydantic import BaseModel


router = APIRouter()


## CADASTRAR PRODUTO
@router.post("/produtos")
async def cadastrar_produto(produto: Produto):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Produto(ID_PRODUTO,NOME_PRODUTO, VALOR_PRODUTO, ESTOQUE_PRODUTO) VALUES (%s, %s, %s)",
            (produto.id_produto, produto.nome_produto, produto.valor_produto, produto.estoque_produto)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao cadastrar produto")
    finally:
        cursor.close()
        conn.close()
    return {"msg": "Produto cadastrado com sucesso!"}


## LISTAR PRODUTOS
@router.get("/produtos", response_model=list[Produto])
async def listar_produtos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PRODUTO, NOME_PRODUTO, VALOR_PRODUTO, ESTOQUE_PRODUTO FROM Produto")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        Produto(
            id_produto=p[0],
            nome_produto=p[1],
            valor_produto=p[2],
            estoque_produto=p[3]
        ) for p in rows
    ]

## LISTAR PRODUTO POR ID
@router.get("/produtos/{id_produto}", response_model=Produto)
async def get_produto_por_id(id_produto: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PRODUTO, NOME_PRODUTO, VALOR_PRODUTO, ESTOQUE_PRODUTO FROM Produto WHERE ID_PRODUTO = %s", (id_produto,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Produto(
            id_produto=row[0],
            nome_produto=row[1],
            valor_produto=row[2],
            estoque_produto=row[3]
        )
    raise HTTPException(status_code=404, detail="Produto não encontrado")

## ATUALIZAR PRODUTO POR ID
@router.patch("/produtos/{id_produto}")
async def atualizar_produto(id_produto: int, produtoUp: ProdutoUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PRODUTO FROM Produto WHERE ID_PRODUTO = %s", (id_produto,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    fields = []
    values = []
    for campo, valor in produtoUp.dict(exclude_unset=True).items():
        fields.append(f"{campo.upper()} = %s")
        values.append(valor)
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    try:
        cur.execute(
            f"UPDATE Produto SET {', '.join(fields)} WHERE ID_PRODUTO = %s",
            values + [id_produto]
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao atualizar produto")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Produto atualizado com sucesso"}

## DELETAR PRODUTO POR ID
@router.delete("/produtos/{id_produto}")
async def deletar_produto(id_produto: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PRODUTO FROM Produto WHERE ID_PRODUTO = %s", (id_produto,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    try:
        cur.execute("DELETE FROM Produto WHERE ID_PRODUTO = %s", (id_produto,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao deletar produto")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Produto deletado com sucesso"}
