from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image

model_name = "nlpconnect/vit-gpt2-image-captioning"

def load_captioning_model():
    model = VisionEncoderDecoderModel.from_pretrained(model_name)
    feature_extractor = ViTFeatureExtractor.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, feature_extractor, tokenizer

def generate_caption(image_path):
    model, feature_extractor, tokenizer = load_captioning_model()
    image = Image.open(image_path)
    
    if image.mode != "RGB":
        image = image.convert(mode="RGB")

    pixel_values = feature_extractor(images=[image], return_tensors="pt").pixel_values
    
    with torch.no_grad():
        output = model.generate(pixel_values, max_length=16, num_beams=4)
    
    caption = tokenizer.decode(output[0], skip_special_tokens=True)
    return caption