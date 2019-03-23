/*==============================================================*/
/* DBMS name:      PostgreSQL 8                                 */
/* Created on:     15.03.2019 21:15:35                          */
/*==============================================================*/


/*==============================================================*/
/* Table: attributes                                            */
/*==============================================================*/
create table attributes (
   attributeid          SERIAL               not null,
   type                 VARCHAR(255)         not null
      constraint CKC_TYPE_ATTRIBUT check (type in ('age','sex','race')),
   value                TEXT                 not null,
   constraint PK_ATTRIBUTES primary key (attributeid)
);

/*==============================================================*/
/* Index: attributes_PK                                         */
/*==============================================================*/
create unique index attributes_PK on attributes (
attributeid
);

/*==============================================================*/
/* Table: maps                                                  */
/*==============================================================*/
create table maps (
   mapid                SERIAL               not null,
   userid               INT4                 not null,
   map                  TEXT                 not null,
   level                INT4                 not null,
   name                 VARCHAR(255)         not null,
   constraint PK_MAPS primary key (mapid)
);

/*==============================================================*/
/* Index: maps_PK                                               */
/*==============================================================*/
create unique index maps_PK on maps (
mapid
);

/*==============================================================*/
/* Index: usersmaps_FK                                          */
/*==============================================================*/
create  index usersmaps_FK on maps (
userid
);

/*==============================================================*/
/* Table: places                                                */
/*==============================================================*/
create table places (
   placeid              SERIAL               not null,
   mapid                INT4                 null,
   y                    FLOAT8               not null,
   x                    FLOAT8               not null,
   name                 VARCHAR(255)         not null,
   constraint PK_PLACES primary key (placeid)
);

/*==============================================================*/
/* Index: places_PK                                             */
/*==============================================================*/
create unique index places_PK on places (
placeid
);

/*==============================================================*/
/* Table: recomendations                                        */
/*==============================================================*/
create table recomendations (
   recomendationid      SERIAL               not null,
   placeid              INT4                 not null,
   message              TEXT                 not null,
   constraint PK_RECOMENDATIONS primary key (recomendationid)
);

/*==============================================================*/
/* Index: recomendations_PK                                     */
/*==============================================================*/
create unique index recomendations_PK on recomendations (
recomendationid
);

/*==============================================================*/
/* Index: placesrecomendations_FK                               */
/*==============================================================*/
create  index placesrecomendations_FK on recomendations (
placeid
);

/*==============================================================*/
/* Table: recomendationsattributes                              */
/*==============================================================*/
create table recomendationsattributes (
   id			        SERIAL               not null,
   attributeid          INT4                 not null,
   recomendationid      INT4                 not null,
   constraint PK_RECOMENDATIONSATTRIBUTES primary key (attributeid, recomendationid)
);

/*==============================================================*/
/* Index: recomendationsattributes_PK                           */
/*==============================================================*/
create unique index recomendationsattributes_PK on recomendationsattributes (
id
);

/*==============================================================*/
/* Index: recomendationsattributes_FK                           */
/*==============================================================*/
create  index recomendationsattributes_FK on recomendationsattributes (
attributeid
);

/*==============================================================*/
/* Index: recomendationsattributes2_FK                          */
/*==============================================================*/
create  index recomendationsattributes2_FK on recomendationsattributes (
recomendationid
);

/*==============================================================*/
/* Table: users                                                 */
/*==============================================================*/
create table users (
   userid               SERIAL               not null,
   password             VARCHAR(40)          not null,
   email                VARCHAR(40)          not null,
   name                 VARCHAR(255)         not null,
   address              VARCHAR(255)         null,
   phone                VARCHAR(20)          null,
   constraint PK_USERS primary key (userid)
);

/*==============================================================*/
/* Index: users_PK                                              */
/*==============================================================*/
create unique index users_PK on users (
userid
);

alter table maps
   add constraint FK_MAPS_USERSMAPS_USERS foreign key (userid)
      references users (userid)
      on delete restrict on update restrict;

alter table places
   add constraint FK_PLACES_REFERENCE_MAPS foreign key (mapid)
      references maps (mapid)
      on delete restrict on update restrict;

alter table recomendations
   add constraint FK_RECOMEND_PLACESREC_PLACES foreign key (placeid)
      references places (placeid)
      on delete restrict on update restrict;

alter table recomendationsattributes
   add constraint FK_RECOMEND_RECOMENDA_ATTRIBUT foreign key (attributeid)
      references attributes (attributeid)
      on delete restrict on update restrict;

alter table recomendationsattributes
   add constraint FK_RECOMEND_RECOMENDA_RECOMEND foreign key (recomendationid)
      references recomendations (recomendationid)
      on delete restrict on update restrict;

