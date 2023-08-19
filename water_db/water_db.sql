show databases;
create database water_management;
use water_management;

create table wsc(scid int(11) primary key,availabilty
 int(10),region varchar(40),pipelen int(10),loc varchar
 (40),population double);
 
create table am(pin int,no_building int,
Station_Address varchar(40),
demand int,
ph_no bigint,
email varchar(40),
scid int,
primary key(pin),foreign key(scid) references wsc(scid) on delete cascade);

create table build(bid int primary key,pin int,noh bigint,nop bigint,b_name varchar(20) not null
,consumption double,adrress varchar(80),conn varchar(20),foreign key (pin) references
am(pin));

create table owners(bid int,passwd varchar(20),b_name varchar(20),
primary key(bid,b_name),phno bigint,foreign key(bid) references build(bid) on 
delete cascade);

create table compliants(scid int,bid int,sub varchar(20),complain varchar(100),foreign key(bid) references build(bid) on 
delete cascade,foreign key(scid) references wsc(scid) on delete cascade);

create table bill(bill_no int primary key,scid int,amt double,consumed double,
pay_date date,due_date date,foreign key(scid) references wsc(scid) on delete cascade);

show tables;


insert into wsc values(180,1450,"BANGALORE",8746,"Jalahalli");
desc am;
insert into am values(560043,789,"Banaswadi",79.87,8881110043,"bwwsc@gov.in",180);
insert into am values(560050,867,"Banashankari",87.65,8881110050,"bshwsc@gov.in",180);
insert into am values(560093,589,"C.V.raman nagar",58.87,8881110093,"cvrnwsc@gov.in",180);
insert into am values(560037,1156,"Doddanekkundi",101.57,8881110037,"bwwsc@gov.in",180);
insert into am values(560024,981,"Hebbal",95.787,8881110024,"hbwsc@gov.in",180);
insert into am values(560038,1456,"Indirnagar",114.59,8881110038,"inwsc@gov.in",180);
insert into am values(562125,789,"Sarjapura",78.97,8881112125,"srwsc@gov.in",180);
insert into am values(560064,971,"Yelahanka",99.79,8881110064,"ylwsc@gov.in",180);
update am set email="ddwsc@gov.in" where pin=560037;
select * from am;
desc build;
insert into build values(4301,560043,18,87,"Nilam",360,"5th cross, st. road","yes");
insert into build values(3701,560037,15,54,"jannat",300,"8th stret, br road","yes");

select * from build where bid=4301 and pin=560043;




