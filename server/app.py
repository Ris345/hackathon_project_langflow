import os
import requests
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
import os
from langchain_google_community import GoogleSearchAPIWrapper
from flask import Flask, jsonify, request

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- Configuration from Environment Variables ---
# Your Twilio Account SID and Auth Token
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# Your Langflow API URL (e.g., http://localhost:7860/api/v1/run)
# Replace with your actual Langflow flow's API endpoint
LANGFLOW_API_URL = os.getenv('LANGFLOW_API_URL')
# Your Langflow API Key (if your flow requires authentication)
LANGFLOW_API_KEY = os.getenv('LANGFLOW_API_KEY')

# --- Helper Function to Call Langflow API ---
def call_langflow_api(user_input):
    """
    Sends the user's transcribed input to the Langflow API and returns the AI's response.
    """
    if not LANGFLOW_API_URL:
        print("Error: LANGFLOW_API_URL is not set.")
        return "I'm sorry, the AI service is not configured."

    headers = {
        "Content-Type": "application/json",
    }
    if LANGFLOW_API_KEY:
        headers["X-API-Key"] = LANGFLOW_API_KEY # Or "Authorization": f"Bearer {LANGFLOW_API_KEY}" depending on Langflow setup

    payload = {
        "input": {
            "question": user_input # Adjust 'question' key based on your Langflow flow's input component name
        },
        "output_type": "chat", # Or "text" or "json" depending on your Langflow flow's output
        "stream": False
    }

    try:
        print(f"Sending to Langflow: {user_input}")
        response = requests.post(LANGFLOW_API_URL, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        langflow_response = response.json()
        print(f"Received from Langflow: {langflow_response}")

        # Extract the actual response text. This might vary based on your Langflow flow's output.
        # Common structures are 'result', 'text', or 'outputs'
        # Let's assume a common structure like {'outputs': [{'results': {'text': '...'}}]} or similar
        # You might need to inspect the actual JSON response from your Langflow flow.
        if 'outputs' in langflow_response and langflow_response['outputs']:
            # Assuming the first output contains the main text response
            for output in langflow_response['outputs']:
                if 'results' in output and 'text' in output['results']:
                    return output['results']['text']
                elif 'text' in output: # Fallback for simpler text output
                    return output['text']
        elif 'result' in langflow_response: # Another common structure
            return langflow_response['result']
        elif 'response' in langflow_response: # Yet another common structure
            return langflow_response['response']

        return "I received a response from the AI, but I couldn't understand its format."

    except requests.exceptions.RequestException as e:
        print(f"Error calling Langflow API: {e}")
        return "I'm sorry, I'm having trouble connecting to the AI service right now."
    except ValueError as e:
        print(f"Error parsing Langflow response: {e}")
        return "I'm sorry, I received an invalid response from the AI service."


# --- Twilio Voice Webhook ---
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """
    Handles incoming Twilio voice calls.
    """
    response = VoiceResponse()
    speech_result = request.form.get('SpeechResult')

    if speech_result:
        print(f"User said: {speech_result}")
        # Process the user's speech with Langflow
        ai_response_text = call_langflow_api(speech_result)
        response.say(ai_response_text)
    else:
        # Initial greeting for a new call
        response.say("Hello! How can I help you today?")

    # Always gather more input after speaking
    # Set input='speech' to enable speech recognition
    # Set action to point back to this same endpoint for subsequent interactions
    # Set speechTimeout to control how long Twilio waits for speech (in seconds)
    response.gather(input='speech', action='/voice', speechTimeout='auto')

    # If the user doesn't say anything after the gather, or if there's an error
    # and the gather times out, Twilio will hit this endpoint again without SpeechResult.
    # We can add a fallback or simply hang up.
    if not speech_result:
        response.say("I didn't hear anything. Goodbye!")
        response.hangup()

    return str(response)


@app.route('/search')
def test_your_search():
    """Test Google Search API and return results to browser"""
    
    try:
        # Initialize search
        search = GoogleSearchAPIWrapper(
            google_api_key=os.getenv('GOOGLE_API_KEY'),
            google_cse_id=os.getenv('GOOGLE_CSE_ID'), # Your CSE ID
            k=3
        )
        print(search)
        # Perform search
        results = search.results("software engineer jobs", num_results=3)
        print("✅ Search successful!")  # This prints to console
        print(f"Found {len(results)} results")
        
        # Prepare response for browser
        response_data = {
            "status": "success",
            "message": f"Found {len(results)} results",
            "results_count": len(results),
            "results": []
        }
        
        # Process results for JSON response
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            link = result.get('link', 'No link')
            snippet = result.get('snippet', 'No snippet')
            
            print(f"- {title}")  # Console output
            print(f"  {link}")
            print()
            
            # Add to response
            response_data["results"].append({
                "index": i,
                "title": title,
                "link": link,
                "snippet": snippet
            })
        
        # Return JSON response to browser
        return jsonify(response_data)
        
    except Exception as e:
        error_message = f"❌ Error: {e}"
        print(error_message)  # Console output
        
        # Return error response to browser
        return jsonify({
            "status": "error",
            "message": str(e),
            "results_count": 0,
            "results": []
        }), 500


# --- Main execution block ---
if __name__ == "__main__":
    # Ensure environment variables are set before running
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not LANGFLOW_API_URL:
        print("Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and LANGFLOW_API_URL environment variables.")
        print("You can create a .env file in the same directory as this script.")
        print("Example .env content:")
        print("TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("TWILIO_AUTH_TOKEN=your_auth_token")
        print("LANGFLOW_API_URL=http://localhost:7860/api/v1/run/your_flow_id")
        print("LANGFLOW_API_KEY=your_langflow_api_key_if_any")
    else:
        print("Flask app starting...")
        app.run(debug=True, port=5000) # Run in debug mode for development