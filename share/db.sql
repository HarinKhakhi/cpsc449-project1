-- ./bin/init.sh
-- sqlite3 var/uni.sql

PRAGMA foreign_keys=ON;

DROP TABLE IF EXISTS Enrollments;
DROP TABLE IF EXISTS Classes;
DROP TABLE IF EXISTS Instructors;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Admin;

-- ---------------------------------------------

CREATE TABLE Instructors (
   PFCWID INTEGER PRIMARY KEY,
   instructor_name VARCHAR(64) NOT NULL,
   email VARCHAR(64) NOT NULL,
   UNIQUE(email)
);

CREATE TABLE Students (
   cwid INTEGER PRIMARY KEY,
   student_name VARCHAR(64) NOT NULL,
   email VARCHAR(64) NOT NULL,
   UNIQUE(email)
);

CREATE TABLE Admin(
   admin_id INTEGER PRIMARY KEY,
   admin_name VARCHAR(64) NOT NULL,
   email VARCHAR(64) NOT NULL,
   UNIQUE(email)
);

CREATE TABLE Classes (
   class_id INTEGER PRIMARY KEY,
   class_title VARCHAR(255) NOT NULL,
   department VARCHAR(255) NOT NULL,
   section_num INTEGER NOT NULL,
   instructor_cwid INTEGER NOT NULL,
   max_size INTEGER NOT NULL,
   UNIQUE(class_title, section_num)
   FOREIGN KEY (instructor_cwid) REFERENCES instructors(PFCWID)
);

CREATE TABLE Enrollments (
   id INTEGER PRIMARY KEY,
   cwid INTEGER NOT NULL,
   class_id INTEGER NOT NULL,
   status INT2 NOT NULL,
   time DATETIME NOT NULL,
   UNIQUE(cwid,class_id),
   FOREIGN KEY (cwid) REFERENCES students(cwid),
   FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- STUDENT INSERT
INSERT INTO Students(cwid, student_name, email) VALUES (888659596, 'Luis Alvarado', 'lalvarado@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (12345678, 'Nala Alvarado', 'Nalita@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (888321456, 'Ken Dwight', 'Kdwight@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (888987561, 'David Harboyan', 'hdavid@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (878987611, 'Aditya Singh', 'ASingh@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (776967621, 'Harin Khaki', 'HKhaki@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (931965221, 'Donald Novasky', 'DNovasky@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (568796452, 'Carolina Herrera', 'CHerr@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (888456925, 'Mark Gabriel', 'GabrielM@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (564289523, 'Jeorge Lemon', 'JLmon@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (963514785, 'Daemon Knight', 'DKnight@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (987654321, 'Luca Daemon', 'Lucaaaa@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (654987123, 'Illiana Garcia', 'ili@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (123468957, 'Peter Parker', 'Parker@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (987123456, 'Joseph Diaz', 'Jdiaz@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (987873456, 'Joselina Gian', 'JG@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (1876734786, 'Juilian Hernandez', 'JulianHern@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (555875456, 'Karina Duff', 'KDuff21@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (777773956, 'Danny Alvarez', 'AlvarezDanny@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (345600012, 'Andrew Bao', 'BBaoAnd@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (543601013, 'Shawn Mendoza', 'Mendoza@csu.fullerton.edu');
INSERT INTO Students(cwid, student_name, email) VALUES (010123234, 'Camila Cabillo', 'CamCabillo@csu.fullerton.edu');


-- INSTRUCTORS
INSERT INTO Instructors(PFCWID,instructor_name,email)  VALUES(123456, 'Kenyt Avery', 'KAvery@csu.fullerton.edu');
INSERT INTO Instructors(PFCWID,instructor_name,email)  VALUES(123467, 'Paul Invertado', 'PaulInventado@csu.fullerton.edu');
INSERT INTO Instructors(PFCWID,instructor_name,email)  VALUES(213456, 'Rong Jin', 'RJin@csu.fullerton.edu');
INSERT INTO Instructors(PFCWID,instructor_name,email)  VALUES(125689, 'Moe Miller', 'MillerMoe@csu.fullerton.edu');


-- ADMIN
INSERT INTO Admin(admin_id,admin_name,email)  VALUES(123456, 'James Lasely', 'JLasely@csu.fullerton.edu');
INSERT INTO Admin(admin_id,admin_name,email)  VALUES(000123, 'Mike Floyd', 'MFloyd@csu.fullerton.edu');
INSERT INTO Admin(admin_id,admin_name,email)  VALUES(000124, 'Homer Simpson', 'HSimp@csu.fullerton.edu');


--CLASSES
INSERT INTO Classes(class_id, class_title, department, section_num, instructor_cwid, max_size) VALUES (1234,'CPSC101: Into to CS','Computer Science',1,123467,5);
INSERT INTO Classes(class_id, class_title, department, section_num, instructor_cwid, max_size) VALUES (5734,'CPSC449: Into to Back-End','Computer Science',2,123456,10);
INSERT INTO Classes(class_id, class_title, department, section_num, instructor_cwid, max_size) VALUES (6921,'CE-101: Into to Computer Engineering','Computer Engineering',5, 213456,10);
INSERT INTO Classes(class_id, class_title, department, section_num, instructor_cwid, max_size) VALUES (4567,'CRJ-345: Correctional Law','Criminal Justice',1, 125689,10);




--ENROLLMENTS

-- CLASS ID 1234 INSERT
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(888659596, 1234, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(12345678, 1234, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(888321456, 1234, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(888987561, 1234, 0, '2023-01-05 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(987654321, 1234, 0, '2023-01-01 10:00:00.000');
-- WAITLIST
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(123468957, 1234, 1, '2023-06-01 09:30:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(987123456, 1234, 1, '2023-05-01 10:10:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(654987123, 1234, 1, '2023-01-01 09:00:15.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(878987611, 1234, 1, '2023-01-01 09:00:30.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(776967621, 1234, 1, '2023-01-01 08:59:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(931965221, 1234, 1, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(568796452, 1234, 1, '2023-02-01 07:30:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(888456925, 1234, 1, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(564289523, 1234, 1, '2023-01-02 12:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(963514785, 1234, 1, '2023-01-02 12:00:01.000');
-- DROPPED
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(555875456, 1234, 2, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(777773956, 1234, 2, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(345600012, 1234, 2, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(543601013, 1234, 2, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(987873456, 1234, 2, '2023-01-01 10:00:00.000');


-- CLASS ID 5734
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(878987611, 5734, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(776967621, 5734, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(931965221, 5734, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(568796452, 5734, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(888659596, 5734, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(12345678, 5734, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(888321456, 5734, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(888987561, 5734, 0, '2023-01-05 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(987654321, 5734, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(888456925, 5734, 0, '2023-01-01 10:00:00.000');
-- Waitlist
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(564289523, 5734, 1, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(963514785, 5734, 1, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(123468957, 5734, 1, '2023-06-01 09:30:00.000');


--CLASS ID 6921
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(888456925, 6921, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(564289523, 6921, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(963514785, 6921, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(987654321, 6921, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(1876734786, 6921, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(555875456, 6921, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(777773956, 6921, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(345600012, 6921, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(543601013, 6921, 0, '2023-01-01 10:00:00.000');
-- WAITLIST
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(123468957, 6921, 1, '2023-06-01 09:30:00.000');
-- DROPPED
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(987123456, 6921, 2, '2023-05-01 10:10:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(654987123, 6921, 2, '2023-01-01 09:00:15.000');


--CLASS ID 4567
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(555875456, 4567, 0, '2023-06-01 09:30:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(987123456, 4567, 0, '2023-05-01 10:10:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(654987123, 4567, 0, '2023-01-01 09:00:15.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(878987611, 4567, 0, '2023-01-01 09:00:30.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(776967621, 4567, 0, '2023-01-01 08:59:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(931965221, 4567, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(568796452, 4567, 0, '2023-02-01 07:30:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(888456925, 4567, 0, '2023-01-01 10:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(564289523, 4567, 0, '2023-01-02 12:00:00.000');
INSERT INTO Enrollments(cwid, class_id, status, time) VALUES(963514785, 4567, 0, '2023-01-02 12:00:01.000');
