import numpy as np
import cv2
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import base64

# Generate RSA key pair
key = RSA.generate(2048)

# Encrypt text message using RSA public key
def encrypt_rsa(public_key, plaintext):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    cipher_text = cipher_rsa.encrypt(plaintext.encode())
    return base64.b64encode(cipher_text).decode()

# Hide encrypted message in video using Discrete Cosine Transform (DCT)
def hide_message_in_video(video_path, encrypted_message, output_video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate total number of pixels in each frame
    total_pixels = frame_width * frame_height

    # Calculate number of frames required to hide the entire message
    frames_required = len(encrypted_message) // total_pixels + 1

    # Initialize index for the encrypted message
    message_index = 0

    # Write video with hidden message
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    # Process each frame
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break

        # Check if there are more parts of encrypted message to hide
        if message_index < len(encrypted_message):
            # Extract a part of the encrypted message to hide in current frame
            part_length = min(total_pixels, len(encrypted_message) - message_index)
            part_message = encrypted_message[message_index:message_index + part_length]
            message_index += part_length

            # Generate DCT coefficients from the part of encrypted message
            encrypted_message_bytes = part_message.encode()
            dct_coefficients = np.frombuffer(encrypted_message_bytes, dtype=np.uint8)

            # Reshape DCT coefficients to match video frame dimensions
            dct_coefficients = dct_coefficients.reshape((frame_height, frame_width))

            # Apply DCT coefficients to the corresponding frame
            frame_dct = cv2.dct(np.float32(frame))
            frame_dct += dct_coefficients.astype(np.float32)
            frame_dct_clipped = np.clip(frame_dct, 0, 255)
            frame_hidden = cv2.idct(frame_dct_clipped.astype(np.uint8))

            # Write frame with hidden message to output video
            out.write(frame_hidden)
        else:
            # If no more parts of encrypted message, just write the original frame
            out.write(frame)

    # Release resources
    cap.release()
    out.release()

# Example usage:
public_key = key.publickey()
plaintext = "Aku adalah mahasiswa Teknik Informatika"
encrypted_rsa = encrypt_rsa(public_key, plaintext)
print("Encrypted RSA:", encrypted_rsa)

# Example usage to hide encrypted message in video
video_path = 'D:\Video Kripto\Peuron.mp4'
output_video_path = 'D:\File Kripto\Enkripsi Video.avi'
hide_message_in_video(video_path, encrypted_rsa, output_video_path)
