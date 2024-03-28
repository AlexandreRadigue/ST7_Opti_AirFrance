from flask import Flask, jsonify, redirect, render_template, request
from dynamicModel import options_convert, updating_convert

app = Flask(__name__)

registered_grp = set()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def registering():
    global registered_grp
    group_number = request.form.get("group-number")
    if group_number in registered_grp or int(group_number) > 111:
        return render_template("index.html", message="Group number already registered")
    registered_grp.add(group_number)
    return redirect("/seatmap" + "?groupNumber=" + group_number)


@app.route("/seatmap", methods=["GET", "POST"])
def seatmap():
    group_number = request.args.get("groupNumber")
    availableSeats = options_convert(int(group_number))
    return render_template("seatmap.html", availableSeats=availableSeats)


@app.route("/update_seats", methods=["POST"])
def update_seats():
    selected_seat = request.json.get("seat")
    if updating_convert(selected_seat):
        return jsonify(message="failed")
    return jsonify(message="success")


if __name__ == "__main__":
    app.run(debug=True)
