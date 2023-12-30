import cell_types as types
from lark import Lark, Token, Tree


def _indices_between(a, b):
    # Given two indices in a 2d array, return all indices between them assuming they are diagonal corners in a rectangle
    # a and b are tuples of the form (row, column)
    indices = []
    # Access variables a and b
    row_start, col_start = a
    row_end, col_end = b
    # Determine the top-left and bottom-right corners
    top_left = (min(row_start, row_end), min(col_start, col_end))
    bottom_right = (max(row_start, row_end), max(col_start, col_end))
    # Add indices between the top-left and bottom-right corners to the list
    for row in range(top_left[0], bottom_right[0] + 1):
        for col in range(top_left[1], bottom_right[1] + 1):
            indices.append((row, col))
    return indices

def eval_expression(node, context):
    if isinstance(node, Token):
        if node.type == 'NUMBER':
            return float(node.value)
        elif node.type == 'ESCAPED_STRING':
            return node.value[1:-1]
    
    elif isinstance(node, Tree):
        rule_name = node.data.value
        if rule_name == 'arithmetic_expr':
            if len(node.children) == 1:
                return eval_expression(node.children[0], context)
            operator = node.children[1].value
            if operator == '+':
                return eval_expression(node.children[0], context) + eval_expression(node.children[2], context)
            elif operator == '-':
                return eval_expression(node.children[0], context) - eval_expression(node.children[2], context)
        elif rule_name == 'term':
            if len(node.children) == 1:
                return eval_expression(node.children[0], context)
            operator = node.children[1].value
            if operator == '*':
                return eval_expression(node.children[0], context) * eval_expression(node.children[2], context)
            elif operator == '/':
                return eval_expression(node.children[0], context) / eval_expression(node.children[2], context)
        elif rule_name == 'power_expr':
            if len(node.children) == 1:
                return eval_expression(node.children[0], context)
            return eval_expression(node.children[0], context) ** eval_expression(node.children[2], context)
        elif rule_name == 'cell_range_address':
            if len(node.children) == 1: #Single cell reference
                return context.get_a1(eval_expression(node.children[0], context))
            else:
                a1_start = eval_expression(node.children[0], context)
                a1_end = eval_expression(node.children[1], context)
                start_idx = context._a1_to_idx(a1_start)
                end_idx = context._a1_to_idx(a1_end)
                indices = _indices_between(start_idx, end_idx)
                values = [context.get(*idx) for idx in indices]
                return types.List(values)

        elif rule_name == 'cell_address':
            a1 = ""
            if len(node.children) != 2:
                raise ValueError("Cell address must have two tokens as children")
            a1 += node.children[0].value + node.children[1].value
            return a1
        elif rule_name == 'function_call':
            function_name = node.children[0].value
            args = [eval_expression(child, context) for child in node.children[1:]]
            args = [types.detect_literal_type(arg) for arg in args]
            return context.function_engine.call_fn(function_name, args)
        elif len(node.children) == 1:
            return eval_expression(node.children[0], context)
        else:
            raise NotImplementedError(f'Rule {rule_name} not implemented')