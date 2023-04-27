from flask import Flask, request, jsonify, render_template
import json
import requests
import traceback

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chat():
    chat_history = []
    if request.method == 'POST':
        user_input = request.form['user_input']
        # TODO: Process user input here and generate a response
        # For now, let's just return the user's message
        chat_history.append(('User', user_input))
        chat_history.append(('Bot', user_input))
        # Pass the user input to the Rasa chatbot
        try:
            response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": user_input})
            print(response)
            response.raise_for_status()
        except Exception as e:
            error_message = f"Sorry, rasa is having issues. Error message: {traceback.format_exc()}."            
            app.logger.error(error_message)
            traceback.print_exc()
            return jsonify({'response': error_message})

        response_data = json.loads(response.content.decode('utf-8'))
        # Return the response from the chatbot to the user
        return jsonify({'response': response_data})
        
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

