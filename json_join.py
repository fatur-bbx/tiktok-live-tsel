import json
import os

# Mendapatkan daftar file JSON di dalam direktori ./result/chat/
chat_dir = './result/chat/'
chat_files = [f for f in os.listdir(chat_dir) if f.endswith('.json')]

# Mendapatkan daftar file teks di dalam direktori ./result/video/text/
text_dir = './result/video/text/'
text_files = [f for f in os.listdir(text_dir) if f.endswith('.txt')]

# Fungsi untuk mengekstrak nama file dasar dari teks berdasarkan pola
def extract_base_filename(filename):
    return filename.split('_')[1]

# Menggabungkan data sesuai dengan pola yang disebutkan
merged_data = []

for text_file in text_files:
    base_name = extract_base_filename(text_file)

    for chat_file in chat_files:
        if base_name in chat_file:
            # Membaca data dari file chat.json
            chat_path = os.path.join(chat_dir, chat_file)
            with open(chat_path, 'r', encoding='utf-8') as chat_file:
                chat_data = json.load(chat_file)

            # Membaca teks dari file text.txt
            text_path = os.path.join(text_dir, text_file)
            with open(text_path, 'r', encoding='utf-8') as text_file:
                text_data = text_file.read().strip()

            # Menyiapkan output dalam bentuk yang diinginkan
            output = {
                "nama_toko" : base_name,
                "text": text_data,
                "chat": chat_data
            }

            merged_data.append(output)

# Pastikan direktori ./result/merge/ tersedia
output_dir = './result/merge/'
os.makedirs(output_dir, exist_ok=True)

# Simpan output ke file output.json di dalam direktori ./result/merge/
output_path = os.path.join(output_dir, 'output.json')
with open(output_path, 'w', encoding='utf-8') as output_file:
    json.dump(merged_data, output_file, ensure_ascii=False, indent=4)

print(f"Data berhasil digabungkan dan disimpan dalam file {output_path}.")
