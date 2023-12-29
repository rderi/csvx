from csv_engine import CsvEngine
if __name__ == '__main__':
    engine = CsvEngine('John,Doe,25\nJane,Smith,=10+20\nAdam,Johnson,=5*7\n="Well, I like to think of myself as an idiot"')
    for row in engine.contents:
        print(row)
    
