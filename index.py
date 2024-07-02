import os
import sys

try: 
    os.system("python scrapper.py")
except KeyboardInterrupt:
    pass
os.system("python extract_audio.py")
os.system("python json_join.py")
os.system("python database.py")
