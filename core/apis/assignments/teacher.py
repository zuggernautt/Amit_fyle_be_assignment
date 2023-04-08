from core.apis import decorators
from flask import Blueprint, request
from core import db
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema, GradeEnumSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

  #new
@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignment(p):
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade/', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p,  incoming_payload=None):
    """Grade an assignment"""

    grade_assignment_payload = GradeEnumSchema().load(incoming_payload)
    assignment_id = incoming_payload.get('id')
    assignment = Assignment.get_assignments_by_teacher(assignment_id, p.teacher_id)
    
    graded_assignment = Assignment.set_grade(
        assignment_id=assignment_id,
        grade= grade_assignment_payload['grade'],
        principal=p
    )

    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
    
