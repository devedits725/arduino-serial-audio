import time
import sys
import os
import serial
import serial.tools.list_ports
import miniaudio
import numpy as np

# ----- SETTINGS ------
BAUD = 115200
SAMPLE_RATE = 7664 # this worked best for me , optimal rate = 8000
CHUNK = 256
# ----------------------

SUPPORTED = [".mp3", ".wav", ".ogg", ".flac"]


def find_arduino():
    ports = serial.tools.list_ports.comports()

    for p in ports:
        if any(x in p.description.upper() for x in
               ["ARDUINO", "CH340", "CH341", "FTDI", "USB SERIAL", "CP210"]):
            print(f"Found Arduino on {p.device} ({p.description})")
            return p.device

    print("Arduino not found automatically.")
    print("Available ports:")

    for p in ports:
        print(f"  {p.device} - {p.description}")

    return None


def convert(input_path):
    print(f"Converting {os.path.basename(input_path)}...")

    ext = os.path.splitext(input_path)[1].lower()

    if ext == ".mp3":
        decoded = miniaudio.mp3_read_file_s16(input_path)
    elif ext == ".wav":
        decoded = miniaudio.wav_read_file_s16(input_path)
    elif ext == ".ogg":
        decoded = miniaudio.vorbis_read_file_s16(input_path)
    elif ext == ".flac":
        decoded = miniaudio.flac_read_file_s16(input_path)
    else:
        raise ValueError("Unsupported format")

    print("Channels:", decoded.nchannels)
    print("Source sample rate:", decoded.sample_rate)

    samples = np.array(decoded.samples, dtype=np.int16)

    # Stereo to Mono
    if decoded.nchannels == 2:
        samples = samples.reshape(-1, 2)
        samples = samples.mean(axis=1)

    samples = samples.astype(np.float32)

    # Normalize
    peak = np.max(np.abs(samples))

    if peak > 0:
        samples *= (32767.0 / peak)

    # Resample
    old_length = len(samples)
    new_length = int(old_length * SAMPLE_RATE / decoded.sample_rate)

    old_x = np.arange(old_length)
    new_x = np.linspace(0, old_length - 1, new_length)

    samples = np.interp(new_x, old_x, samples)

    samples = np.sign(samples) * (
        np.abs(samples) / 32768.0
    ) ** 0.8

    samples *= 32767.0

    # Convert to 8-bit
    samples = np.clip(samples, -32768, 32767)

    output = ((samples + 32768) / 256).astype(np.uint8)

    duration = len(output) / SAMPLE_RATE

    print(f"Resampled: {decoded.sample_rate} Hz -> {SAMPLE_RATE} Hz")
    print("Min sample:", int(output.min()))
    print("Max sample:", int(output.max()))
    print("Conversion complete.")

    return output.tobytes(), duration


def play(samples, duration, port):
    print(f"Connecting to {port}...")

    try:
        ser = serial.Serial(port, BAUD, timeout=1)
        time.sleep(2)
    except Exception as e:
        print("Serial error:", e)
        sys.exit(1)

    print(f"Duration: {duration:.1f}s")
    print("Playing...")

    total = len(samples)
    start = time.time()

    try:
        for i in range(0, total, CHUNK):
            chunk = samples[i:i + CHUNK]
            ser.write(chunk)
            expected = start + (i / SAMPLE_RATE)
            delay = expected - time.time()

            if delay > 0:
                time.sleep(delay)

            if i % 8000 == 0:
                percent = int(i * 100 / total)

                print(
                    f"Progress: {percent}% "
                    f"({int(time.time() - start)}s/{int(duration)}s)",
                    end="\r"
                )

    except KeyboardInterrupt:
        print("\nStopped.")

    ser.close()
    print("\nDone.")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("python play.py song.xyz COM3")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print("File not found:", input_file)
        sys.exit(1)

    ext = os.path.splitext(input_file)[1].lower()

    if ext not in SUPPORTED:
        print("Unsupported format:", ext)
        sys.exit(1)

    if len(sys.argv) >= 3:
        port = sys.argv[2]
    else:
        port = find_arduino()

    if port is None:
        sys.exit(1)

    samples, duration = convert(input_file)

    print(f"Generated {len(samples)} audio bytes")

    play(samples, duration, port)
