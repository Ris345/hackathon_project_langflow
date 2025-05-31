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
