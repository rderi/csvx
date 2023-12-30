from lark import Lark


_expr_grammar = r"""
    formula: expression
    expression: NUMBER
              | ESCAPED_STRING
              | cell_specifier
              | formula_variable
              | binary_operation
              | UNARY_OP expression
              | function_call

    formula_variable: IDENTIFIER
    binary_operation: comparison_expr | arithmetic_expr
    comparison_expr: expression COMPARISON_OP expression
    arithmetic_expr: term
                   | arithmetic_expr ARITHMETIC_OP term
    term: power_expr
        | term MUL_OP power_expr 
    power_expr: atom
              | power_expr POWER_OP atom 
    atom: NUMBER 
        | cell_specifier
        | ("(" expression ")")
    function_call: IDENTIFIER "(" expression_list ")"
    expression_list: parameter ("," parameter)*
    parameter: expression
    cell_specifier: "[" cell_range_address "]"
    cell_range_address: cell_address ( ":" cell_address )?
    cell_address: LETTER+ DIGIT+
    COMPARISON_OP: "<" | ">" | "<=" | ">=" | "===" | "!="
    ARITHMETIC_OP: "+" | "-"
    MUL_OP: "*" | "/"
    POWER_OP: "^"

    UNARY_OP: "+" | "-"

    %import common.NUMBER
    %import common.ESCAPED_STRING
    %import common.CNAME -> IDENTIFIER
    %import common.LETTER
    %import common.DIGIT
    %import common.WS 
    %ignore WS
    """

class ExpressionParser:
    def __init__(self):
        self.parser = Lark(_expr_grammar, start='formula')
    
    def parse(self, expr):
        return self.parser.parse(expr)

'''
if __name__ == '__main__':
    parser = Lark(grammar, start='formula')
    print(parser.parse('[A3:A4]').pretty())
    print(parser.parse('PI').pretty())
    print(parser.parse('3+4*2^[C5]').pretty())
    print(parser.parse('SUM([C5:C7], [B5:B7])').pretty())
'''