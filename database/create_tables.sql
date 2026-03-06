CREATE TABLE agendamentos (
    id SERIAL NOT NULL,
    cliente_nome VARCHAR(100) NOT NULL,
    servico VARCHAR(100) NOT NULL,
    data_agendamento DATE NOT NULL,
    hora_agendamento TIME NOT NULL,
    telefone VARCHAR(20),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_agd_id PRIMARY KEY (id),
    CONSTRAINT un_agd_data_hora UNIQUE (data_agendamento, hora_agendamento)
);

select * from agendamentos;