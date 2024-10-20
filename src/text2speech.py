import os
from dotenv import load_dotenv

load_dotenv()

def generate_audio(prompt: str, prompt_index: int) -> str:
    """Generates audio from a given prompt using the NVIDIA TTS API.

    Args:
        prompt (str): the text to be converted to speech
        prompt_index (int): the index of the prompt

    Returns:
        str: the path to the generated audio file
    """
    current_path = os.getcwd()

    # Create a "data" directory if it doesn't exist
    data_dir = os.path.join(current_path, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Define the output path
    output_path = os.path.join(current_path, "data", str(prompt_index)+".wav")

    # Use the python-clients to generate the audio
    # https://github.com/nvidia-riva/python-clients
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
