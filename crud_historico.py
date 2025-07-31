from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Historico
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/historico")
async def criar_historico(historico: Historico):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Historico(ID_PEDIDO, STATUS_ANTIGO, STATUS_NOVO) VALUES (%s, %s, %s)",
            (historico.id_pedido, historico.status_antigo, historico.status_novo)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar histórico")
    finally:
        cursor.close()
        conn.close()
    return {"msg": "Histórico criado com sucesso!"}

@router.get("/historico", response_model=List[Historico])
async def listar_historico():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_HISTORICO, ID_PEDIDO, STATUS_ANTIGO, STATUS_NOVO, DATA_HORA_ALTERACAO FROM Historico")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        Historico(
            id_historico=row[0],
            id_pedido=row[1],
            status_antigo=row[2],
            status_novo=row[3],
            data_hora_alteracao=row[4]
        ) for row in rows
    ]

@router.get("/historico/{id_historico}", response_model=Historico)
async def get_historico_por_id(id_historico: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_HISTORICO, ID_PEDIDO, STATUS_ANTIGO, STATUS_NOVO, DATA_HORA_ALTERACAO FROM Historico WHERE ID_HISTORICO = %s", (id_historico,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Historico(
            id_historico=row[0],
            id_pedido=row[1],
            status_antigo=row[2],
            status_novo=row[3],
            data_hora_alteracao=row[4]
        )
    raise HTTPException(status_code=404, detail="Histórico não encontrado")

@router.delete("/historico/{id_historico}")
async def deletar_historico(id_historico: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_HISTORICO FROM Historico WHERE ID_HISTORICO = %s", (id_historico,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Histórico não encontrado")
    try:
        cur.execute("DELETE FROM Historico WHERE ID_HISTORICO = %s", (id_historico,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao deletar histórico")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Histórico deletado com sucesso"}

