import sys
import random

s = {} #varmap

#Player Character
class Character:
    def Character(name, level, clss):
        nm = name
        lvl = level
        role = clss


#Math Parser
def eval_expr(expr):
    if isinstance(expr, int):
        return expr 
    else:
        if '-' in expr:
            left, right = expr.split('-')
            left = eval_expr(left)
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
    return ans

def varmap(var, s):
    return s[var]

def eval_var(var, s):
    if var in s:
        return varmap(var, s)
    else:
        raise Exception(f"Variable '{var}' not defined")

def interpret_action(c, turn=None):
    if c.__class__.__name__ == "Declaration":
        mob_name = c.entity.name
        mob_lvl = c.entity.level
        s[mob_name] = eval_expr(mob_lvl)
        #print(mob_name, ", level ", eval_var(mob_name, s))

    elif c.__class__.__name__ == "Fight":
        pHealth = c.player.level * 10
        mHealth = c.entity.level * 10
        i = 0


        print(f"The fight begins between {c.player.name} and the {c.entity.name}!")
        
       
        #combat
        while (pHealth > 0):

            print(f"Turn {i+1}!")
            print(f"{c.player.name}'s Health: {pHealth}")
            print(f"{c.entity.name}'s Health: {mHealth}")  
            print()

            if i % 2 == 0:
                roll = random.choice(range(1,21))
                print(f"Hero's turn!")
                if roll <= 5:
                    print(f"{c.player.name} rolls a {roll} and misses! Tragedy!")
                elif roll <=19:
                    print(f"{c.player.name} attacks, rolling a {roll} and dealing {roll + c.player.level} damage!")
                    mHealth -= roll + c.player.level
                else:
                    print(f"Critical Success! {c.player.name} rolls a {roll} and lands a hefty strike! for {roll + c.player.level} damage!")
                    mHealth -= roll + c.player.level
            else:
                roll = random.choice(range(1,21))
                print(f"Enemy turn!")
                if roll <= 5:
                    print(f"{c.entity.name} rolls a {roll} and misses! Tragedy!")
                elif roll <=19:
                    print(f"{c.entity.name} attacks, rolling a {roll}! and dealing {roll + c.entity.level} damage!")
                    pHealth -= roll + c.entity.level
                else:
                    print(f"Critical Success! {c.entity.name} rolls a {roll} and lands a hefty strike for {roll + c.entity.level} damage! Oh No!")
                    pHealth -= roll + c.entity.level
            i += 1
            print()
            if pHealth <= 0:
                print(f"{c.player.name} was defeated!")
                break
            if mHealth <= 0:
                print(f"{c.player.name} defeated the {c.entity.name}!")
                break

    elif c.__class__.__name__ == "ConIf":
        cond = c.condition
        op = cond.operator
        right = cond.right

        if isinstance(cond.left, str) and "turn" in cond.left:
            left = turn  # 'turn' comes from ConFor
        elif isinstance(cond.left, int):
            left = cond.left
        elif hasattr(cond.left, 'level'):
            left = cond.left.level
        else:
            left = eval_var(cond.left, s)



        if op == "is":
            ans = left == right
            #print("'is ==' is", ans)
        elif op == "is not":
            ans = left != right
            #print("'is !=' is", ans)
        elif op == "is more than":
            ans = left > right
            #print("'is >' is", ans)
        elif op == "is less than":
            ans = left < right
            #print("'is <' is", ans)
        elif op == "is parted true by":
            ans = left % right == 0

        if ans:
            for action in c.action:
                interpret_action(action, turn)
        elif getattr(c, 'otherwise', None) and c.otherwise.action:
            for action in c.otherwise.action:
                interpret_action(action, turn)


    elif c.__class__.__name__ == "ConFor":
        iterations = c.iterations + 1
        for i in range (1, iterations):
            for action in c.action:
                interpret_action(action, i)

    elif c.__class__.__name__ == "Speak":
        print(f"{c.player.name} speaks, stating '{c.speech}'")

    elif c.__class__.__name__ == "Count":
        print(f"We are on Turn {turn}")



    else:
        print(f"Our hero does... nothing?")



#Interpreter
def interpret_program(model):
    s[model.subject.name] = eval_expr(model.subject.level)
    #Action interpreter
    for c in model.action:
        interpret_action(c)
        



def main(debug=False):
    from textx import metamodel_from_file
    with open('TheBattle!.RPG', 'r') as f:
        print(f.read())
    print()
    rPG_mm = metamodel_from_file('RPG.tx') #Insert grammar file here
    rPG_model = rPG_mm.model_from_file('TheBattle!.RPG') #Insert program file here



    interpret_program(rPG_model)

main()

