--CREATE
BEGIN;

INSERT INTO "Perfil_Usuario" (id_perfil, nome, telefone, endereco, sexo, data_criacao_conta)
VALUES (0, 'Renan Rigolon Coelho Pinto', 32988560397, 'Rua Roberto de Barros, nº 206, apto 203', TRUE, '2024-04-11 04:36:32.459873');

INSERT INTO "Perfil_Usuario" (id_perfil, nome, telefone, sexo, data_criacao_conta)
VALUES (1, 'Victor Martins', 48998595692, TRUE, '2024-03-22 04:36:32.459873');

INSERT INTO "Perfil_Usuario" (id_perfil, nome, telefone, sexo, data_criacao_conta)
VALUES (2, 'Cleverson', 49999522693, TRUE, '2023-12-03 04:36:32.459873');

INSERT INTO "Perfil_Usuario" (id_perfil, nome, telefone, sexo, data_criacao_conta)
VALUES (3, 'Luan', 31996026122, TRUE, '2024-01-16 04:36:32.459873');

INSERT INTO "Perfil_Usuario" (id_perfil, nome, telefone, sexo, data_criacao_conta)
VALUES (4, 'Gabriel Freire', 81994768636, TRUE, '2024-02-19 04:36:32.459873');


INSERT INTO "Login_table" (id_login, email, nome_usuario, senha, usuario_id)
VALUES (0, 'renanrcpinto@gmail.com', 'Renan Pinto', '123senha', 0);

INSERT INTO "Login_table" (id_login, email, nome_usuario, senha, usuario_id)
VALUES (1, 'victor.martins@gmail.com', 'Victor Martins', '123senha*', 1);

INSERT INTO "Login_table" (id_login, email, nome_usuario, senha, usuario_id)
VALUES (2, 'cleverson@gmail.com', 'Cleverson', '123senha45', 2);

INSERT INTO "Login_table" (id_login, email, nome_usuario, senha, usuario_id)
VALUES (3, 'luanzim2003@gmail.com', 'Luan', 'Senha', 3);

INSERT INTO "Login_table" (id_login, email, nome_usuario, senha, usuario_id)
VALUES (4, 'gabriel_freire@gmail.com', 'Gabriel Freire', 'essa_e_minha_senha', 4);


--INSERT INTO "Documento" (id_doc, tipo, usuario_id)
--VALUES (0, 'CNH', 5);

--INSERT INTO "CNH" (doc_id, nome, rg, orgao_emissor_rg, uf_rg, cpf, data_nasc, filiacao_pai, filiacao_mae, cat, registro, validade, primeira_hab)
--VALUES (0, 'EDNEY DE BRITO ELIAS', '20185260', 'SSP', 'AM', '85035831272', '1987-04-06', 'jose da silva elias', 'mariamar de brito elias', 'AB', 054229857609, '2020-09-17', '2010-07-26');

--INSERT INTO "Documento" (id_doc, tipo, usuario_id)
--VALUES (1, 'CNH', 6);

--INSERT INTO "CNH" (doc_id, nome, rg, orgao_emissor_rg, uf_rg, cpf, data_nasc, filiacao_pai, filiacao_mae, cat, registro, validade, primeira_hab)
--VALUES (1, 'bolzani anghinoni elton', '296989411', 'snj', 'go', '47445848371', '1967-05-15', 'yoshida thielly pierro', 'reato lepine knudse da mata', 'c', 33407763599, '1983-05-31', '1979-02-19');

INSERT INTO "Documento" (id_doc, tipo, usuario_id)
VALUES (2, 'CNH', 1);

INSERT INTO "CNH" (doc_id, nome, primeira_hab, data_nasc, local_nasc, uf_nasc, data_emissao, validade, rg, orgao_emissor_rg, uf_rg, cpf, registro, cat, nacionalidade, filiacao_pai, filiacao_mae, localizacao)
VALUES (2, 'victor martins', '2023-06-27', '2004-09-21', 'ararangua', 'sc', '2023-06-27', '2024-06-26', '7404629', 'sesp', 'sc', '12091071986', 08218072835, 'ab', 'brasileiro', 'vilson americo martins', 'sandra goretti carlos', 'florianopolis, sc');

INSERT INTO "Documento" (id_doc, tipo, usuario_id)
VALUES (3, 'rg', 1);

INSERT INTO "RG" (doc_id, nome, filiacao_pai, filiacao_mae, data_nasc, naturalidade, cpf, rg, orgao_emissor, data_emissao)
VALUES (3, 'victor martins', 'vilson americo martins', 'sandra goretti carlos', '2004-09-21', 'ararangua sc', '12091071986', '7404629', 'sespsc', '2021-08-09');

INSERT INTO "Documento" (id_doc, tipo, usuario_id)
VALUES (4, 'rg', 3);

INSERT INTO "RG" (doc_id, nome, filiacao_pai, filiacao_mae, data_nasc, naturalidade, cpf, rg, orgao_emissor, data_emissao, validade)
VALUES (4, 'luan henrry vidal oliveira', 'geraldo jose vidal neto', 'luana marcia gomes oliveira', '2005-10-03', 'contagem mg', '17160633610', '17160633610', 'ii/pcmg', '2024-03-11', '2034-03-11');

INSERT INTO "Documento" (id_doc, tipo, usuario_id)
VALUES (5, 'rg', 0);

INSERT INTO "RG" (doc_id, nome, filiacao_pai, filiacao_mae, data_nasc, naturalidade, cpf, rg, orgao_emissor, data_emissao, titulo_eleitor, zona_eleitoral, secao_eleitoral, nis_pis_pasep, cns, ctps, serie_ctps, uf_ctps)
VALUES (5, 'renan rigolon coelho pinto', 'robson coelho pinto', 'cresiane valente rigolon coelho pinto', '1999-04-15', 'rio de janeiro rj', '07208704619', 'mg-18.971.768', 'pcmg', '2022-06-24', 215532980281, 258, 43, 20408259722, 898003449720467, 9335407, 0040, 'mg');

END;

--READ
BEGIN;

SELECT * FROM "Login_table";

SELECT nome, telefone FROM "Perfil_Usuario"
WHERE id_perfil > 2;

SELECT nome, data_nasc FROM "RG";

SELECT * FROM "CNH";

END;

--UPDATE
BEGIN;

UPDATE "Login_table" SET nome_usuario = 'Renan Rigolon' WHERE id = 0;

UPDATE "Perfil_Usuario" SET nome = 'Renan Pinto' WHERE id = 0;

UPDATE "Documento" SET id_doc = 101 WHERE id = 0;

END;

--DELETE
BEGIN;

DELETE FROM "Login_table" WHERE nome_usuario = 'Renan Pinto';

DELETE FROM "Perfil_Usuario" WHERE nome = 'Renan Rigolon Coelho Pinto';

DELETE * FROM "CNH";

END;