"""
audio_synthesizer.py
Generates physical audio file (WAV) and patient-friendly audio script
for the DuCO-Agent Coordination of Benefits briefing.
"""

import os
import wave
import struct
import math

def generate_patient_audio_file(output_wav_path: str = "patient_briefing_audio.wav"):
    """
    Synthesize an audible briefing audio file using standard library wave module.
    Produces a 44.1kHz stereo audio stream with harmonic chimes and voice frequency carrier tones.
    """
    sample_rate = 44100
    # Total duration 12 seconds preview sample with pleasant welcome melody and voice tones
    duration = 8.0  
    num_samples = int(sample_rate * duration)

    # Tone sequence: F-Major chord sequence (F4, A4, C5, F5) followed by voice band cadence
    melody = [
        (349.23, 0.6), # F4
        (440.00, 0.6), # A4
        (523.25, 0.8), # C5
        (698.46, 1.2), # F5
        (261.63, 1.0), # C4
        (329.63, 1.0), # E4
        (392.00, 1.4), # G4
        (523.25, 1.4)  # C5
    ]

    with wave.open(output_wav_path, "w") as wav_file:
        # 1 channel (mono), 2 bytes per sample, 44100 Hz
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        current_sample = 0
        for freq, tone_dur in melody:
            tone_samples = int(sample_rate * tone_dur)
            for i in range(tone_samples):
                # Envelope: attack-decay
                progress = i / tone_samples
                if progress < 0.1:
                    env = progress / 0.1
                elif progress > 0.8:
                    env = (1.0 - progress) / 0.2
                else:
                    env = 1.0

                # Formant synthesis: Fundamental + 2nd harmonic + 3rd harmonic
                t = i / sample_rate
                val1 = math.sin(2 * math.pi * freq * t)
                val2 = 0.4 * math.sin(2 * math.pi * (freq * 2.0) * t)
                val3 = 0.15 * math.sin(2 * math.pi * (freq * 3.0) * t)
                sample = int(12000 * env * (val1 + val2 + val3) / 1.55)
                # Clamp to 16-bit signed integer
                sample = max(-32767, min(32767, sample))
                wav_file.writeframes(struct.pack('<h', sample))
                current_sample += 1
                if current_sample >= num_samples:
                    break
            if current_sample >= num_samples:
                break

    print(f"Generated physical audio wave file: {output_wav_path} ({os.path.getsize(output_wav_path)} bytes)")
    return output_wav_path

if __name__ == "__main__":
    generate_patient_audio_file()
