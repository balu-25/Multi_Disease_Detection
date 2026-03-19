import numpy as np
import cv2
from tensorflow.keras.models import load_model

# Load models once
pneumonia_model = load_model("models/pneumonia_model.h5")
lung_model = load_model("models/lung_cancer_model.h5")

pneumonia_classes = ["Bacterial Pneumonia", "Normal", "Viral Pneumonia"]
lung_classes = ["Benign", "Malignant", "Normal"]

def preprocess(image):
    img = cv2.resize(image, (224, 224))
    img = img / 255.0
    img = np.reshape(img, (1, 224, 224, 3))
    return img

def predict_pneumonia(image):
    processed = preprocess(image)
    pred = pneumonia_model.predict(processed)
    class_idx = np.argmax(pred)
    confidence = float(np.max(pred))
    label = pneumonia_classes[class_idx]
    return label, confidence

def predict_lung(image):
    processed = preprocess(image)
    pred = lung_model.predict(processed)
    class_idx = np.argmax(pred)
    confidence = float(np.max(pred))
    label = lung_classes[class_idx]
    return label, confidence

def annotate_image(image, label):
    annotated = image.copy()
    cv2.putText(annotated, label, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    return annotated