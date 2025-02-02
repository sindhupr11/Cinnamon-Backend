import librosa
import numpy as np
import noisereduce as nr  

def convert_audio_to_notes(file_path: str) -> list:
    # Load audio with noise reduction
    y, sr = librosa.load(file_path, sr=22050, duration=30)
    
    # Step 1: Noise reduction
    reduced_noise = nr.reduce_noise(
        y=y, 
        sr=sr,
        stationary=True
    )
    
    # Step 2: Harmonic-percussive separation
    y_harmonic = librosa.effects.harmonic(reduced_noise, margin=8)
    
    # Step 3: Improved pitch detection
    f0 = librosa.yin(
        y_harmonic,
        fmin=200,   # C4 ≈ 261.63Hz, but we'll go lower to catch attacks
        fmax=600,   # C5 ≈ 523.25Hz
        sr=sr,
        frame_length=4096,  # Larger window for better accuracy
        win_length=1024,
        hop_length=512
    )
    
    # Step 4: Filter sustained notes
    notes = []
    previous_note = None
    for freq in f0:
        if freq > 0:
            note = freq_to_note(freq)
            if note and (note != previous_note):  # Remove repeated notes
                notes.append(note)
                previous_note = note
    
    return notes

def freq_to_note(freq: float) -> str:
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    try:
        midi_note = int(round(69 + 12 * np.log2(freq / 440.0)))
        if not (60 <= midi_note <= 72):  # C4-C5 range
            return ""
        
        # Quantize to nearest semitone to handle off-pitch frequencies
        quantized_freq = 440 * (2 ** ((midi_note - 69) / 12))
        if abs(freq - quantized_freq) > (quantized_freq * 0.03):  # 3% tolerance
            return ""
        
        return f"{note_names[midi_note % 12]}{(midi_note // 12) - 1}"
    
    except:
        return ""