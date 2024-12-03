from flask import Flask, request, render_template, url_for, send_from_directory
import os
import subprocess
import matplotlib.pyplot as plt

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
COMPRESSED_FOLDER = 'static/compressed'
WAVEFORM_FOLDER = 'static/waveforms'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)
os.makedirs(WAVEFORM_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return "No file provided!", 400
    
    video = request.files['file']
    input_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(input_path)
    
    # Compress the video
    try:
        compressed_path = compress_video('C:\Users\Fabheads21\AI based video compression\static\uploads\6214616-hd_1080_1920_25fps.mp4')
        print(input_path)
    except Exception as e:
        return f"Error during compression: {str(e)}", 500
    
    # Generate waveforms
    try:
        waveform_path = generate_waveform(input_path, compressed_path)
    except Exception as e:
        return f"Error during waveform generation: {str(e)}", 500
    
    # Generate URLs for the results
    compressed_video_url = url_for('static', filename=f'compressed/{os.path.basename(compressed_path)}')
    waveform_url = url_for('static', filename=f'waveforms/{os.path.basename(waveform_path)}')
    
    return render_template('result.html', compressed_video=compressed_video_url, waveform=waveform_url)

def compress_video(input_path):
    filename = os.path.basename(input_path)
    compressed_path = os.path.join(COMPRESSED_FOLDER, f"compressed_{filename}")
    
    try:
        # HEVC Compression using FFmpeg
        result = subprocess.run(
            ["ffmpeg", "-i", input_path, "-c:v", "libx265", "-crf", "28", compressed_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")
    except Exception as e:
        raise RuntimeError(f"Failed to compress video: {str(e)}")
    
    return compressed_path

def generate_waveform(input_path, compressed_path):
    try:
        input_bitrate = get_bitrate(input_path)
        compressed_bitrate = get_bitrate(compressed_path)
    except Exception as e:
        raise RuntimeError(f"Error getting bitrate: {str(e)}")
    
    wave_path = os.path.join(WAVEFORM_FOLDER, f"waveform_{os.path.basename(input_path)}.png")
    try:
        plt.figure()
        plt.bar(["Original", "Compressed"], [input_bitrate, compressed_bitrate], color=['blue', 'orange'])
        plt.title("Bitrate Comparison")
        plt.ylabel("Bitrate (kbps)")
        plt.savefig(wave_path)
        plt.close()
    except Exception as e:
        raise RuntimeError(f"Error generating waveform: {str(e)}")
    
    return wave_path

def get_bitrate(video_path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=bit_rate", "-of", "default=noprint_wrappers=1", video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        bitrate = result.stdout.decode().strip().split("=")[-1]
        return int(bitrate) / 1000  # Convert to kbps
    except Exception as e:
        raise RuntimeError(f"Error getting bitrate: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
