import unittest, httplib, getpass, base64
from run import *

class AdamVigAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app_name = 'gocostudent'
        self.version = '2.1.5'
        self.end_point_prefix = '/' + self.app_name + '/' + self.version
        self.username = 'adam.vigneaux'
        self.password = base64.b64encode(getpass.getpass('Password: '))
        self.bad_username = 'adam.vig'
        self.bad_password = 'YWRhbXZpZw=='

    def test_root(self):
        response = self.app.get('/')
        self.assertIn('Resource not found.', response.data)

    def test_end_point_prefix(self):
        response = self.app.get(self.end_point_prefix)
        self.assertIn("The app server is running correctly for " + \
            self.app_name + " " + \
            self.version + ".", response.data)

    def test_app_info(self):
        end_point = 'appinfo'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)

    def test_chapel_credits(self):
        end_point = 'chapelcredits'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)

    def test_meal_points(self):
        end_point = 'mealpoints'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)

    def test_days_left_in_semester(self):
        end_point = 'daysleftinsemester'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)

    def test_mealpoints_per_day(self):
        end_point = 'mealpointsperday'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.password)

        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.OK)

    def test_chapel_credits_baduser(self):
        end_point = 'chapelcredits'
        credentials = '?username={username}&password={password}' \
            .format(username=self.bad_username, password=self.password)

        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    def test_meal_points_baduser(self):
        end_point = 'mealpoints'
        credentials = '?username={username}&password={password}' \
            .format(username=self.bad_username, password=self.password)

        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    def test_mealpoints_per_day_baduser(self):
        end_point = 'mealpointsperday'
        credentials = '?username={username}&password={password}' \
            .format(username=self.bad_username, password=self.password)

        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    def test_chapel_credits_badpass(self):
        end_point = 'chapelcredits'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.bad_password)

        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    def test_meal_points_badpass(self):
        end_point = 'mealpoints'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.bad_password)

        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)

    def test_mealpoints_per_day_badpass(self):
        end_point = 'mealpointsperday'
        credentials = '?username={username}&password={password}' \
            .format(username=self.username, password=self.bad_password)

        response = self.app.get(self.end_point_prefix + '/' + end_point + credentials)
        self.assertEqual(response.status_code, httplib.UNAUTHORIZED)


if __name__ == '__main__':
    unittest.main()
