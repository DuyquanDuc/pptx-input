from openai import AzureOpenAI
import base64
from utils import ExtractJSON, replace_newlines, ensure_single_value
import instructor
import json
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv('local.env')

#Set up Azure client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-07-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

#Response for each image
def response(image_path):
    """
    Sends an Image and gets a response.
    """ 

    # Reformat the image
    with open(image_path, "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Initialize return string
    summary = ""
    
    # Assuming `client.chat.completions.create` returns a complete response when not streaming
    response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Summarize the content of the image in 2 sentences. Pay attention to numbers, highlight or visualization."},
                        {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}"
                        },
                        },
                    ],
                    }
                ],
                max_tokens=300,
                )
    
    if response.choices and response.choices[0].message.content:
        summary += response.choices[0].message.content
    
    return summary

def compiling_agent(input):
    """
    Sends a chunk of text to the model and gets a response.
    """ 
    #Initiate a blank
    output = ""
    # Assuming `client.chat.completions.create` returns a complete response when not streaming
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant. Your job is to summarize the content provide."},
                  {"role": "user", "content": f"""based on this information: "{input}"  + 
                   summarize and aggregate the content and organize it so that it visually attractive. 
                   The output should be a general summary of everything. """}
                  ]
    )
    if response.choices and response.choices[0].message.content:
        output += response.choices[0].message.content
    return output

    
#This function is for JSON Parsing 
def parse_json(image_path: str, extract_fields, slide_class)-> ExtractJSON:
    """
    Sends an image and gets a response containing a list of objects.
    
    """
    # Reformat the image
    with open(image_path, "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Define field lists based on slide class
    """
    # Build the extract prompt based on slide_class
    if slide_class == "schedule":
        extract_fields = schedule_fields
    elif slide_class == "organization":
        extract_fields = org_fields
    else:  # "both" or any other value
        extract_fields = extract_fields
    """
    # Constructing the prompt or message content based on the extract_fields
    extract_prompt = f"""
    Please extract the following fields in a JSON data key-value format: {extract_fields}.
    The data should be formatted into a structured JSON format, ensuring that 
    each key is clearly defined and that similar data is grouped together under appropriate categories. 
    The JSON should be concise and avoid any redundancy.
    """
    # Patch the OpenAI client
    azure_client = instructor.from_openai(AzureOpenAI(api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-07-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    ))
    # Assuming `instructor` is the correct client or replace it with the appropriate API call
    response = azure_client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=ExtractJSON,
        messages=[
            {
                "role": "user",
                "content": f'{extract_prompt}',
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}"
                        }
                    },
                ],
            }
        ],
    )
    
    # Parse the JSON response to ObjectList
    try:
        # Convert the Pydantic model to a dictionary
        response_dict = response.dict()
        # Replace \n with spaces in the dictionary
        response_dict = replace_newlines(response_dict)
        response_dict = ensure_single_value(response_dict)
        # Pretty-print the JSON output
        json_output = json.dumps(response_dict, indent=4, ensure_ascii=False) 
        return json_output
    except Exception as e:
        print(f"Error parsing response: {e}")
        return None