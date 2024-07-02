import moviepy.editor as mp
import os
import speech_recognition as sr

# Konfigurasi bahasa untuk Google Speech Recognition
r = sr.Recognizer()
language = "id-ID"  # Kode bahasa untuk bahasa Indonesia

def extract_audio_file(video):
    try:
        video_clip = mp.VideoFileClip(video)
        audio_clip = video_clip.audio
        audio_file_path = video.replace(".mp4", ".wav")
        audio_clip.write_audiofile(audio_file_path)
        
        with sr.AudioFile(audio_file_path) as source:
            audio_text = r.listen(source)
            try:
                text = r.recognize_google(audio_text, language=language)
                print('Mengonversi transkrip audio menjadi teks ...')
                
                os.makedirs("./result/video/text", exist_ok=True)
                
                text_file_path = os.path.join("./result/video/text", os.path.basename(video).replace(".mp4", ".txt"))
                with open(text_file_path, "w", encoding="utf-8") as text_file:
                    text_file.write(text)
                
            except sr.UnknownValueError:
                print("Google Speech Recognition tidak bisa mengenali audio")
            except sr.RequestError as e:
                print(f"Permintaan ke Google Speech Recognition error; {e}")
    finally:
        video_clip.close()
        audio_clip.close()
        os.remove(audio_file_path)

if __name__ == "__main__":
    folder_path = "./result/video/media"
    video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

    for video in video_files:
        video_path = os.path.join(folder_path, video)
        extract_audio_file(video_path)
