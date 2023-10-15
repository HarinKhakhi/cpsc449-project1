from datetime import datetime
status_to_int = {
    'Enrolled': 0,
    'Waitlisted': 1,
    'Dropped': 2
}

######################### Student #########################
def is_valid_student(db, student_id) -> bool:
    response = db.execute(f"""
        SELECT * 
        FROM Students
        WHERE cwid={student_id}
    """).fetchone()

    if response: return True
    return False
#################################################################

######################### Instructor ############################
def is_valid_instructor(db, instructor_id) -> bool:
    response = db.execute(f"""
        SELECT *
        FROM Instructors
        WHERE PFCWID={instructor_id}
    """).fetchone()

    if response: return True
    return False
#################################################################

########################### Classes #############################
def is_valid_class_title(db, title) -> bool:
    response = db.execute(f"""
        SELECT *
        FROM Classes
        WHERE class_title="{title}"
    """).fetchone()

    if response: return True
    return False


def is_valid_class(db, class_id) -> bool:
    response = db.execute(f"""
        SELECT *
        FROM Classes
        WHERE class_id={class_id}
    """).fetchone()

    if response: return True
    return False


def get_class_info(db, class_id):
    response = db.execute(f"""
        SELECT *
        FROM Classes
        WHERE
            class_id={class_id}
    """).fetchone()

    return response


def get_all_classes(db):
    response = db.execute(f"""
        SELECT *
        FROM Classes
    """).fetchall()

    return response


def get_available_classes(db):    
    available_classes = list()
    classes_fetched = db.execute("SELECT * FROM Classes").fetchall()

    for c in classes_fetched:
        if get_enrollment_count(db, c['class_id']) < c['max_size']:
            available_classes.append(dict(c))

    return available_classes


def get_enrollment_count(db, class_id):
    response = db.execute(f"""
        SELECT *
        FROM Enrollments
        WHERE 
            class_id={class_id}
            AND
            status={status_to_int["Enrolled"]}
    """).fetchall()
    
    return len(response)


def section_exists(db, title, section_num):
    response = db.execute(f"""
        SELECT * 
        FROM Classes
        WHERE
            class_title="{title}"
            AND
            section_num={section_num}
    """).fetchone()

    if response: return True
    return False


def add_class(db, class_info):
    response = db.execute(f"""
        INSERT INTO Classes
        (class_title, department, instructor_cwid, section_num, max_size)
        VALUES
        (
            "{class_info.title}", 
            "{class_info.department}", 
            {class_info.instructor_id}, 
            {class_info.section_num},
            {class_info.max_size}
        )
    """)
    db.commit()

    return response


def update_class(db, id, class_info):
    response = db.execute(
        f"""
            UPDATE Classes
            SET
                class_title=?,
                department=?,
                section_num=?,
                instructor_cwid=?
            WHERE class_id={id}
        """, 
        (class_info.title,class_info.department,class_info.section_num,class_info.instructor_id)
    )
    db.commit()

    return response


def delete_section(db, class_id):
    response = db.execute(f"""
        DELETE FROM Classes
        WHERE class_id={class_id}
    """)
    db.commit()

    return response


def delete_class_title(db, title):
    response = db.execute(f"""
        DELETE FROM Classes
        WHERE class_title="{title}"
    """)
    db.commit()

    return response
#################################################################

########################## Enrollments ##########################
def is_enrolled(db, class_id, student_id) -> bool:
    response = db.execute(f"""
        SELECT *
        FROM Enrollments
        WHERE 
            class_id={class_id}
            AND
            cwid={student_id}
            AND
            (status={status_to_int["Enrolled"]}
            OR
            status={status_to_int["Waitlisted"]})
    """).fetchone()
    
    if response: return True
    return False


def has_dropped(db, class_id, student_id) -> bool:
    response = db.execute(f"""
        SELECT *
        FROM Enrollments
        WHERE 
            class_id={class_id}
            AND
            cwid={student_id}
            AND
            status={status_to_int["Dropped"]}
    """).fetchone()
    
    if response: return True
    return False


def is_class_full(db, class_id) -> bool:
    response = db.execute(f"""
        SELECT COUNT(*)
        FROM Enrollments
        WHERE 
            class_id={class_id}
            AND
            status={status_to_int["Enrolled"]}
    """).fetchone()

    current_enrollments = int(response[0])
    
    response = db.execute(f"""
        SELECT max_size
        FROM Classes
        WHERE 
            class_id={class_id}
    """).fetchone()

    max_enrollments = int(response[0])

    return current_enrollments >= max_enrollments


def get_enrollments(db, class_id, status):
    response = db.execute(f"""
        SELECT * FROM Students
        WHERE CWID IN
        (
            SELECT CWID
            FROM Enrollments
            WHERE 
                class_id={class_id}
                AND
                status={status_to_int[status]}
        )
    """).fetchall()

    return response


def add_enrollment(db, class_id, student_id, status):
    response = db.execute(
        """
            INSERT INTO Enrollments
            (cwid,class_id,status,time)
            VALUES
            (?,?,?,?)
        """,
        (student_id, class_id, status, datetime.now(),)
    )
    db.commit()
    return response


def update_enrollment_status(db, class_id, student_id, status):
    response = db.execute(f"""
        UPDATE Enrollments
        SET Status={status}
        WHERE 
            class_id={class_id}
            AND
            cwid={student_id}
    """)
    db.commit()
    
    return response


def get_enrollment_status(db, class_id, student_id) -> str:
    response = db.execute(f"""
        SELECT status
        FROM Enrollments
        WHERE
            class_id={class_id}
            AND
            cwid={student_id}
    """).fetchone()

    if response: return int_to_status[int(response[0])]
    return None


def get_next_waitlisted(db, class_id):
    response = db.execute(f"""
        SELECT cwid
        FROM Enrollments
        WHERE
            class_id={class_id}
            AND
            status={status_to_int['Waitlisted']}
        ORDER BY time
        LIMIT 1
    """).fetchone()

    if response: return response[0]
    return None


def delete_section_enrollments(db, class_id):
    response = db.execute(f"""
        DELETE FROM Enrollments
        WHERE class_id = {class_id}
    """)
    db.commit()

    return response


def delete_class_enrollments(db, class_title):
    response = db.execute(f"""
        DELETE FROM Enrollments
        WHERE class_id 
        IN (
            SELECT class_id
            FROM Classes
            WHERE class_title="{class_title}"
        )
    """)
    db.commit()

    return response
################################################################


############################ Status ############################
int_to_status = {v:k for k,v in status_to_int.items()}
valid_status = list(status_to_int.keys())
def is_valid_status(status) -> bool:
    return status in valid_status
###########################################################
