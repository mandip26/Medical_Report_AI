import os
import fitz
from PIL import Image
import io
import concurrent.futures
from google import genai

class GeminiService:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash"

    def pdf_to_images(self, pdf_path: str):
        doc = fitz.open(pdf_path)
        images = []
        for page in doc:
            pix = page.get_pixmap(dpi=150)  # Reduced DPI for faster processing
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            images.append(img)
        return images

    def image_to_bytes(self, image: Image.Image):
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        return buf.read()

    def extract_json_from_image(self, image: Image.Image, prompt: str):
        image_bytes = self.image_to_bytes(image)
        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {"inline_data": {"mime_type": "image/png", "data": image_bytes}}
                    ]
                }
            ]
        )
        return response.text  # Should be JSON

    def extract_from_file(self, file_path: str, ext: str, prompt: str):
        images = self.pdf_to_images(file_path) if ext == ".pdf" else [Image.open(file_path)]
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.extract_json_from_image, img, prompt) for img in images]
            results = [future.result() for future in futures]
        return results
