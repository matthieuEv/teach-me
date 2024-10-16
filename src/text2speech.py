import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def generate_audio(prompt, prompt_index):
    current_path = os.getcwd()

    data_dir = os.path.join(current_path, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    output_path = os.path.join(current_path, "data", str(prompt_index)+".wav")

    os.system(f'python {current_path}/src/python-clients/scripts/tts/talk.py '
        '--server grpc.nvcf.nvidia.com:443 --use-ssl '
        '--metadata function-id "5e607c81-7aa6-44ce-a11d-9e08f0a3fe49"  '
        f'--metadata authorization "Bearer {os.getenv("NVIDIA_API_KEY")}" '
        f'--text "{prompt}" '
        '--voice "English-US-RadTTS.Male-1" '
        f'--output {output_path}'
    )
    return output_path

if __name__ == "__main__":
    prompt = "I'm an engineer who lives in Angers, in france, and i love biking."

    generate_audio(prompt, 2)
