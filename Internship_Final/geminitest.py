import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=r"F:\Internship\secrets.env")
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)
# Configure Gemini
genai.configure(api_key=google_api_key)
MODEL_NAME = "models/learnlm-2.0-flash-experimental"
model = genai.GenerativeModel(model_name=MODEL_NAME)
# Now, generate content and set the timeout within request_options
response = model.generate_content("hello gemini"  # Set the timeout in seconds here
)
print(response.text)
