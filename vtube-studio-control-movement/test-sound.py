import requests
import json
import io
import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import time

def text_to_speech_and_play(text):
    """Call the TTS API and play the WAV content directly with volume control"""
    url = "http://localhost:5000"
    payload = {"text": text}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        wav_bytes = response.content
        wav_io = io.BytesIO(wav_bytes)
        data, samplerate = sf.read(wav_io)
        
        def monitor_loudness():
            monitor_block_size = int(samplerate * 0.05)  # 50ms
            
            for i in range(0, len(data), monitor_block_size):
                if i + monitor_block_size <= len(data):
                    block = data[i:i+monitor_block_size]
                    block_rms = np.sqrt(np.mean(block**2))
                    mouth_val = min(block_rms * 5, 1.0) 
                    
                    # Print loudness every 200ms to avoid spam
                    if i % (monitor_block_size * 4) == 0:
                        print(f"Time: {i/samplerate:.2f}s | Mouth Value: {mouth_val:.3f} | RMS: {block_rms:.4f}")
                
                time.sleep(0.05)
        
        monitor_thread = threading.Thread(target=monitor_loudness)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        monitor_thread.join(timeout=60)
        print("Playback finished")

if __name__ == "__main__":
    test_text = "This is a test of the text-to-speech system with volume control."
    text_to_speech_and_play(test_text)