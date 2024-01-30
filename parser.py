
code = ""

def load(program):
  global code
  global i
  code = program
  i = 0

# The current letter we're on
i = 0

def next():
  global i
  i += 1

def current_char():
  return "EOF" if i >= len(code) else code[i]

# Returns true if a character is a digit from 0 to 9
def is_digit(character):
	return character in "1234567890"

# Returns true if a character is a letter or a symbol
def is_letter_or_symbol(character):
  return character in "!@#$%^&*_+-=|:<>?/.~_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Given some code like "1234 abc ++!" returns the number 1234
def parse_number():
  contents = ""

  while i < len(code) and is_digit(code[i]):
    contents += code[i]
    next()

  if contents == "": 
    raise "Expected a number"

  return {
    "ast_type": "number",
    "value": float(contents),
  }

# Given some code like "abc 1 2 3 _!dasdjasdh" returns the string "abc"
def parse_name():
  contents = ""
  while i < len(code) and is_letter_or_symbol(code[i]):
    contents += code[i]
    next()

  if contents == "":
    raise "Expected a name"

  return {
    "ast_type": "variable",
    "name": contents
  }

def skip_whitespace():
  while i < len(code) and (code[i] == " " or code[i] == "\n"):
    next()

def parse_string():
  if code[i] != '"':
    raise "Strings should start with '\"'"

  next()
  content = ""
  while code[i] != '"':
    if code[i] == "\\":
      next()
    content += code[i]
    next()

  next()
  return {
    "ast_type": "array",
    "elements": list(map(lambda c: { "ast_type": "char", "value": c }, list(content)))
  }

def parse_char():
  if code[i] != "'":
    raise "Characters should start with '\"'"

  next()
  c = code[i]
  next()
  next()

  return {
    "ast_type": "char",
    "value": c
  }

def parse_array():
  if code[i] != "[":
    raise "Arrays should start with '['"

  next()
  skip_whitespace()

  elements = [ ]
  while code[i] != "]":
    arg = parse()
    elements.append(arg)
    skip_whitespace()

  next() # Eat the ')'

  return {
    "ast_type": "array",
    "elements": elements
  }

def parse_instruction_args():
  instruction_args = [ ]
  while i < len(code) and code[i] != ")":
    arg = parse()
    instruction_args.append(arg)
    skip_whitespace()

  if len(instruction_args) < 1:
    print("Expected a function to call")
    return None

  return instruction_args
  
def parse_instruction():
  if code[i] != "(":
    raise "Instructions should start with '(' or '$'"

  next() # Eat the '('
  skip_whitespace()

  instruction_args = parse_instruction_args()

  if i >= len(code):
    print("Expected ')' to close instruction")
    return None

  next() # Eat the ')'

  return { 
    "ast_type": "instruction",
    "arguments": instruction_args
  }

def parse_instruction_bracketless():
  if code[i] != "$":
    raise "Instructions should start with '(' or '$'"

  next()
  skip_whitespace()

  instruction_args = parse_instruction_args()

  return {
    "ast_type": "instruction",
    "arguments": instruction_args
  }

def parse():
  skip_whitespace()

  if code[i] == "(":
    return parse_instruction()
  elif code[i] == "$":
    return parse_instruction_bracketless()
  elif code[i] == "[":
    return parse_array()
  elif code[i] == '"':
    return parse_string()
  elif code[i] == "'":
    return parse_char()
  elif is_letter_or_symbol(code[i]):
    return parse_name()
  elif is_digit(code[i]):
    return parse_number()
  else:
    print("Unexpected character: " + code[i])
