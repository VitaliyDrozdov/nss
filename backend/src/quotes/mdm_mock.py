from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/process_mdm_data", methods=["POST"])
def process_data():
    data = request.get_json()
    run_id = data.get("runId")
    # заглушка
    response_data = {"runId": run_id, "subjectIds": ["01937646", "02948576"]}
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
