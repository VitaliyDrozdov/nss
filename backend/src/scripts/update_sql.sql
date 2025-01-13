--------------------------------------------------------------- DWH ------------------------------------------------------------------------------------
--drop schema dborchestrator cascade; -- if exists
create schema if not exists dborchestrator;

-- features - информация о фичах
create table
    if not exists dborchestrator.features (
        feature_name varchar(20) primary key,
        feature_value varchar(20),
        run_id varchar(128) -- Данные поля нужны для формирования витрины, для избежания дублей, исходя из логики ТЗ
,
        quote_id varchar(128) -- Данные поля нужны для формирования витрины, для избежания дублей, исходя из логики ТЗ
    );

comment on table dborchestrator.features is 'Информация о фичах';

comment on column dborchestrator.features.feature_name is 'Наименование фичи';

comment on column dborchestrator.features.feature_value is 'Значение фичи';

comment on column dborchestrator.features.run_id is 'Уникальный идентификатор запроса котировки';

comment on column dborchestrator.features.quote_id is 'Уникальный идентификатор котировки';

insert into
    dborchestrator.features (feature_name, feature_value, run_id, quote_id)
values
    (
        'driver_region',
        'value',
        '123e4567-e89b-12d3-a456-426655440000',
        '123'
    ),
    (
        'driver_kvs',
        'value',
        '123e4567-e89b-12d3-a456-426655440000',
        '123'
    ),
    (
        'driver_gender',
        'value',
        '123e4567-e89b-12d3-a456-426655440000',
        '123'
    ),
    (
        'driver_age',
        'value',
        '123e4567-e89b-12d3-a456-426655440000',
        '123'
    ),
    (
        'driver_bonus',
        'value',
        '123e4567-e89b-12d3-a456-426655440000',
        '123'
    ),
    (
        'feature_name1',
        'value',
        '456e4567-e89b-12d3-a456-426655440000',
        '321'
    ),
    (
        'feature_name2',
        'value',
        '456e4567-e89b-12d3-a456-426655440000',
        '321'
    ),
    (
        'feature_name3',
        'value',
        '456e4567-e89b-12d3-a456-426655440000',
        '321'
    ),
    (
        'feature_name4',
        'value',
        '456e4567-e89b-12d3-a456-426655440000',
        '321'
    ),
    (
        'feature_name5',
        'value',
        '456e4567-e89b-12d3-a456-426655440000',
        '321'
    ),
    (
        'feature_name6',
        'value',
        '345e5780-e89b-12d3-a456-426655440000',
        '231'
    ),
    (
        'feature_name7',
        'value',
        '345e5780-e89b-12d3-a456-426655440000',
        '231'
    ),
    (
        'feature_name8',
        'value',
        '345e5780-e89b-12d3-a456-426655440000',
        '231'
    ),
    (
        'feature_name9',
        'value',
        '345e5780-e89b-12d3-a456-426655440000',
        '231'
    ),
    (
        'feature_name10',
        'value',
        '345e5780-e89b-12d3-a456-426655440000',
        '231'
    );

--select * from dborchestrator.features;
-- products - информация о страховых продуктах
create table
    if not exists dborchestrator.products (id bigint primary key, product_type varchar(50));

comment on table dborchestrator.products is 'Информация о страховых продуктах';

comment on column dborchestrator.products.id is 'Уникальный идентификатор продукта';

comment on column dborchestrator.products.product_type is 'Тип страхового продукта';

insert into
    dborchestrator.products (id, product_type)
values
    (1, 'ОСАГО');

--select * from dborchestrator.products;
-- таблица-связка между features и products
create table
    if not exists dborchestrator.products_feature (product_id bigint, feature_name varchar(20));

comment on table dborchestrator.products_feature is 'Таблица-связка между features и products';

comment on column dborchestrator.products_feature.product_id is 'Уникальный идентификатор продукта';

comment on column dborchestrator.products_feature.feature_name is 'Наименование фичи';

insert into
    dborchestrator.products_feature (product_id, feature_name)
values
    (1, 'driver_region'),
    (1, 'driver_kvs'),
    (1, 'driver_gender'),
    (1, 'driver_age'),
    (1, 'driver_bonus'),
    (1, 'feature_name1'),
    (1, 'feature_name2'),
    (1, 'feature_name3'),
    (1, 'feature_name4'),
    (1, 'feature_name5'),
    (1, 'feature_name6'),
    (1, 'feature_name7'),
    (1, 'feature_name8'),
    (1, 'feature_name9'),
    (1, 'feature_name10');

--select * from dborchestrator.products_feature;
-- Создаем внешний ключ - product_id таблицы products_feature к таблице products
alter table dborchestrator.products_feature add constraint fk_pf_product_id foreign key (product_id) references dborchestrator.products (id);

-- Создаем внешний ключ - feature_name таблицы products_feature к таблице features
alter table dborchestrator.products_feature add constraint fk_pf_feature_name foreign key (feature_name) references dborchestrator.features (feature_name);

-- models - информация о моделях
create table
    if not exists dborchestrator.models (
        id bigint primary key,
        product_id bigint,
        model_name varchar(50),
        foreign key (product_id) references dborchestrator.products (id)
    );

comment on table dborchestrator.models is 'Информация о моделях';

comment on column dborchestrator.models.id is 'Уникальный идентификатор модели';

comment on column dborchestrator.models.product_id is 'Идентификатор продукта по модели';

comment on column dborchestrator.models.model_name is 'Наименование модели';

insert into
    dborchestrator.models (id, product_id, model_name)
values
    (1, 1, 'OSAGO');

--select * from dborchestrator.models;
-- scores - информация о результатах работы моделей
create table
    if not exists dborchestrator.scores (
        model_id bigint,
        predict numeric(17, 16),
        run_id varchar(128),
        quote_id varchar(128),
        foreign key (model_id) references dborchestrator.models (id)
    );

comment on table dborchestrator.scores is 'Информация о результатах работы моделей';

comment on column dborchestrator.scores.model_id is 'Уникальный идентификатор модели';

comment on column dborchestrator.scores.predict is 'Скор-балл';

comment on column dborchestrator.scores.run_id is 'Уникальный идентификатор запроса котировки';

comment on column dborchestrator.scores.quote_id is 'Уникальный идентификатор котировки';

insert into
    dborchestrator.scores (model_id, predict, run_id, quote_id)
values
    (
        1,
        0.2,
        '123e4567-e89b-12d3-a456-426655440000',
        '123'
    ),
    (
        1,
        0.2,
        '456e4567-e89b-12d3-a456-426655440000',
        '321'
    ),
    (
        1,
        0.15,
        '345e5780-e89b-12d3-a456-426655440000',
        '231'
    );

----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
--drop schema dbhadoop cascade; -- if exists
create schema if not exists dbhadoop;

-- contracts - Информация о договорах
create table
    if not exists dbhadoop.contracts (
        id varchar(20) primary key,
        start_date date,
        end_date date,
        is_insurance_case boolean,
        data_insurance_case date,
        run_id varchar(128),
        quote_id varchar(128)
    );

insert into
    dbhadoop.contracts (
        id,
        start_date,
        end_date,
        is_insurance_case,
        data_insurance_case,
        run_id,
        quote_id
    )
values
    (
        '1',
        to_date ('2024-03-31', 'yyyy-mm-dd'),
        to_date ('2025-02-28', 'yyyy-mm-dd'),
        True,
        to_date ('2024-06-15', 'yyyy-mm-dd'),
        '123e4567-e89b-12d3-a456-426655440000',
        '123'
    ),
    (
        '2',
        to_date ('2024-06-30', 'yyyy-mm-dd'),
        to_date ('2025-06-30', 'yyyy-mm-dd'),
        False,
        null,
        '456e4567-e89b-12d3-a456-426655440000',
        '321'
    ),
    (
        '3',
        to_date ('2024-01-31', 'yyyy-mm-dd'),
        to_date ('2025-01-31', 'yyyy-mm-dd'),
        False,
        null,
        '345e5780-e89b-12d3-a456-426655440000',
        '231'
    );

--select * from dbhadoop.contracts;
comment on table dbhadoop.contracts is 'Информация о договорах';

comment on column dbhadoop.contracts.id is 'Идентификатор договора';

comment on column dbhadoop.contracts.start_date is 'Дата начала действия договора';

comment on column dbhadoop.contracts.end_date is 'Дата окончания действия договора';

comment on column dbhadoop.contracts.is_insurance_case is 'Признак наступления события "Страховой случай"';

comment on column dbhadoop.contracts.data_insurance_case is 'Дата наступления события "Страховой случай"';

comment on column dbhadoop.contracts.run_id is 'Уникальный идентификатор запроса котировки';

comment on column dbhadoop.contracts.quote_id is 'Уникальный идентификатор котировки';

----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
--drop schema dwh cascade; -- if exists
create schema if not exists dwh;

create table
    if not exists dwh.raw_contracts (
        id varchar(20) primary key,
        start_date date,
        end_date date,
        is_insurance_case boolean,
        data_insurance_case date,
        run_id varchar(128),
        quote_id varchar(128)
    );

insert into
    dwh.raw_contracts (
        id,
        start_date,
        end_date,
        is_insurance_case,
        data_insurance_case,
        run_id,
        quote_id
    )
select
    *
from
    dbhadoop.contracts;

--select * from dwh.raw_contracts;
comment on table dwh.raw_contracts is 'Информация о договорах';

comment on column dwh.raw_contracts.id is 'Идентификатор договора';

comment on column dwh.raw_contracts.start_date is 'Дата начала действия договора';

comment on column dwh.raw_contracts.end_date is 'Дата окончания действия договора';

comment on column dwh.raw_contracts.is_insurance_case is 'Признак наступления события "Страховой случай"';

comment on column dwh.raw_contracts.data_insurance_case is 'Дата наступления события "Страховой случай"';

comment on column dwh.raw_contracts.run_id is 'Уникальный идентификатор запроса котировки';

comment on column dwh.raw_contracts.quote_id is 'Уникальный идентификатор котировки';

create table
    if not exists dwh.raw_features (
        --id int primary key
        feature_name varchar(20) primary key,
        feature_value varchar(20),
        run_id varchar(128),
        quote_id varchar(128)
    );

insert into
    dwh.raw_features (feature_name, feature_value, run_id, quote_id)
select
    *
from
    dborchestrator.features;

--select * from dwh.raw_features;
comment on table dwh.raw_features is 'Информация о фичах';

comment on column dwh.raw_features.feature_name is 'Наименование фичи';

comment on column dwh.raw_features.feature_value is 'Значение фичи';

comment on column dwh.raw_features.run_id is 'Уникальный идентификатор запроса котировки';

comment on column dwh.raw_features.quote_id is 'Уникальный идентификатор котировки';

-- products - информация о страховых продуктах
create table
    if not exists dwh.raw_products (id bigint primary key, product_type varchar(50));

insert into
    dwh.raw_products (id, product_type)
select
    *
from
    dborchestrator.products;

--select * from dwh.raw_products;
comment on table dwh.raw_products is 'Информация о страховых продуктах';

comment on column dwh.raw_products.id is 'Уникальный идентификатор продукта';

comment on column dwh.raw_products.product_type is 'Тип страхового продукта';

-- таблица-связка между features и products
create table
    if not exists dwh.raw_products_feature (product_id bigint, feature_name varchar(20));

insert into
    dwh.raw_products_feature (product_id, feature_name)
select
    *
from
    dborchestrator.products_feature;

--select * from dwh.raw_products_feature;
comment on table dwh.raw_products_feature is 'Таблица-связка между features и products';

comment on column dwh.raw_products_feature.product_id is 'Уникальный идентификатор продукта';

comment on column dwh.raw_products_feature.feature_name is 'Наименование фичи';

-- Создаем внешний ключ - product_id таблицы products_feature к таблице products
alter table dwh.raw_products_feature add constraint fk_pf_product_id foreign key (product_id) references dwh.raw_products (id);

-- Создаем внешний ключ - feature_name таблицы products_feature к таблице features
alter table dwh.raw_products_feature add constraint fk_pf_feature_name foreign key (feature_name) references dwh.raw_features (feature_name);

-- models - информация о моделях
create table
    if not exists dwh.raw_models (
        id bigint primary key,
        product_id bigint,
        model_name varchar(50),
        foreign key (product_id) references dwh.raw_products (id)
    );

insert into
    dwh.raw_models (id, product_id, model_name)
select
    *
from
    dborchestrator.models;

--select * from dwh.raw_models;
comment on table dwh.raw_models is 'Информация о моделях';

comment on column dwh.raw_models.id is 'Уникальный идентификатор модели';

comment on column dwh.raw_models.product_id is 'Идентификатор продукта по модели';

comment on column dwh.raw_models.model_name is 'Наименование модели';

-- scores - информация о результатах работы моделей
create table
    if not exists dwh.raw_scores (
        model_id bigint,
        predict numeric(17, 16),
        run_id varchar(128),
        quote_id varchar(128),
        foreign key (model_id) references dwh.raw_models (id)
    );

insert into
    dwh.raw_scores (model_id, predict, run_id, quote_id)
select
    *
from
    dborchestrator.scores;

--select * from dwh.raw_scores;
comment on table dwh.raw_scores is 'Информация о результатах работы моделей';

comment on column dwh.raw_scores.model_id is 'Уникальный идентификатор модели';

comment on column dwh.raw_scores.predict is 'Скор-балл';

comment on column dwh.raw_scores.run_id is 'Уникальный идентификатор запроса котировки';

comment on column dwh.raw_scores.quote_id is 'Уникальный идентификатор котировки';

----------------------------------------------------------------------------------------------------------------------------------------------
-- Формирование витрины данных
create table
    if not exists dwh.data_mart (
        product_type varchar(50),
        run_id varchar(128),
        quote_id varchar(128),
        briefcase_date date,
        start_date date,
        end_date date,
        model_name varchar(50),
        feature_name varchar(20),
        feature_value varchar(20),
        predict numeric(17, 16),
        is_insurance_case boolean,
        data_insurance_case date
    );

comment on table dwh.data_mart is 'Витрина данных';

comment on column dwh.data_mart.product_type is 'Тип страхового продукта';

comment on column dwh.data_mart.run_id is 'Уникальный идентификатор запроса котировки';

comment on column dwh.data_mart.quote_id is 'Уникальный идентификатор котировки';

comment on column dwh.data_mart.briefcase_date is 'Дата месячного портфеля';

comment on column dwh.data_mart.start_date is 'Дата начала действия договора';

comment on column dwh.data_mart.end_date is 'Дата окончания действия договора';

comment on column dwh.data_mart.model_name is 'Наименование модели';

comment on column dwh.data_mart.feature_name is 'Наименование фичи';

comment on column dwh.data_mart.feature_value is 'Значение фичи';

comment on column dwh.data_mart.predict is 'Скор-балл';

comment on column dwh.data_mart.is_insurance_case is 'Признак наступления страхового случая';

comment on column dwh.data_mart.data_insurance_case is 'Дата страхового случая';

-- Заполнение данными Витрины (dwh.data_mart) Вариант 1
insert into
    dwh.data_mart (
        product_type,
        run_id,
        quote_id,
        briefcase_date,
        start_date,
        end_date,
        model_name,
        feature_name,
        feature_value,
        predict,
        is_insurance_case,
        data_insurance_case
    )
select
    p.product_type,
    c.run_id,
    c.quote_id,
    to_date ('2024-12-31', 'yyyy-mm-dd') --,:last_day_of_month as portfolio_date -- последний день месяца
,
    c.start_date,
    c.end_date,
    m.model_name,
    f.feature_name,
    f.feature_value,
    s.predict,
    c.is_insurance_case,
    c.data_insurance_case
from
    dwh.raw_contracts c
    join dwh.raw_scores s on c.run_id = s.run_id
    and c.quote_id = s.quote_id
    join dwh.raw_models m on s.model_id = m.id
    join dwh.raw_products p on m.product_id = p.id
    left join dwh.raw_features f on c.run_id = f.run_id
    and c.quote_id = f.quote_id
    --join dwh.raw_products_feature pf on p.id = pf.product_id
    --join dwh.raw_features f on pf.feature_name = f.feature_name
where
    1 = 1
    and c.start_date <= to_date ('2024-12-31', 'yyyy-mm-dd')
    and (
        end_date >= to_date ('2024-12-31', 'yyyy-mm-dd')
        or end_date is null
    )
    --and c.start_date <= :last_day_of_month -- :last_day_of_month - последний день месяца -- Договор активный
    --and (end_date >= :last_day_of_month or end_date is null) -- :last_day_of_month - последний день месяца -- Договор действует на конец месяца
;

--select * from dwh.data_mart;
-- Заполнение данными Витрины (dwh.data_mart) Вариант 2
/*
insert into dwh.data_mart(product_type,run_id,quote_id,briefcase_date,start_date,end_date,model_name,feature_name,feature_value,predict,is_insurance_case,data_insurance_case)
values
('ОСАГО','123e4567-e89b-12d3-a456-426655440000','123',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-03-31','yyyy-mm-dd'),to_date('2025-02-28','yyyy-mm-dd'),'OSAGO','driver_region','value',0.20,true,to_date('2024-06-15','yyyy-mm-dd')),
('ОСАГО','123e4567-e89b-12d3-a456-426655440000','123',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-03-31','yyyy-mm-dd'),to_date('2025-02-28','yyyy-mm-dd'),'OSAGO','driver_kvs','value',0.20,true,to_date('2024-06-15','yyyy-mm-dd')),
('ОСАГО','123e4567-e89b-12d3-a456-426655440000','123',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-03-31','yyyy-mm-dd'),to_date('2025-02-28','yyyy-mm-dd'),'OSAGO','driver_gender','value',0.20,true,to_date('2024-06-15','yyyy-mm-dd')),
('ОСАГО','123e4567-e89b-12d3-a456-426655440000','123',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-03-31','yyyy-mm-dd'),to_date('2025-02-28','yyyy-mm-dd'),'OSAGO','driver_age','value',0.20,true,to_date('2024-06-15','yyyy-mm-dd')),
('ОСАГО','123e4567-e89b-12d3-a456-426655440000','123',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-03-31','yyyy-mm-dd'),to_date('2025-02-28','yyyy-mm-dd'),'OSAGO','driver_bonus','value',0.20,true,to_date('2024-06-15','yyyy-mm-dd')),
('ОСАГО','456e4567-e89b-12d3-a456-426655440000','321',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-06-30','yyyy-mm-dd'),to_date('2025-06-30','yyyy-mm-dd'),'OSAGO','feature_name1','value',0.20,False,null),
('ОСАГО','456e4567-e89b-12d3-a456-426655440000','321',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-06-30','yyyy-mm-dd'),to_date('2025-06-30','yyyy-mm-dd'),'OSAGO','feature_name2','value',0.20,False,null),
('ОСАГО','456e4567-e89b-12d3-a456-426655440000','321',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-06-30','yyyy-mm-dd'),to_date('2025-06-30','yyyy-mm-dd'),'OSAGO','feature_name3','value',0.20,False,null),
('ОСАГО','456e4567-e89b-12d3-a456-426655440000','321',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-06-30','yyyy-mm-dd'),to_date('2025-06-30','yyyy-mm-dd'),'OSAGO','feature_name4','value',0.20,False,null),
('ОСАГО','456e4567-e89b-12d3-a456-426655440000','321',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-06-30','yyyy-mm-dd'),to_date('2025-06-30','yyyy-mm-dd'),'OSAGO','feature_name5','value',0.20,False,null),
('ОСАГО','345e5780-e89b-12d3-a456-426655440000','231',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-01-31','yyyy-mm-dd'),to_date('2025-01-31','yyyy-mm-dd'),'OSAGO','feature_name6','value',0.15,False,null),
('ОСАГО','345e5780-e89b-12d3-a456-426655440000','231',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-01-31','yyyy-mm-dd'),to_date('2025-01-31','yyyy-mm-dd'),'OSAGO','feature_name7','value',0.15,False,null),
('ОСАГО','345e5780-e89b-12d3-a456-426655440000','231',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-01-31','yyyy-mm-dd'),to_date('2025-01-31','yyyy-mm-dd'),'OSAGO','feature_name8','value',0.15,False,null),
('ОСАГО','345e5780-e89b-12d3-a456-426655440000','231',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-01-31','yyyy-mm-dd'),to_date('2025-01-31','yyyy-mm-dd'),'OSAGO','feature_name9','value',0.15,False,null),
('ОСАГО','345e5780-e89b-12d3-a456-426655440000','231',to_date('2024-12-31','yyyy-mm-dd'),to_date('2024-01-31','yyyy-mm-dd'),to_date('2025-01-31','yyyy-mm-dd'),'OSAGO','feature_name10','value',0.15,False,null);


--select * from dwh.data_mart;
 */
----------------------------------------------------------------------------------------------------------------------------------------------
/*
-- logs - Таблица для логов
create table if not exists dwh.logs (
id int primary key
,load_date date
,cnt_raw int
,load_status numeric(1)
,load_err_descr text
);

insert into dwh.logs(id, load_date, cnt_raw, load_status, load_err_descr)
values(1, to_date('2024-12-31','yyyy-mm-dd'), 15, 1, null);

comment on table dwh.logs is 'Логирование загрузки';
comment on column dwh.logs.id is 'Уникальный идентификатор лога';
comment on column dwh.logs.load_date is 'Количество загруженных записей';
comment on column dwh.logs.cnt_raw is 'Результат выполнения операции (1 - успех/0 - ошибка)';
comment on column dwh.logs.load_status is 'Уникальный идентификатор котировки';
comment on column dwh.logs.load_err_descr is 'Описание ошибки (если она имела место)';

--select * from dwh.logs;
 */
--------------------------------------------------------------- Каталог моделей ------------------------------------------------------------------------------------
--drop schema cmodel cascade; -- if exists
create schema if not exists cmodel;

-- models - Каталог моделей
create table
    if not exists cmodel.models (
        model_id int primary key,
        product_id int,
        model_name text,
        status boolean,
        version text,
        description text,
        creation_date timestamp,
        last_launch_date timestamp,
        last_modified_date timestamp,
        foreign key (product_id) references dwh.raw_products (id)
    );

insert into
    cmodel.models (
        model_id,
        product_id,
        model_name,
        status,
        version,
        description,
        creation_date,
        last_launch_date,
        last_modified_date
    )
values
    (
        1,
        1,
        'OSAGO',
        True,
        '1.0',
        'Модель для расчета скоринга по..',
        to_date ('2024-04-12 12:03:00', 'yyyy-mm-dd hh:mi:ss'),
        to_date ('2024-04-12 12:03:00', 'yyyy-mm-dd hh:mi:ss'),
        to_date ('2024-04-12 12:03:00', 'yyyy-mm-dd hh:mi:ss')
    );

--select * from cmodel.models;
comment on table cmodel.models is 'Каталог моделей';

comment on column cmodel.models.model_id is 'Уникальный идентификатор модели';

comment on column cmodel.models.product_id is 'Идентификатор продукта по модели';

comment on column cmodel.models.model_name is 'Наименование модели';

comment on column cmodel.models.status is 'Статус модели(1-включена, 0-отключена)';

comment on column cmodel.models.version is 'Версия модели';

comment on column cmodel.models.description is 'Описание модели';

comment on column cmodel.models.creation_date is 'Дата создания модели';

comment on column cmodel.models.last_launch_date is 'Дата, когда последний раз модель была запущена';

comment on column cmodel.models.last_modified_date is 'Дата, когда последний раз модель была отредактирована';

-- Создаем внешний ключ - product_id таблицы models к таблице products
--alter table cmodel.models
--	add constraint fk_m_product_id foreign key (product_id) references dwh.raw_products(id);
--select * from dwh.logs;
--select * from cmodel.models m join dwh.raw_products p on m.product_id = p.id;
---------------------------------------------
--Observability
--------------------------------------------
CREATE SCHEMA IF NOT EXISTS observability;

CREATE TABLE
    observability.notifications (
        id_notifications SERIAL PRIMARY KEY,
        incident_id INT NOT NULL UNIQUE,
        message TEXT,
        is_read BOOLEAN,
        created_at TIMESTAMP
    );

COMMENT ON TABLE observability.notifications IS 'Таблица хранит информацию о уведомлениях, связанных с инцидентами';

COMMENT ON COLUMN observability.notifications.id_notifications IS 'Уникальный идентификатор уведомления';

COMMENT ON COLUMN observability.notifications.incident_id IS 'Уникальный идентификатор инцидента (внешний ключ)';

COMMENT ON COLUMN observability.notifications.message IS 'Текст уведомления';

COMMENT ON COLUMN observability.notifications.is_read IS 'Флаг, указывающий, было ли уведомление прочитано';

COMMENT ON COLUMN observability.notifications.created_at IS 'Дата и время создания уведомления';

INSERT INTO
    Observability.notifications (incident_id, message, is_read, created_at)
VALUES
    (
        1000,
        'High memory usage detected in Orchestrator service',
        FALSE,
        '2025-01-14 09:30:00'
    ),
    (
        1010,
        'Data quality threshold exceeded in DQ service',
        TRUE,
        '2025-01-14 08:00:00'
    ),
    (
        1020,
        'Unauthorized access attempt in AUTH service',
        FALSE,
        '2025-01-14 10:00:00'
    ),
    (
        1030,
        'UI service is unresponsive',
        FALSE,
        '2025-01-14 07:45:00'
    ),
    (
        1040,
        'Feature service latency is above normal',
        TRUE,
        '2025-01-14 06:00:00'
    ),
    (
        1050,
        'Proxy service experiencing high error rate',
        FALSE,
        '2025-01-14 11:00:00'
    ),
    (
        1060,
        'Model service output mismatch detected',
        FALSE,
        '2025-01-14 12:30:00'
    ),
    (
        1070,
        'Data warehouse (DWH service) query performance degraded',
        TRUE,
        '2025-01-14 05:15:00'
    ),
    (
        1080,
        'Model catalog update failed',
        FALSE,
        '2025-01-14 04:50:00'
    );

CREATE TABLE
    observability.incidents (
        id_incident SERIAL PRIMARY KEY,
        state VARCHAR(50) NOT NULL,
        priority VARCHAR(20) NOT NULL,
        description TEXT,
        last_updated TIMESTAMP NOT NULL,
        service VARCHAR(100) NOT NULL,
        trace_id INT NOT NULL
    );

COMMENT ON TABLE observability.incidents IS 'Таблица содержит информацию о каждом инциденте.';

COMMENT ON COLUMN observability.incidents.id_incident IS 'Уникальный идентификатор инцидента';

COMMENT ON COLUMN observability.incidents.state IS 'Состояние инцидента (Активен, В работе, Завершён)';

COMMENT ON COLUMN observability.incidents.priority IS 'Приоритет (Высокий, Средний, Низкий)';

COMMENT ON COLUMN observability.incidents.description IS 'Описание инцидента';

COMMENT ON COLUMN observability.incidents.last_updated IS 'Дата и время последнего обновления';

COMMENT ON COLUMN observability.incidents.service IS 'Название сервиса';

COMMENT ON COLUMN observability.incidents.trace_id IS 'Уникальный идентификатор трассировки';

INSERT INTO
    Observability.incidents (
        id_incident,
        state,
        priority,
        description,
        last_updated,
        service,
        trace_id
    )
VALUES
    (
        1000,
        'Active',
        'High',
        'Memory usage reached 90% in Orchestrator service',
        '2025-01-14 09:30:00',
        'Orchestrator service',
        1001
    ),
    (
        1010,
        'In Progress',
        'Medium',
        'Data quality check failed for key metrics in DQ service',
        '2025-01-14 08:00:00',
        'DQ service',
        1002
    ),
    (
        1020,
        'Resolved',
        'High',
        'Detected multiple unauthorized login attempts in AUTH service',
        '2025-01-14 10:00:00',
        'AUTH service',
        1003
    ),
    (
        1030,
        'Active',
        'High',
        'UI service stopped responding to requests',
        '2025-01-14 07:45:00',
        'UI service',
        1004
    ),
    (
        1040,
        'In Progress',
        'Low',
        'Feature service response time exceeded 1 second',
        '2025-01-14 06:00:00',
        'Feature service',
        1005
    ),
    (
        1050,
        'Resolved',
        'Medium',
        'Proxy service returning 502 errors for some endpoints',
        '2025-01-14 11:00:00',
        'Proxy service',
        1006
    ),
    (
        1060,
        'Active',
        'High',
        'Model service predictions do not match expected outcomes',
        '2025-01-14 12:30:00',
        'Model service',
        1007
    ),
    (
        1070,
        'Resolved',
        'Medium',
        'Query execution time in DWH service has increased significantly',
        '2025-01-14 05:15:00',
        'DWH service',
        1008
    ),
    (
        1080,
        'In Progress',
        'High',
        'Failed to update model catalog with latest configurations',
        '2025-01-14 04:50:00',
        'Model Catalog service',
        1009
    );

---------------------------------------------
--model_monitoring
--------------------------------------------
CREATE SCHEMA IF NOT EXISTS model_monitoring;

CREATE TABLE
    model_monitoring.report_log (
        id SERIAL PRIMARY KEY,
        model_name VARCHAR(50) NOT NULL,
        metric_name VARCHAR(50) NOT NULL,
        monitoring_type VARCHAR(50) NOT NULL,
        calculation_date TIMESTAMP NOT NULL
    );

COMMENT ON TABLE model_monitoring.report_log IS 'Журнал отчетов о мониторинге моделей';

COMMENT ON COLUMN model_monitoring.report_log.id IS 'Уникальный идентификатор отчета';

COMMENT ON COLUMN model_monitoring.report_log.model_name IS 'Название модели';

COMMENT ON COLUMN model_monitoring.report_log.metric_name IS 'Название метрики';

COMMENT ON COLUMN model_monitoring.report_log.monitoring_type IS 'Тип мониторинга';

COMMENT ON COLUMN model_monitoring.report_log.calculation_date IS 'Дата расчета метрики';

INSERT INTO
    model_monitoring.report_log (
        model_name,
        metric_name,
        monitoring_type,
        calculation_date
    )
VALUES
    (
        'life_insurance',
        'Metric 1',
        'On-demand',
        '2025-01-15 10:00:00'
    ),
    (
        'life_insurance',
        'Metric 2',
        'Scheduled',
        '2025-01-14 14:30:00'
    ),
    (
        'osago',
        'Metric 3',
        'On-demand',
        '2025-01-13 09:00:00'
    ),
    (
        'osago',
        'Metric 4',
        'Scheduled',
        '2025-01-12 16:45:00'
    ),
    (
        'osago',
        'Metric 5',
        'On-demand',
        '2025-01-11 11:15:00'
    ),
    (
        'osago',
        'Metric 6',
        'Scheduled',
        '2025-01-10 13:00:00'
    ),
    (
        'osago',
        'Metric 7',
        'On-demand',
        '2025-01-09 15:30:00'
    ),
    (
        'osago',
        'Metric 8',
        'Scheduled',
        '2025-01-08 10:00:00'
    );
