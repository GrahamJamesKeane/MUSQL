drop table if exists WindowCities cascade;

create table WindowCities(
	pID INTEGER primary key not null,
	city text not null,
	pop numeric not null,
	continent text not null
);

insert into WindowCities (pID,city,pop,continent) values 
	(13,'London',10.2,'Europe'),
	(31,'Rio de Janeiro',13.3,'South America'),
	(6,'Delhi',28.5,'Asia'),
	(11,'New York',18.8,'North America'),
	(98,'Tokyo',37.4,'Asia'),
	(198,'Dhaka',19.2,'Asia'),
	(1098,'Lagos',15.9,'Africa'),
	(28,'Paris',10.8,'Europe'),
	(212,'Dar Es Salaam',7.73,'Africa'),
	(111,'Toronto',6.38,'North America'),
	(1112,'Alexandria',5.58,'Africa'),
	(3,'Istanbul',14.7,'Europe'),
	(21,'Buenos Aires',14.4,'South America'),
	(2,'Bangalore',11.4,'Asia'),
	(22,'Shanghai',25.8,'Asia'),
	(222,'Kolkata',15.3,'Asia'),
	(341,'Sao Paulo',10.3,'South America'),
	(3141,'Buenos Aires',13.3,'South America');