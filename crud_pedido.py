from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Pedido, PedidoUpdate
from typing import List, Optional
from pydantic import BaseModel


router = APIRouter()

## CADASTRAR PEDIDO
@router.post("/pedidos")
async def cadastrar_pedido(pedido: Pedido):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Pedido(ID_CLIENTE, STATUS_PEDIDO, VALOR_PEDIDO) VALUES (%s, %s, %s)",
            (pedido.id_cliente, pedido.status_pedido, pedido.valor_pedido)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao cadastrar pedido")
    finally:
        cursor.close()
        conn.close()
    return {"msg": "Pedido cadastrado com sucesso!"}

## LISTAR PEDIDOS
@router.get("/pedidos", response_model= List[Pedido])
async def listar_pedidos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PEDIDO, ID_CLIENTE, STATUS_PEDIDO, VALOR_PEDIDO, DATA_HORA_PEDIDO FROM Pedido")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        Pedido(
            id_pedido=p[0],
            id_cliente=p[1],
            status_pedido=p[2],
            valor_pedido=p[3],
            data_hora_pedido=p[4]
        ) for p in rows
    ]




## LISTAR PEDIDO POR ID
@router.get("/pedidos/{id_pedido}", response_model=Pedido)
async def get_pedido_por_id(id_pedido: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PEDIDO, ID_CLIENTE, STATUS_PEDIDO, VALOR_PEDIDO, DATA_HORA_PEDIDO FROM Pedido WHERE ID_PEDIDO = %s", (id_pedido,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Pedido(
            id_pedido=row[0],
            id_cliente=row[1],
            status_pedido=row[2],
            valor_pedido=row[3],
            data_hora_pedido=row[4]
        )
    raise HTTPException(status_code=404, detail="Pedido não encontrado")

## ATUALIZAR PEDIDO POR ID
@router.patch("/pedidos/{id_pedido}")
async def atualizar_pedido(id_pedido: int, pedidoUp: PedidoUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PEDIDO FROM Pedido WHERE ID_PEDIDO = %s", (id_pedido,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    fields = []
    values = []
    for campo, valor in pedidoUp.dict(exclude_unset=True).items():
        fields.append(f"{campo.upper()} = %s")
        values.append(valor)
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    try:
        cur.execute(
            f"UPDATE Pedido SET {', '.join(fields)} WHERE ID_PEDIDO = %s",
            values + [id_pedido]
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao atualizar pedido")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Pedido atualizado com sucesso"}

## DELETAR PEDIDO POR ID
@router.delete("/pedidos/{id_pedido}")
async def deletar_pedido(id_pedido: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PEDIDO FROM Pedido WHERE ID_PEDIDO = %s", (id_pedido,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    try:
        cur.execute("DELETE FROM Pedido WHERE ID_PEDIDO = %s", (id_pedido,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao deletar pedido")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Pedido deletado com sucesso"}
