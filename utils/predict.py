from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
# Load models once
pneumonia_model = YOLO("models/pneumonia.pt")
lung_model = YOLO("models/lungcancer.pt")

pneumonia_classes = ["Bacterial Pneumonia", "Normal", "Viral Pneumonia"]
lung_classes = ["Benign", "Malignant", "Normal"]

def predict_image(model, image, classes):
    # ---------- Prediction ----------
    results = model(image)

    probs = results[0].probs.data.cpu().numpy()
    pred_index = np.argmax(probs)
    confidence = probs[pred_index]
    label = classes[pred_index]

    # ---------- Image Processing for Region Detection ----------
    img_np = np.array(image)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # Blur to remove noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold (adaptive for medical images)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding box on largest contour
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(largest_contour) > 500:  # ignore noise
            x, y, w, h = cv2.boundingRect(largest_contour)

            cv2.rectangle(img_np, (x, y), (x + w, y + h), (0, 255, 0), 3)

            text = f"{label} ({confidence:.2f})"
            cv2.putText(img_np, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Convert back to PIL
    output_img = Image.fromarray(img_np)

    return label, confidence, output_img