import xml.etree.ElementTree
import facesheet


class Test_facesheet:

    @classmethod
    def setup_class(self):
        self.row = [1, '2015-77128059', '10/09/2015', 'accident', 'ry4927404',
                    '18', 'psb', 'william walker', '27363 oak valley center',
                    'a15', 'los palacios', 'mn', '82156', '3/18/1999',
                    '357-219-0456', 'white', 'male', 'west', 1]

    @classmethod
    def teardown_class(self):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """

    def test_parse_row(self):
        expected = {'case_number': '2015-77128059',
                    'occurred_date': '10/09/2015',
                    'incident_type': 'Accident',
                    'age': '18',
                    'name': 'William Walker',
                    'address': '27363 Oak Valley Center APT: A15 Los Palacios, MN 82156',
                    'DOB': '3/18/1999',
                    'phone': '357-219-0456',
                    'race': 'White',
                    'sex': 'Male',
                    'district': 'West'}

        results = facesheet.parse_row(self.row)

        for key in expected:
            assert expected[key] == results[key]
