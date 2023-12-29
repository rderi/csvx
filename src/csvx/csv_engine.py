import csv
from io import StringIO
from expressions import ExpressionParser

class CsvEngine:
    def __init__(self, input):
        self.expression_parser = ExpressionParser()
        self.input = StringIO(input)
        self.contents = self.read_csv()
        self.parse_expressions()

    def read_csv(self):
        reader = csv.reader(self.input, skipinitialspace=True, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        return list(reader)

    def parse_expression(self, cell_value):
        return self.expression_parser.parse(cell_value)

    def parse_expressions(self):
        for row in self.contents:
            for i, cell in enumerate(row):
                if isinstance(cell, str) and cell.startswith('='):
                    #Meant to fix the error of python's CSV reader ignoring quotes if they are not the first character in a cell.
                    #This is an issue when a cell starts with =" and contains a delimiter, as the delimiter will be treated as regular
                    #Hacky but it works
                    if cell.startswith('="') and len(row) > i + 1 and not row[i + 1].startswith('"') and row[i + 1].endswith('"'):
                        cell = cell + ',' + row[i + 1]
                        row.pop(i + 1)
                    parsed_expression = self.parse_expression(cell[1:])
                    row[i] = parsed_expression

