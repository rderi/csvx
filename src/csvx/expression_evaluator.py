from lark import Lark, Token, Tree

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
            if len(node.children) == 1:
                return context.get_a1(eval_expression(node.children[0], context))
            else:
                raise NotImplementedError("Cell range address between two cells not implemented")
        elif rule_name == 'cell_address':
            a1 = ""
            if len(node.children) != 2:
                raise ValueError("Cell address must have two tokens as children")
            a1 += node.children[0].value + node.children[1].value
            return a1
        elif len(node.children) == 1:
            return eval_expression(node.children[0], context)