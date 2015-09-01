"""Test the application."""
import unittest
import httplib
import getpass
import base64
import json
from run import *


class AdamVigAPITestCase(unittest.TestCase):

    """Test the application."""

    @classmethod
    def setUpClass(self):
        """Initialize application for testing."""
        if not app.config['TESTING']:
            print '-----------------------------------'
            print 'Set testing to True in config.py and restart this script.'
            print '-----------------------------------'
            raise SystemExit(0)
        self.app = app.test_client()
        self.app_name = 'gocostudent'
        self.version = '2.1.5'
        self.end_point_prefix = '/' + self.app_name + '/' + self.version
        self.username = 'adam.vigneaux'
        self.password = base64.b64encode(getpass.getpass('Password: '))
        self.bad_username = 'adam.vig'
        self.bad_password = 'YWRhbXZpZw=='

    def test_root(self):
        """Test application root."""
        print "Test root: "
        response = self.app.get('/')
        self.assertIn('Resource not found.', response.data)

    def test_end_point_prefix(self):
        """Test end point prefix."""
        print "Test end point prefix: "
        response = self.app.get(self.end_point_prefix)
        self.assertIn("The app server is running correctly for " +
                      self.app_name + " " +
                      self.version + ".", response.data)

    def test_app_info(self):
        """Test app info."""
        end_point = 'appinfo'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test app info: "
        response = self.app.get(self.end_point_prefix + '/' +
                                end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

    def test_days_left_in_semester(self):
        """Test days left in semester."""
        end_point = 'daysleftinsemester'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test days left in semester: "
        response = self.app.get(self.end_point_prefix + '/' +
                                end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

    ##################
    # CHAPEL CREDITS #
    ##################

    def test_chapel_credits(self):
        """Test chapel credits."""
        end_point = 'chapelcredits'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test chapel credits: "
        response = self.app.get(self.end_point_prefix + '/' +
                                end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

    ##############
    # MEALPOINTS #
    ##############

    def test_mealpoints(self):
        """Test mealpoints."""
        end_point = 'mealpoints'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test mealpoints: "
        response = self.app.get(self.end_point_prefix + '/' +
                                end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

        print "Test mealpoints (bad user): "

    ######################
    # MEALPOINTS PER DAY #
    ######################

    def test_mealpoints_per_day(self):
        """Test mealpoints per day."""
        end_point = 'mealpointsperday'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test mealpoints per day: "
        response = self.app.get(self.end_point_prefix + '/' +
                                end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

    ##############
    # STUDENT ID #
    ##############

    def test_student_id(self):
        """Test student ID."""
        end_point = 'studentid'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test student ID: "
        response = self.app.get(self.end_point_prefix + '/' +
                                end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

    #############
    # NEXT MEAL #
    #############

    def test_next_meal(self):
        """Test next meal."""
        end_point = 'nextmeal'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test next meal: "
        response = self.app.get(self.end_point_prefix + '/' +
                                end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

    ###############
    # CHECK LOGIN #
    ###############

    def test_check_login(self):
        """Test check login."""
        end_point = 'checklogin'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test check login: "
        response = self.app.get(self.end_point_prefix + '/' +
                                end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

    ################
    # STUDENT INFO #
    ################

    def test_student_info(self):
        """Test student info."""
        end_point = 'studentinfo'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test student info: "
        response = self.app.get(self.end_point_prefix + '/' +
                                end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

    #####################
    # NEXT CHAPEL EVENT #
    #####################

    def test_next_chapel_event(self):
        """Test next chapel event."""
        end_point = 'nextchapelevent'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test next chapel event: "
        response = self.app.get(self.end_point_prefix + '/' +
                                end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)


if __name__ == '__main__':
    unittest.main()
