import os
import mysql.connector
import json

# Fungsi untuk memuat data dari file JSON
def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Fungsi untuk menyisipkan data ke dalam database
def insert_data_to_database(data):
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="tiktoklive"
        )
        
        cursor = db_connection.cursor()

        for toko_data in data:
            nama_toko = toko_data['nama_toko']
            text = toko_data['text']

            # Memeriksa apakah toko sudah ada di database
            query_check_toko = "SELECT id_toko FROM toko WHERE nama_toko = %s"
            cursor.execute(query_check_toko, (nama_toko,))
            result = cursor.fetchone()

            if result:
                id_toko = result[0]
            else:
                # Jika belum ada, masukkan toko baru ke dalam database
                query_insert_toko = "INSERT INTO toko (nama_toko) VALUES (%s)"
                cursor.execute(query_insert_toko, (nama_toko,))
                id_toko = cursor.lastrowid

            # Masukkan teks ke dalam tabel audio_to_text
            query_text = "INSERT INTO audio_to_text (isi, id_toko) VALUES (%s, %s)"
            cursor.execute(query_text, (text, id_toko,))
            id_att = cursor.lastrowid

            # Masukkan data chat ke dalam tabel chat
            for chat_data in toko_data['chat']:
                username = chat_data['username']
                comment = chat_data['comment']

                query_chat = "INSERT INTO chat (username, comment, id_att) VALUES (%s, %s, %s)"
                cursor.execute(query_chat, (username, comment, id_att))

        db_connection.commit()
        print("Data berhasil dimasukkan ke dalam database.")

    except mysql.connector.Error as error:
        print(f"Error MySQL: {error}")

    finally:
        if 'db_connection' in locals() and db_connection.is_connected():
            cursor.close()
            db_connection.close()

# Fungsi untuk membersihkan file-file yang tidak diperlukan
def clean_up_files():
    folders_to_clean = [
        './result/chat/',
        './result/merge/',
        './result/video/media/',
        './result/video/text/'
    ]

    for folder in folders_to_clean:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"File {file_path} berhasil dihapus.")
            except Exception as e:
                print(f"Error saat menghapus {file_path}: {e}")

try:
    json_file_path = './result/merge/output.json'
    data_to_insert = load_data_from_json(json_file_path)

    insert_data_to_database(data_to_insert)
    clean_up_files()

except mysql.connector.Error as e:
    print(f"Error koneksi MySQL: {e}")