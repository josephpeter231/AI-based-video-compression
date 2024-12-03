# import subprocess
# import os
# import matplotlib.pyplot as plt

# input_video_path = r"C:\\Users\\Fabheads21\\AI based video compression\\static\\uploads\\6214616-hd_1080_1920_25fps.mp4"
# output_video_path = r"C:\\Users\\Fabheads21\\AI based video compression\\static\\compressed\\compressed_video.mp4"
# waveform_path = r"C:\\Users\\Fabheads21\\AI based video compression\\static\\waveforms\\bitrate_comparison.png"

# def get_bitrate(video_path):
#     try:
#         result = subprocess.run(
#             ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=bit_rate", "-of", "default=noprint_wrappers=1", video_path],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
#         bitrate = result.stdout.strip().split("=")[-1]
#         return int(bitrate) / 1000
#     except Exception as e:
#         print(f"Error getting bitrate for {video_path}: {str(e)}")
#         return 0

# try:
#     result = subprocess.run(
#         ["ffmpeg", "-i", input_video_path, "-c:v", "libx265", "-crf", "28", output_video_path],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True
#     )

#     if result.returncode == 0:
#         print(f"Video successfully compressed! Output saved at: {output_video_path}")
#     else:
#         print("Error during compression:")
#         print(result.stderr)

# except FileNotFoundError as e:
#     print(f"Error: FFmpeg executable not found. Please check the system's PATH. {str(e)}")

# except Exception as e:
#     print(f"An error occurred during compression: {str(e)}")

# input_bitrate = get_bitrate(input_video_path)
# compressed_bitrate = get_bitrate(output_video_path)

# try:
#     plt.figure(figsize=(6, 4))
#     plt.bar(["Original", "Compressed"], [input_bitrate, compressed_bitrate], color=['blue', 'orange'])
#     plt.title("Bitrate Comparison (kbps)")
#     plt.ylabel("Bitrate (kbps)")
#     plt.tight_layout()
#     plt.savefig(waveform_path)
#     plt.close()

#     print(f"Waveform generated and saved at: {waveform_path}")

# except Exception as e:
#     print(f"Error generating waveform: {str(e)}")
import subprocess
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

input_video_path = r"C:\\Users\\Fabheads21\\AI based video compression\\static\\uploads\\6214616-hd_1080_1920_25fps.mp4"
output_video_path = r"C:\\Users\\Fabheads21\\AI based video compression\\static\\compressed\\compressed_video.mp4"
waveform_path = r"C:\\Users\\Fabheads21\\AI based video compression\\static\\waveforms\\bitrate_comparison.png"
distortion_path = r"C:\\Users\\Fabheads21\\AI based video compression\\static\\waveforms\\distortion_comparison.png"

def get_bitrate(video_path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=bit_rate", "-of", "default=noprint_wrappers=1", video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        bitrate = result.stdout.strip().split("=")[-1]
        return int(bitrate) / 1000
    except Exception as e:
        print(f"Error getting bitrate for {video_path}: {str(e)}")
        return 0

def calculate_psnr(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if mse == 0:
        return 100
    return 20 * np.log10(255.0 / np.sqrt(mse))

def calculate_ssim(original, compressed):
    return ssim(original, compressed, multichannel=True, win_size=3)  

def extract_frame(video_path, frame_number):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    cap.release()
    if ret:
       
        frame_resized = cv2.resize(frame, (224, 224))  
        return frame_resized
    else:
        raise ValueError(f"Could not extract frame {frame_number} from {video_path}")

try:
    result = subprocess.run(
        ["ffmpeg", "-i", input_video_path, "-c:v", "libx265", "-crf", "28", output_video_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode == 0:
        print(f"Video successfully compressed! Output saved at: {output_video_path}")
    else:
        print("Error during compression:")
        print(result.stderr)

except FileNotFoundError as e:
    print(f"Error: FFmpeg executable not found. Please check the system's PATH. {str(e)}")

except Exception as e:
    print(f"An error occurred during compression: {str(e)}")

input_bitrate = get_bitrate(input_video_path)
compressed_bitrate = get_bitrate(output_video_path)

frame_number = 100  
original_frame = extract_frame(input_video_path, frame_number)
compressed_frame = extract_frame(output_video_path, frame_number)


psnr_value = calculate_psnr(original_frame, compressed_frame)
ssim_value = calculate_ssim(original_frame, compressed_frame)

print(f"PSNR: {psnr_value} dB")
print(f"SSIM: {ssim_value}")

try:
    plt.figure(figsize=(6, 4))
    plt.bar(["Original", "Compressed"], [input_bitrate, compressed_bitrate], color=['blue', 'orange'])
    plt.title("Bitrate Comparison (kbps)")
    plt.ylabel("Bitrate (kbps)")
    plt.tight_layout()
    plt.savefig(waveform_path)
    plt.close()

    plt.figure(figsize=(6, 4))
    plt.bar(["PSNR", "SSIM"], [psnr_value, ssim_value], color=['blue', 'orange'])
    plt.title("Distortion Metrics")
    plt.ylabel("Metric Value")
    plt.tight_layout()
    plt.savefig(distortion_path)
    plt.close()

    print(f"Waveform and Distortion graphs generated and saved.")

except Exception as e:
    print(f"Error generating waveform and distortion graphs: {str(e)}")
