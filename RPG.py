


#Math Parser
def eval_expr(expr):
    if '-' in expr:
        left, right = expr.split('-')
        left = expr(left)
        right = eval_expr(right)
        ans = left - right
    elif '+' in expr:
        left, right = expr.split('+')
        left = eval_expr(left)
        right = eval_expr(right)
        ans = left + right
    elif '/' in expr:
        left, right = expr.split('/')
        left = eval_expr(left)
        right = eval_expr(right)
        ans = left / right
    elif '*' in expr:
        left, right = expr.split('*')
        left = eval_expr(left)
        right = eval_expr(right)
        ans = left * right
    elif '^' in expr:
        left, right = expr.split('^')
        left = eval_expr(left)
        right = eval_expr(right)
        ans = left ** right
    else:
        return (float(expr))
    return expr

def varmap(var, s):
    return s[var]

def eval_var(var, s):
    if var in s:
        return varmap(var, s)
    else:
        raise Exception(f"Variable '{var}' not defined")

#Interpreter
def interpret(self, model):
    for c in model.commands:
        if c.__class__.__name__ == "":
            return
        elif c.__class__.__name__ == "":
            return
        else:
            return



def main(debug=False):
    from textx import metamodel_fromfile
    rPG_m = metamodel_fromfile('RPG.tx') #Insert grammar file here
    rPG_model = rPG_m.model_from_file('Program.RPG') #Insert program file here
    
    interpret(rPG_model)

if __name__ == "__main__":
    main()


