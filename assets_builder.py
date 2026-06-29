import os
import math
import wave
import struct
from PIL import Image, ImageDraw

def create_dirs():
    for d in ["images", "sounds", "music"]:
        os.makedirs(d, exist_ok=True)

def generate_image(filename, color, text, size=(64, 64)):
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([2, 2, size[0]-3, size[1]-3], fill=color, outline="white", width=2)
    # Simple text placement, not using a specific font to avoid dependency issues
    img.save(f"images/{filename}.png")

def generate_tone(filename, freq, duration, volume=0.5):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for i in range(num_samples):
            t = float(i) / sample_rate
            value = int(volume * 32767.0 * math.sin(2.0 * math.pi * freq * t))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)

def generate_assets():
    create_dirs()
    
    # Hero (Blue square)
    generate_image("hero_idle1", (50, 50, 200), "H-I1")
    generate_image("hero_idle2", (60, 60, 220), "H-I2")
    generate_image("hero_run1", (40, 40, 255), "H-R1")
    generate_image("hero_run2", (70, 70, 180), "H-R2")
    
    # Enemy (Red square)
    generate_image("enemy_idle1", (200, 50, 50), "E-I1")
    generate_image("enemy_idle2", (220, 60, 60), "E-I2")
    generate_image("enemy_run1", (255, 40, 40), "E-R1")
    generate_image("enemy_run2", (180, 70, 70), "E-R2")
    
    # Environment
    generate_image("coin", (255, 215, 0), "C", size=(32, 32))
    generate_image("platform", (100, 200, 100), "P", size=(200, 32))
    generate_image("bg", (30, 30, 40), "BG", size=(800, 600))
    
    # Button
    generate_image("btn_bg", (100, 100, 100), "BTN", size=(200, 50))

    # Sounds
    generate_tone("sounds/jump.wav", 400, 0.15)
    generate_tone("sounds/coin.wav", 1000, 0.1)
    generate_tone("sounds/hit.wav", 150, 0.3)
    generate_tone("sounds/bgm.wav", 300, 2.0, 0.2) # Simple tone for music (will be looped)

if __name__ == "__main__":
    generate_assets()
    print("Assets generated successfully!")
