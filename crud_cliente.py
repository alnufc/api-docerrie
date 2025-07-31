from fastapi import APIRouter, HTTPException
from db import get_connection
from pydantic import BaseModel
from typing import List, Optional
from models import Clientes, ClientesUpdate

router = APIRouter()


##CADASTRAR CLIENTE --completo
@router.post("/clientes")
async def cadastrar_cliente(cli: Clientes):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Cliente(id_cliente, nome_cliente, email, telefone) VALUES (%s, %s, %s, %s)",
            (cli.id_cliente, cli.nome_cliente, cli.email, cli.telefone)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao cadastrar cliente")
    finally:
        cursor.close()
        conn.close()
    return {"msg": "Cliente cadastrado com sucesso!"}
        

## LISTAR CLIENTES --completo
@router.get("/clientes", response_model = List[Clientes])
async def listar_clientes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_cliente, nome_cliente, email, telefone FROM cliente")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        Clientes(
            id_cliente=c[0],
            nome_cliente=c[1],
            email=c[2],
            telefone=c[3]
        ) for c in rows
    ]



## LISTAR POR ID -- Completo
@router.get("/clientes/{id_cliente}", response_model = Clientes)
async def get_cliente_por_id(id_cliente: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_cliente, nome_cliente, email, telefone FROM cliente WHERE id_cliente = %s", (id_cliente,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Clientes(
            id_cliente=row[0],
            nome_cliente=row[1],
            email=row[2],
            telefone=row[3]
        )
    raise HTTPException(status_code=404, detail="Cliente não encontrado")


## ATUALIZAR CLIENTE POR ID
@router.patch("/clientes/{id_cliente}")
async def atualizar_cliente (id_cliente: int, cliUp: ClientesUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_cliente FROM Cliente WHERE id_cliente = %s", (id_cliente,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    fields = []
    values = []

    for campo, valor in cliUp.dict(exclude_unset=True).items():
        fields.append(f"{campo} = %s")
        values.append(valor)
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    values
    try:
        cur.execute(
            f"UPDATE cliente SET {', '.join(fields)} WHERE id_cliente = %s",
            values + [id_cliente]
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao atualizar cliente")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Cliente atualizado com sucesso"}



## DELETAR CLIENTE POR ID                            
@router.delete("/clientes/{id_cliente}")
async def deletar_cliente(id_cliente: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_cliente FROM cliente WHERE id_cliente = %s", (id_cliente,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    try:
        cur.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao deletar cliente")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Cliente deletado com sucesso"}