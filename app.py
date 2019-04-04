from json import dumps

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from os.path import isdir, join, realpath, dirname
from os import listdir, mkdir, environ
from mimetypes import guess_type

app = Flask(__name__)
CORS(app)
token = environ.get("AUTH_TOKEN")

proj_dir = dirname(realpath(__file__))
files_dir = join(proj_dir, "files")

next_file_id = 0
files = {}
if isdir(files_dir):
    files = {int(file_name.split(".")[0]):file_name for file_name in listdir(files_dir)
             if file_name.split(".")[0].isnumeric()}
    if files:
        next_file_id = max(files) + 1
else:
    mkdir(files_dir)


def is_authorized():
    return (request.cookies.get("auth_token") == token) if token else True


@app.route('/upload', methods=["POST"])
def upload():
    if not is_authorized():
        return Response(dumps({"error": "authorization failed"}), status=403, mimetype="application/json")
    global next_file_id
    global files
    file = list(request.files.values())[0]
    file_id = next_file_id
    next_file_id += 1
    ext = file.filename.split(".")[-1]
    with open(join(files_dir, str(file_id) + "." + ext), "w+b") as f:
        f.write(file.read())
    files[file_id] = str(file_id) + "." + ext
    return jsonify({"file_id": file_id})


@app.route('/<file_id>', methods=["GET"])
def download(file_id):
    if not is_authorized():
        return Response(dumps({"error": "authorization failed"}), status=403, mimetype="application/json")
    global files
    if not file_id.isnumeric():
        return Response(dumps({"error": "file_not_found"}), status=404, mimetype="application/json")
    file_id = int(file_id)
    file_name = files.get(file_id)
    if not file_name:
        return Response(dumps({"error": "file_not_found"}), status=404, mimetype="application/json")
    try:
        with open(join(files_dir, file_name), "rb") as f:
            _type = guess_type(file_name)[0]
            return Response(f.read(), content_type=_type, mimetype=_type, headers={
                "Content-Disposition": "attachment;filename=" + file_name
            })
    except FileNotFoundError:
        return Response(dumps({"error": "file_not_found"}), status=404, mimetype="application/json")


if __name__ == '__main__':
    app.run()
