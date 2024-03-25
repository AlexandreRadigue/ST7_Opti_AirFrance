from flask import Flask, redirect, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print("sos")
        group_number = request.form.get("group-number")
        return redirect("/seatmap" + "?groupNumber=" + group_number)
    return render_template("index.html")


@app.route("/seatmap", methods=["GET", "POST"])
def seatmap():
    group_number = request.args.get("groupNumber")
    return render_template("seatmap.html", groupNumber=group_number)


if __name__ == "__main__":
    app.run(debug=True)
