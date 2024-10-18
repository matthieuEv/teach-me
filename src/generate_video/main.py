from moviepy.editor import *
from pydub import AudioSegment
import os
from PIL import Image, ImageDraw, ImageFont

# Taille des images après recadrage
picture_size = (1344, 768)
color_white = '#D9D9D9'
color_blue = '#414A6E'

def generate_chapter_video(audio_path, image_paths, chapter_index):
    # Charger l'audio pour obtenir sa durée
    audio = AudioSegment.from_file(audio_path)
    audio_duration = audio.duration_seconds

    # Calculer la durée de chaque image
    image_duration = audio_duration / len(image_paths)

    # Créer un clip vidéo pour chaque image
    clips = []
    for image_path in image_paths:
        # Charger l'image
        clip = ImageClip(image_path)
        
        # Recadrer l'image pour obtenir la taille désirée
        clip = clip.crop(width=picture_size[0], height=picture_size[1], x_center=clip.w/2, y_center=clip.h/2)
        
        # Définir la durée pour chaque image
        clip = clip.set_duration(image_duration)
        
        # Ajouter le clip à la liste
        clips.append(clip)
    
    # Définir le fps pour chaque clip
    clips = [clip.set_fps(24) for clip in clips]

    # Combiner les clips en une seule séquence vidéo
    video = concatenate_videoclips(clips, method="compose")

    # Exporter la vidéo finale sans audio d'abord
    video.write_videofile(f"data/{chapter_index}_temp.mp4", codec="libx264", audio_codec="libvorbis", fps=24)

    # Charger le clip vidéo généré et l'audio
    videoclip = VideoFileClip(f"data/{chapter_index}_temp.mp4")
    audioclip = AudioFileClip(audio_path)

    # Créer un nouveau clip audio composite
    new_audioclip = CompositeAudioClip([audioclip])

    # Ajouter 1sec de silence à la fin de l'audio pour éviter les erreurs
    new_audioclip = new_audioclip.set_duration(videoclip.duration - 0.1)

    videoclip = videoclip.set_audio(new_audioclip)

    # Exporter la vidéo finale avec audio
    videoclip.write_videofile(f"data/{chapter_index}.mp4", codec="libx264", audio_codec="aac")

    # Supprimer le fichier temporaire
    os.remove(f"data/{chapter_index}_temp.mp4")

    return f"data/{chapter_index}.mp4"

def generate_title_picture(title, chapter_index, font_size=60):
    max_char_in_line = 23

    # Fonction pour diviser le texte en lignes
    def split_text_to_lines(text, max_chars):
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            # Vérifie si ajouter ce mot dépasse la limite de caractères
            if current_length + len(word) + len(current_line) > max_chars:
                # Joins les mots pour former une ligne et l'ajoute à la liste
                lines.append(" ".join(current_line))
                # Réinitialise la ligne actuelle avec le mot en cours
                current_line = [word]
                current_length = len(word)
            else:
                current_line.append(word)
                current_length += len(word)

        # Ajoute la dernière ligne si elle n'est pas vide
        if current_line:
            lines.append(" ".join(current_line))

        return lines

    # Diviser le titre en plusieurs lignes
    lines = split_text_to_lines(title, max_char_in_line)

    # Créer une image avec un fond bleu
    img = Image.new('RGB', picture_size, color=color_blue)

    # Initialiser ImageDraw
    d = ImageDraw.Draw(img)

    # Définir la police et la taille
    font_path = "src/generate_video/Poppins-SemiBold.ttf"  # Met à jour ce chemin vers la police que tu veux utiliser
    font = ImageFont.truetype(font_path, font_size)

    # Calculer la position Y de départ pour centrer le texte verticalement
    total_text_height = sum(d.textbbox((0, 0), line, font=font)[3] - d.textbbox((0, 0), line, font=font)[1] for line in lines)
    y = (picture_size[1] - total_text_height) / 2

    # Ajouter chaque ligne de texte à l'image
    for line in lines:
        text_bbox = d.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (picture_size[0] - text_width) / 2
        d.text((x, y), line, font=font, fill=color_white)
        y += text_height  # Avance la position Y pour la ligne suivante

    # Sauvegarder l'image
    img_path = f"data/title_{chapter_index}.png"
    img.save(img_path)

    return img_path

def generate_title_video(title, chapter_index, font_size=60, duration=3):
    # Créer une image avec un fond bleu
    img = Image.new('RGB', picture_size, color=color_blue)

    # Initialiser ImageDraw
    d = ImageDraw.Draw(img)

    # Définir la police et la taille
    font_path = "src/generate_video/Poppins-SemiBold.ttf"  # Met à jour ce chemin vers la police que tu veux utiliser
    font = ImageFont.truetype(font_path, font_size)

    # Calculer la largeur et la hauteur du texte à ajouter
    text_bbox = d.textbbox((0, 0), title, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calculer la position X, Y du texte
    x = (picture_size[0] - text_width) / 2
    y = (picture_size[1] - text_height) / 2

    # Ajouter du texte à l'image
    d.text((x, y), title, font=font, fill=color_white)

    # Sauvegarder l'image temporairement
    img_path = f"data/title_{chapter_index}.png"
    img.save(img_path)

    # Créer un clip vidéo de 5 secondes à partir de l'image
    video_clip = ImageClip(img_path).set_duration(duration)

    # Exporter la vidéo
    video_path = f"data/title_{chapter_index}.mp4"
    video_clip.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac')

    # Supprimer l'image temporaire
    os.remove(img_path)

    return video_path

def concat_videos(videos_path, output_path):
    # Charger les clips vidéo
    clips = []
    for video_path in videos_path:
        clip = VideoFileClip(video_path)

        # enlever 1s
        clip = clip.subclip(0, clip.duration-0.2)

        clips.append(clip)

    # Combiner les clips en une seule séquence vidéo
    final_clip = concatenate_videoclips(clips, method="compose")

    # Exporter la vidéo finale
    final_clip.write_videofile(f"data/{output_path}.mp4", codec="libx264", audio_codec="aac")

    return f"data/{output_path}.mp4"

if __name__ == "__main__":
    # generate_chapter_video("data/0.wav", ["data/0_0.jpg.jpg", "data/0_1.jpg.jpg", "data/0_2.jpg.jpg", "data/0_3.jpg.jpg"], 0)
    # generate_title_picture("This is a very long text and its good",0,font_size=90)
    concat_videos(["data/0.mp4","data/title_1.mp4","data/1.mp4"], "output")
    # generate_chapter_video("data/0.wav", ["data/title_0.png"], 10)