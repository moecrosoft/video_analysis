import cv2
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests
import torch

processor = BlipProcessor.from_pretrained('Salesforce/blip-image-captioning-base')
model = BlipForConditionalGeneration.from_pretrained('Salesforce/blip-image-captioning-base')
model.eval()

def extract_captions(video_path: str, every_n_frames: int = 30) -> list[str]:
    cap = cv2.VideoCapture(video_path)
    captions = []
    frames_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frames_count % every_n_frames == 0:
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            inputs = processor(image, return_tensors='pt')
            with torch.no_grad():
                out = model.generate(**inputs, max_new_tokens=50)
            caption = processor.decode(out[0], skip_special_tokens=True)
            captions.append(caption)
        frames_count += 1

    cap.release()
    return captions

def summarise_with_ollama(captions: list[str]) -> str:
    prompt = f''' These are frame by frame descriptions of a video:
    {chr(10).join(f'- {c}' for c in captions)}

    Based on these descriptions, write a clear and concise summary of what is happening in the video.
    Focus on the main activity, the subject, and the environment.'''

    response = requests.post(
        'http://ollama:11434/api/generate',
        json={'model': 'llama3', 'prompt': prompt, 'stream': False},
        timeout=60
    )
    response.raise_for_status()
    return response.json()['response']