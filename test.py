import unittest, httplib, getpass, base64, json
from run import *

class AdamVigAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
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
        print "Test root: "
        response = self.app.get('/')
        self.assertIn('Resource not found.', response.data)

    def test_end_point_prefix(self):
        print "Test end point prefix: "
        response = self.app.get(self.end_point_prefix)
        self.assertIn("The app server is running correctly for " + \
            self.app_name + " " + \
            self.version + ".", response.data)

    def test_app_info(self):
        end_point = 'appinfo'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test app info: "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

    def test_days_left_in_semester(self):
        end_point = 'daysleftinsemester'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test days left in semester: "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

    ##################
    # CHAPEL CREDITS #
    ##################

    def test_chapel_credits(self):
        end_point = 'chapelcredits'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)


        print "Test chapel credits: "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
          json.loads(response.data)
        except ValueError:
          self.fail("Data is not valid JSON: " + response.data)

    def test_chapel_credits_baduser(self):
        end_point = 'chapelcredits'
        credentials = '?username={username}&password={password}' \
            .format(username=self.bad_username, password=self.password)


        print "Test chapel credits (bad user): "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    def test_chapel_credits_badpass(self):
        end_point = 'chapelcredits'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.bad_password)


        print "Test chapel credits (bad pass): "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    ##############
    # MEALPOINTS #
    ##############

    def test_mealpoints(self):
        end_point = 'mealpoints'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test mealpoints: "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

        print "Test mealpoints (bad user): "
    def test_mealpoints_baduser(self):
        end_point = 'mealpoints'
        credentials = '?username={username}&password={password}' \
            .format(username=self.bad_username, password=self.password)

        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    def test_mealpoints_badpass(self):
        end_point = 'mealpoints'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.bad_password)

        print "Test mealpoints (bad pass): "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    ######################
    # MEALPOINTS PER DAY #
    ######################

    def test_mealpoints_per_day(self):
        end_point = 'mealpointsperday'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test mealpoints per day: "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

    def test_mealpoints_per_day_baduser(self):
        end_point = 'mealpointsperday'
        credentials = '?username={username}&password={password}' \
            .format(username=self.bad_username, password=self.password)

        print "Test mealpoints per day (bad user): "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    def test_mealpoints_per_day_badpass(self):
        end_point = 'mealpointsperday'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.bad_password)

        print "Test mealpoints per day (bad pass): "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    ##############
    # STUDENT ID #
    ##############

    def test_student_id(self):
        end_point = 'studentid'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test student ID: "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

    def test_student_id_baduser(self):
        end_point = 'studentid'
        credentials = '?username={username}&password={password}' \
            .format(username=self.bad_username, password=self.password)

        print "Test student ID (bad user): "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    def test_student_id_badpass(self):
        end_point = 'studentid'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.bad_password)

        print "Test student ID (bad pass): "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    #############
    # NEXT MEAL #
    #############

    def test_next_meal(self):
        end_point = 'nextmeal'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        print "Test next meal: "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Data is not valid JSON: " + response.data)

    def test_next_meal_baduser(self):
        end_point = 'nextmeal'
        credentials = '?username={username}&password={password}' \
            .format(username=self.bad_username, password=self.password)

        print "Test next meal (bad user): "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    def test_next_meal_badpass(self):
        end_point = 'nextmeal'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.bad_password)

        print "Test next meal (bad pass): "
        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)


if __name__ == '__main__':
    unittest.main()
