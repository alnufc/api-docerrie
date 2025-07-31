from fastapi import APIRouter, HTTPException
from db import get_connection
from pydantic import BaseModel
from typing import List, Optional
from models import EnderecoCliente, EnderecoClienteUpdate

router = APIRouter()

@router.post("/endereco_cliente")
async def criar_endereco_cliente(endereco: EnderecoCliente):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Endereco_Cliente (ID_CLIENTE, RUA, NUMERO, BAIRRO, CIDADE) VALUES (%s, %s, %s, %s, %s)",
            (endereco.id_cliente, endereco.rua, endereco.numero, endereco.bairro, endereco.cidade)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar Endereco_Cliente")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Endereco_Cliente criado com sucesso!"}

@router.get("/endereco_cliente", response_model=list[EnderecoCliente])
async def listar_enderecos_cliente():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_CLIENTE, RUA, NUMERO, BAIRRO, CIDADE FROM Endereco_Cliente")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        EnderecoCliente(
            id_cliente=e[0],
            rua=e[1],
            numero=e[2],
            bairro=e[3],
            cidade=e[4]
        ) for e in rows
    ]

@router.get("/endereco_cliente/{id_cliente}", response_model=list[EnderecoCliente])
async def get_endereco_cliente(id_cliente: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_CLIENTE, RUA, NUMERO, BAIRRO, CIDADE FROM Endereco_Cliente WHERE ID_CLIENTE = %s", (id_cliente,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if rows:
        return [
            EnderecoCliente(
                id_cliente=e[0],
                rua=e[1],
                numero=e[2],
                bairro=e[3],
                cidade=e[4]
            ) for e in rows
        ]
    raise HTTPException(status_code=404, detail="Endereço do cliente não encontrado")

@router.patch("/endereco_cliente/{id_cliente}")
async def atualizar_endereco_cliente(id_cliente: int, endereco: EnderecoClienteUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_CLIENTE FROM Endereco_Cliente WHERE ID_CLIENTE = %s", (id_cliente,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Endereço do cliente não encontrado")
    try:
        cur.execute(
            "UPDATE Endereco_Cliente SET RUA = %s, NUMERO = %s, BAIRRO = %s, CIDADE = %s WHERE ID_CLIENTE = %s",
            (endereco.rua, endereco.numero, endereco.bairro, endereco.cidade, id_cliente)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao atualizar Endereco_Cliente")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Endereço do cliente atualizado com sucesso"}

@router.delete("/endereco_cliente/{id_cliente}")
async def deletar_endereco_cliente(id_cliente: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_CLIENTE FROM Endereco_Cliente WHERE ID_CLIENTE = %s", (id_cliente,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Endereço do cliente não encontrado")
    try:
        cur.execute("DELETE FROM Endereco_Cliente WHERE ID_CLIENTE = %s", (id_cliente,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao deletar Endereco_Cliente")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Endereço do cliente deletado com sucesso"}
