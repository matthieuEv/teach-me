from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import json

# Charger les variables d'environnement

def generate_educational_content(subject):
    load_dotenv()
    nbr_errors = 0

    print("Using model: ", os.getenv("LLAMA_MODEL"))

    while nbr_errors < 3:
        print("Nb errors: ", nbr_errors)
        nbr_errors += 1
        start_time = time.time()
        # Prompt initial basé sur le modèle de ton README, avec le sujet inséré
        initial_prompt = f"""
        You are a teacher. Teach me about {subject}. You will make separated chapters, and return a response like this json. There is a max of 3 chapters. In the end, you will have to make a QCM based on the class you gave using the json format i gave you. There is a max of 5 questions.

        the introduction paragraph is the first paragraph of your course, it has to be very general, and very attractive, so the student will want to learn more about the subject, but also small, so the student will not be bored.

        for the end paragraph, it has to be a conclusion of the course, and it has to be very general, and very attractive, so the student will want to learn more about the subject, but also realy small. At the end, talk about the test, and tell the student to do it.

        ## Script Json Format

        {{
        "script": {{
        "title_course": str,
        "introduction_paragraph": str,
        "end_paragraph": str,
        "chapters": [
        {{
        "title_chapter": str,
        "content": str
        "images": [str]
        }},
        ...
        ]
        }},
        "qcm": [
        {{
        "question": str,
        "list_answers": [str],
        "index_good_answer": int
        }}
        ]
        }}

        in the chapters the images are a list of prompt you will give to illustrate your content. the prompt have to be very descriptif, it has to be very realistic, so do the prompt so.
        there could be multiple images for one chapter. in the image list, there must be only the string

        you will response with the json, and only the json, whitout the ```json``` tag, and without the ```\n``` tag.

        for the title_chapters, i want a simple namne, simply describing with 2-3 words. And i dont want "Chapter 1." or something like that at the start
        """

        # Initialisation du client OpenAI
        client = OpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
            api_key = os.getenv("NVIDIA_API_KEY")
        )

        response = client.chat.completions.create(
            model=os.getenv("LLAMA_MODEL"),
            messages=[{"role":"user","content":initial_prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False
        )

        # Récupération et affichage du résultat
        result = response.choices[0].message.content

        if(verify_json_output(result[0])):
            print("the result is valid")
            break

    end_time = time.time()

    execution_time = end_time - start_time

    print("result: ",result,"\n\n")

    return {
        "json": json.loads(result),
        "exec": execution_time
    }

def verify_json_output(output):
    try:
        # Parse the output as JSON
        data = json.loads(output)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"

    # Define the expected structure
    expected_structure = {
        "script": {
            "title_course": str,
            "introduction_paragraph": str,
            "end_paragraph": str,
            "chapters": [
                {
                    "title_chapter": str,
                    "content": str,
                    "images": list
                }
            ]
        },
        "qcm": [
            {
                "question": str,
                "list_answers": list,
                "index_good_answer": int
            }
        ]
    }

    # Helper function to check if a value matches the expected type or structure
    def matches_structure(expected, actual, path="root"):
        if isinstance(expected, dict):
            if not isinstance(actual, dict):
                return False, f"Expected a dictionary at {path}, got {type(actual).__name__}"
            for key, expected_value in expected.items():
                if key not in actual:
                    return False, f"Missing key '{key}' at {path}"
                is_valid, message = matches_structure(expected_value, actual[key], f"{path}.{key}")
                if not is_valid:
                    return is_valid, message
            return True, ""
        elif isinstance(expected, list):
            if not isinstance(actual, list):
                return False, f"Expected a list at {path}, got {type(actual).__name__}"
            if len(actual) == 0:
                return True, ""  # Allow empty lists
            for index, item in enumerate(actual):
                is_valid, message = matches_structure(expected[0], item, f"{path}[{index}]")
                if not is_valid:
                    return is_valid, message
            return True, ""
        else:
            if not isinstance(actual, expected):
                return False, f"Expected {expected.__name__} at {path}, got {type(actual).__name__}"
            return True, ""

    # Validate the structure
    is_valid, message = matches_structure(expected_structure, data)
    return is_valid, message

if __name__ == "__main__":
    # Exemple d'utilisation
    # subject = "the Solar System"

    # result = generate_educational_content(subject)
    # print(result.json)
    f = open("example.json", "r")
    print(verify_json_output(f.read()))