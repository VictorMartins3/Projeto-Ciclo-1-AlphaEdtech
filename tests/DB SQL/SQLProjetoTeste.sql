BEGIN;


CREATE TABLE IF NOT EXISTS public."Documento"
(
    id_doc serial,
    tipo character varying(50),
    usuario_id integer,
    CONSTRAINT id_doc_pk PRIMARY KEY (id_doc)
);

CREATE TABLE IF NOT EXISTS public."Login_table"
(
    id_login serial,
    email character varying(255),
    nome_usuario character varying(100),
    senha character varying(255),
    usuario_id integer,
    CONSTRAINT id_login_pk PRIMARY KEY (id_login)
);

CREATE TABLE IF NOT EXISTS public."Perfil_Usuario"
(
    id_perfil serial,
    nome character varying(255),
    telefone bigint,
    endereco text,
    sexo boolean,
    data_criacao_conta timestamp with time zone,
    CONSTRAINT id_perfil_pk PRIMARY KEY (id_perfil)
);

CREATE TABLE IF NOT EXISTS public."RG"
(
    doc_id integer,
    foto bytea,
    assinatura bytea,
    orgao_emissor character varying(255),
    data_emissao date,
    rg character varying(50),
    nome character varying(255),
    filiacao_pai character varying(255),
    filiacao_mae character varying(255),
    cpf character varying(20),
    origem_doc character varying(255),
    naturalidade character varying(50),
    data_nasc date,
    rh boolean,
    observacao text,
    dni bigint,
    titulo_eleitor bigint,
    zona_eleitoral integer,
    secao_eleitoral integer,
    nis_pis_pasep bigint,
    cert_militar bigint,
    cnh bigint,
    cns bigint,
    id_profissional character varying(255),
    ctps integer,
    serie_ctps integer,
    uf_ctps character varying(2),
    validade date,
    CONSTRAINT doc_id_pk_rg PRIMARY KEY (doc_id)
);

CREATE TABLE IF NOT EXISTS public."CNH"
(
    doc_id integer,
    nome character varying(255),
    foto bytea,
    observacao text,
    data_emissao date,
    localizacao character varying(100),
    rg character varying(50),
    orgao_emissor_rg character varying(255),
    uf_rg character varying(2),
    cpf character varying(20),
    data_nasc date,
    filiacao_pai character varying(255),
    filiacao_mae character varying(255),
    registro bigint,
    validade date,
    primeira_hab date,
    cat character varying(10),
    acc integer,
    permissao character varying(50),
    local_nasc character varying(50),
    uf_nasc character varying(2),
    nacionalidade character varying(50),
    CONSTRAINT doc_id_pk_cnh PRIMARY KEY (doc_id)
);

ALTER TABLE IF EXISTS public."Documento"
    ADD CONSTRAINT usuario_id_fk FOREIGN KEY (usuario_id)
    REFERENCES public."Perfil_Usuario" (id_perfil) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Login_table"
    ADD CONSTRAINT usuario_id_fk FOREIGN KEY (usuario_id)
    REFERENCES public."Perfil_Usuario" (id_perfil) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."RG"
    ADD CONSTRAINT doc_id_fk FOREIGN KEY (doc_id)
    REFERENCES public."Documento" (id_doc) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."CNH"
    ADD CONSTRAINT doc_id_fk FOREIGN KEY (doc_id)
    REFERENCES public."Documento" (id_doc) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

CREATE INDEX IF NOT EXISTS idx_id_doc ON "Documento"(id_doc);

CREATE INDEX IF NOT EXISTS idx_email ON "Login_table"(email);
CREATE INDEX IF NOT EXISTS idx_nome_usuario ON "Login_table"(nome_usuario);
CREATE INDEX IF NOT EXISTS idx_id_login ON "Login_table"(id_login);

CREATE INDEX IF NOT EXISTS idx_id_perfil ON "Perfil_Usuario"(id_perfil);
CREATE INDEX IF NOT EXISTS idx_nome ON "Perfil_Usuario"(nome);
CREATE INDEX IF NOT EXISTS idx_data_criacao_conta ON "Perfil_Usuario" USING BRIN (data_criacao_conta);

CREATE INDEX IF NOT EXISTS idx_doc_id_rg ON "RG"(doc_id);
CREATE INDEX IF NOT EXISTS idx_orgao_emissor ON "RG"(orgao_emissor);
CREATE INDEX IF NOT EXISTS idx_rg ON "RG"(rg);
CREATE INDEX IF NOT EXISTS idx_origem_doc ON "RG"(origem_doc);
CREATE INDEX IF NOT EXISTS idx_data_emissao_rg ON "RG" USING BRIN (data_emissao);

CREATE INDEX IF NOT EXISTS idx_doc_id_cnh ON "CNH"(doc_id);
CREATE INDEX IF NOT EXISTS idx_data_emissao_cnh ON "CNH" USING BRIN (data_emissao);
CREATE INDEX IF NOT EXISTS idx_registro ON "CNH"(registro);
CREATE INDEX IF NOT EXISTS idx_validade ON "CNH" USING BRIN (validade);
CREATE INDEX IF NOT EXISTS idx_cat ON "CNH"(cat);
CREATE INDEX IF NOT EXISTS idx_primeira_hab ON "CNH" USING BRIN (primeira_hab);

END;