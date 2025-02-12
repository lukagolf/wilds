import javalang
import secrets
import random
import json
import textwrap
from nltk.corpus import wordnet as wn

from os import listdir
from os.path import isfile, join


def get_radom_var_name():
    """
    Generates a random variable name consisting of 8 lowercase letters.
    
    Returns:
        str: A string representing the generated variable name.
    """
    res_string = ''
    for x in range(8):
        res_string += random.choice('abcdefghijklmnopqrstuvwxyz')
    return res_string


def get_dead_for_condition():
    """
    Creates a for loop condition that will never execute because the condition is always false.
    
    Returns:
        str: A string representing the for loop condition.
    """
    var = get_radom_var_name()
    return "int "+var+" = 0; "+var+" < 0; "+var+"++"


def get_random_false_stmt():
    """
    Generates a boolean expression that will always evaluate to False.
    
    Returns:
        str: A string representing the boolean expression.
    """
    res = [random.choice(["True", "False"]) for x in range(10)]
    res.append("False")
    res_str = " and ".join(res)
    return res_str


def get_tree(data):
    """
    Parses the given Java code into an Abstract Syntax Tree (AST).
    
    Args:
        data (str): A string containing Java code.
    
    Returns:
        object: The root of the AST generated by parsing the code.
    """
    tokens = javalang.tokenizer.tokenize(data)
    parser = javalang.parser.Parser(tokens)
    tree = parser.parse_member_declaration()
    return tree


def verify_method_syntax(data):
    """
    Checks if the given Java method has correct syntax.
    
    Args:
        data (str): A string containing a Java method.
    
    Prints:
        A message indicating whether the syntax check passed or failed.
    """
    try:
        tokens = javalang.tokenizer.tokenize(data)
        parser = javalang.parser.Parser(tokens)
        tree = parser.parse_member_declaration()
        print("syantax check passed")
    except:
        print("syantax check failed")


def get_random_type_name_and_value_statment():
    """
    Generates a random variable declaration with an appropriate value based on the variable's type.
    
    Returns:
        str: A string representing the variable declaration statement.
    """
    datatype = random.choice(
        'byte,short,int,long,float,double,boolean,char,String'.split(','))
    var_name = get_radom_var_name()

    if datatype == "byte":
        var_value = get_random_int(-128, 127)
    elif datatype == "short":
        var_value = get_random_int(-10000, 10000)
    elif datatype == "boolean":
        var_value = random.choice(["True", "False"])
    elif datatype == "char":
        var_value = str(random.choice(
            'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.split(',')))
        var_value = '"'+var_value+'"'
    elif datatype == "String":
        var_value = str(get_radom_var_name())
        var_value = '"'+var_value+'"'
    else:
        var_value = get_random_int(-1000000000, 1000000000)

    mutant = str(var_name) + ' = ' + str(var_value)
    return mutant


def generate_file_name_list_file_from_dir(method_path):
    """
    Creates a text file containing a list of all filenames in the specified directory.
    
    Args:
        method_path (str): The path to the directory.
    
    Prints:
        A message indicating completion of the operation.
    """
    filenames = [f for f in listdir(
        method_path) if isfile(join(method_path, f))]
    with open(method_path+'\\'+'all_file_names.txt', 'w') as f:
        f.write(json.dumps(filenames))
    print("done")


def get_file_name_list(method_path):
    """
    Reads a list of filenames from a text file in the specified directory.
    
    Args:
        method_path (str): The path to the directory containing the text file.
    
    Returns:
        list: A list of filenames read from the file.
    """
    with open(method_path+'\\'+'all_file_names.txt') as f:
        data = json.load(f)
    return data


def get_random_int(min, max):
    """
    Generates a random integer between the specified minimum and maximum values.
    
    Args:
        min (int): The minimum value of the random integer.
        max (int): The maximum value of the random integer.
    
    Returns:
        int: A randomly generated integer within the specified range.
    """
    return random.randint(min, max)


def format_code_chuncks(code_chuncks):
    """
    Formats a list of code chunks by removing unnecessary spaces around punctuation.
    
    Args:
        code_chunks (list): A list of strings representing code chunks.
    
    Returns:
        list: The list of formatted code chunks.
    """
    for idx, c in enumerate(code_chuncks):
        c = c.replace(' . ', '.')
        c = c.replace(' ( ', '(')
        c = c.replace(' ) ', ')')
        c = c.replace(' ;', ';')
        c = c.replace('[ ]', '[]')
        code_chuncks[idx] = c
    return code_chuncks


def format_code(c):
    """
    Formats a single string of code by removing unnecessary spaces around punctuation.
    
    Args:
        c (str): A string representing a chunk of code.
    
    Returns:
        str: The formatted code string.
    """
    c = c.replace(' . ', '.')
    c = c.replace(' ( ', '(')
    c = c.replace(' ) ', ')')
    c = c.replace(' ;', ';')
    c = c.replace('[ ]', '[]')
    return c


def get_method_header(string):
    """
    Extracts the header of a method from a given string containing Java code.
    
    Args:
        string (str): A string containing Java code.
    
    Returns:
        str: The method header extracted from the code.
    """
    method_header = ''
    tree = get_tree(string)

    tokens = list(javalang.tokenizer.tokenize(string))

    chunck_start_poss = [s.position.column for s in tree.body]
    if len(chunck_start_poss) > 0:
        method_header = ' '.join([t.value for t in tokens
                                  if t.position.column < chunck_start_poss[0]])

    method_header = format_code_chuncks([method_header])[0]
    return method_header


def get_method_statement(string):
    """
    Extracts the statements of a method from a given string containing Java code.
    
    Args:
        string (str): A string containing Java code.
    
    Returns:
        list: A list of strings representing the method's statements.
    """
    code_chuncks = []
    tree = get_tree(string)
    tokens = list(javalang.tokenizer.tokenize(string))
    chunck_start_poss = [s.position.column for s in tree.body]

    if len(chunck_start_poss) > 1:
        for idx, statement in enumerate(chunck_start_poss[:-1]):
            statment = ' '.join([t.value for t in tokens
                                 if t.position.column >= chunck_start_poss[idx]
                                 and t.position.column < chunck_start_poss[idx+1]])
            code_chuncks.append(statment)

        last_statment = ' '.join([t.value for t in tokens
                                  if t.position.column >= chunck_start_poss[-1]][:-1])
        code_chuncks.append(last_statment)

    if len(chunck_start_poss) == 1:
        last_statment = ' '.join([t.value for t in tokens
                                  if t.position.column >= chunck_start_poss[0]][:-1])
        code_chuncks.append(last_statment)
    code_chuncks = format_code_chuncks(code_chuncks)
    return code_chuncks


def scan_tree(tree):
    """
    Prints the nodes of the given Abstract Syntax Tree (AST).
    
    Args:
        tree (object): The root of the AST to be scanned.
    """
    for path, node in tree:
        print("=======================")
        print(node)


def get_all_type(tree):
    """
    Retrieves all types from the given Abstract Syntax Tree (AST).
    
    Args:
        tree (object): The root of the AST.
    
    Returns:
        list: A list of all types found in the AST.
    """
    res_list=[]
    for path, node in tree.filter(javalang.tree.ReferenceType):
        if node.name != None:
            res_list.append(node.name)
    return list(set(res_list))


def scan_local_vars(tree):
    """
    Prints the names and types of local variables found in the given Abstract Syntax Tree (AST).
    
    Args:
        tree (object): The root of the AST.
    """
    for path, node in tree.filter(javalang.tree.LocalVariableDeclaration):
        print("name=========type=============")
        print(node.declarators[0].name, "\t", node.type.name)


def get_local_vars(tree):
    """
    Retrieves a list of local variables from the given Abstract Syntax Tree (AST).
    
    Args:
        tree (object): The root of the AST.
    
    Returns:
        list: A list of local variables, each represented as a [name, type] pair.
    """
    var_list = []
    for path, node in tree.filter(javalang.tree.LocalVariableDeclaration):
        var_list.append([node.declarators[0].name, node.type.name])
    return var_list


def get_local_assignments(tree):
    """
    Retrieves a list of local variable assignments from the given Abstract Syntax Tree (AST).
    
    Args:
        tree (object): The root of the AST.
    
    Returns:
        list: A list of local variable assignments, each represented as a [name, type] pair.
    """
    var_list = []
    for path, node in tree.filter(javalang.tree.Assignment):
        var_list.append([node.declarators[0].name, node.type.name])
    return var_list


def get_branch_if_else_mutant():
    """
    Generates a mutant if-else branch with a random type name and value statement, where the if condition is always false.
    
    Returns:
        str: A string representing the mutant if-else branch.
    """
    mutant = get_random_type_name_and_value_statment() + ' if '+get_random_false_stmt() + ' else ' + str(get_random_int(-1000000000, 1000000000))
    return mutant


def get_branch_if_mutant():
    """
    Generates a mutant if branch with a random type name and value statement, where the if condition is always false.
    
    Returns:
        str: A string representing the mutant if branch.
    """
    mutant = 'if '+get_random_false_stmt()+': ' + \
        get_random_type_name_and_value_statment()
    return mutant


def get_branch_while_mutant():
    """
    Generates a mutant while loop with a random type name and value statement, where the while condition is always false.
    
    Returns:
        str: A string representing the mutant while loop.
    """
    mutant = 'while '+get_random_false_stmt()+': ' + \
        get_random_type_name_and_value_statment()
    return mutant


def get_branch_for_mutant():
    """
    Generates a mutant for loop that will never execute because the range is zero.
    
    Returns:
        str: A string representing the mutant for loop.
    """
    var = get_radom_var_name()
    mutant = 'for ' + var + ' in range(0): ' + get_random_type_name_and_value_statment()
    return mutant

def get_related_words(word, pos=wn.NOUN, limit=3):
    """
    Fetches a list of words related to the given word up to a specified limit.

    :param word: The word for which to find related words.
    :param pos: Part of speech (default is noun).
    :param limit: The maximum number of related words to return.
    :return: A list of related words.
    """
    synsets = wn.synsets(word, pos=pos)
    related_words = set()
    for syn in synsets:
        for lemma in syn.lemmas():
            if len(related_words) < limit:
                related_words.add(lemma.name().replace('_', ' '))
            else:
                break
    return list(related_words)

def generate_function_name():
    """
    Generates a random function name using nouns from WordNet.

    :return: A string representing a randomly chosen function name.
    """
    synsets = list(wn.all_synsets(wn.NOUN))
    word = random.choice(synsets).lemmas()[0].name().replace('_', '')
    return word

def generate_random_string_value(base_word):
    """
    Generates a random string value that is semantically related to the given base word.

    :param base_word: The base word to find related string values.
    :return: A string value related to the base word.
    """
    related_words = get_related_words(base_word, limit=10)
    if related_words:
        return random.choice(related_words)
    else:
        # Fallback to a generic string if no related words are found
        return "related string"

def generate_random_value(base_word):
    """
    Generates a random value which could be an integer, a float, or a string semantically related to the base word.

    :param base_word: The base word used for generating a related string value.
    :return: A randomly chosen integer, float, or string.
    """
    value_types = [
        lambda: random.randint(0, 100),
        lambda: round(random.uniform(0.0, 100.0), 2),
        lambda: generate_random_string_value(base_word)
    ]
    return random.choice(value_types)()

def generate_related_var_name(arg_name):
    """
    Generates a variable name that is semantically related to the given argument name.

    :param arg_name: The name of the argument for which to generate a related variable name.
    :return: A string representing a related variable name.
    """
    related_words = get_related_words(arg_name, limit=10)
    for word in related_words:
        if word.replace(' ', '_') != arg_name:
            return word.replace(' ', '_')
    return arg_name + '_var'  # Fallback if no different name is found

def get_synonyms(word):
    """
    Fetches synonyms for a given word.

    :param word: The word for which to find synonyms.
    :return: A list of synonyms for the given word.
    """
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return list(synonyms)

def generate_function_purpose_comment(func_name, related_args):
    """
    Generates a purpose statement for a function based on its name and related arguments.

    :param func_name: The name of the function.
    :param related_args: A list of arguments related to the function.
    :return: A string representing the purpose statement of the function.
    """
    action_words = get_synonyms("process")
    complexity_words = get_related_words(func_name, limit=5)
    complexity_word = random.choice(complexity_words) if complexity_words else "complex"
    action_word = random.choice(action_words) if action_words else "processes"

    args_description = ", ".join(related_args)
    return f"    # The function '{func_name}' {action_word} {args_description} for {complexity_word} tasks."

def generate_comment_for_var(var_name, func_name):
    """
    Generates a comment for a variable within the context of a function.

    :param var_name: The name of the variable.
    :param func_name: The name of the function in which the variable is used.
    :return: A string representing the comment for the variable.
    """
    action_words = get_synonyms("operation")
    action_word = random.choice(action_words) if action_words else "operation"
    return f"    # {var_name} is utilized in {func_name} {action_word}."

def generate_random_function():
    """
    Generates a random function with a random name, arguments, and body. The function includes operations and comments.

    :return: A string representing the complete definition of the randomly generated function.
    """
    func_name = generate_function_name()
    related_args = get_related_words(func_name, pos=wn.NOUN, limit=random.randint(1, 3))
    args = ', '.join([arg.replace(' ', '_') for arg in related_args])
    
    body_lines = [generate_function_purpose_comment(func_name, related_args)]
    operation_lines = []
    for arg in related_args:
        related_var_name = generate_related_var_name(arg.replace(' ', '_'))
        operation_value = repr(generate_random_value(func_name))
        operation_line = f"    {related_var_name} = {arg.replace(' ', '_')} + {operation_value}"
        if random.choice([True, False]):  # Randomly decide to add a comment
            comment = generate_comment_for_var(related_var_name, func_name)
            operation_line += " " + comment  # Append comment on the same line
        operation_lines.append(operation_line)
        body_lines.append(operation_line)

    if operation_lines:
        num_vars_to_return = random.randint(1, len(operation_lines))
        return_vars = random.sample(operation_lines, num_vars_to_return)
        return_statement = 'return ' + ', '.join([var.split('=')[0].strip() for var in return_vars])
        body_lines.append(return_statement)

    function_def = f"def {func_name}({args}):\n" + '\n'.join(body_lines)
    return function_def

def generate_class_name():
    """
    Generates a class name by randomly selecting a noun from WordNet and formatting it as a class name.

    :return: A string representing a class name.
    """
    synsets = list(wn.all_synsets(wn.NOUN))
    word = random.choice(synsets).lemmas()[0].name().capitalize().replace('_', '')
    return word

def generate_field_names(num_fields):
    """
    Generates a list of field names for a class. Each field name is a randomly selected function name.

    :param num_fields: The number of field names to generate.
    :return: A list of strings, each representing a field name.
    """
    return [generate_function_name() for _ in range(num_fields)]

def generate_class_fields(num_fields):
    """
    Generates class field declarations with random types and names.

    :param num_fields: The number of fields to generate for the class.
    :return: A list of strings, each representing a field declaration in the class.
    """
    types = ["int", "float", "str"]
    field_names = generate_field_names(num_fields)
    return [f"{name}: {random.choice(types)}" for name in field_names]

def generate_inheritance():
    """
    Generates a string representing class inheritance by randomly selecting from a predefined set of base classes.

    :return: A string containing the base classes from which the new class will inherit, separated by commas.
    """
    BASE_CLASSES = ["object", "list", "dict", "set"]
    base_classes = random.sample(BASE_CLASSES, random.randint(1, 2))
    return ', '.join(base_classes)

def generate_class_constructor(fields):
    """
    Generates a constructor method for a class, initializing each field provided.

    :param fields: A list of fields to be initialized in the constructor.
    :return: A string representing the constructor method of the class.
    """
    if not fields:
        return "    def __init__(self):\n        pass\n"

    args = ", ".join(["self"] + [f"{name}" for name in fields])
    assignments = "\n".join([f"        self.{name} = {name}" for name in fields])
    return f"    def __init__({args}):\n{assignments}\n"

def apply_decorators(entity, is_class=False):
    """
    Optionally applies decorators to a class or method.

    :param entity: The class or method code to which decorators may be applied.
    :param is_class: Boolean indicating whether the entity is a class (affects the choice of decorators).
    :return: The possibly decorated class or method code.
    """
    decorators = ["@classmethod", "@staticmethod", "@property"]
    if random.choice([True, False]) and not is_class:
        return random.choice(decorators) + "\n" + entity
    return entity

def generate_class_method(is_static=False):
    """
    Generates a class method, potentially adapting an existing sophisticated function for use as a class method.
    The method can be static or instance (non-static).

    :param is_static: Boolean indicating whether the generated method should be static.
    :return: A string representing the class method definition.
    """
    method_code = generate_random_function()
    
    # Adjust the function definition to turn it into a class method
    method_lines = method_code.split('\n')
    if not is_static:
        # Replace function name and add 'self' to arguments
        def_line_parts = method_lines[0].split('(')
        method_lines[0] = def_line_parts[0] + "(self, " + def_line_parts[1]
        # Adjust operations to interact with class fields using 'self'
        for i, line in enumerate(method_lines[1:], start=1):
            if " = " in line:
                left_side = line.split(" = ")[0]
                if not left_side.strip().startswith("self."):
                    method_lines[i] = "    self." + line.strip()
    else:
        # For static methods, remove 'self' from the method
        def_line_parts = method_lines[0].split('(')
        method_lines[0] = def_line_parts[0] + "()"

    # Reassemble the method code
    return '\n'.join(method_lines)

def generate_class_methods(num_methods):
    """
    Generates a specified number of methods for a class.

    :param num_methods: The number of methods to generate for the class.
    :return: A list of strings, each representing a method definition for the class.
    """
    methods = []
    for _ in range(num_methods):
        is_static = random.choice([True, False])
        method = generate_class_method(is_static)
        methods.append(apply_decorators(method))
    return methods

def generate_random_class(num_fields, num_methods):
    """
    Generates a complete random class definition, including fields, methods, and optionally inherited classes.

    :param num_fields: The number of fields to include in the class.
    :param num_methods: The number of methods to include in the class.
    :return: A string representing the complete definition of the class.
    """
    class_name = generate_class_name()
    base_class = generate_inheritance()
    fields = generate_class_fields(num_fields)
    constructor = generate_class_constructor(fields)
    methods = generate_class_methods(num_methods)

    class_def = f"@apply_decorators\nclass {class_name}({base_class}):\n"
    class_def += "    \"\"\"Advanced class definition with fields and methods.\"\"\"\n"
    # Include field definitions
    for field in fields:
        class_def += f"    {field}\n"
    class_def += constructor + "\n"
    for method in methods:
        class_def += method + "\n\n"

    return class_def.strip()
