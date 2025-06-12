LLM + Named Entity Recognition App
A simple web application that combines Named Entity Recognition (NER) with a locally running Large Language Model (LLM) to analyze user input and display relevant information.

Overview
This project allows users to input natural language prompts through a web interface. It performs the following tasks:

Extracts named entities using spaCy.

Sends the prompt to a local LLM via Ollama for contextual response generation.

Highlights detected entities in the original text.

Displays the generated LLM response.



Features
Fast and interactive user interface for input and output display.

Entity highlighting for PERSON, LOCATION, ORGANIZATION, DATE, etc.

Integration with local LLMs through the Ollama API.

Modern dark-mode themed UI for better readability and user experience.



Tech Stack
Backend: FastAPI

NER Engine: spaCy (en_core_web_sm)

LLM: Mistral (or other local models via Ollama)

Frontend: HTML, CSS, JavaScript (Vanilla)