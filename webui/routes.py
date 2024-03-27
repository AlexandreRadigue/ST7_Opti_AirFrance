from flask import Flask, jsonify, redirect, render_template, request
from dynamicModel import options_convert, updating_convert

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        group_number = request.form.get("group-number")
        return redirect("/seatmap" + "?groupNumber=" + group_number)
    return render_template("index.html")


@app.route("/seatmap", methods=["GET", "POST"])
def seatmap():
    group_number = request.args.get("groupNumber")
    availableSeats = options_convert(int(group_number))
    return render_template("seatmap.html", availableSeats=availableSeats)


@app.route("/update_seats", methods=["POST"])
def update_seats():
    selected_seat = request.json.get("seat")
    updating_convert(selected_seat)
    return jsonify(message="success")


if __name__ == "__main__":
    app.run(debug=True)
