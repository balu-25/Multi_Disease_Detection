from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pneumonia")
def pneumonia():
    return render_template("pneumonia_detection.html")

@app.route("/brain")
def brain():
    return render_template("brain_tumor_detection.html")
@app.route("/kidney")
def kidney():
    return render_template("kidney_stone_detection.html")
@app.route("/eye")
def eye():
    return render_template("eye_disease_detection.html")
@app.route("/heart")
def heart():
    return render_template("heart_disease_detection.html")
@app.route("/lungcancer")
def lungcancer():
    return render_template("lung_cancer_detection.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
