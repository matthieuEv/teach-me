from prompt import generate_educational_content
from text2speech import generate_audio
from text2image import generate_picture
from generate_video.main import generate_chapter_video, generate_title_picture, concat_videos, generate_title_video
import os
from dotenv import load_dotenv
import time

load_dotenv()

def delete_all_files_in_data_directory():
    data_dir = os.path.join(os.getcwd(), 'data')
    if os.path.exists(data_dir):
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
    start_time = time.time()
    delete_all_files_in_data_directory()

    # prompt = input("Teach me about ")
    prompt = "the solar system"
    jsonOut = generate_educational_content(prompt)

    count_chapters = len(jsonOut["json"]["script"]["chapters"])
    generate_audio(jsonOut["json"]["script"]["introduction_paragraph"],0)
    generate_audio(jsonOut["json"]["script"]["end_paragraph"],count_chapters+1)
    for chapter_index, chapter in enumerate(jsonOut["json"]["script"]["chapters"]):
        print("\n"+str(chapter_index+1)+" - "+chapter["content"]+"\n")
        generate_audio(chapter["content"],chapter_index+1)

        for images_index, images_prompt in enumerate(chapter["images"]):
            print("\n"+images_prompt+"\n")
            generate_picture(images_prompt,str(chapter_index+1)+"_"+str(images_index))

    title_picture_path = generate_title_picture(jsonOut["json"]["script"]["title_course"],0,font_size=100)
    print("title_picture_path: ",title_picture_path)

    title_video_path = generate_chapter_video("data/0.wav",[title_picture_path],0)
    print("title_video_path: ",title_video_path)

    for chapter_index, chapter in enumerate(jsonOut["json"]["script"]["chapters"]):
        title_video = generate_title_video(chapter["title_chapter"],chapter_index+1,font_size=80)

        images_path = [f"data/{chapter_index+1}_{i}.jpg" for i in range(len(chapter["images"]))]
        chapter_video = generate_chapter_video(f"data/{chapter_index+1}.wav",images_path,chapter_index+1)

    end_picture_path = generate_title_picture("The END",count_chapters+1,font_size=100)
    end_video_path = generate_chapter_video(f"data/{count_chapters+1}.wav",[end_picture_path],count_chapters+1)

    chapter_videos = []
    for i in range(count_chapters):
        chapter_videos.append(f"data/title_{i+1}.mp4")
        chapter_videos.append(f"data/{i+1}.mp4")
    print("list ",[title_video_path] + chapter_videos + [end_video_path])
    concat_videos([title_video_path] + chapter_videos + [end_video_path], "output")
    end_time = time.time()

    print(f"Execution time: {int((end_time - start_time) // 60)} minutes and {int((end_time - start_time) % 60)} seconds")