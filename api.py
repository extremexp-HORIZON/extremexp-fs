import shutil
from datetime import datetime

from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import logging
logging.basicConfig(level=logging.INFO)

from pathlib import Path
import os

app = Flask(__name__)
cors = CORS(app) # cors is added in advance to allow cors requests
app.config['CORS_HEADERS'] = 'Content-Type'

workspace_path = Path() / os.getenv("WORKSPACE_PATH", Path(__file__).parent / "workspace")
archives_path = Path() / os.getenv("ARCHIVE_PATH", Path(__file__).parent / "archives")


@app.route('/experiments/create/<experiment_name>', methods=["PUT"])
@cross_origin()
def create_experiment(experiment_name):

    filepath = workspace_path / "experiments" / f"{experiment_name}.xxp"
    if filepath.exists():
        return {"message": f"experiment name {experiment_name} already exists"}, 406

    os.makedirs(workspace_path / "experiments", exist_ok=True)
    with open(filepath, 'w') as fileobject:
        fileobject.write(request.get_data(as_text=True))

    return {"message": f"experiment started with name {experiment_name}"}, 201


@app.route('/experiments/rename/<experiment_name>', methods=["POST"])
@cross_origin()
def rename_experiment(experiment_name):
    content = request.json
    filepath = workspace_path / "experiments" / f"{experiment_name}.xxp"
    if not filepath.exists():
        return {"message": f"experiment name {experiment_name} does not exist"}, 404

    if "name" in content:
        os.rename(filepath, workspace_path / "experiments" / f"{content["name"]}.xxp")
        return {"message": f"experiment {experiment_name} was renamed to {content["name"]}"}, 200

    return {"message": f"no update on {experiment_name}"}, 200


@app.route('/experiments/delete/<experiment_name>', methods=["DELETE"])
@cross_origin()
def archive_experiment(experiment_name):
    filepath = workspace_path / "experiments" / f"{experiment_name}.xxp"
    if not filepath.exists():
        return {"message": f"experiment name {experiment_name} does not exist"}, 404

    os.makedirs(archives_path, exist_ok=True)

    # Get current date and time as a string
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Create new file name with timestamp suffix
    new_name = f"{experiment_name}.xxp.{timestamp}"

    # Define full destination path
    destination_path = os.path.join(archives_path, new_name)

    # Move and rename the file
    shutil.move(filepath , destination_path)

    return {"message": f"{experiment_name} has been deleted"}, 200


@app.route('/experiments/update/<experiment_name>', methods=["POST"])
@cross_origin()
def update_experiment(experiment_name):
    filepath = workspace_path / "experiments" / f"{experiment_name}.xxp"
    if not filepath.exists():
        return {"message": f"experiment name {experiment_name} does not exist"}, 404

    with open(filepath, 'w', encoding='utf-8') as fileobject:
        fileobject.write(request.get_data(as_text=True))

    return {"message": f"{experiment_name} has been updated"}, 200


@app.route('/experiments/recover/<experiment_name>', methods=["PUT"])
@cross_origin()
def recover_experiment(experiment_name):
    files = {
            f"experiments/{experiment_name}_{exp.name.split(".xxp.")[1]}.xxp": exp
            for exp in archives_path.glob(f"{experiment_name}.xxp.*")
    }

    if len(files) == 0:
        return {"message": f"experiment name {experiment_name} does not exist in archives"}, 404

    os.makedirs(workspace_path / "experiments", exist_ok=True)

    for new_file, old_file in files.items():
        destination_path = os.path.join(workspace_path, new_file)

        # Move and rename the file
        shutil.move(old_file, destination_path)

    return {"message": f"{len(files)} versions of {experiment_name} ha{"ve" if len(files)>1 else "s"} been recovered"}, 200


@app.route('/experiments/', methods=["GET"])
@cross_origin()
def get_experiments():
    experiments = [ exp for exp in (workspace_path / "experiments").glob(f"*.xxp") ]
    filenames = "\n".join(f.name for f in experiments)
    return Response(filenames, mimetype="text/plain")


@app.route('/experiments/<experiment_name>', methods=["GET"])
@cross_origin()
def get_experiment(experiment_name):
    filepath = workspace_path / "experiments" / f"{experiment_name}.xxp"
    if not filepath.exists():
        return {"message": f"experiment name {experiment_name} does not exist"}, 404

    with open(filepath, "r") as dsl:
        text = dsl.read()

    return Response(text, mimetype="text/plain")


@app.route('/experiments/dsl2graph/<experiment_name>', methods=["GET"])
@cross_origin()
def dsl2graph(experiment_name):
    filepath = workspace_path / "experiments" / f"{experiment_name}.xxp"
    if not filepath.exists():
        return {"message": f"experiment name {experiment_name} does not exist"}, 404

    #TODO: read the DSL and convert it to graph_json
    graph_json = {}

    return graph_json, 200


@app.route('/experiments/graph2dsl/<experiment_name>', methods=["PUT"])
@cross_origin()
def graph2dsl(experiment_name):
    filepath = workspace_path / "experiments" / f"{experiment_name}.xxp"
    if not filepath.exists():
        #TODO
        print ("creating ...")

    else:
        #TODO
        print ("updating ...")

    # TODO: read the json form data, and convert it DSL and store it
    graph_json = request.json

    return {"message": "not done yet"}, 201