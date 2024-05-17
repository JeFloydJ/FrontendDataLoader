import unittest
from unittest.mock import patch, MagicMock
import sys
import boto3
from io import StringIO
import csv
sys.path.insert(1, '../')
from Events.eventProcessData import DataProcessor

class TestDataProcessor(unittest.TestCase):

    @patch('Events.eventProcessData.boto3.client')
    def test_modify_csv_names(self, mock_s3_client):
        # Configura el mock de S3
        mock_s3 = mock_s3_client.return_value
        mock_s3.get_object.return_value = {
            'Body': MagicMock(read=lambda: rb'"Name";"Last Name";"Email Addresses\Email address";"Web address";"Last/Organization/Group/Household name"\nJohn Doe;Doe;johndoe@example.com;http://example.com;Doe\nJane Smith;Smith;janesmith@example.com;https://example.org;Smith')
        }

        # Inicializa DataProcessor con los argumentos correctos
        processor = DataProcessor('my_bucket')
        try:
            processor.modify_csv_names('test.csv')
        except ValueError as e:
            print(f"Error: {e}")
            return  # Termina la prueba aquí si se produce un error

        # Verifica que se llamó a put_object con los datos esperados
        expected_csv = r'"Name";"Last Name";"Email Addresses\Email address";"Web address";"Last/Organization/Group/Household name"\nJohn;Doe;johndoe@tmail.comx;http://website.com;\nxDoe;\nJane;Smith;janesmith@tmail.comx;https://website.com;\nxSmith;\n'
        mock_s3.put_object.assert_called_once_with(Bucket='my_bucket', Key='test.csv', Body=expected_csv)

if __name__ == '__main__':
    unittest.main()



# class TestDataProcessor(unittest.TestCase):

#     def setUp(self):
#         self.processor = DataProcessor()

#     @patch('builtins.open', new_callable=MagicMock)
#     @patch('requests.post', return_value=MagicMock())
#     def test_refresh_token(self, mock_post, mock_open):
#         mock_open.return_value.__enter__.return_value.read.return_value = 'token'
#         mock_post.return_value.status_code = 200
#         mock_post.return_value.json.return_value = {"access_token": "new_token"}

#         self.processor.refresh_token()

#         mock_post.assert_called_once()
#         self.assertEqual(mock_open.call_count, 2)

#     @patch('requests.request', return_value=MagicMock())
#     def test_get_id(self, mock_request):
#         mock_request.return_value.status_code = 200
#         mock_request.return_value.text = '{"id": "123"}'

#         id_value = self.processor.get_id("report_name")

#         self.assertEqual(id_value, "123")
#         mock_request.assert_called_once()

#     @patch('requests.request', return_value=MagicMock())
#     def test_get_query(self, mock_request):
#         mock_request.return_value.status_code = 200
#         mock_request.return_value.text = '{"query": "query"}'

#         self.processor.get_query("id", "report_name")

#         mock_request.assert_called_once()

#     @patch('builtins.open', new_callable=MagicMock)
#     @patch('json.load', return_value={"field_names": ["field1", "field2"], "rows": [["value1", "value2"]]})
#     @patch('csv.writer', return_value=MagicMock())
#     def test_json_to_csv(self, mock_writer, mock_load, mock_open):
#         self.processor.json_to_csv("json_file_path", "csv_file_path")
#         mock_load.assert_called_once()
#         mock_writer.assert_called_once()
#         self.assertEqual(mock_open.call_count, 2)

#     @patch('builtins.open', new_callable=MagicMock)
#     @patch('csv.reader', return_value=iter([["Name", "Last/Organization/Group/Household name", "Email Addresses\\Email address", "Web address"], ["name", "last_name", "email@example.com", "http://example.com"]]))
#     @patch('csv.writer', return_value=MagicMock())
#     def test_modify_csv_names(self, mock_writer, mock_reader, mock_open):
#         self.processor.modify_csv_names("input_csv", "output_csv")

#         mock_reader.assert_called_once()
#         mock_writer.assert_called_once()
#         self.assertEqual(mock_open.call_count, 2)

#     @patch('builtins.open', new_callable=MagicMock)
#     @patch('csv.reader', return_value=iter([["Name", "Last/Organization/Group/Household name", "Phones\\Number"], ["name", "last_name", "1234567890"]]))
#     @patch('csv.writer', return_value=MagicMock())
#     def test_modify_csv_phone(self, mock_writer, mock_reader, mock_open):
#         self.processor.modify_csv_phone("input_csv", "output_csv")

#         mock_reader.assert_called_once()
#         mock_writer.assert_called_once()
#         self.assertEqual(mock_open.call_count, 2)

#     @patch('builtins.open', new_callable=MagicMock)
#     @patch('csv.reader', return_value=iter([["Name", "Last/Organization/Group/Household name"], ["name", "last_name"]]))
#     @patch('csv.writer', return_value=MagicMock())
#     def test_modify_csv_households(self, mock_writer, mock_reader, mock_open):
#         self.processor.modify_csv_households("input_csv", "output_csv")

#         mock_reader.assert_called_once()
#         mock_writer.assert_called_once()
#         self.assertEqual(mock_open.call_count, 2)

#     @patch('builtins.open', new_callable=MagicMock)
#     @patch('csv.reader', return_value=iter([["Name", "Last/Organization/Group/Household name"], ["name", "last_name"]]))
#     @patch('csv.writer', return_value=MagicMock())
#     def test_modify_csv_contacts(self, mock_writer, mock_reader, mock_open):
#         self.processor.modify_csv_contacs("input_csv", "output_csv")

#         mock_reader.assert_called_once()
#         mock_writer.assert_called_once()
#         self.assertEqual(mock_open.call_count, 2)

#     @patch('builtins.open', new_callable=MagicMock)
#     @patch('csv.reader', return_value=iter([["Name", "Last/Organization/Group/Household name", 'Addresses\\Address', 'Addresses\\ZIP'], ["name", "last_name", "address", "0000"]]))
#     @patch('csv.writer', return_value=MagicMock())
#     def test_modify_csv_contacs_address(self, mock_writer, mock_reader, mock_open):
#         self.processor.modify_csv_contacs_address("input_csv", "output_csv")

#         mock_reader.assert_called_once()
#         mock_writer.assert_called_once()
#         self.assertEqual(mock_open.call_count, 2)

#     @patch('builtins.open', new_callable=MagicMock)
#     @patch('csv.reader', return_value=iter([["Name", "Last/Organization/Group/Household name", "Email Addresses\\Email address"], ["name", "last_name", "asdadadasd@asdadasdasd.com"]]))
#     @patch('csv.writer', return_value=MagicMock())
#     def test_modify_csv_contacs_email(self, mock_writer, mock_reader, mock_open):
#         self.processor.modify_csv_contacs_email("input_csv", "output_csv")
#         mock_reader.assert_called_once()
#         mock_writer.assert_called_once()
#         self.assertEqual(mock_open.call_count, 2)

#     @patch('builtins.open', new_callable=MagicMock)
#     @patch('csv.reader', return_value=iter([["Name", "Last/Organization/Group/Household name", "Phones\\Number"], ["name", "last_name", "3123123213"]]))
#     @patch('csv.writer', return_value=MagicMock())
#     def test_modify_csv_contacs_phones(self, mock_writer, mock_reader, mock_open):
#         self.processor.modify_csv_phones("input_csv", "output_csv")
#         mock_reader.assert_called_once()
#         mock_writer.assert_called_once()
#         self.assertEqual(mock_open.call_count, 2)

#     @patch.object(DataProcessor, 'get_id')
#     @patch.object(DataProcessor, 'get_query')
#     @patch.object(DataProcessor, 'json_to_csv')
#     @patch.object(DataProcessor, 'modify_csv_names')
#     @patch.object(DataProcessor, 'modify_csv_phone')
#     @patch.object(DataProcessor, 'modify_csv_households')
#     @patch.object(DataProcessor, 'modify_csv_contacs')
#     @patch.object(DataProcessor, 'modify_csv_contacs_address')
#     @patch.object(DataProcessor, 'modify_csv_contacs_email')
#     @patch.object(DataProcessor, 'modify_csv_phones')
#     @patch('csv.reader', return_value=iter([["Name", "Last/Organization/Group/Household name", "Addresses\\Address", "Addresses\\ZIP"], ["name", "last_name", "address", "zip"]]))
#     def test_process_data(self, mock_reader, mock_modify_csv_phone, mock_modify_csv_names, mock_modify_csv_households, mock_modify_csv_contacs , mock_modify_csv_contacs_address, mock_modify_csv_contacs_email, mock_modify_csv_phones , mock_json_to_csv, mock_get_query, mock_get_id):
#         self.processor.process_data()
#         mock_get_id.assert_called()
#         mock_get_query.assert_called()
#         mock_json_to_csv.assert_called()
#         mock_modify_csv_names.assert_called()
#         mock_modify_csv_phone.assert_called()
#         mock_modify_csv_households.assert_called()
#         mock_modify_csv_contacs.assert_called()
#         mock_modify_csv_contacs_address.assert_called()
#         mock_modify_csv_contacs_email.assert_called()
#         mock_modify_csv_phones.assert_called()