from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import spacy

app = FastAPI()

#This Allow CORS for frontend fetch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Loading better spaCy NER model
try:
    nlp = spacy.load("en_core_web_trf")
except:
    nlp = spacy.load("en_core_web_sm") 
    print("Falling back to en_core_web_sm. Run `python -m spacy download en_core_web_trf` for better accuracy.")

# Ollama endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

class PromptRequest(BaseModel):
    prompt: str

# Serving the HTML
@app.get("/")
def read_index():
    return FileResponse("index.html")

@app.post("/process_prompt")
def process_prompt(data: PromptRequest):
    prompt = data.prompt

    doc = nlp(prompt)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    llm_ner_output = ""
    if not entities:
        fallback_prompt = (
            f"Extract named entities and their types from the following sentence:\n\"{prompt}\""
        )
        fallback_payload = {
            "model": MODEL_NAME,
            "prompt": fallback_prompt,
            "stream": False
        }

        try:
            ner_response = requests.post(OLLAMA_URL, json=fallback_payload)
            llm_ner_output = ner_response.json().get("response", "No fallback response.")
            print("LLM Fallback NER Response:", llm_ner_output)
        except Exception as e:
            llm_ner_output = f"Error in fallback NER: {str(e)}"

    #Call LLM for main response
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        llm_output = response.json().get("response", "No response from LLM.")
    except Exception as e:
        llm_output = f"Error calling LLM: {str(e)}"

    # Logging everything
    print("Detected spaCy Entities:", entities)
    print("LLM Response:", llm_output)

    return {
        "entities": entities,
        "llm_response": llm_output,
        "llm_fallback_ner": llm_ner_output if not entities else ""
    }
