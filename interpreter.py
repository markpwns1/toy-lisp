
import parser
import functools

stack = [ ]
variables = { }

def eval_primitive(ast):
  return ast["value"]

def eval_array(ast):
  return list(map(lambda x: eval(x), ast["elements"]))

def eval_add(args):
  return eval(args[0]) + eval(args[1])

def eval_sub(args):
  return eval(args[0]) - eval(args[1])

def eval_mul(args):
  return eval(args[0]) * eval(args[1])

def eval_div(args):
  return eval(args[0]) / eval(args[1])

def name_of(variable):
  return variable["name"]

def eval_set(args):
  variables[name_of(args[0])] = eval(args[1]) 

def eval_var(ast):
  name = name_of(ast)
  if name in variables.keys():
    return variables[name]
  elif name in instructions.keys():
    return instructions[name]
  else:
    # print("Unknown variable: " + name)
    return None

def eval_eq(args):
  return eval(args[0]) == eval(args[1])

def eval_lt(args):
  return eval(args[0]) < eval(args[1])

def eval_or(args):
  return eval(args[0]) or eval(args[1])

def eval_and(args):
  return eval(args[0]) and eval(args[1])

def eval_not(args):
  return not eval(args[0])

def eval_if(args):
  if eval(args[0]):
    return eval(args[1])
  else:
    return eval(args[2])

def eval_fn(args):
  return {
    "datatype": "function",
    "args": args[0]["elements"],
    "body": args[1]
  }

def eval_len(args):
  return len(eval(args[0]))

def eval_head(args):
  return eval(args[0])[0]

def eval_tail(args):
  return eval(args[0])[1:]

def eval_prepend(args):
  tail = eval(args[1]).copy()
  tail.insert(0, eval(args[0]))
  return tail

def eval_call(args):
  global variables
  fn = eval(args[0])
  fn_args = fn["args"]
  given_args = args[1:]
  variables_before = variables.copy()
  for i in range(0, len(fn_args)):
    variables[name_of(fn_args[i])] = eval(given_args[i])
  result = eval(fn["body"])
  variables = variables_before
  return result

def eval_let_in(args):
  global variables
  variables_before = variables.copy()
  variables[name_of(args[0])] = eval(args[1])
  result = eval(args[2])
  variables = variables_before
  return result

preamble = """
(def or ([x y] => (if x true y)))
(def and ([x y] => (if x y false)))
(def not ([x] => (if x false true)))
(def != ([x y] => (not (x == y))))
(def >= ([x y] => (not (x < y))))
(def > ([x y] => ((x >= y) and (x != y))))
(def <= ([x y] => ((x < y) or (x == y))))
(def nor ([x y] => (not (x or y))))
(def nand ([x y] => (not (x and y))))
(def xor ([x y] => ((x or y) and (x nand y))))
(def ^ ([x y] => (if (y < 2) x (x * (x ^ (y - 1))))))
(def fn =>)
(def null ([x] => (x == [])))
(def len ([a] => (if (null a) 0 (1 + (len (tail a))))))
(def ++ ([x y] => 
  (if (null x) y ((head x) : ((tail x) ++ y)))))
(def # ([a i] => (if (i == 0) 
  (head a)
  ((tail a) # (i - 1)))))
"""

# let f = (x) => x + 1

instructions = {
  "-": eval_sub,
  "+": eval_add,
  "*": eval_mul,
  "/": eval_div,
  "==": eval_eq,
  "<": eval_lt,
  "=>": eval_fn,
  ":": eval_prepend,
  "if": eval_if,
  "def": eval_set,
  "head": eval_head,
  "tail": eval_tail,
  "let-in": eval_let_in,
  "true": True,
  "false": False
}

def eval(ast):
  if ast is None:
    return
  else:
    ast_type = ast["ast_type"] 
    if ast_type == "number":
      return eval_primitive(ast)
    elif ast_type == "variable":
      return eval_var(ast)
    elif ast_type == "boolean":
      return eval_primitive(ast)
    elif ast_type == "array":
      return eval_array(ast)
    elif ast_type == "char":
      return eval_primitive(ast)
    elif ast_type == "instruction":
      args = ast["arguments"]
      func = eval(args[0])
      if callable(func):
        return func(args[1:])
      elif type(func) is dict and func["datatype"] == "function": 
        return eval_call(args)
      else:
        func = eval(args[1])
        if callable(func):
          return func([args[0], args[2]])
        elif type(func) is dict and func["datatype"] == "function": 
          return eval_call([args[1], args[0], args[2]])
        else:
          print ("Can only call a function, not a " + str(func))
    else:
      print("Unknown operation: " + str(ast))

def run(code):
  parser.load(code)
  return eval(parser.parse())
  # return (parser.parse())

def load_preamble():
  parser.load(preamble)
  parser.skip_whitespace()
  while parser.current_char() == "(":
    eval(parser.parse())
    parser.skip_whitespace()
  
def type_of(val):
  if type(val) is dict:
    return val["datatype"]
  else:
    return val.__class__.__name__

def values_equal(a, b):
  if type(a) != type(b): return False
  
def to_string(val):
  t = type_of(val)
  if t == "function":
    return "<function>";
  elif t == "list":
    if len(val) == 0: return "[]"
    elif all(type(x) is str and len(x) == 1 for x in val):
      return functools.reduce(lambda a, b: a+b, val)
    else:
      return str(list(map(to_string, val)))
  else:
    return str(val)
    
  
