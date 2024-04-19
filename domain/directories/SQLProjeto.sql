BEGIN;


CREATE TABLE IF NOT EXISTS public."Documento"
(
    id_doc serial NOT NULL,
    tipo character varying(50) NOT NULL,
    usuario_id integer NOT NULL,
    CONSTRAINT id_doc_pk PRIMARY KEY (id_doc)
);

CREATE TABLE IF NOT EXISTS public."Usuario"
(
    id_usuario serial NOT NULL,
    email character varying(255) NOT NULL,
    senha character varying(255) NOT NULL,
    nome character varying(255) NOT NULL,
    telefone bigint,
    endereco text,
    sexo boolean,
    data_criacao_conta timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT id_usuario_pk PRIMARY KEY (id_usuario)
);

CREATE TABLE IF NOT EXISTS public."RG"
(
    doc_id integer NOT NULL,
    foto bytea NOT NULL,
    assinatura bytea,
    orgao_emissor character varying(255) NOT NULL,
    data_emissao date NOT NULL,
    rg character varying(50) NOT NULL,
    nome character varying(255) NOT NULL,
    filiacao_pai character varying(255),
    filiacao_mae character varying(255),
    cpf character varying(20),
    origem_doc character varying(255) NOT NULL,
    naturalidade character varying(50) NOT NULL,
    data_nasc date NOT NULL,
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
    doc_id integer NOT NULL,
    nome character varying(255) NOT NULL,
    foto bytea NOT NULL,
    observacao text,
    data_emissao date NOT NULL,
    localizacao character varying(100) NOT NULL,
    rg character varying(50) NOT NULL,
    orgao_emissor_rg character varying(255) NOT NULL,
    uf_rg character varying(2) NOT NULL,
    cpf character varying(20) NOT NULL,
    data_nasc date NOT NULL,
    filiacao_pai character varying(255),
    filiacao_mae character varying(255),
    registro bigint NOT NULL,
    validade date NOT NULL,
    primeira_hab date NOT NULL,
    cat character varying(10) NOT NULL,
    acc integer,
    permissao character varying(50),
    local_nasc character varying(50),
    uf_nasc character varying(2),
    nacionalidade character varying(50),
    CONSTRAINT doc_id_pk_cnh PRIMARY KEY (doc_id)
);

ALTER TABLE IF EXISTS public."Documento"
    ADD CONSTRAINT usuario_id_fk FOREIGN KEY (usuario_id)
    REFERENCES public."Usuario" (id_usuario) MATCH SIMPLE
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

CREATE INDEX IF NOT EXISTS idx_email ON "Usuario"(email);
CREATE INDEX IF NOT EXISTS idx_id_usuario ON "Usuario"(id_usuario);
CREATE INDEX IF NOT EXISTS idx_nome ON "Usuario"(nome);
CREATE INDEX IF NOT EXISTS idx_data_criacao_conta ON "Usuario" USING BRIN (data_criacao_conta);

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