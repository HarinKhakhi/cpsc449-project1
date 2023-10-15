import sqlite3
import contextlib

from fastapi import FastAPI, Depends
from fastapi import status as webStatus
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import Optional

import utils

app = FastAPI()
DATABASE = "./var/mock.db"

freeze_autoenroll = False

# Helper function to connect to the db
def get_db():
    with contextlib.closing(sqlite3.connect(DATABASE)) as db:
        db.row_factory = sqlite3.Row
        yield db


@app.get("/classes")
def list_available_classes(only_available:bool = True, db: sqlite3.Connection = Depends(get_db)):
    # retrieve classes based on the request
    if only_available:
        response = utils.get_available_classes(db)

        return JSONResponse(
            status_code=webStatus.HTTP_200_OK,
            content={
                'message': f'All Available Classes',
                'body': response
            }
        )
    else:
        response = utils.get_all_classes(db)

    # generating return object
    classes = []
    for row in response:
        classes.append(dict(row))

    return JSONResponse(
        status_code=webStatus.HTTP_200_OK,
        content={
            'message': f'All Classes',
            'body': classes
        }
    )


class ClassInfoModel(BaseModel):
    title: str
    section_num: int
    department: str
    instructor_id: int
    max_size: int = 30
@app.post('/classes/add')
def add_class_section(class_info: ClassInfoModel, db: sqlite3.Connection = Depends(get_db)):
    
    # check if instructor_id is valid
    if not utils.is_valid_instructor(db, class_info.instructor_id):
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'messsage': f'instructor with id={class_info.instructor_id} does not exist!',
                'body': {}
            }
        )

    # check if that section_id already exist
    if utils.section_exists(db, class_info.title, class_info.section_num):
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'class with title={class_info.title} and section_num={class_info.section_num} already exists',
                'body': {}
            }
        )

    # add the class in table
    response = utils.add_class(db, class_info)

    return JSONResponse(
        status_code=webStatus.HTTP_200_OK,
        content={
            'message': 'successfully added class',
            'body': {}
        }
    )


@app.delete('/classes/delete')
def remove_class_all_section(title, db: sqlite3.Connection = Depends(get_db)):

    # check if class_id is valid
    if not utils.is_valid_class_title(db, title):
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'class with title={title} not found',
                'body': {}
            }
        )

    # delete all enrollements for that class title
    response = utils.delete_class_enrollments(db, title)

    # delete all sections related to that class title
    response = utils.delete_class_title(db, title)

    return JSONResponse(
        status_code=webStatus.HTTP_200_OK,
        content={
            'message': f'all classes with title={title} deleted',
            'body': {}
        }
    )


@app.put('/classes/freeze-autoenroll')
def set_autoenroll(set: Optional[bool] = None):
    global freeze_autoenroll
    if set and set != 'false':
        freeze_autoenroll = True
    else:
        freeze_autoenroll = False

    return JSONResponse(
        status_code=webStatus.HTTP_200_OK,
        content={
            'message': f'successfully set the status freeze_autoenroll = {freeze_autoenroll}',
            'body': {}
        }
    )


@app.put('/class/{id}/enroll')
def enroll_into_class(id, student_id, db: sqlite3.Connection = Depends(get_db)):

    # check if valid class id
    if not utils.is_valid_class(db, id):
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'class with id={id} does not exist',
                'body': {}
            }
        )

    # check if valid student id
    if not utils.is_valid_student(db, student_id):
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'student with cwid={student_id} does not exist',
                'body': {}
            }
        )
    
    curr_enrollment_status = utils.get_enrollment_status(db, id, student_id)

    # check if student is already enrolled or currently waitlisted
    if curr_enrollment_status in ['Enrolled', 'Waitlisted']:
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'student({student_id}) is already enrolled in course({id}) with status={curr_enrollment_status}',
                'body': {}
            }
        )
    # check if student previously dropped this course
    elif curr_enrollment_status == 'Dropped' and utils.is_class_full(db, id):
        # then update the status (instead of adding new entry)
        response = utils.update_enrollment_status(db,
            class_id=id,
            student_id=student_id,
            status=utils.status_to_int['Enrolled']
        )

        return JSONResponse(
            status_code=webStatus.HTTP_200_OK,
            content={
                'message': f'status of enrollment of student({student_id}) for course({id}) is now Enrolled',
                'body': {
                    'status': 'Enrolled'
                }
            } 
        )
    # the reason program reached here means, there is no entry for the student
    # adding a new entry in enrollments
    else:
        # figuring out the status of enrollment
        # Enrolled if class is not full
        # Waitlisted if class is full
        is_full = utils.is_class_full(db, id)
        status = utils.status_to_int['Waitlisted'] if is_full else utils.status_to_int['Enrolled']

        # adding new entry with correct status
        response = utils.add_enrollment(db,
            class_id=id,
            student_id=student_id,
            status=status
        )

        return JSONResponse(
            status_code=webStatus.HTTP_200_OK,
            content={
                'message': f'status of enrollment of student({student_id}) for course({id}) is {utils.int_to_status[status]}',
                'body': {
                    'status': utils.int_to_status[status]
                }
            }
        )


@app.put('/class/{id}/drop')
def drop_students(id, student_id, db: sqlite3.Connection = Depends(get_db)):
    
    # check if valid class id
    if not utils.is_valid_class(db, id):
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'class with id={id} does not exist',
                'body': {}
            }
        )

    # check if valid student id
    if not utils.is_valid_student(db, student_id):
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'student with cwid={student_id} does not exist',
                'body': {}
            }
        )
    
    # check if student is enrolled in that course
    if not utils.is_enrolled(db, id, student_id) and utils.get_enrollment_status(db, id, student_id) != "Waitlisted":
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'student:{student_id} is not enrolled in class:{id}',
                'body': {}
            }
        )

    # update the status for that enrollment
    response = utils.update_enrollment_status(db, 
        class_id=id, 
        student_id=student_id, 
        status=utils.status_to_int['Dropped']
    )

    # get the next student in waitlist
    student_id = utils.get_next_waitlisted(db, id)

    if student_id:
        # auto enroll the first waitlisted student
        response = utils.update_enrollment_status(db, 
            class_id=id, 
            student_id=student_id, 
            status=utils.status_to_int['Enrolled']
        )

    return JSONResponse(
        status_code=webStatus.HTTP_200_OK,
        content={
            'message': f'status of enrollment of student({student_id}) for course({id}) was updated to Dropped',
            'body': {}
        }
    )


@app.get("/class/{id}/enrollments")
def get_enrollments(id, db: sqlite3.Connection = Depends(get_db), status:str = "Enrolled"):
    
    # checks if class id is vaid
    if not utils.is_valid_class(db, id):
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'class with id={id} does not exist',
                'body': {}
            }
        )

    # checks if status is valid
    if not utils.is_valid_status(status):
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'{status} is not valid status list {utils.valid_status}',
                'body': {}
            }
        )
    
    # execute query
    response = utils.get_enrollments(db, id, status)

    # generating the return object
    students = []
    for row in response:
        students.append({
            'CWID': row[0],
            'Name': row[1],
            'Email': row[2]
        })

    return JSONResponse(
        status_code=webStatus.HTTP_200_OK,
        content={
            'message': f'Successfully found enrollments with status={status}',
            'body': students
        }
    )


@app.get("/student/waitlist/position")
def view_waitlist_position(cwid: int, class_id: int, db: sqlite3.Connection = Depends(get_db)):

    # check if valid class
    if not utils.is_valid_class(db, class_id):
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'class with id={class_id} does not exist',
                'body': {}
            }
        )

    waitlist_students = utils.get_enrollments(db, 
        class_id=class_id,
        status='Waitlisted'
    )

    # find the position in the waitlit
    curr_position = 0
    for row in waitlist_students:
        curr_position += 1
        if row['cwid'] == cwid:
            return JSONResponse(
                status_code=webStatus.HTTP_200_OK,
                content={
                    'message': f'Successfully found waitlist position for student with id={cwid} in class with id {class_id}',
                    'body': {
                        'Position': curr_position
                    }
                }
            )

    # return failure if student is not in waitlist
    return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'waitlist info for student with id={cwid} and class {class_id} does not exist',
                'body': {}
            }
        )


@app.delete('/class/{id}/delete')
def delete_section(id, db: sqlite3.Connection = Depends(get_db)):
    
    # check if id is valid
    if not utils.is_valid_class(db, id):
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'class with id={id} does not exist',
                'body': {}
            }
        )

    # remove all enrollments for this course
    response = utils.delete_section_enrollments(db, id)

    # delete the section entry
    response = utils.delete_section(db, id)
    
    return JSONResponse(
        status_code=webStatus.HTTP_200_OK,
        content={
            'message': f'class with id={id} deleted',
            'body': {}
        }
    )


class NewClassInfo(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    section_num: Optional[int] = None
    instructor_id: Optional[str] = None
    max_size: Optional[str] = None
@app.put('/class/{id}/edit')
def update_info(id, new_info: NewClassInfo, db: sqlite3.Connection = Depends(get_db)):
    
    # retrieve old info from table
    old_info = utils.get_class_info(db, id)
    
    # check if class is valid
    if not old_info:
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'class with id={id} does not exist',
                'body': {}
            }
        )

    # fill in old value of department if not passed
    if not new_info.department:
        new_info.department = old_info['department']
    
    # fill in old value of max_size if not passed
    if not new_info.max_size:
        new_info.max_size = old_info['max_size']
    
    # fill in old value of class_title if not passed
    if not new_info.title:
        new_info.title = old_info['class_title'] 

    # fill in old value of section_num if not passed
    if not new_info.section_num:
        new_info.section_num = old_info['section_num']
    # if value passed, check if its valid
    elif utils.section_exists(db, new_info.title, new_info.section_num):
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'class with title={new_info.title} and section_num={new_info.section_num} already exists',
                'body': {}
            }
        )

    # fill in old value of instructor if not passed
    if not new_info.instructor_id:
        new_info.instructor_id = old_info['instructor_cwid']
    # if value passed, check if its vaid
    elif not utils.is_valid_instructor(db, new_info.instructor_id):
        return JSONResponse(
            status_code=webStatus.HTTP_400_BAD_REQUEST,
            content={
                'message': f'instructor with id={new_info.instructor_id} does not exist',
                'body': {}
            }
        )

    # update the information
    response = utils.update_class(db, id, new_info)

    return JSONResponse(
        status_code=webStatus.HTTP_200_OK,
        content={
            'message': f'class with id={id} updated successfully',
            'body': {}
        }
    )
