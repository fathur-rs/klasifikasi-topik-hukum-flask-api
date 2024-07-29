from flask import request
from app.api import model_blueprint
from ml_model.indobert import IndoBERTClassifier
from ..utilities import make_response_util, handle_exceptions, token_required
from ..models.question import QuestionSchema

classifier = IndoBERTClassifier()

@model_blueprint.route('/predict', methods=['POST'])
@handle_exceptions
@token_required
def predict():
    """Predict the legal topic of a given question using the IndoBERTClassifier model."""
    if not request.is_json:
        return make_response_util(400, description="Invalid JSON", error="Bad Request")

    try:
        content = QuestionSchema(**request.get_json())
    except TypeError as e:
        return make_response_util(400, description=str(e), error="Bad Request")

    prediction = classifier.predict(content.question)
    return make_response_util(200, message={"prediction": prediction})

@model_blueprint.route('/healthcheck', methods=['GET'])
@handle_exceptions
@token_required
def health_check():
    """Perform a health check of the IndoBERTClassifier model."""
    sample = """
    Seorang korban penganiayaan telah mengadukan tindak pidana yang menimpa dirinya. Namun dalam menyampaikan kronologi kejadian kepada pihak kepolisian, korban tersebut merekayasa kronologi tindak pidana yang sama sekali tidak pernah terjadi. Apakah korban tersebut dapat dikenakan sanksi hukum karena memberikan keterangan palsu? Mohon jawabannya.
    """
    test_prediction = classifier.predict(sample)
    health_info = {
        "model_version": "1.0",
        "status": "Healthy",
        "model_loaded": True,
        "sample": sample,
        "test_prediction": test_prediction
    }
    return make_response_util(200, message=health_info)

@model_blueprint.route("/architecture", methods=["GET"])
@handle_exceptions
@token_required
def architecture():
    """Retrieve the architecture information of the IndoBERTClassifier model."""
    architecture_info = classifier.model_architecture()
    return make_response_util(200, message={"architecture": architecture_info})
