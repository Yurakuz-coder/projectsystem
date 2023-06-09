﻿-- Скрипт сгенерирован Devart dbForge Studio for MySQL, Версия 6.0.441.0
-- Домашняя страница продукта: http://www.devart.com/ru/dbforge/mysql/studio
-- Дата скрипта: 18.05.2023 16:57:00
-- Версия сервера: 5.5.25
-- Версия клиента: 4.1

-- 
-- Отключение внешних ключей
-- 
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;

-- 
-- Установка кодировки, с использованием которой клиент будет посылать запросы на сервер
--
SET NAMES 'utf8';

-- 
-- Установка базы данных по умолчанию
--
USE projectsystem;

--
-- Описание для таблицы form_studing
--
DROP TABLE IF EXISTS form_studing;
CREATE TABLE form_studing (
  IDform_st INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  form_stName VARCHAR(100) NOT NULL,
  PRIMARY KEY (IDform_st),
  UNIQUE INDEX UK_form_studing_form_stName (form_stName)
)
ENGINE = INNODB
AUTO_INCREMENT = 4
AVG_ROW_LENGTH = 5461
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Формы обучения';

--
-- Описание для таблицы levels
--
DROP TABLE IF EXISTS levels;
CREATE TABLE levels (
  IDlevels INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  levelsName TINYTEXT NOT NULL,
  PRIMARY KEY (IDlevels),
  UNIQUE INDEX UK_levels_levelsName (levelsName(255))
)
ENGINE = INNODB
AUTO_INCREMENT = 4
AVG_ROW_LENGTH = 5461
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Уровни сформированности компетенций';

--
-- Описание для таблицы positions
--
DROP TABLE IF EXISTS positions;
CREATE TABLE positions (
  IDpositions INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  positionsName VARCHAR(100) NOT NULL,
  PRIMARY KEY (IDpositions),
  UNIQUE INDEX UK_positions_positionsName (positionsName)
)
ENGINE = INNODB
AUTO_INCREMENT = 5
AVG_ROW_LENGTH = 4096
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Должности';

--
-- Описание для таблицы shefforganizations
--
DROP TABLE IF EXISTS shefforganizations;
CREATE TABLE shefforganizations (
  IDshefforg INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  shefforgFirstname VARCHAR(255) NOT NULL,
  shefforgName VARCHAR(255) NOT NULL,
  shefforgFathername VARCHAR(255) DEFAULT NULL,
  shefforgPositions TINYTEXT NOT NULL,
  shefforgDoc TINYTEXT NOT NULL,
  shefforgEmail VARCHAR(100) NOT NULL,
  shefforgPhone VARCHAR(12) NOT NULL,
  Login VARCHAR(100) NOT NULL,
  Pass VARCHAR(100) NOT NULL,
  PRIMARY KEY (IDshefforg),
  INDEX IDX_shefforganizations (shefforgFirstname, shefforgName, shefforgFathername),
  UNIQUE INDEX UK_shefforganizations_Login (Login, Pass)
)
ENGINE = INNODB
AUTO_INCREMENT = 8
AVG_ROW_LENGTH = 3276
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Руководители организаций';

--
-- Описание для таблицы specializations
--
DROP TABLE IF EXISTS specializations;
CREATE TABLE specializations (
  IDspec INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  specShifr VARCHAR(20) NOT NULL,
  specNapravlenie VARCHAR(255) NOT NULL,
  specNapravlennost VARCHAR(255) NOT NULL,
  PRIMARY KEY (IDspec),
  UNIQUE INDEX UK_specializations (specShifr, specNapravlenie, specNapravlennost)
)
ENGINE = INNODB
AUTO_INCREMENT = 9
AVG_ROW_LENGTH = 2730
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Специализации';

--
-- Описание для таблицы stadiaofprojects
--
DROP TABLE IF EXISTS stadiaofprojects;
CREATE TABLE stadiaofprojects (
  IDstadiaofpr INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  stadiaofprName VARCHAR(255) NOT NULL,
  PRIMARY KEY (IDstadiaofpr),
  UNIQUE INDEX UK_stadiaofprojects_stadiaofprName (stadiaofprName)
)
ENGINE = INNODB
AUTO_INCREMENT = 6
AVG_ROW_LENGTH = 3276
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Стадии проекта';

--
-- Описание для таблицы stadiaofworks
--
DROP TABLE IF EXISTS stadiaofworks;
CREATE TABLE stadiaofworks (
  IDstadiaofworks INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  stadiaofworksName VARCHAR(255) NOT NULL,
  PRIMARY KEY (IDstadiaofworks),
  UNIQUE INDEX UK_stadiaofworks_stadiaofworksName (stadiaofworksName)
)
ENGINE = INNODB
AUTO_INCREMENT = 4
AVG_ROW_LENGTH = 5461
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Стадии работы';

--
-- Описание для таблицы competensions
--
DROP TABLE IF EXISTS competensions;
CREATE TABLE competensions (
  IDcompetensions INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDspec INT(11) UNSIGNED NOT NULL,
  competensionsShifr VARCHAR(7) NOT NULL,
  competensionsFull TEXT NOT NULL,
  PRIMARY KEY (IDcompetensions),
  INDEX IDX_competensions_IDspec (IDspec),
  UNIQUE INDEX UK_competensions (IDspec, competensionsShifr),
  CONSTRAINT FK_competensions_specializations_IDspec FOREIGN KEY (IDspec)
    REFERENCES specializations(IDspec) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 14
AVG_ROW_LENGTH = 1638
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Компетенции учебного плана';

--
-- Описание для таблицы groups
--
DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
  IDgroups INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  groupsName VARCHAR(10) NOT NULL,
  groupsYear YEAR(4) NOT NULL,
  IDform_st INT(11) UNSIGNED NOT NULL,
  IDspec INT(11) UNSIGNED NOT NULL,
  PRIMARY KEY (IDgroups),
  UNIQUE INDEX UK_groups_groupsName (groupsName),
  CONSTRAINT FK_groups_form_studing_IDform_st FOREIGN KEY (IDform_st)
    REFERENCES form_studing(IDform_st) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT FK_groups_specializations_IDspec FOREIGN KEY (IDspec)
    REFERENCES specializations(IDspec) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 7
AVG_ROW_LENGTH = 4096
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Группы';

--
-- Описание для таблицы organizations
--
DROP TABLE IF EXISTS organizations;
CREATE TABLE organizations (
  IDorg INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDshefforg INT(11) UNSIGNED NOT NULL,
  orgName TINYTEXT NOT NULL,
  orgYuraddress TINYTEXT NOT NULL,
  orgPostaddress TINYTEXT NOT NULL,
  orgEmail VARCHAR(100) NOT NULL,
  orgPhone VARCHAR(12) NOT NULL,
  PRIMARY KEY (IDorg),
  INDEX IDX_organizations_orgName (orgName(255)),
  UNIQUE INDEX UK_organizations_orgName (orgName(255), orgYuraddress(255)),
  CONSTRAINT FK_organizations_shefforganizations_IDshefforg FOREIGN KEY (IDshefforg)
    REFERENCES shefforganizations(IDshefforg) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 8
AVG_ROW_LENGTH = 3276
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Организации';

--
-- Описание для таблицы sheffofprojects
--
DROP TABLE IF EXISTS sheffofprojects;
CREATE TABLE sheffofprojects (
  IDsheffpr INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDpositions INT(11) UNSIGNED NOT NULL,
  sheffprFirstname VARCHAR(255) NOT NULL,
  sheffprName VARCHAR(255) NOT NULL,
  sheffprFathername VARCHAR(255) DEFAULT NULL,
  sheffprPhone VARCHAR(12) NOT NULL,
  sheffprEmail VARCHAR(100) NOT NULL,
  Login VARCHAR(100) NOT NULL,
  Pass VARCHAR(100) NOT NULL,
  PRIMARY KEY (IDsheffpr),
  INDEX IDX_sheffofprojects_IDpositions (IDpositions),
  INDEX IDX_sheffofprojects_sheffofprojectsFirstname (sheffprFirstname),
  UNIQUE INDEX UK_sheffofprojects (Login, Pass),
  UNIQUE INDEX UK_sheffofprojects2 (IDpositions, sheffprFirstname, sheffprName, sheffprFathername),
  CONSTRAINT FK_sheffofprojects_positions_IDpositions FOREIGN KEY (IDpositions)
    REFERENCES positions(IDpositions) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 9
AVG_ROW_LENGTH = 3276
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Руководители проектов';

--
-- Описание для таблицы initiatorsofprojects
--
DROP TABLE IF EXISTS initiatorsofprojects;
CREATE TABLE initiatorsofprojects (
  IDinitpr INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDorg INT(11) UNSIGNED NOT NULL,
  initprFirstname VARCHAR(255) NOT NULL,
  initprName VARCHAR(255) NOT NULL,
  initprFathername VARCHAR(255) DEFAULT NULL,
  initprPositions TINYTEXT NOT NULL,
  initprEmail VARCHAR(100) NOT NULL,
  initprPhone VARCHAR(12) NOT NULL,
  Login VARCHAR(100) NOT NULL,
  Pass VARCHAR(100) NOT NULL,
  PRIMARY KEY (IDinitpr),
  INDEX IDX_initiatorsofprojects (initprFirstname, initprName, initprFathername),
  UNIQUE INDEX UK_initiatorsofprojects (initprFirstname, initprName, initprFathername, IDorg),
  UNIQUE INDEX UK_initiatorsofprojects2 (Login, Pass),
  CONSTRAINT FK_initiatorsofprojects_organizations_IDorg FOREIGN KEY (IDorg)
    REFERENCES organizations(IDorg) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 5
AVG_ROW_LENGTH = 8192
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Инициаторы проектов';

--
-- Описание для таблицы projectsudycontracts
--
DROP TABLE IF EXISTS projectsudycontracts;
CREATE TABLE projectsudycontracts (
  IDcontracts INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDorg INT(11) UNSIGNED NOT NULL,
  contractsNumber INT(4) UNSIGNED NOT NULL,
  contractsStart DATE DEFAULT NULL,
  contractsFinish DATE DEFAULT NULL,
  contractsPattern VARCHAR(1000) NOT NULL DEFAULT 'C:\\MyProject\\1.docx',
  contractsFull VARCHAR(1000) NOT NULL,
  contractsSigned VARCHAR(1000) DEFAULT NULL,
  PRIMARY KEY (IDcontracts),
  INDEX IDX_projectsudycontracts_IDorg (IDorg),
  UNIQUE INDEX UK_projectsudycontracts_contractsNumber (contractsNumber, contractsStart, contractsFinish),
  CONSTRAINT FK_projectsudycontracts_organizations_IDorg FOREIGN KEY (IDorg)
    REFERENCES organizations(IDorg) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 10
AVG_ROW_LENGTH = 8192
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Договоры об организации проектного обучения';

--
-- Описание для таблицы students
--
DROP TABLE IF EXISTS students;
CREATE TABLE students (
  IDstudents INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDgroups INT(11) UNSIGNED NOT NULL,
  studentsFirstname VARCHAR(255) NOT NULL,
  studentsName VARCHAR(255) NOT NULL,
  studentsFathername VARCHAR(255) DEFAULT NULL,
  studentsStudbook INT(9) UNSIGNED NOT NULL,
  studentsPhone VARCHAR(12) NOT NULL,
  studentsEmail VARCHAR(100) NOT NULL,
  Login VARCHAR(100) NOT NULL,
  Pass VARCHAR(100) NOT NULL,
  PRIMARY KEY (IDstudents),
  INDEX IDX_students_IDgroups (IDgroups),
  UNIQUE INDEX UK_students (Login, Pass),
  UNIQUE INDEX UK_students_studentsStudbook (studentsStudbook),
  UNIQUE INDEX UK_students2 (IDgroups, studentsFirstname, studentsName, studentsFathername, studentsStudbook),
  CONSTRAINT FK_students_groups_IDgroups FOREIGN KEY (IDgroups)
    REFERENCES groups(IDgroups) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 5
AVG_ROW_LENGTH = 4096
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Студенты';

--
-- Описание для таблицы passportofprojects
--
DROP TABLE IF EXISTS passportofprojects;
CREATE TABLE passportofprojects (
  IDpassport INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDinitpr INT(11) UNSIGNED NOT NULL,
  IDsheffpr INT(11) UNSIGNED DEFAULT NULL,
  passportName TINYTEXT NOT NULL,
  passportDate DATE DEFAULT NULL,
  passportProblem TEXT DEFAULT NULL,
  passportPurpose TEXT DEFAULT NULL,
  passportTasks TEXT DEFAULT NULL,
  passportResults TEXT DEFAULT NULL,
  passportContent TEXT DEFAULT NULL,
  passportDeadlines TEXT DEFAULT NULL,
  passportStages TEXT DEFAULT NULL,
  passportResources TEXT DEFAULT NULL,
  passportCost TEXT DEFAULT NULL,
  passportCriteria TEXT DEFAULT NULL,
  passportFormresults TEXT DEFAULT NULL,
  passportPattern VARCHAR(1000) NOT NULL DEFAULT 'C:\\MyProject\\2.docx',
  passportFull VARCHAR(1000) NOT NULL,
  passportSigned VARCHAR(1000) DEFAULT NULL,
  PRIMARY KEY (IDpassport),
  INDEX IDX_passportofprojects_IDinitpr (IDinitpr),
  INDEX IDX_passportofprojects_passportDate (passportDate),
  UNIQUE INDEX UK_passportofprojects (IDinitpr, passportName(255)),
  CONSTRAINT FK_passportofprojects_initiatorsofprojects_IDinitpr FOREIGN KEY (IDinitpr)
    REFERENCES initiatorsofprojects(IDinitpr) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT FK_passportofprojects_sheffofprojects_IDsheffpr FOREIGN KEY (IDsheffpr)
    REFERENCES sheffofprojects(IDsheffpr) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 14
AVG_ROW_LENGTH = 5461
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Паспорта проектов';

--
-- Описание для таблицы projects
--
DROP TABLE IF EXISTS projects;
CREATE TABLE projects (
  IDprojects INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDpassport INT(11) UNSIGNED NOT NULL,
  IDstadiaofpr INT(11) UNSIGNED NOT NULL,
  projectsFull VARCHAR(1000) DEFAULT NULL,
  PRIMARY KEY (IDprojects),
  UNIQUE INDEX UK_projects_IDpassport (IDpassport),
  CONSTRAINT FK_projects_passportofprojects_IDpassport FOREIGN KEY (IDpassport)
    REFERENCES passportofprojects(IDpassport) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT FK_projects_stadiaofprojects_IDstadiaofpr FOREIGN KEY (IDstadiaofpr)
    REFERENCES stadiaofprojects(IDstadiaofpr) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 14
AVG_ROW_LENGTH = 5461
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Проекты';

--
-- Описание для таблицы rolesofprojects
--
DROP TABLE IF EXISTS rolesofprojects;
CREATE TABLE rolesofprojects (
  IDroles INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDpassport INT(11) UNSIGNED NOT NULL,
  rolesRole VARCHAR(500) NOT NULL,
  rolesAmount INT(3) UNSIGNED NOT NULL,
  rolesFunction TEXT NOT NULL,
  rolesCost INT(2) UNSIGNED DEFAULT NULL,
  rolesRequirements TEXT NOT NULL,
  PRIMARY KEY (IDroles),
  INDEX IDX_rolesofprojects_IDpassport (IDpassport),
  UNIQUE INDEX UK_rolesofprojects (IDpassport, rolesRole(255)),
  CONSTRAINT FK_rolesofprojects_passportofprojects_IDpassport FOREIGN KEY (IDpassport)
    REFERENCES passportofprojects(IDpassport) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 14
AVG_ROW_LENGTH = 5461
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Роли в проекте';

--
-- Описание для таблицы applications
--
DROP TABLE IF EXISTS applications;
CREATE TABLE applications (
  IDapplications INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDprojects INT(11) UNSIGNED NOT NULL,
  IDstudents INT(11) UNSIGNED NOT NULL,
  applicationsCourse INT(1) UNSIGNED NOT NULL,
  IDroles INT(11) UNSIGNED NOT NULL,
  applicationsPurpose TEXT DEFAULT NULL,
  applicationsPattern VARCHAR(1000) NOT NULL DEFAULT 'C:\\MyProject\\3.docx',
  applicationsFull VARCHAR(1000) NOT NULL,
  applicationsSigned VARCHAR(1000) DEFAULT NULL,
  applicationApproved TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (IDapplications),
  INDEX IDX_applications_IDprojects (IDprojects),
  UNIQUE INDEX UK_applications (IDprojects, IDstudents),
  CONSTRAINT FK_applications_projects_IDprojects FOREIGN KEY (IDprojects)
    REFERENCES projects(IDprojects) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT FK_applications_rolesofprojects_IDroles FOREIGN KEY (IDroles)
    REFERENCES rolesofprojects(IDroles) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT FK_applications_students_IDstudents FOREIGN KEY (IDstudents)
    REFERENCES students(IDstudents) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 15
AVG_ROW_LENGTH = 4096
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Заявки на участие в проекте';

--
-- Описание для таблицы competensionsinproject
--
DROP TABLE IF EXISTS competensionsinproject;
CREATE TABLE competensionsinproject (
  IDcompetensionspr INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDroles INT(11) UNSIGNED NOT NULL,
  IDcompetensions INT(11) UNSIGNED NOT NULL,
  PRIMARY KEY (IDcompetensionspr),
  CONSTRAINT FK_competensionsinproject_competensions_IDcompetensions FOREIGN KEY (IDcompetensions)
    REFERENCES competensions(IDcompetensions) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT FK_competensionsinproject_rolesofprojects_IDroles FOREIGN KEY (IDroles)
    REFERENCES rolesofprojects(IDroles) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 111
AVG_ROW_LENGTH = 682
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Компетенции в проекте';

--
-- Описание для таблицы specializationsinprojects
--
DROP TABLE IF EXISTS specializationsinprojects;
CREATE TABLE specializationsinprojects (
  IDspecinpr INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDroles INT(11) UNSIGNED NOT NULL,
  IDspec INT(11) UNSIGNED NOT NULL,
  PRIMARY KEY (IDspecinpr),
  CONSTRAINT FK_specializationsinprojects_rolesofprojects_IDroles FOREIGN KEY (IDroles)
    REFERENCES rolesofprojects(IDroles) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT FK_specializationsinprojects_specializations_IDspec FOREIGN KEY (IDspec)
    REFERENCES specializations(IDspec) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 46
AVG_ROW_LENGTH = 1820
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Специализации в проекте';

--
-- Описание для таблицы confirmation
--
DROP TABLE IF EXISTS confirmation;
CREATE TABLE confirmation (
  IDconfirmation INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDapplications INT(11) UNSIGNED NOT NULL,
  confirmationPeriod TINYTEXT NOT NULL,
  confirmationResults TEXT NOT NULL,
  IDlevels INT(11) UNSIGNED NOT NULL,
  confirmationPattern VARCHAR(1000) NOT NULL DEFAULT 'C:\\MyProject\\4.docx',
  confirmationFull VARCHAR(1000) NOT NULL,
  confirmationSigned VARCHAR(1000) DEFAULT NULL,
  PRIMARY KEY (IDconfirmation),
  UNIQUE INDEX UK_confirmation_IDapplications (IDapplications),
  CONSTRAINT FK_confirmation_applications_IDapplications FOREIGN KEY (IDapplications)
    REFERENCES applications(IDapplications) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT FK_confirmation_levels_IDlevels FOREIGN KEY (IDlevels)
    REFERENCES levels(IDlevels) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 7
AVG_ROW_LENGTH = 8192
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Подтверждение участия в проекте';

--
-- Описание для таблицы studentsinprojects
--
DROP TABLE IF EXISTS studentsinprojects;
CREATE TABLE studentsinprojects (
  IDstudentspr INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  IDstudents INT(11) UNSIGNED NOT NULL,
  IDprojects INT(11) UNSIGNED NOT NULL,
  IDroles INT(11) UNSIGNED NOT NULL,
  IDconfirmation INT(11) UNSIGNED DEFAULT NULL,
  IDstadiaofworks INT(11) UNSIGNED NOT NULL,
  studentsinprFull VARCHAR(1000) DEFAULT NULL,
  IDapplications INT(11) UNSIGNED NOT NULL,
  PRIMARY KEY (IDstudentspr),
  INDEX IDX_studentsinprojects_IDstudents (IDstudents),
  UNIQUE INDEX UK_studentsinprojects (IDstudents, IDprojects, IDconfirmation),
  CONSTRAINT FK_studentsinprojects_applications_IDapplications FOREIGN KEY (IDapplications)
    REFERENCES applications(IDapplications) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT FK_studentsinprojects_confirmation_IDconfirmation FOREIGN KEY (IDconfirmation)
    REFERENCES confirmation(IDconfirmation) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT FK_studentsinprojects_projects_IDprojects FOREIGN KEY (IDprojects)
    REFERENCES projects(IDprojects) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT FK_studentsinprojects_rolesofprojects_IDroles FOREIGN KEY (IDroles)
    REFERENCES rolesofprojects(IDroles) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT FK_studentsinprojects_stadiaofworks_IDstadiaofworks FOREIGN KEY (IDstadiaofworks)
    REFERENCES stadiaofworks(IDstadiaofworks) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT FK_studentsinprojects_students_IDstudents FOREIGN KEY (IDstudents)
    REFERENCES students(IDstudents) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 8
AVG_ROW_LENGTH = 4096
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Студенты в проекте';

-- 
-- Вывод данных для таблицы form_studing
--
INSERT INTO form_studing VALUES
(3, 'заочная'),
(1, 'очная'),
(2, 'очно-заочная');

-- 
-- Вывод данных для таблицы levels
--
INSERT INTO levels VALUES
(1, 'Высокий уровень компетенций'),
(2, 'Достаточный уровень компетенций'),
(3, 'Недостаточный уровень компетенций');

-- 
-- Вывод данных для таблицы positions
--
INSERT INTO positions VALUES
(1, 'Администратор'),
(2, 'Доцент кафедры ИВТ'),
(4, 'Профессор кафедры ИВТ'),
(3, 'Старший преподаватель кафедры ИВТ');

-- 
-- Вывод данных для таблицы shefforganizations
--
INSERT INTO shefforganizations VALUES
(1, 'Кузнецов', 'Василий', 'Александрович', 'директор', 'доверенность', 'sibir124@hotmail.com', '+7913197341', 'prazdnik', '358b3ade2fed6f80e801633b056c4d78'),
(3, 'Борисов', 'Алишер', 'Александрович', 'директор', 'доверенность', '432@yandex.ru', '+72334561231', 'boris', '4dbf44c6b1be736ee92ef90090452fc2'),
(4, 'Ляпин', 'Евгений', 'Михайлович', 'директор', 'устав', 'szp@24.ru', '+73912345678', 'lypin', '21d91e97f73f488ea635bd0a63968453'),
(6, 'Михайлова', 'Анастасия', 'Михайловна', 'директор', 'доверенность', 'nastya@mail.ru', '+79762543456', 'nastya', 'f7126b1ce9faf63a53673ccb3de5f653'),
(7, 'Полозов', 'Сергей', 'Геннадьевич', 'директор', 'устав', 'poloz@ya.ru', '+79863217855', 'poloz', '9904176e4e796bb39aee6e83d9d57c3d');

-- 
-- Вывод данных для таблицы specializations
--
INSERT INTO specializations VALUES
(8, '09.03.02', 'Информационные системы и технологии', 'Информационные системы в нефтегазовой отрасли'),
(7, '09.03.02', 'Информационные системы и технологии', 'Информационные системы и технологии в управлении'),
(4, '09.04.01', 'Информатика и вычислительная техника', 'Интеллектуальные системы'),
(3, '09.04.02', 'Информационные системы и технологии', 'Мультимедиатехнологии'),
(5, '09.04.02', 'Информационные системы и технологии', 'Управление данными'),
(6, '09.04.04', 'Программная инженерия', 'Разработка программных комплексов и систем');

-- 
-- Вывод данных для таблицы stadiaofprojects
--
INSERT INTO stadiaofprojects VALUES
(1, 'На рассмотрении'),
(2, 'Одобрено администратором, идёт поиск руководителя'),
(3, 'Поиск участников'),
(5, 'Проект завершён'),
(4, 'Участники найдены, идёт работа над проектом');

-- 
-- Вывод данных для таблицы stadiaofworks
--
INSERT INTO stadiaofworks VALUES
(2, 'В процессе выполнения'),
(1, 'Начата работа'),
(3, 'Работа выполнена');

-- 
-- Вывод данных для таблицы competensions
--
INSERT INTO competensions VALUES
(4, 3, 'УK-1', 'Способен управлять своим временем, выстраивать и реализовывать траекторию саморазвития на основе принципов образования в течении всей жизни'),
(5, 4, 'УK-2', 'Способен определять круг задач в рамах поставленной цели и выбирать оптимальные  способы их \r\nрешения, исходя из действующих правовых норм имеющихся решений и ограничений'),
(6, 3, 'УK-2', 'Способен определять круг задач в рамах поставленной цели и выбирать оптимальные способы их решения, исходя из действующих правовых норм имеющихся решений и ограничений'),
(7, 3, 'УK-3', 'Способен организовывать и руководить работой команды, вырабатывая командную стратегию для \r\nдостижения поставленной цели'),
(8, 4, 'УK-4', 'Способен осуществлять деловую коммуникацию в устной и письменной формах на государственном языке Российской Федерации и иностранном (ых) языке (ах)\r\n'),
(9, 3, 'УK-4', 'Способен осуществлять деловую коммуникацию в устной и письменной формах на государственном языке Российской Федерации и иностранном (ых) языке (ах)\r\n'),
(10, 3, 'УK-5', 'Способен анализировать и учитывать разнообразие культур в процессе межкультурного взаимодействия'),
(11, 3, 'УК-6', 'Способен управлять своим временем, выстраивать и реализовывать траекторию саморазвития на основе принципов образования в течении всей жизни.'),
(12, 3, 'ОПК-1', 'Способен самостоятельно приобретать, развивать и применять математические, естественнонаучные, социально-экономические и профессиональные знания для решения нестандартных задач, в том числе в новой или незнакомой среде и в междисциплинарном контексте'),
(13, 3, 'ПК-1', 'Способен разрабатывать и исследовать модели объектов профессиональной деятельности, предлагать и адаптировать методики, определять качество проводимых исследований, составлять отчеты о проделанной работе, обзоры, готовить публикации\r\n');

-- 
-- Вывод данных для таблицы groups
--
INSERT INTO groups VALUES
(3, 'МИФ22-01', 2022, 1, 3),
(4, 'МИД21-01', 2021, 1, 5),
(5, 'МИИ21-01', 2021, 1, 4),
(6, 'МИИ22-01', 2022, 1, 4);

-- 
-- Вывод данных для таблицы organizations
--
INSERT INTO organizations VALUES
(1, 1, 'ООО "Праздник 1"', '662525, Красноярский край, Емельяновский район, п. Емельяново, ул. Борисова, д. 3', '662525, Красноярский край, Емельяновский район, п. Емельяново, ул. Борисова, д. 2', 'sibir124@hotmail.com', '+73913132244'),
(4, 3, 'КГКУ УСЗН', '662500, Красноярский край, г. Красноярск, пр. Мира, д. 10', '662500, Красноярский край, г. Красноярск, пр. Мира, д. 10', 'uszn21@mail.ru', '+73913123345'),
(5, 4, 'ООО "Орион-Телеком"', '662400, Красноярский край, г. Красноярск, ул. Ленина д. 1, пом. 125', '662400, Красноярский край, г. Красноярск, ул. Ленина д. 1, пом. 125', 'orion@mail.ru', '+73912345665'),
(6, 6, 'ЗАО "Типография №1"', '662598, Красноярский край, г. Красноярск, ул. Борисевича д. 13, пом. 123', '662598, Красноярский край, г. Красноярск, ул. Борисевича д. 13, пом. 123', 'tip1@yandex.ru', '+73912390088'),
(7, 7, 'АО "ИТ-Проф"', '662401, Красноярский край, г. Красноярск, ул. 9 Мая, д. 123, пом. 64', '662401, Красноярский край, г. Красноярск, ул. 9 Мая, д. 123, пом. 64', 'it@prof.ru', '+73912667799');

-- 
-- Вывод данных для таблицы sheffofprojects
--
INSERT INTO sheffofprojects VALUES
(1, 1, 'Козлова', 'Юлия', 'Борисовна', '83912139623', 'iurij.kuznetsov2011@yandex.ru', 'Admin', '9e727fdd3aec8274f46685441900280d'),
(2, 2, 'Козлова', 'Юлия', 'Борисовна', '+78927892144', 'yulya_sib_gau@mail.ru', 'yulia', '03be66295cd7eb6cf6001c9181bb904d'),
(6, 1, 'Зотин', 'Александр', 'Геннадьевич', '+79121973415', 'iu@yandex.ru', '33', '182be0c5cdcd5072bb1864cdee4d3d6e'),
(7, 2, 'Зотин', 'Александр', 'Геннадьевич', '+79137864563', 'zotin@sibsau.ru', 'zotin', '2e15b1ffbb7b73b0c3f2e91c2b3d1aef'),
(8, 2, 'Буряченко', 'Владимир', 'Викторович', '+79927892144', 'buryachenko@sibsau.ru', 'buryachenko', '150b86373c84f2f7f08a890e8ec13f43');

-- 
-- Вывод данных для таблицы initiatorsofprojects
--
INSERT INTO initiatorsofprojects VALUES
(3, 4, 'f', 'f', 'f', 'проба', 'iurij.kuznetsov2011@yandex.ru', '+73912256799', 'а', '0cc175b9c0f1b6a831c399e269772661'),
(4, 1, 'Игорев', 'Игорь', 'Игоревич', 'начальник IT-отдела', 'igor10@mail.ru', '+79123334455', 'igor', 'dd97813dd40be87559aaefed642c3fbb');

-- 
-- Вывод данных для таблицы projectsudycontracts
--
INSERT INTO projectsudycontracts VALUES
(7, 4, 122, '2023-04-13', '2024-04-15', 'test', 'full', 'documents\\Отчет НИП.doc'),
(9, 1, 123, '2023-04-13', '2024-04-15', 'test', 'full', 'documents\\Отчет ПП.doc');

-- 
-- Вывод данных для таблицы students
--
INSERT INTO students VALUES
(1, 4, 'Тимофеев', 'Сергей', 'Николаевич', 125678096, '+79131973415', 'iurij.kuznetsov2011@yandex.ru', '987654321', '6ebe76c9fb411be97b3b0d48b791a7c9'),
(2, 4, 'Сергеев', 'Сергей', 'Николаевич', 123456789, '+79082209565', 'e.star00@mail.ru', '123456789', '25f9e794323b453885f5181f1b624d0b'),
(3, 4, 'Вакарчук', 'Анатолий', 'Петрович', 234489012, '+78927892144', '1@ya.ru', '234489012', '9d6b7e06a07cef69baf2e2b52e43cf49'),
(4, 4, 'Антонов', 'Антон', 'Антонович', 123456780, '+79991233211', 'anton@ya.ru', '123456780', '102a23a0e4661368943dacb516a18cc8');

-- 
-- Вывод данных для таблицы passportofprojects
--
INSERT INTO passportofprojects VALUES
(7, 4, 2, 'Разработка и создание интернет-портала (web-приложения) «Школьные лесничества Красноярского края»', NULL, 'Интернет-портал (web-приложение) «Школьные лесничества Красноярского края» позволит проводить мониторинг деятельности и достижений каждого учащегося школьных лесничеств на протяжении всего периода обучения. Также интернет-портал предоставит широкий спектр возможностей школьным лесничествам для предоставления информации о своей деятельности в сети интернет (новости, статьи, фото и видео с мероприятий и др.)', 'Разработка и создание интернет-портала (web-приложения) для проведения мониторинга деятельности и достижений каждого учащегося школьных лесничеств Красноярского края на протяжении всего периода обучения', '1. Разработка технического задания на разработку интернет-портала (web-приложения)\r\n2. Разработка веб-дизайна интернет-портала (web-приложения)\r\n3. Разработка базы данных\r\n4. Программирование, тестирование и запуск интернет-портала (web-приложения)\r\n5. Администрирование и сопровождение интернет-портала (web-приложения)', 'Интернет-портал (web-приложение) «Школьные лесничества Красноярского края»', 'Техническое задание приложения (структура, возможности учебной платформы). Веб-дизайн мобильного приложения. База данных. Программирование, тестирование и запуск приложения. Администрирование и сопровождение приложения.\r\n', '2024 г.', '2023 г.:\r\n1. Определение и постановка задач. Разработка технического задания (далее ТЗ)\r\n2024 г.:\r\n1. Разработка прототипа структуры и дизайна мобильного приложения в рамках ТЗ \r\n2. Разработка пользовательской части мобильного приложения в частности главной страницы и внутренние страницы приложения\r\n3. Разработка дизайна административной части приложения \r\n4. Вёрстка дизайна пользовательской части приложения\r\n5. Вёрстка дизайна административной части приложения \r\n6. Разработка базы данных приложения\r\n7. Программирование\r\n8. Тестирование приложения\r\n9. Запуск приложения на сервер \r\n10. Сопровождение приложения\r\n11. Доработка выявленных недочетов', 'Материально-техническое обеспечение и информационные ресурсы СибГУ им. М.Ф. Решетнева (ИИТК)', 'Финансирование проекта не предусмотрено', 'Проект оценивается на основе комплексного анализа полученных результатов', 'Результатами проекта является оформленный презентационный материал, согласованный с заказчиком', '', '', ''),
(13, 4, 2, 'Разработка и создание мобильного приложения «Школьные лесничества Красноярского края»', NULL, 'Мобильное приложение «Школьные лесничества Красноярского края» позволит проводить мониторинг деятельности и достижений каждого учащегося школьных лесничеств на протяжении всего периода обучения. Также мобильное приложение предоставит широкий спектр возможностей школьным лесничествам для предоставления информации о своей деятельности в сети интернет (новости, статьи, фото и видео с мероприятий и др.).', 'Разработка и создание мобильного приложения для проведения мониторинга деятельности и достижений каждого учащегося школьных лесничеств Красноярского края на протяжении всего периода обучения', '1. Разработка технического задания на разработку мобильного приложения\r\n2. Разработка веб-дизайна мобильного приложения\r\n3. Разработка базы данных\r\n4. Программирование, тестирование и запуск мобильного приложения\r\n5. Администрирование и сопровождение мобильного приложения', 'Мобильное приложение «Школьные лесничества Красноярского края»', 'Техническое задание приложения (структура, возможности учебной платформы). Веб-дизайн мобильного приложения. База данных. Программирование, тестирование и запуск приложения. Администрирование и сопровождение приложения.', '2024 г.', '2023 г.:\r\n1. Определение и постановка задач. Разработка технического задания (далее ТЗ)\r\n2024 г.:\r\n1. Разработка прототипа структуры и дизайна мобильного приложения в рамках ТЗ \r\n2. Разработка пользовательской части мобильного приложения в частности главной страницы и внутренние страницы приложения\r\n3. Разработка дизайна административной части приложения \r\n4. Вёрстка дизайна пользовательской части приложения\r\n5. Вёрстка дизайна административной части приложения \r\n6. Разработка базы данных приложения\r\n7. Программирование\r\n8. Тестирование приложения\r\n9. Запуск приложения на сервер \r\n10. Сопровождение приложения\r\n11. Доработка выявленных недочетов', 'Материально-техническое обеспечение и информационные ресурсы СибГУ им. М.Ф. Решетнева (ИИТК)', 'Финансирование проекта не предусмотрено', 'Проект оценивается на основе комплексного анализа полученных результатов', 'Результатами проекта является оформленный презентационный материал, согласованный с заказчиком', '', '', '');

-- 
-- Вывод данных для таблицы projects
--
INSERT INTO projects VALUES
(7, 7, 5, NULL),
(13, 13, 3, NULL);

-- 
-- Вывод данных для таблицы rolesofprojects
--
INSERT INTO rolesofprojects VALUES
(8, 7, 'Программист', 2, 'Разаработать интернет-портал', 4, 'Исполнительность'),
(13, 13, 'Программист', 2, 'Разработка мобильного приложения', 3, 'Дисциплинированность');

-- 
-- Вывод данных для таблицы applications
--
INSERT INTO applications VALUES
(6, 7, 2, 2, 8, 'Мне интересна данная работа', '', '', '', 1),
(7, 7, 1, 2, 8, 'Хочу развиваться как программист', '', '', '', 1),
(14, 13, 1, 2, 13, 'Мне хочется развиваться как программист', '', '', '', 1);

-- 
-- Вывод данных для таблицы competensionsinproject
--
INSERT INTO competensionsinproject VALUES
(39, 8, 4),
(40, 8, 6),
(41, 8, 7),
(42, 8, 9),
(43, 8, 10),
(44, 8, 11),
(45, 8, 12),
(46, 8, 13),
(103, 13, 4),
(104, 13, 6),
(105, 13, 7),
(106, 13, 9),
(107, 13, 10),
(108, 13, 11),
(109, 13, 12),
(110, 13, 13);

-- 
-- Вывод данных для таблицы specializationsinprojects
--
INSERT INTO specializationsinprojects VALUES
(28, 8, 4),
(29, 8, 3),
(30, 8, 5),
(43, 13, 4),
(44, 13, 3),
(45, 13, 5);

-- 
-- Вывод данных для таблицы confirmation
--
INSERT INTO confirmation VALUES
(5, 7, 'Весь проект', 'Хорошие результаты', 1, '', '', NULL),
(6, 6, 'Весь период', 'Студент научился программировать', 1, '', '', 'documents\\МИФ21-Кузнецов-НИП.pdf');

-- 
-- Вывод данных для таблицы studentsinprojects
--
INSERT INTO studentsinprojects VALUES
(4, 1, 7, 8, 5, 1, NULL, 7),
(5, 2, 7, 8, 6, 2, 'documents\\Отчет НИП.doc', 6),
(7, 1, 13, 13, NULL, 1, NULL, 14);

-- 
-- Включение внешних ключей
-- 
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;