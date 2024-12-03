import subprocess
import os
import matplotlib.pyplot as plt

# Path to your input video
input_video_path = r"C:\\Users\\Fabheads21\\AI based video compression\\static\\uploads\\6214616-hd_1080_1920_25fps.mp4"
output_video_path = r"C:\\Users\\Fabheads21\\AI based video compression\\static\\compressed\\compressed_video.mp4"
waveform_path = r"C:\\Users\\Fabheads21\\AI based video compression\\static\\waveforms\\bitrate_comparison.png"

# Function to get the bitrate of a video
def get_bitrate(video_path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=bit_rate", "-of", "default=noprint_wrappers=1", video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Ensure output is returned as a string (Python 3)
        )
        bitrate = result.stdout.strip().split("=")[-1]  # No need for .decode() in Python 3
        return int(bitrate) / 1000  # Convert to kbps
    except Exception as e:
        print(f"Error getting bitrate for {video_path}: {str(e)}")
        return 0

# Run FFmpeg command to compress the video
try:
    result = subprocess.run(
        ["ffmpeg", "-i", input_video_path, "-c:v", "libx265", "-crf", "28", output_video_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Check if FFmpeg ran successfully
    if result.returncode == 0:
        print(f"Video successfully compressed! Output saved at: {output_video_path}")
    else:
        print("Error during compression:")
        print(result.stderr)

except FileNotFoundError as e:
    print(f"Error: FFmpeg executable not found. Please check the system's PATH. {str(e)}")

except Exception as e:
    print(f"An error occurred during compression: {str(e)}")

# Get the bitrates of the original and compressed videos
input_bitrate = get_bitrate(input_video_path)
compressed_bitrate = get_bitrate(output_video_path)

# Generate a waveform (bar chart) comparing the bitrates
try:
    plt.figure(figsize=(6, 4))
    plt.bar(["Original", "Compressed"], [input_bitrate, compressed_bitrate], color=['blue', 'orange'])
    plt.title("Bitrate Comparison (kbps)")
    plt.ylabel("Bitrate (kbps)")
    plt.tight_layout()
    plt.savefig(waveform_path)
    plt.close()

    print(f"Waveform generated and saved at: {waveform_path}")

except Exception as e:
    print(f"Error generating waveform: {str(e)}")
