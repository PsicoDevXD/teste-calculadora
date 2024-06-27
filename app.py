from flask import Flask, request, render_template_string
import sympy as sp

app = Flask(__name__)

# Função para ler o conteúdo do arquivo index.html
def read_template(template_path):
    with open(template_path, 'r') as file:
        return file.read()

@app.route('/', methods=['GET', 'POST'])
def index():
    solution = None
    if request.method == 'POST':
        equation = request.form['equation']
        x = sp.symbols('x')
        try:
            lhs, rhs = equation.split('=')
            lhs_expr = sp.sympify(lhs)
            rhs_expr = sp.sympify(rhs)
            expr = sp.Eq(lhs_expr, rhs_expr)
            solutions = sp.solve(expr, x)
            # Filtrar apenas soluções reais e formatar para 4 casas decimais
            real_solutions = [round(sol.evalf(), 4) for sol in solutions if sol.is_real]
            solution = real_solutions if real_solutions else solutions
        except Exception as e:
            solution = f"Erro ao resolver a equação: {e}"
    template = read_template('index.html')
    return render_template_string(template, solution=solution)

if __name__ == '__main__':
    app.run(debug=True)
