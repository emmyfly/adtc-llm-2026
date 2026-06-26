import onnxruntime as ort
import numpy as np
from PIL import Image
import json
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "plant_disease_model.onnx")
CLASSES_PATH = os.path.join(os.path.dirname(__file__), "models", "plant_disease_classes.json")

_session = None
_classes = None

def load_model():
    global _session, _classes
    if _session is None:
        _session = ort.InferenceSession(MODEL_PATH)
        with open(CLASSES_PATH) as f:
            _classes = json.load(f)
    return _session, _classes

def classify_image(image_path):
    session, classes = load_model()
    image = Image.open(image_path).convert("RGB")
    image = image.resize((224, 224))
    arr = np.array(image).astype(np.float32) / 255.0
    arr = (arr - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    arr = arr.transpose(2, 0, 1)
    arr = np.expand_dims(arr, 0)
    outputs = session.run(None, {"image": arr})
    probs = np.exp(outputs[0]) / np.exp(outputs[0]).sum()
    idx = np.argmax(probs)
    label = classes[idx]
    confidence = float(probs[0][idx])
    return label, confidence

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        label, conf = classify_image(sys.argv[1])
        print(f"Disease: {label}")
        print(f"Confidence: {conf:.2%}")
    else:
        print("Usage: python image_classifier.py <image_path>")
