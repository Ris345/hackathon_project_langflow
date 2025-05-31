from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# the flask app.py is going to intialize the agent 
# once the agent is intialized the agent makes a call to the llm 
# the llm or lang flow in this case will call twilio 
# to call the twilio the lanflow needs to invoke the 
# with the provided information from the prompt 
# the agent will call twillio to talk to the customer 
#  if this work flow is successful then we can integrate a darth vader voice from some third part API 



if __name__ == "__main__":
    app.run(debug=True)
