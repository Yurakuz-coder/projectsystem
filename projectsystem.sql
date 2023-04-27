-- Скрипт сгенерирован Devart dbForge Studio for MySQL, Версия 6.0.441.0
-- Домашняя страница продукта: http://www.devart.com/ru/dbforge/mysql/studio
-- Дата скрипта: 20.04.2023 23:53:02
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
AUTO_INCREMENT = 1
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
AUTO_INCREMENT = 4
AVG_ROW_LENGTH = 8192
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
AUTO_INCREMENT = 6
AVG_ROW_LENGTH = 5461
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
AUTO_INCREMENT = 1
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
AUTO_INCREMENT = 1
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
AUTO_INCREMENT = 4
AVG_ROW_LENGTH = 5461
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
AUTO_INCREMENT = 6
AVG_ROW_LENGTH = 5461
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
AUTO_INCREMENT = 5
AVG_ROW_LENGTH = 8192
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
    REFERENCES positions(IDpositions) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 2
AVG_ROW_LENGTH = 16384
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
    REFERENCES organizations(IDorg) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 1
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
    REFERENCES organizations(IDorg) ON DELETE RESTRICT ON UPDATE RESTRICT
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
  studentsStudbook INT(9) NOT NULL,
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
AUTO_INCREMENT = 1
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
    REFERENCES initiatorsofprojects(IDinitpr) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT FK_passportofprojects_sheffofprojects_IDsheffpr FOREIGN KEY (IDsheffpr)
    REFERENCES sheffofprojects(IDsheffpr) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 1
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
    REFERENCES passportofprojects(IDpassport) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT FK_projects_stadiaofprojects_IDstadiaofpr FOREIGN KEY (IDstadiaofpr)
    REFERENCES stadiaofprojects(IDstadiaofpr) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 1
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
    REFERENCES passportofprojects(IDpassport) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 1
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
  PRIMARY KEY (IDapplications),
  INDEX IDX_applications_IDprojects (IDprojects),
  UNIQUE INDEX UK_applications (IDprojects, IDstudents),
  CONSTRAINT FK_applications_projects_IDprojects FOREIGN KEY (IDprojects)
    REFERENCES projects(IDprojects) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT FK_applications_rolesofprojects_IDroles FOREIGN KEY (IDroles)
    REFERENCES rolesofprojects(IDroles) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT FK_applications_students_IDstudents FOREIGN KEY (IDstudents)
    REFERENCES students(IDstudents) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 1
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
    REFERENCES competensions(IDcompetensions) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT FK_competensionsinproject_rolesofprojects_IDroles FOREIGN KEY (IDroles)
    REFERENCES rolesofprojects(IDroles) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 1
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
    REFERENCES rolesofprojects(IDroles) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT FK_specializationsinprojects_specializations_IDspec FOREIGN KEY (IDspec)
    REFERENCES specializations(IDspec) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 1
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
    REFERENCES applications(IDapplications) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT FK_confirmation_levels_IDlevels FOREIGN KEY (IDlevels)
    REFERENCES levels(IDlevels) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 1
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
  IDconfirmation INT(11) UNSIGNED NOT NULL,
  IDstadiaofworks INT(11) UNSIGNED NOT NULL,
  studentsinprFull VARCHAR(1000) DEFAULT NULL,
  PRIMARY KEY (IDstudentspr),
  INDEX IDX_studentsinprojects_IDstudents (IDstudents),
  UNIQUE INDEX UK_studentsinprojects (IDstudents, IDprojects, IDconfirmation),
  CONSTRAINT FK_studentsinprojects_confirmation_IDconfirmation FOREIGN KEY (IDconfirmation)
    REFERENCES confirmation(IDconfirmation) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT FK_studentsinprojects_projects_IDprojects FOREIGN KEY (IDprojects)
    REFERENCES projects(IDprojects) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT FK_studentsinprojects_rolesofprojects_IDroles FOREIGN KEY (IDroles)
    REFERENCES rolesofprojects(IDroles) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT FK_studentsinprojects_stadiaofworks_IDstadiaofworks FOREIGN KEY (IDstadiaofworks)
    REFERENCES stadiaofworks(IDstadiaofworks) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT FK_studentsinprojects_students_IDstudents FOREIGN KEY (IDstudents)
    REFERENCES students(IDstudents) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 1
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

-- Таблица projectsystem.levels не содержит данных

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
(1, 'Кузнецов', 'Юрий', 'Александрович', 'начальник', 'Доверенность', 'iurij.kuznetsov2011@yandex.ru', '+7913197341', 'Admin', '9e727fdd3aec8274f46685441900280d'),
(3, 'Борисов', 'Алишер', 'Александрович', 'директор', 'доверенность', '432@yandex.ru', '+72334561231', 'Boris', '4dbf44c6b1be736ee92ef90090452fc2');

--
-- Вывод данных для таблицы specializations
--
INSERT INTO specializations VALUES
(4, '09.04.01', 'Информатика и вычислительная техника', 'Интеллектуальные системы'),
(3, '09.04.02', 'Информационные системы и технологии', 'Мультимедиатехнологии'),
(5, '09.04.02', 'Информационные системы и технологии', 'Управление данными');

--
-- Вывод данных для таблицы stadiaofprojects
--

-- Таблица projectsystem.stadiaofprojects не содержит данных

--
-- Вывод данных для таблицы stadiaofworks
--

-- Таблица projectsystem.stadiaofworks не содержит данных

--
-- Вывод данных для таблицы competensions
--
INSERT INTO competensions VALUES
(1, 4, 'ПК-1', 'Способен критически воспринимать информацию'),
(2, 3, 'ПК-1', 'Способен думать'),
(3, 4, 'ПК-2', 'Плавать');

--
-- Вывод данных для таблицы groups
--
INSERT INTO groups VALUES
(3, 'МИФ22-01', 2022, 1, 3),
(4, 'МИД21-01', 2021, 1, 5),
(5, 'МИИ21-01', 2021, 1, 4);

--
-- Вывод данных для таблицы organizations
--
INSERT INTO organizations VALUES
(1, 1, 'ООО "Праздник 1"', '662525, Красноярский край, Емельяновский район, п. Емельяново, ул. Борисова, д. 2', '662525, Красноярский край, Емельяновский район, п. Емельяново, ул. Борисова, д. 2', 'sibir124@hotmail.com', '+73913132244'),
(4, 3, 'ТО КГКУ УСЗН', 'Красноярск', 'Красноярск', 'uszn21@mail.ru', '+73913123345');

--
-- Вывод данных для таблицы sheffofprojects
--
INSERT INTO sheffofprojects VALUES
(1, 1, 'Козлова', 'Юлия', 'Борисовна', '83912139623', 'yulya_sib_gau@mail.ru\r\n', 'Admin', '9e727fdd3aec8274f46685441900280d');

--
-- Вывод данных для таблицы initiatorsofprojects
--

-- Таблица projectsystem.initiatorsofprojects не содержит данных

--
-- Вывод данных для таблицы projectsudycontracts
--
INSERT INTO projectsudycontracts VALUES
(7, 4, 122, '2023-04-13', '2024-04-15', 'test', 'full', NULL),
(9, 1, 123, '2023-04-13', '2024-04-15', 'test', 'full', NULL);

--
-- Вывод данных для таблицы students
--

-- Таблица projectsystem.students не содержит данных

--
-- Вывод данных для таблицы passportofprojects
--

-- Таблица projectsystem.passportofprojects не содержит данных

--
-- Вывод данных для таблицы projects
--

-- Таблица projectsystem.projects не содержит данных

--
-- Вывод данных для таблицы rolesofprojects
--

-- Таблица projectsystem.rolesofprojects не содержит данных

--
-- Вывод данных для таблицы applications
--

-- Таблица projectsystem.applications не содержит данных

--
-- Вывод данных для таблицы competensionsinproject
--

-- Таблица projectsystem.competensionsinproject не содержит данных

--
-- Вывод данных для таблицы specializationsinprojects
--

-- Таблица projectsystem.specializationsinprojects не содержит данных

--
-- Вывод данных для таблицы confirmation
--

-- Таблица projectsystem.confirmation не содержит данных

--
-- Вывод данных для таблицы studentsinprojects
--

-- Таблица projectsystem.studentsinprojects не содержит данных

--
-- Включение внешних ключей
--
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
INSERT INTO projectsystem.stadiaofprojects
(IDstadiaofpr, stadiaofprName)
VALUES(1, 'На рассмотрении');
INSERT INTO projectsystem.stadiaofprojects
(IDstadiaofpr, stadiaofprName)
VALUES(2, 'Участники найдены, идет работа над проектом');
INSERT INTO projectsystem.stadiaofprojects
(IDstadiaofpr, stadiaofprName)
VALUES(3, 'Одобрено администратором, идет поиск руководителя');
INSERT INTO projectsystem.stadiaofprojects
(IDstadiaofpr, stadiaofprName)
VALUES(4, 'Поиск участников');
INSERT INTO projectsystem.stadiaofprojects
(IDstadiaofpr, stadiaofprName)
VALUES(5, 'Проект завершен');
