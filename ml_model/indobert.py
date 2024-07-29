from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch.nn.functional as F
import torch
import os
from dotenv import load_dotenv
load_dotenv()

class IndoBERTClassifier:
    LABELS = [
        'Pidana', 'Ketenagakerjaan', 'Keluarga', 'Kenegaraan', 'Bisnis', 
        'Ilmu Hukum', 'Pertanahan & Properti', 'Teknologi', 'Kekayaan Intelektual', 
        'Perdata', 'Hak Asasi Manusia', 'Profesi Hukum', 'Perlindungan Konsumen'
    ]

    def __init__(self, model_name=os.environ.get("MODEL_NAME", "fathurfrs/indobert-classifying-topik-hukum-indonesia")):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.id2label = {idx: label for idx, label in enumerate(self.LABELS)}

    @torch.no_grad()
    def predict(self, text):
        encodings = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=256)
        encodings = {k: v.to(self.device) for k, v in encodings.items()}
        
        self.model.eval()
        outputs = self.model(**encodings)
        predictions = torch.argmax(outputs.logits, dim=-1)
        probs = F.softmax(outputs.logits, dim=-1)
        max_prob = probs.max().item()

        predicted_label = self.id2label[predictions.item()]
        
        return {"label": predicted_label, "confidence": max_prob}
    
    def model_architecture(self):
        return str(self.model)