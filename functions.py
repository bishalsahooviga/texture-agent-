
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
GOOGLE_API_KEY=os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


generation_config = {
  "temperature": 0.7,
  "top_p": 1,
  "top_k": 0,
  "max_output_tokens": 2048,
}

safety_settings = [
{ "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE",
      "probability": "NEGLIGIBLE" },
    { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE",
      "probability": "NEGLIGIBLE" },
    { "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE",
      "probability": "NEGLIGIBLE" },
    { "category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE",
      "probability": "NEGLIGIBLE" },
]

text_model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
def text_gemini(prompt):
    try:
       response = text_model.generate_content(prompt)
    #    print(response.candidate.safety_ratings)
    except:
       return prompt
    
    return response.text

def generate_prompt(task_description, asset_description, user_description=None):
    # Base prompt guidelines
    prompt_guidelines = """
    In Meshy, a basic prompt is to describe an object you want to generate or retexture, e.g. a sword, a helmet, a house, a treasure chest, etc.
   
    Advanced Prompts:
    If you want to add more details to the model, you'll need to provide the AI with more information through prompts. It is recommended that your prompts be specific and descriptive. Try describing the shape, color, size, style, and other attributes of the object you want to generate. Longer prompts don't necessarily equate to better results, focus on the key concepts!
   
    Useful terms:
    Related to detail: highly detailed, high resolution, highest quality, best quality, 4K, 8K, HDR, studio quality
    Related to style: beautiful, elegant, realistic, ultra realistic, trending on artstation, masterpiece, cinema 4d, unreal engine, octane render
    Related to lighting: ambient lighting, soft lighting, sunlight, moonlight, fluorescent, glowing
   
    Negative Prompts:
    bad anatomy/proportions, deformed, dull, duplicate, extra arms/fingers/legs, low quality, missing arms/fingers/legs, obscure, poor lighting, ugly, unnatural colors, worst quality
    """
 
    # Construct the full prompt
    full_prompt = f"Task Description: {task_description}\nAsset Description: {asset_description}"
    if user_description:
        full_prompt += f"\nUser Description: {user_description}"
    full_prompt += f"\n\n{prompt_guidelines}\n\nGenerate a prompt for texturing based on the above descriptions and guidelines."
 
    # Use the LLM to generate the texturing prompt
    texturing_prompt = text_gemini(full_prompt)
    return texturing_prompt

if __name__=="__main__":
    print(generate_prompt('create a realistic dragon','a realistic dragon in medival China '))