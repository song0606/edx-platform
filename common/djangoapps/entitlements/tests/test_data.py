"""
Test the Data Aggregation Layer for Course Enrollments.

"""
import datetime
import unittest

import ddt
from django.conf import settings

from entitlements.models import CourseEntitlement
from student.tests.factories import UserFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory
from student.tests.factories import CourseEnrollmentFactory


@ddt.ddt
@unittest.skipUnless(settings.ROOT_URLCONF == 'lms.urls', 'Test only valid in lms')
class EntitlementDataTest(ModuleStoreTestCase):
    """
    Test course enrollment data aggregation.

    """
    USERNAME = "Bob"
    EMAIL = "bob@example.com"
    PASSWORD = "edx"

    def setUp(self):
        """Create a course and user, then log in. """
        super(EntitlementDataTest, self).setUp()
        self.course = CourseFactory.create()
        self.user = UserFactory.create(username=self.USERNAME, email=self.EMAIL, password=self.PASSWORD)
        self.client.login(username=self.USERNAME, password=self.PASSWORD)

    def _get_parent_course_from_course_run(self, course):
        return "{}+{}".format(course.org, course.number)

    def _add_entitlement_for_user(self, course, user):
        entitlement_data = {
            'user': user,
            'root_course': self._get_parent_course_from_course_run(course),
            'enroll_end_date': '2017-09-14 11:47:58.000000',
            'mode': 'verified',
            'is_active': True
        }
        stored_entitlement, is_created = CourseEntitlement.update_or_create_new_entitlement(
            user,
            self._get_parent_course_from_course_run(course),
            entitlement_data
        )
        return stored_entitlement, is_created

    def test_get_entitlement_info(self):
        stored_entitlement, is_created = self._add_entitlement_for_user(self.course, self.user)
        test_parent_course_id = self._get_parent_course_from_course_run(self.course)
        self.assertTrue(is_created)

        # Get the Entitlement and verify the data
        entitlement = CourseEntitlement.get_user_course_entitlement(self.user, test_parent_course_id)
        self.assertEqual(entitlement.root_course, test_parent_course_id)
        self.assertEqual(entitlement.mode, 'verified')
        self.assertEqual(entitlement.is_active, True)
        self.assertIsNone(entitlement.enrollment_course)

    def test_get_course_entitlements(self):
        course2 = CourseFactory.create()

        stored_entitlement, is_created = self._add_entitlement_for_user(self.course, self.user)
        test_parent_course_id = self._get_parent_course_from_course_run(self.course)
        self.assertTrue(is_created)

        stored_entitlement2, is_created2 = self._add_entitlement_for_user(course2, self.user)
        test_parent_course_id2 = self._get_parent_course_from_course_run(course2)
        self.assertTrue(is_created2)

        # Get the Entitlement and verify the data
        entitlement_list = CourseEntitlement.entitlements_for_user(self.user)

        self.assertEqual(2, len(entitlement_list))
        self.assertEqual(test_parent_course_id, entitlement_list[0].root_course)
        self.assertEqual(test_parent_course_id2, entitlement_list[1].root_course)

    def test_set_enrollment(self):
        stored_entitlement, is_created = self._add_entitlement_for_user(self.course, self.user)
        test_parent_course_id = self._get_parent_course_from_course_run(self.course)
        self.assertTrue(is_created)

        # Entitlement set not enroll the user in the Course run
        enrollment = CourseEnrollmentFactory(
            user=self.user,
            course_id=self.course.id,
            is_active=True,
            mode="verified",
        )
        CourseEntitlement.set_entitlement_enrollment(self.user, test_parent_course_id, enrollment)

        entitlement = CourseEntitlement.get_user_course_entitlement(self.user, test_parent_course_id)
        self.assertIsNotNone(entitlement.enrollment_course)

    def test_remove_enrollment(self):
        stored_entitlement, is_created = self._add_entitlement_for_user(self.course, self.user)
        test_parent_course_id = self._get_parent_course_from_course_run(self.course)
        self.assertTrue(is_created)

        # Entitlement set not enroll the user in the Course run
        enrollment = CourseEnrollmentFactory(
            user=self.user,
            course_id=self.course.id,
            is_active=True,
            mode="verified",
        )
        CourseEntitlement.set_entitlement_enrollment(self.user, test_parent_course_id, enrollment)

        entitlement = CourseEntitlement.get_user_course_entitlement(self.user, test_parent_course_id)
        self.assertIsNotNone(entitlement.enrollment_course)

        CourseEntitlement.remove_entitlement_enrollment(self.user, test_parent_course_id)
        entitlement = CourseEntitlement.get_user_course_entitlement(self.user, test_parent_course_id)
        self.assertIsNone(entitlement.enrollment_course)
