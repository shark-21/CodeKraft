import google.generativeai as genai
from transformers import AutoModel
from numpy.linalg import norm

# Generate an API Key from references as given in README
GEMINI_API_KEY = ""

# We use Gemini Pro for our implemetation
model = genai.GenerativeModel('gemini-pro')
genai.configure(api_key = GEMINI_API_KEY)

# This function return the similarity between prompt and the code description generated by model
def get_similarity(prompt, description):
    cos_sim = lambda a,b: (a @ b.T) / (norm(a)*norm(b))
    jina_model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True)
    embeddings = jina_model.encode([prompt,description])
    return cos_sim(embeddings[0], embeddings[1])

# This function returns the code, pseudocode, description and similarity score from the given prompt, database schema and template
def get_result(user_prompt = "Haleluya", database_schema = "", template = ""):
    print(user_prompt)
    print(database_schema)
    print(template)
    print("gr: 0")
    if (GEMINI_API_KEY == ""):
        raise ValueError("Please set your API key.")
    # We have two things: user_prompt and database schema
    prompt = "Output code as requested here: " + user_prompt + "Consider the following database schema: " + database_schema + "Display the result uding this format: " + template
    code = model.generate_content(prompt)
    pseudocode_prompt = "Give me a pseudocode for the following code: " + code.text
    pseudocode = model.generate_content(pseudocode_prompt)
    description_prompt = "Give me a breif description of the following code: " + code.text

    description = model.generate_content(description_prompt)
    print(description.text)
    similarity_score = get_similarity(user_prompt, description.text)
    return code.text, pseudocode.text, description.text, similarity_score

# This function evaluates performance metrics 
def eval_query(query):
    prompt = "Give example, expected output and actual output as a json along with time and memory taken for the following code: " + query
    response = model.generate_content(prompt)
    return response.text