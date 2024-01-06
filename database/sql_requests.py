PROFILE_TABLE = '''
--создание таблици профиля
create table if not exists profile
(
    id           serial constraint profile_pk primary key,
    uid          text,
    first_name   text,
    last_name    text,
    email        text,
    active       boolean default false,
    is_deleted   boolean default false,
    created_date timestamp,
    is_superuser boolean default false,
    pass_count   integer,
    update_date  timestamp,
    password     bytea
);

alter table profile
    owner to fp_db_admin;
'''

SESSION_TABLE = '''
--создание таблици сессии

create table if not exists sessions
(
    id                 serial constraint sessions_pk primary key,
    uid                text,
    profile_id         integer,
    ip_address         text,
    created_date       timestamp,
    exp_date           timestamp,
    active             boolean default true,
    blocked            boolean default true,
    user_device        text,
    device_public_keys text
);

alter table sessions
    owner to fp_db_admin;
'''

USER_DATA_PUBLIC_KEYS_TABLE = '''
--создание таблици публичных ключей пользователя
create table if not exists user_data_public_keys
(
    id          serial constraint user_data_public_keys_pk primary key,
    id_user     integer,
    public_key  text,
    private_key text
);

alter table user_data_public_keys
    owner to fp_db_admin;
'''

USER_FILE_TABLE = '''
--создание таблици файлов пользователя
create table if not exists user_files
(
    id            serial constraint user_files_pk primary key,
    profile_id    integer,
    id_folder     integer,
    file_name     text,
    active_delete boolean default false,
    create_date   timestamp,
    date_delete   timestamp,
    content       text
);

alter table user_files
    owner to fp_db_admin;
'''

USER_FOLDER_TABLE = '''
--создание папок пользователя
create table if not exists user_folder
(
    id            serial constraint user_folder_pk primary key,
    profile_id    integer,
    folder_name   text,
    folder_parent integer,
    active_delete boolean default false,
    date_delete   timestamp
);

alter table user_folder
    owner to fp_db_admin;
'''

CONFIRM_CODE_TABLE = '''
--таблица кодов подтверждения пользователей
create table if not exists confirm_code
(
    id           serial constraint confirm_code_pk primary key,
    id_user      integer,
    code         text,
    confirmed    boolean default true,
    created_date timestamp,
    exp_date     timestamp,
    type_code    text
);

alter table confirm_code
    owner to fp_db_admin;
'''