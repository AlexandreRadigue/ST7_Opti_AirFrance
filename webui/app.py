from flask import Flask, redirect, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        group_number = request.form.get("group-number")
        return redirect("/seatmap" + "?availableSeats=" + group_number)
    return render_template("index.html")


@app.route("/seatmap", methods=["GET", "POST"])
def seatmap():
    group_number = request.args.get("groupNumber")
    availableSeats = ["1A", "2F", "4B"]
    return render_template("seatmap.html", availableSeats=availableSeats)


if __name__ == "__main__":
    app.run(debug=True)
