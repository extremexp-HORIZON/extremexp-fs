from flask import Flask, request
from flask_cors import CORS, cross_origin
import logging
logging.basicConfig(level=logging.INFO)

from pathlib import Path
import os

app = Flask(__name__)
cors = CORS(app) # cors is added in advance to allow cors requests
app.config['CORS_HEADERS'] = 'Content-Type'

# TODO changed to the shared workspace
path = Path(__file__).parent / "workspace"


@app.route('/experiments/create/<experiment_name>', methods=["PUT"])
@cross_origin()
def create_experiment(experiment_name):

    filepath = path / "experiments" / f"{experiment_name}.xxp"
    if filepath.exists():
        return {"message": f"experiment name {experiment_name} already exists"}, 406

    os.makedirs(path / "experiments", exist_ok=True)
    with open(filepath, 'w') as _:
        # fileobject.write(f"experiment {experiment_name} " + "{\n\n}")
        pass

    return {"message": f"experiment started with name {experiment_name}"}, 201


@app.route('/experiments/rename/<experiment_name>', methods=["POST"])
@cross_origin()
def rename_experiment(experiment_name):
    content = request.json
    filepath = path / "experiments" / f"{experiment_name}.xxp"
    if not filepath.exists():
        return {"message": f"experiment name {experiment_name} does not exist"}, 404

    if "name" in content:
        os.rename(filepath, path / "experiments" / f"{content["name"]}.xxp")
        return {"message": f"experiment {experiment_name} was renamed to {content["name"]}"}, 200

    return {"message": f"no update on {experiment_name}"}, 200


@app.route('/experiments/delete/<experiment_name>', methods=["DELETE"])
@cross_origin()
def delete_experiment(experiment_name):
    filepath = path / "experiments" / f"{experiment_name}.xxp"
    if not filepath.exists():
        return {"message": f"experiment name {experiment_name} does not exist"}, 404

    os.remove(filepath)

    return {"message": f"{experiment_name} has been deleted"}, 200


@app.route('/experiments/update/<experiment_name>', methods=["POST"])
@cross_origin()
def update_experiment(experiment_name):
    filepath = path / "experiments" / f"{experiment_name}.xxp"
    if not filepath.exists():
        return {"message": f"experiment name {experiment_name} does not exist"}, 404

    with open(filepath, 'w', encoding='utf-8') as fileobject:
        fileobject.write(request.get_data(as_text=True))

    return {"message": f"{experiment_name} has been updated"}, 200
