import psycopg2
import json
from psycopg2 import sql
#from dotenv import load_dotenv
#import os

# Carregar variáveis de ambiente
#load_dotenv()

# Conectando ao banco de dados
#conn = psycopg2.connect(
#    dbname=os.getenv("DBNAME"),
#    user=os.getenv("USER"),
#    password=os.getenv("PASSWORD"),
#    host=os.getenv("HOST"),
#    port=os.getenv("PORT")
#)

def create(tabela, j_son, usuario_id = None):
    try:
        # Conectando ao banco de dados
        conn = psycopg2.connect(
            dbname="Projeto Teste",
            user="postgres",
            password="SENHA-FALSA123",
            host="localhost",
            port=5432
        )
        
        # Inicia a transação
        conn.autocommit = False

        # Criando um cursor
        cur = conn.cursor()
        
        # Executar comandos
        # Converte o JSON em um dicionário Python
        dados = json.loads(j_son)
    
        # Monta a lista de nomes das colunas e valores
        colunas = dados.keys()
        valores = dados.values()
    
        # Monta a string SQL para os nomes das colunas
        colunas_sql = sql.SQL(', ').join(map(sql.Identifier, colunas))
    
        # Monta a string SQL para os valores usando placeholders (%s)
        valores_sql = sql.SQL(', ').join([sql.Placeholder()] * len(colunas))
        
        if tabela == "RG" or tabela == "CNH":
            # Monta a consulta SQL
            query = sql.SQL('INSERT INTO "Documento" (tipo, usuario_id) VALUES (%s, %s, %s)')
            values = (tabela, usuario_id, )
            # Executa a consulta SQL
            cur.execute(query, values)
            
            # Monta a consulta SQL
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(tabela),
                colunas_sql,
                valores_sql
            )
            # Executa a consulta SQL
            cur.execute(query, tuple(valores))
        
        else:
            # Monta a consulta SQL
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(tabela),
                colunas_sql,
                valores_sql
            )
            # Executa a consulta SQL
            cur.execute(query, tuple(valores))
        
        # Faz o commit
        conn.commit()
        print("Operação concluída com sucesso.")
        
        # Fechando o cursor e a conexão
        cur.close()
        conn.close()
        
    except Exception as e:
        # Se ocorrer um erro, realiza um rollback
        conn.rollback()
        print(f"Operação concluída com falha. Erro: {e}.")

def read(tabela):
    try:
        # Conectando ao banco de dados
        conn = psycopg2.connect(
            dbname="Projeto Teste",
            user="postgres",
            password="SENHA-FALSA123",
            host="localhost",
            port=5432
        )
        
        # Inicia a transação
        conn.autocommit = False

        # Criando um cursor
        cur = conn.cursor()
        
        # Executar comandos
        if tabela == "RG" or tabela == "CNH":
            #consulta parametrizada
            postgreSQL_select_query = sql.SQL('SELECT * FROM "Documento" JOIN {} ON "Documento".id_doc = {}.doc_id').format(sql.Identifier(tabela), sql.Identifier(tabela))
            cur.execute(postgreSQL_select_query)
        
            # Obtendo o resultado da consulta
            rows = cur.fetchall()
            for row in rows:
                print(row)
        
        else:
            #consulta parametrizada
            postgreSQL_select_query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(tabela))
            cur.execute(postgreSQL_select_query)
        
            # Obtendo o resultado da consulta
            rows = cur.fetchall()
            for row in rows:
                print(row)
        
        # Faz o commit
        conn.commit()
        print("Operação concluída com sucesso.")
        
        # Fechando o cursor e a conexão
        cur.close()
        conn.close()
        
    except Exception as e:
        # Se ocorrer um erro, realiza um rollback
        conn.rollback()
        print(f"Operação concluída com falha. Erro: {e}.")

def update(tabela, j_son, id_usuario = None, id_doc = None):
    try:
        # Conectando ao banco de dados
        conn = psycopg2.connect(
            dbname="Projeto Teste",
            user="postgres",
            password="SENHA-FALSA123",
            host="localhost",
            port=5432
    )
        
        # Inicia a transação
        conn.autocommit = False

        # Criando um cursor
        cur = conn.cursor()
        
        # Executar comandos
        if tabela == "RG" or tabela == "CNH":
            delete(tabela, id_doc)
            create(tabela, j_son, id_usuario)
        
        else:
            delete(tabela, id_usuario)
            create(tabela, j_son)
        
        # Faz o commit
        conn.commit()
        print("Operação concluída com sucesso.")
        
        # Fechando o cursor e a conexão
        cur.close()
        conn.close()
        
    except Exception as e:
        # Se ocorrer um erro, realiza um rollback
        conn.rollback()
        print(f"Operação concluída com falha. Erro: {e}.")

def delete(tabela, id):
    try:
        # Conectando ao banco de dados
        conn = psycopg2.connect(
            dbname="Projeto Teste",
            user="postgres",
            password="SENHA-FALSA123",
            host="localhost",
            port=5432
        )
        
        # Inicia a transação
        conn.autocommit = False

        # Criando um cursor
        cur = conn.cursor()
        
        # Executar comandos
        if tabela == "RG" or tabela == "CNH":       
            postgreSQL_delete_query_tabela = sql.SQL("DELETE FROM {} WHERE doc_id = %s").format(sql.Identifier(tabela))
            record_to_delete = (id, )
            cur.execute(postgreSQL_delete_query_tabela, record_to_delete)
        
            postgreSQL_delete_query_doc = sql.SQL('DELETE FROM "Documento" WHERE id_doc = %s')
            cur.execute(postgreSQL_delete_query_doc, record_to_delete)
            
        else:
            postgreSQL_delete_query = sql.SQL("DELETE FROM {} WHERE id_perfil = %s").format(sql.Identifier(tabela))
            record_to_delete = (id, )
            cur.execute(postgreSQL_delete_query, record_to_delete)
        
        # Faz o commit
        conn.commit()
        print("Operação concluída com sucesso.")
        
        # Fechando o cursor e a conexão
        cur.close()
        conn.close()
        
    except Exception as e:
        # Se ocorrer um erro, realiza um rollback
        conn.rollback()
        print(f"Operação concluída com falha. Erro: {e}.")