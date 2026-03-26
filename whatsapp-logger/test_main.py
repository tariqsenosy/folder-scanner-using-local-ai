import unittest
from main import load_config, main
from scanner import get_modified_files
from filter import filter_lines
from sender import send_message

class TestWhatsAppLogger(unittest.TestCase):

    def setUp(self):
        # Create a temporary configuration file for testing
        with open('config/test_settings.ini', 'w') as config_file:
            config_file.write("""
[DEFAULT]
folder_path = ./test_folder
keywords = exception, error

[WHATSAPP]
api_token = test_api_token
from_number = +1234567890
to_number = +0987654321
""")
    
    def tearDown(self):
        # Remove the temporary configuration file
        import os
        if os.path.exists('config/test_settings.ini'):
            os.remove('config/test_settings.ini')

    def test_load_config(self):
        config = load_config()
        self.assertEqual(config['folder_path'], './test_folder')
        self.assertEqual(config['keywords'], ['exception', 'error'])
        self.assertEqual(config['whatsapp']['api_token'], 'test_api_token')
        self.assertEqual(config['whatsapp']['from_number'], '+1234567890')
        self.assertEqual(config['whatsapp']['to_number'], '+0987654321')

    def test_get_modified_files(self):
        # Create a temporary folder and file for testing
        import os
        if not os.path.exists('test_folder'):
            os.makedirs('test_folder')
        
        with open('test_folder/test_file.py', 'w') as f:
            f.write("def foo():\n    print('This is a test file')")
        
        # Simulate file modification time
        import time
        initial_time = int(os.path.getmtime('test_folder/test_file.py'))
        time.sleep(2)
        
        modified_files = get_modified_files('test_folder')
        self.assertEqual(len(modified_files), 1)
        self.assertEqual(modified_files[0][1], 'test_file.py')
        
        # Clean up
        os.remove('test_folder/test_file.py')
        os.rmdir('test_folder')

    def test_filter_lines(self):
        lines = [
            "def foo():\n    print('This is a test file')",
            "raise Exception('An exception occurred')"
        ]
        keywords = ['exception']
        filtered_lines = filter_lines(lines, keywords)
        self.assertEqual(filtered_lines, ["raise Exception('An exception occurred')"])

    def test_send_message(self):
        # Mock the send_message function to avoid actual WhatsApp message sending
        def mock_send_message(message, api_token, from_number, to_number):
            print(f"Mocked send_message: {message}")
        
        original_send_message = sender.send_message
        sender.send_message = mock_send_message
        
        send_message("This is a test message", "test_api_token", "+1234567890", "+0987654321")
        
        # Restore the original function
        sender.send_message = original_send_message

if __name__ == "__main__":
    unittest.main()