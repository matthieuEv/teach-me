import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def generate_audio(prompt, prompt_index):
    current_path = os.getcwd()

    output_path = os.path.join(current_path, "data", str(prompt_index)+".wav")

    os.system(
        f'python {current_path}/src/python-clients/scripts/tts/talk.py '
        '--server grpc.nvcf.nvidia.com:443 --use-ssl '
        '--metadata function-id "0149dedb-2be8-4195-b9a0-e57e0e14f972" '
        f'--metadata authorization "Bearer {os.getenv("OPENAI_API_KEY")}" '
        f'--text "{prompt}" '
        '--voice "English-US.Male-1" '
        f'--output {output_path}'
    )
    return output_path

if __name__ == "__main__":
    prompt = "I'm an engineer who lives in Angers, in france, and i love biking."

    generate_audio(prompt, 2)
