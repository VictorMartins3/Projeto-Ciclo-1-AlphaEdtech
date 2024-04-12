
BEGIN;


CREATE TABLE IF NOT EXISTS public."Documento"
(
    id_doc serial NOT NULL,
    tipo character varying NOT NULL,
    CONSTRAINT id_doc_pk PRIMARY KEY (id_doc)
);

CREATE TABLE IF NOT EXISTS public."Login_table"
(
    id_login serial NOT NULL,
    email character varying(255) NOT NULL,
    nome_usuario character varying(100) NOT NULL,
    senha character varying(255) NOT NULL,
    CONSTRAINT id_login_pk PRIMARY KEY (id_login)
);

CREATE TABLE IF NOT EXISTS public."Perfil_Usuario"
(
    id_perfil serial NOT NULL,
    nome character varying(255) NOT NULL,
    telefone integer NOT NULL,
    endereco text NOT NULL,
    sexo boolean,
    data_criacao_conta timestamp with time zone NOT NULL,
    login_id integer NOT NULL,
    docs_id integer,
    CONSTRAINT id_perfil_pk PRIMARY KEY (id_perfil)
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
    cpf integer,
    origem_doc character varying(255) NOT NULL,
    naturalidade character varying(50) NOT NULL,
    data_nasc date NOT NULL,
    rh boolean,
    observacao text,
    dni integer,
    titulo_eleitor integer,
    zona_eleitoral integer,
    secao_eleitoral integer,
    nis_pis_pasep integer,
    cert_militar integer,
    cnh integer,
    cns integer,
    id_profissional character varying(255),
    ctps integer,
    serie_ctps integer,
    uf_ctps character varying(2),
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
    cpf integer NOT NULL,
    data_nasc date NOT NULL,
    filiacao_pai character varying(255),
    filiacao_mae character varying(255),
    registro integer NOT NULL,
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

ALTER TABLE IF EXISTS public."Perfil_Usuario"
    ADD CONSTRAINT login_id_fk FOREIGN KEY (login_id)
    REFERENCES public."Login_table" (id_login) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Perfil_Usuario"
    ADD CONSTRAINT docs_id_fk FOREIGN KEY (docs_id)
    REFERENCES public."Documento" (id_doc) MATCH SIMPLE
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