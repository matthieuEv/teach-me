from prompt import generate_educational_content
from text2speech import generate_audio
from text2image import generate_picture
import os

def delete_all_files_in_data_directory():
    data_directory = os.path.join(os.getcwd(), 'data')
    for filename in os.listdir(data_directory):
        file_path = os.path.join(data_directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print(f'Deletec: {file_path}')
        except Exception as e:
            print(f'Erreur lors de la suppression de {file_path}. Raison: {e}')

if __name__ == "__main__":
    delete_all_files_in_data_directory()

    prompt = input("Teach me about ")
    # prompt = "the solar system"
    jsonOut = generate_educational_content(prompt)
    print(jsonOut["json"]["script"])
    for chapter_index, chapter in enumerate(jsonOut["json"]["script"]["chapters"]):
        
        generate_audio(chapter["content"],chapter_index)

        for images_index, images_prompt in enumerate(chapter["images"]):
            print("\n"+images_prompt+"\n")
            generate_picture(images_prompt,str(chapter_index)+"_"+str(images_index)+".jpg")