                      ┌────────────────────────────┐
                      │     Frontend (React/HTML)  │
                      │  - Prompt UI               │
                      │  - Call progress status    │
                      └────────────┬───────────────┘
                                   │
                                   ▼
                      ┌────────────────────────────┐
                      │ Flask API (app.py)         │
                      │  - /initialize_agent       │
                      │  - Starts agent lifecycle  │
                      └────────────┬───────────────┘
                                   │
                                   ▼
                ┌────────────────────────────┐
                │ Agent Runner (Python Logic)│
                │ - Receives prompt          │
                │ - Calls Langflow           │
                │ - Receives structured reply│
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Langflow LLM Chain         │
                │ - Parses prompt            │
                │ - Generates call script    │
                │ - Provides job market tips │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Twilio Call Orchestrator   │
                │ - Receives Langflow output │
                │ - Calls Twilio API         │
                │ - Sends TwiML script       │
                └────────────┬───────────────┘
                             │
                             ▼
              ┌────────────────────────────────┐
              │ Twilio Programmable Voice API  │
              │ - Calls user's phone           │
              │ - Plays response (TwiML)       │
              │ - (Future) Darth Vader Voice   │
              └────────────────────────────────┘





# the flask app.py is going to intialize the agent 
# once the agent is intialized the agent makes a call to the llm 
# the llm or lang flow in this case will call twilio 
# to call the twilio the lanflow needs to invoke the 
# with the provided information from the prompt 
# the agent will call twillio to talk to the customer 
#  if this work flow is successful then we can integrate a darth vader voice from some third part API 