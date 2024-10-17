from moviepy.editor import *
from pydub import AudioSegment
import os

def generate_chapter_video(audio_path, image_paths, chapter_index):
    # Chemin vers ton fichier audio
    audio_path = "data/0.wav"

    # Liste des chemins vers tes images
    image_paths = [
        "data/0_0.jpg.jpg",
        "data/0_1.jpg.jpg",
        "data/0_2.jpg.jpg",
        "data/0_3.jpg.jpg",
    ]

    # Charger l'audio pour obtenir sa durée
    audio = AudioSegment.from_file(audio_path)
    audio_duration = audio.duration_seconds

    # Calculer la durée de chaque image
    image_duration = audio_duration / len(image_paths)

    # Créer un clip vidéo pour chaque image
    clips = [ImageClip(image).set_duration(image_duration) for image in image_paths]

    # Définir le fps pour chaque clip
    clips = [clip.set_fps(24) for clip in clips]  # 24 est un exemple, tu peux ajuster selon tes besoins

    # Combiner les clips en une seule séquence vidéo
    video = concatenate_videoclips(clips, method="compose")

    # Exporter la vidéo finale
    video.write_videofile(f"{chapter_index}_temp.mp4", codec="libx264", audio_codec="libvorbis", fps=24)

    videoclip = VideoFileClip(f"{chapter_index}_temp.mp4")
    audioclip = AudioFileClip(audio_path)

    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile(f"{chapter_index}.mp4")
    os.remove(f"{chapter_index}_temp.mp4")

    return f"{chapter_index}.mp4"

if __name__ == "__main__":
    generate_chapter_video("data/0.wav", ["data/0_0.jpg.jpg", "data/0_1.jpg.jpg", "data/0_2.jpg.jpg", "data/0_3.jpg.jpg"], 0)