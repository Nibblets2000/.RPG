import argparse
import random

s = {} #varmap
from textx import metamodel_from_file

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
    

#Action interpeter
#Accepts c for lists of actions and 'turn' to help with recursion and parsing for loops correctly.
def interpret_action(c, turn=None):

    #Standard declaration, usually used to declare mobs
    if c.__class__.__name__ == "Declaration":

        #Stores mob name and level into var map.
        mob_name = c.entity.name
        mob_lvl = c.entity.level
        s[mob_name] = eval_expr(mob_lvl)

    #Standard combat system 
    elif c.__class__.__name__ == "Fight":
        pHealth = c.player.level * 10
        mHealth = c.entity.level * 10
        i = 0


        print(f"The fight begins between {c.player.name} and the {c.entity.name}!")
        
       
        #combat
        while (pHealth > 0):

            #Prints turn along with Player and Monster Health values
            print(f"Turn {i+1}!")
            print(f"{c.player.name}'s Health: {pHealth}")
            print(f"{c.entity.name}'s Health: {mHealth}")  
            print()

            #Odd i is mob turn, even i is player turn
            if i % 2 == 0:
                #Rolls D20 dice
                roll = random.choice(range(1,21))

                #Hero's turn; 
                #Combat damage is determined by dice number rolled + player/mob level. dice number below 5 does not apply damage.
                print(f"Hero's turn!")
                if roll <= 5:
                    print(f"{c.player.name} rolls a {roll} and misses! Tragedy!")
                elif roll <=19:
                    print(f"{c.player.name} attacks, rolling a {roll} and dealing {roll + c.player.level} damage!")
                    mHealth -= roll + c.player.level
                else:
                    print(f"Critical Success! {c.player.name} rolls a {roll} and lands a hefty strike for {roll + c.player.level} damage!")
                    mHealth -= roll + c.player.level

                #Mob's turn
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

            #iterates i; changes turn
            i += 1
            print()
            
            #Ends fight loop if either player or mob health is/goes below zero; output printed respectively.
            if pHealth <= 0:
                print(f"{c.player.name} was defeated!")
                break
            if mHealth <= 0:
                print(f"{c.player.name} defeated the {c.entity.name}!")
                break


    #if statement handler
    elif c.__class__.__name__ == "ConIf":
        #spits condition into operator, right, and left
        cond = c.condition
        op = cond.operator
        right = cond.right

        if isinstance(cond.left, str) and "turn" in cond.left:
            #"turn" variable is used for For statements
            left = turn
        elif isinstance(cond.left, int):
            left = cond.left
        elif hasattr(cond.left, 'level'):
            left = cond.left.level
        else:
            left = eval_var(cond.left, s)


        #operator handler in order: ==, !=, >, <, %
        if op == "is":
            ans = left == right
        elif op == "is not":
            ans = left != right
        elif op == "is more than":
            ans = left > right
        elif op == "is less than":
            ans = left < right
        elif op == "is parted true by":
            ans = left % right == 0

        #If condition is true
        if ans:
            #Uses recursion to enter true branch
            for action in c.action:
                interpret_action(action, turn)
        #If condition is false
        elif getattr(c, 'otherwise', None) and c.otherwise.action:
            #Uses recursion to enter "else" branch
            for action in c.otherwise.action:
                interpret_action(action, turn)

        #For statment handler
    elif c.__class__.__name__ == "ConFor":
        #Creates instance for number of iterations and passes them recursively for set amount of times
        iterations = c.iterations + 1
        for i in range (1, iterations):
            for action in c.action:
                interpret_action(action, i)

        #Print handler, imitates player speak
    elif c.__class__.__name__ == "Speak":
        print(f"{c.player.name} speaks, stating '{c.speech}'")

        #Simple turn counter for for loops.
    elif c.__class__.__name__ == "Count":
        print(f"We are on Turn {turn}")

        #Command used to identify declared variables, printing out full varmap vars.
    elif c.__class__.__name__ == "LookAround":
        print(f"{c.player.name} looks around the area, discovering")
        for name in s:
            if name == c.player.name:
                continue
            else:
                print(f"a {name}!")
    else:
        print(f"Our hero does... nothing?")



#Program interpreter, runs the model through the action interpreter

def interpret_program(model):

    #Initializes Player's level and name into the varmap
    s[model.subject.name] = eval_expr(model.subject.level)

    for c in model.action:
        interpret_action(c)
        



def main():
    parser = argparse.ArgumentParser(description="Interpret RPG files with TextX.")
    parser.add_argument("source", help="Path to the .RPG file to interpret")
    parser.add_argument("--grammar", default="RPG.tx", help="Path to the grammar file (.tx) [default: RPG.tx]")

    args = parser.parse_args()

    #Prints the code written in the output; Files will be read if disregarded
    with open(args.source, 'r') as f:
        print(f.read())
    print()

    # Load grammar and model
    rpg_mm = metamodel_from_file(args.grammar)
    rpg_model = rpg_mm.model_from_file(args.source)

    # Interpret program
    interpret_program(rpg_model)

if __name__ == "__main__":
    main()

