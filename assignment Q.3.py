import re
def solve_q3():
    sample_data = """4
x=10
y=x*2
z=y+5
w=z-x
w*2"""

    lines = sample_data.split('\n')
    v = int(lines[0])
    
    # Store equations in a dictionary
    expressions = {}
    for i in range(1, v + 1):
        variable, equation = lines[i].split('=')
        expressions[variable.strip()] = equation.strip()
        
    target_expression = lines[v + 1].strip()
    
    # Dictionaries to track memory and prevent infinite loops
    memo = {}      # Remembers calculated answers
    visiting = set() # Tracks variables currently being calculated
    
    def evaluate(expr):
        # Base case: if we already solved this, return the answer
        if expr in memo: 
            return memo[expr]
            
        # If we are already trying to solve this variable, we are stuck in a loop!
        if expr in visiting: 
            raise ValueError("CYCLE")
            
        visiting.add(expr)
        
        # Break the expression into words/symbols using a simple regular expression
        tokens = re.findall(r'[a-zA-Z_]\w*|\d+|[+\-*()]', expr)
        
        parsed_expr = ""
        for token in tokens:
            if token.isalpha(): # If it's a variable letter (like 'a' or 'b')
                if token not in expressions:
                    raise ValueError("INVALID")
                # Go find what this variable equals!
                val = evaluate(expressions[token])
                parsed_expr += str(val)
            else:
                parsed_expr += token # Numbers and math symbols remain the same
                
        # Calculate the final math string and save it
        try:
            result = eval(parsed_expr)
            memo[expr] = int(result)
            visiting.remove(expr)
            return memo[expr]
        except Exception:
            raise ValueError("INVALID")
            
    # Try to evaluate the target and catch any errors
    try:
        answer = evaluate(target_expression)
        print(answer)
    except ValueError as e:
        print(e)

# Run the program
solve_q3()
