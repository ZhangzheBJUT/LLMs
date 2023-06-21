begin;
DROP TABLE IF EXISTS student;
CREATE TABLE student (
  id serial PRIMARY KEY,
  name text NOT NULL,
  gender text NOT NULL,
  birthday DATE NOT NULL,
  address text NOT NULL,
  phone text NOT NULL
);
COMMENT ON TABLE student IS '学生信息表';
COMMENT ON COLUMN student.id IS '学生ID';
COMMENT ON COLUMN student.name IS '学生姓名';
COMMENT ON COLUMN student.gender IS '学生性别';
COMMENT ON COLUMN student.birthday IS '学生生日';
COMMENT ON COLUMN student.address IS '学生住址';
COMMENT ON COLUMN student.phone IS '学生联系方式';
commit;

SELECT 
    a.attname as 字段名,
    format_type(a.atttypid,a.atttypmod) as 类型, 
    a.attnotnull as 非空, col_description(a.attrelid,a.attnum) as 注释   
FROM 
    pg_class as c,pg_attribute as a 
where 
    a.attrelid = c.oid 
    and 
    a.attnum>0 
    and 
    c.relname = 'student';

INSERT INTO student VALUES 
(1, 'TOM', '男','2001-08-30'::DATE,'China','123'),
(2, 'John', '男','2001-09-30'::DATE,'China','234'),
(3, 'Lucy', '女','2001-07-30'::DATE,'China','345');

SELECT * FROM student;
-----------------------------------------------------

begin;
CREATE TABLE course (
  id serial PRIMARY KEY,
  name text NOT NULL,
  teacher text NOT NULL,
  credit integer NOT NULL
);
COMMENT ON TABLE course IS '学生选修科目表';
COMMENT ON COLUMN course.id IS '科目ID';
COMMENT ON COLUMN course.name IS '科目名称';
COMMENT ON COLUMN course.teacher IS '授课教师';
COMMENT ON COLUMN course.credit IS '科目学分';
commit;

SELECT 
    a.attname as 字段名,
    format_type(a.atttypid,a.atttypmod) as 类型, 
    a.attnotnull as 非空, col_description(a.attrelid,a.attnum) as 注释   
FROM 
    pg_class as c,pg_attribute as a 
where 
    a.attrelid = c.oid 
    and 
    a.attnum>0 
    and 
    c.relname = 'course';

INSERT INTO course VALUES 
(1, '语文', '爱语文', 10),
(2, '数学', '爱数学', 9),
(3, '英语', '爱英语', 8);

SELECT * FROM course;
-----------------------------------------------------


begin;
drop table if exists student_course;
CREATE TABLE student_course (
  id serial PRIMARY KEY,
  student_id integer NOT NULL REFERENCES student(id),
  course_id integer NOT NULL REFERENCES course(id)
);
COMMENT ON TABLE student_course IS '学生选修科目表';
COMMENT ON COLUMN student_course.id IS '关系ID';
COMMENT ON COLUMN student_course.student_id IS '学生ID';
COMMENT ON COLUMN student_course.course_id IS '科目ID';
commit;

SELECT 
    a.attname as 字段名,
    format_type(a.atttypid,a.atttypmod) as 类型, 
    a.attnotnull as 非空, col_description(a.attrelid,a.attnum) as 注释   
FROM 
    pg_class as c,pg_attribute as a 
where 
    a.attrelid = c.oid 
    and 
    a.attnum>0 
    and 
    c.relname = 'student_course';


INSERT INTO student_course VALUES 
(1, 1, 1),
(2, 1, 2),
(3, 2, 2),
(4, 2, 3),
(5, 3, 1);

SELECT * FROM student_course;
-----------------------------------------------------

begin;
CREATE TABLE score (
  id serial PRIMARY KEY,
  student_id integer NOT NULL REFERENCES student(id),
  course_id integer NOT NULL REFERENCES course(id),
  score integer NOT NULL
);
COMMENT ON TABLE score IS '学生成绩表';
COMMENT ON COLUMN score.id IS '成绩ID';
COMMENT ON COLUMN score.student_id IS '学生ID';
COMMENT ON COLUMN score.course_id IS '科目ID';
COMMENT ON COLUMN score.score IS '成绩';
commit;

SELECT 
    a.attname as 字段名,
    format_type(a.atttypid,a.atttypmod) as 类型, 
    a.attnotnull as 非空, col_description(a.attrelid,a.attnum) as 注释   
FROM 
    pg_class as c,pg_attribute as a 
where 
    a.attrelid = c.oid 
    and 
    a.attnum>0 
    and 
    c.relname = 'score';

INSERT INTO score VALUES 
(1, 1, 1, 90),
(2, 1, 2, 80),
(3, 2, 2, 60),
(4, 2, 3, 85),
(5, 3, 1, 76);

SELECT * FROM score;



### Postgres SQL tables, with their properties:
#
# student(id,name,gender,birthday,address,phone)
# course(id,name,teacher,credit)
# student_course(id,student_id,course_id)
# score(id,student_id,course_id,score)
#
### 查询学生TOM的各科目成绩,输出科目名称和分数
SELECT c.name, s.score 
FROM course c 
INNER JOIN student_course sc ON c.id = sc.course_id 
INNER JOIN score s ON sc.id = s.student_course_id 
INNER JOIN student st ON sc.student_id = st.id 
WHERE st.name = 'TOM'


查询各科目的最高分，输出科目名称和相应的最高分数
SELECT c.name AS course_name, MAX(s.score) AS max_score
FROM course AS c
JOIN score AS s ON c.id = s.course_id
GROUP BY c.name;

查询有哪些学生选修了语文课程
SELECT st.name AS student_name
FROM student AS st
JOIN student_course AS sc ON st.id = sc.student_id
JOIN course AS c ON sc.course_id = c.id
WHERE c.name = '语文';


你可以使用以下SQL查询语句来查询学生TOM的各科目成绩，并输出科目名称和分数
SELECT c.name AS subject_name, s.score
FROM student AS st
JOIN student_course AS sc ON st.id = sc.student_id
JOIN course AS c ON sc.course_id = c.id
JOIN score AS s ON st.id = s.student_id AND c.id = s.course_id
WHERE st.name = 'TOM';