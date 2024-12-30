# from flask import Blueprint, jsonify, request
# from google_ai import GoogleAI

# google_blueprint = Blueprint("google", __name__)
# google_ai = GoogleAI()

# @google_blueprint.route("/google/analyze-image", methods=["POST"])
# def analyze_image():
#     try:
#         data = request.json
#         image_uri = data.get("image_uri")
#         if not image_uri:
#             return jsonify({"error": "image_uri is required"}), 400
        
#         response = google_ai.analyze_image(image_uri)
#         return jsonify(response)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
