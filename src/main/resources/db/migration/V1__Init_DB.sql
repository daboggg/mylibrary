create table hibernate_sequence (next_val bigint) engine=MyISAM;
insert into hibernate_sequence values ( 1 );
insert into hibernate_sequence values ( 1 );

create table book (
    id bigint not null,
    author varchar(255),
    bookname varchar(255),
    filename varchar(255),
    pic_name varchar(255),
    user_id bigint,
    primary key (id)) engine=MyISAM;

create table user_role (
    user_id bigint not null,
    roles varchar(255)) engine=MyISAM;

create table usr (
    id bigint not null,
    active bit not null,
    password varchar(255) not null,
    username varchar(255) not null,
    primary key (id)) engine=MyISAM;

alter table book
    add constraint book_user_fk
    foreign key (user_id)
    references usr (id);

alter table user_role
    add constraint user_role_user_fk
    foreign key (user_id) references usr (id);