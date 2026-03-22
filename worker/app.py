from flask import Flask, request, jsonify 
import datetime, time, threading, random  

app = Flask(__name__)

class Job:
    job_id = None
    init_time = None
    finished_time = None
    status = "pending"  # 4 state: pending, running, done or failed
    input = None
    mod = 1e9 + 7
    output = None

    def __init__(self, id: int, n: int):
        self.job_id = id
        self.input = n
        self.init_time = datetime.datetime.now()

    def process(self):
        if self.status in ("done", "failed"):
            return False
        else:
            russian_roullette = random.randint(1, 6)
            if russian_roullette == 6: # failed
                time.sleep(3)
                self.status = "failed"
                self.finished_time = datetime.datetime.now()

            self.result = self.__fib(self.output)
            self.status = "done"
            self.finished_time = datetime.datetime.now()
            return True
            
    def __fib(self, n):
        time.sleep(5)
        num1, num2 = 0, 1
        if n == 1: 
            return 0
        if n == 2: 
            return 1

        for _ in range(2, n):
            z = (num1 + num2) % self.mod
            num1 = num2
            num2 = z
        return num2

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "status": self.status,
            "result": self.result,
            "init_time": self.init_time,
            "finished_time_time": self.finished_time,
            "mod": self.mod,
            "description": "Returns the n'th fibonacci number.",
        }

def run_job(job: Job):
    job.status = "running"
    job.process()

#################################################

state = {
    "idCounter": 0,
    "jobMap": {}
}

@app.route("/process", methods=["POST"])
def process_job():
    data = request.json or {}
    n = data.get("n")
    if not n:
        return jsonify({"error": "Missing json fields"})

    state["idCounter"] += 1
    id = state["idCounter"]

    job = Job(id, n)
    state["jobMap"][id] = job

    t = threading.Thread(target=run_job, args=(job,))
    t.start()

    return jsonify({
        "taken": True,
        "job_id": id,
    })


@app.route("/info", methods=["GET"])
def get_job_info():
    data = request.json or {}
    id = data.get("id")
    if not id:
        return jsonify({"error": "Missing json fields"})

    job = state["jobMap"].get(id)
    if job == None:
        return jsonify({"error": "Cannot find job with given id"})

    return jsonify(job.to_dict())

@app.route("/all", methods=["GET"])
def list_all():
    return jsonify([
        {"job_id": job_id, **job.to_dict()}
        for job_id, job in state["jobMap"].items()
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)   
