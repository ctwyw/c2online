/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2012-7-31 14:37:07                           */
/*==============================================================*/


drop table if exists c2_admin;

drop table if exists c2_files;

drop table if exists c2_log;

drop table if exists c2_project;

drop table if exists c2_revision;

drop table if exists c2_server;

/*==============================================================*/
/* Table: c2_admin                                              */
/*==============================================================*/
create table c2_admin
(
   adm_id               int not null auto_increment,
   adm_user             varchar(30) not null,
   adm_pass             char(32) not null,
   adm_status           tinyint(1) not null default 1 comment '1-���ã�2-����',
   adm_dateline         int not null,
   adm_auth             tinyint(1) not null default 0 comment '1-�ܹ���Ա 0-һ��ʹ����',
   primary key (adm_id)
)
type = MYISAM;

insert into c2_admin values(null, 'admin', 'a66abb5684c45962d887564f08346e8d', 1, '1336374061', 1);

/*==============================================================*/
/* Table: c2_files                                              */
/*==============================================================*/
create table c2_files
(
   f_id                 int not null auto_increment,
   r_id                 int,
   f_action             char(1) not null,
   f_path               varchar(250) not null,
   f_ver                varchar(10) not null,
   primary key (f_id)
)
type = MYISAM;

/*==============================================================*/
/* Table: c2_log                                                */
/*==============================================================*/
create table c2_log
(
   h_id                 int not null auto_increment,
   r_no                 varchar(30) not null,
   s_id                 int,
   r_id                 int,
   s_name               varchar(30) not null,
   r_dateline           int not null,
   primary key (h_id)
)
type = MYISAM;

/*==============================================================*/
/* Table: c2_project                                            */
/*==============================================================*/
create table c2_project
(
   p_id                 int not null auto_increment,
   p_name               varchar(20) not null,
   p_vcspath            varchar(120) not null comment 'svn��git��',
   p_user               varchar(30) not null comment '��Ӧ���˺�',
   p_pass               varchar(30) not null comment '��Ӧ������',
   p_status             tinyint not null default 2 comment '1-���� 2-�ر�',
   p_cdateline          int not null,
   primary key (p_id)
)
type = MYISAM;

/*==============================================================*/
/* Table: c2_revision                                           */
/*==============================================================*/
create table c2_revision
(
   r_id                 int not null auto_increment,
   p_id                 int,
   r_no                 varchar(30) not null,
   s_id                 int not null,
   s_name               varchar(30) not null,
   r_dateline           int not null,
   r_cdateline          int not null,
   r_status             tinyint not null default 1 comment '1-������ 2-ɾ�� 3-�ѷ��� 4-�ѻع�',
   primary key (r_id)
)
type = MYISAM;

/*==============================================================*/
/* Table: c2_server                                             */
/*==============================================================*/
create table c2_server
(
   s_id                 int not null auto_increment,
   p_id                 int,
   s_name               varchar(30) not null,
   s_host               char(25) not null,
   s_user               varchar(30) not null,
   s_pass               varchar(30) not null,
   s_vpn                char(25) not null,
   s_vpnuser            varchar(30) not null,
   s_vpnpass            varchar(30) not null,
   s_vpnpro             tinyint not null default 1 comment '1-pptp',
   s_pdir               varchar(255) not null comment '�����Ŀ��Ӧ�������ַ',
   s_bdir               varchar(255) not null comment '��ŷ���ʱ��Ӧ�������ַ',
   s_status             tinyint not null default 2 comment '1-������2-�ر�',
   s_cdateline          int not null,
   p_name               varchar(20) not null,
   primary key (s_id)
)
type = MYISAM;
