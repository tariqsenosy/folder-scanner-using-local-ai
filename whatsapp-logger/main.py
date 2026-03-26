import time
from configparser import ConfigParser

import filter
import sender
import scanner
from analysis import analyze_message

def load_config():
    config_path = 'config/settings.ini'
    config = ConfigParser()
    config.read(config_path)

    return {
        'folder_path': config['DEFAULT']['folder_path'],
        'keywords': config['DEFAULT']['keywords'].split(','),
        'whatsapp': {
            'api_token': config['WHATSAPP']['api_token'],
            'from_number': config['WHATSAPP']['from_number'],
            'to_number': config['WHATSAPP']['to_number']
        }
    }

def main():
    config = load_config()
    folder_path = config['folder_path']
    keywords = config['keywords']
    whatsapp_info = config['whatsapp']

    try:
        while True:
            modified_files = scanner.get_modified_files(folder_path)
            
            if not modified_files:
                print("No files modified.")
            else:
                for file_path, filename, _ in modified_files:
                    with open(file_path, 'r') as file:
                        lines = file.readlines()

                    filtered_lines = filter.filter_lines(lines, keywords)

                    if filtered_lines:
                        for line in filtered_lines:
                            # Analyze the message
                            root_cause = analyze_message(line)

                            # Send the analyzed root cause via WhatsApp
                            sender.send_message(f"Root Cause: {root_cause}", whatsapp_info['api_token'], whatsapp_info['from_number'], whatsapp_info['to_number'])
                    
            time.sleep(900)  # Wait for 15 minutes (60 * 15 seconds)
    except KeyboardInterrupt:
        print("Stopping the application.")
    except Exception as e:
        print(f"Error in main loop: {e}")

if __name__ == "__main__":
    main()