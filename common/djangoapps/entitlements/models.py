from django.db import models
from django.contrib.auth.models import User
from course_modes.models import CourseMode
from opaque_keys.edx.keys import CourseKey


class CourseEntitlement(models.Model):
    """
    Represents a Student's Entitlement to a Course Run for a given Course.
    """

    user = models.ForeignKey(User)
    # TODO: Consider replacing with an integer Foreign key and a Course Table
    # The Course ID that is assigned to this Entitlement
    root_course = models.CharField(max_length=255, primary_key=True)

    created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)

    # The date that an enrollment must be applied by
    enroll_end_date = models.DateTimeField(null=False)

    # The mode of the Course that will be applied
    # TODO: When storing the Mode in the API should we check that it is an available mode
    # for the Course?
    mode = models.CharField(default=CourseMode.DEFAULT_MODE_SLUG, max_length=100)

    # The ID of the course enrollment for this Entitlement
    # if NULL the entitlement is not in use
    enrollment_course = models.ForeignKey('student.CourseEnrollment', null=True)

    is_active = models.BooleanField(default=1)

    # TODO: Commented out until needed in implementation
    # @classmethod
    # def entitlements_for_username(cls, username):
    #     user = User.objects.get(username=username)
    #     return cls.objects.filter(user_id=user)
    #
    # @classmethod
    # def entitlements_for_user(cls, user):
    #     return cls.objects.filter(user_id=user)
    #
    # @classmethod
    # def get_user_course_entitlement(cls, user, course):
    #     # TODO: Implement check to see if the Course ID is valid
    #     return cls.objects.filter(user_id=user, root_course_id=course).first()
    #
    # @classmethod
    # def set_entitlement_enrollment(cls, user, course_key, course_enrollment):
    #     course = course_key.org + '+' + course_key.course
    #     return cls.objects.filter(
    #         user_id=user,
    #         root_course_id=course
    #     ).update(enrollment_course_id=course_enrollment)
    #
    # @classmethod
    # def remove_entitlement_enrollment(cls, user, course_key):
    #     course = course_key.org + '+' + course_key.course
    #     return cls.objects.filter(
    #         user_id=user,
    #         root_course_id=course
    #     ).update(enrollment_course_id=None)
