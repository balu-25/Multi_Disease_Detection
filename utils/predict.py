from ultralytics import YOLO
from PIL import Image
import numpy as np

# Load models once
pneumonia_model = YOLO("models/pneumonia.pt")
lung_model = YOLO("models/lungcancer.pt")

pneumonia_classes = ["Bacterial Pneumonia", "Normal", "Viral Pneumonia"]
lung_classes = ["Benign", "Malignant", "Normal"]

def predict_image(model, image, classes):
    results = model(image)
    
    probs = results[0].probs.data.cpu().numpy()
    pred_index = np.argmax(probs)
    confidence = probs[pred_index]

    label = classes[pred_index]

    # For classification → no bounding boxes, so return same image
    return label, confidence, image