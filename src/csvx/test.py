import os
from csv_engine import CsvEngine
if __name__ == '__main__':
    test_folder = '/Users/rderi/Programming/Personal/xsvx/test'
    test_files = [os.path.join(test_folder, file) for file in os.listdir(test_folder) if file.endswith('.csvx')]
    for test_file in test_files:
        print('----------------------------------------')
        print(f'Testing file: {test_file}')
        engine = CsvEngine(open(test_file).read())
        for i, row in enumerate(engine.contents):
            print(f'Row {i}:', end='\t')
            print(','.join(map(str, row)))

    
