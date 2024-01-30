
import interpreter

print("TOY LISP COMMAND LINE")
print("Try the following, in order:")
print("(def fib ([n] => (if (n < 2) n ((fib (n - 1)) + (fib (n - 2))))))")
print("(fib 8)")
interpreter.load_preamble()
while True:
  text = input("> ")
  result = interpreter.run(text)
  if result != None:
    print(interpreter.to_string(result))
