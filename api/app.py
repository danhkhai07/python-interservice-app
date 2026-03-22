from flask import Flask, jsonify 
import requests

app = Flask(__name__)

URL_PROCESS_JOB     = "http://worker:5001/process"
URL_GET_JOB_INFO    = "http://worker:5001/info"
URL_LIST_ALL        = "http://worker:5001/list-all"

@app.route("/job/<int:number>", methods=["GET"])
def post_job(number):
    process_res = requests.post(
        URL_PROCESS_JOB,
        json={"n": number},
        timeout=2
    )
    taken = process_res.json().get("taken")
    id = process_res.json().get("job_id")
        
    if not taken or not id:
        return jsonify({"status": "failed"})
    else:
        return jsonify({"status": "taken", "job_id": id})
        
@app.route("/job/<int:job_id>", methods=["GET"])
def get_job(job_id):
    res = requests.get(
        URL_GET_JOB_INFO,
        json={"id": job_id},
        timeout=2,
    ) 
    return jsonify(res.json())

@app.route("/list-all", methods=["GET"])
def list_all():
    res = requests.get(
        URL_LIST_ALL,
        timeout=2,
    )
    return jsonify(res.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)   
