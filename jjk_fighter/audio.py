import pygame
import numpy as np
import struct
import io

# Initialize mixer
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)

_initialized = False

def init_audio():
    global _initialized
    if not _initialized:
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            _initialized = True
        except Exception:
            _initialized = False
    return _initialized

def _generate_tone(frequency, duration_ms, volume=0.3, wave_type="sine"):
    """Generate a tone as a pygame Sound object"""
    if not _initialized:
        return None
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = np.zeros((n_samples, 2), dtype=np.int16)

    for i in range(n_samples):
        t = i / sample_rate
        if wave_type == "sine":
            val = np.sin(2 * np.pi * frequency * t)
        elif wave_type == "square":
            val = 1.0 if np.sin(2 * np.pi * frequency * t) > 0 else -1.0
        elif wave_type == "saw":
            val = 2.0 * (t * frequency - int(t * frequency + 0.5))
        elif wave_type == "noise":
            val = np.random.uniform(-1, 1)
        else:
            val = np.sin(2 * np.pi * frequency * t)

        # Envelope
        attack = min(1.0, i / (sample_rate * 0.01))
        release = min(1.0, (n_samples - i) / (sample_rate * 0.05))
        envelope = attack * release

        sample = int(val * volume * envelope * 32767)
        buf[i] = [sample, sample]

    sound = pygame.sndarray.make_sound(buf)
    return sound

def _generate_sweep(start_freq, end_freq, duration_ms, volume=0.3):
    """Frequency sweep sound"""
    if not _initialized:
        return None
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = np.zeros((n_samples, 2), dtype=np.int16)

    for i in range(n_samples):
        t = i / sample_rate
        progress = i / n_samples
        freq = start_freq + (end_freq - start_freq) * progress
        val = np.sin(2 * np.pi * freq * t)
        attack = min(1.0, i / (sample_rate * 0.005))
        release = min(1.0, (n_samples - i) / (sample_rate * 0.03))
        envelope = attack * release
        sample = int(val * volume * envelope * 32767)
        buf[i] = [sample, sample]

    return pygame.sndarray.make_sound(buf)

# Pre-generated sounds cache
_sounds = {}

def _get_sound(name, generator, *args, **kwargs):
    if name not in _sounds:
        _sounds[name] = generator(*args, **kwargs)
    return _sounds[name]

def play_hit(heavy=False):
    if heavy:
        s = _get_sound("hit_heavy", _generate_sweep, 800, 200, 80, 0.4)
    else:
        s = _get_sound("hit_light", _generate_tone, 600, 40, 0.25, "noise")
    if s:
        s.play()

def play_block():
    s = _get_sound("block", _generate_tone, 200, 60, 0.3, "square")
    if s:
        s.play()

def play_special(char_id="default"):
    name = f"special_{char_id}"
    if name not in _sounds:
        _sounds[name] = _generate_sweep(300, 1200, 150, 0.35)
    _sounds[name].play()

def play_ultimate():
    s = _get_sound("ultimate", _generate_sweep, 200, 2000, 400, 0.45)
    if s:
        s.play()

def play_black_flash():
    s = _get_sound("black_flash", _generate_sweep, 500, 3000, 200, 0.5)
    if s:
        s.play()

def play_parry():
    s = _get_sound("parry", _generate_tone, 1500, 30, 0.4, "sine")
    if s:
        s.play()

def play_ui_select():
    s = _get_sound("ui_select", _generate_tone, 800, 50, 0.2, "sine")
    if s:
        s.play()

def play_ui_back():
    s = _get_sound("ui_back", _generate_tone, 400, 50, 0.2, "sine")
    if s:
        s.play()

def play_ko():
    s = _get_sound("ko", _generate_sweep, 800, 100, 500, 0.5)
    if s:
        s.play()

def play_domain_expansion():
    s = _get_sound("domain", _generate_sweep, 100, 1500, 800, 0.4)
    if s:
        s.play()

def play_heal():
    s = _get_sound("heal", _generate_sweep, 400, 800, 200, 0.25)
    if s:
        s.play()
