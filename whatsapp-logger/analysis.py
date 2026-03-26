import ollama

def analyze_message(message):
    try:
        # Call LLaMA-3.2 to analyze the message
        response = ollama.analyze(message)
        
        # Extract the root cause from the response
        root_cause = response.get('root_cause', 'Unknown error')
        
        return root_cause
    except Exception as e:
        print(f"Error analyzing message: {e}")
        return 'An unknown error occurred'