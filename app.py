from flask import Flask, request, jsonify, render_template_string
import math
import re

app = Flask(__name__)

# ---------------- SAFE MATH FUNCTIONS ----------------
allowed_names = {
    "sqrt": math.sqrt,
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "log": math.log,
    "log10": math.log10,
    "pi": math.pi,
    "e": math.e,
    "abs": abs,
    "round": round
}

def factorial_fix(expr):
    while "!" in expr:
        expr = re.sub(r'(\d+)!', r'math.factorial(\1)', expr)
    return expr

def clean_expression(expr):
    expr = expr.replace("×", "*").replace("÷", "/")
    expr = expr.replace("^", "**")
    expr = expr.replace("√", "sqrt")
    expr = expr.replace("%", "/100")
    expr = factorial_fix(expr)
    return expr

# ---------------- API ROUTE ----------------
@app.route("/math")
def math_api():
    q = request.args.get("q") or request.args.get("math")

    if not q:
        return jsonify({"error": "No expression provided"})

    try:
        expr = clean_expression(q)
        result = eval(expr, {"__builtins__": None}, allowed_names)

        return jsonify({
            "engine": "SULAV ADVANCED MATH ENGINE",
            "expression": q,
            "answer": result
        })

    except Exception as e:
        return jsonify({
            "engine": "SULAV ADVANCED MATH ENGINE",
            "error": "Invalid math expression"
        })

# ---------------- WEBSITE UI ----------------
@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>SULAV ADVANCED MATH ENGINE</title>
<style>
body{
    background:#0f172a;
    color:#e5e7eb;
    font-family:Arial;
    text-align:center;
    padding:40px;
}
input{
    width:80%;
    padding:15px;
    font-size:18px;
    border-radius:8px;
    border:none;
}
button{
    margin-top:15px;
    padding:12px 30px;
    font-size:18px;
    background:#22c55e;
    color:black;
    border:none;
    border-radius:8px;
    cursor:pointer;
}
.result{
    margin-top:25px;
    font-size:22px;
    color:#38bdf8;
}
.footer{
    margin-top:40px;
    color:#9ca3af;
}
</style>
</head>
<body>

<h1>🧠 SULAV ADVANCED MATH ENGINE</h1>
<p>Scientific Math Solver Website + API</p>

<input id="expr" placeholder="Example: (10+5)*sqrt(16)">
<br>
<button onclick="solve()">Calculate</button>

<div class="result" id="out"></div>

<div class="footer">
Developer: @sulav_don1<br>
Channel: @sulav_don2
</div>

<script>
function solve(){
    let q = document.getElementById("expr").value;
    fetch("/math?q=" + encodeURIComponent(q))
    .then(r => r.json())
    .then(d => {
        document.getElementById("out").innerText =
        d.answer !== undefined ? "Answer: " + d.answer : d.error;
    });
}
</script>

</body>
</html>
""")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)