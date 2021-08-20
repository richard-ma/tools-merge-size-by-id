#!/usr/bin/env python
# APP Framework 1.0

import csv
import os
from pprint import pprint

class App:
    def __init__(self):
        self.title_line = "合并带有相同id的行"
        self.counter = 1
        
    def printCounter(self, data=None):
        print("[%04d] Porcessing: %s" % (self.counter, str(data)))
        self.counter += 1
    
    def initCounter(self, value=1):
        self.counter = value
        
    def run(self):
        self.usage()
        self.process()
        
    def usage(self):
        print("*" * 80)
        print("*", " " * 76, "*")
        print("*", 
            " " * ((80-14-len(self.title_line))//2), 
            self.title_line,  
            " " * ((80-14-len(self.title_line))//2),
            "*")
        print("*", " " * 76, "*")
        print("*" * 80)
        
    def input(self, notification, default=None):
        var = input(notification)
        
        if len(var) == 0:
            return default
        else:
            return var
            
    def readCsvToDict(self, filename, encoding="GBK"):
        data = list()
        with open(filename, 'r+', encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
        
    def writeCsvFromDict(self, filename, data, fieldnames=None, encoding="GBK", newline=''):
        if fieldnames is None:
            fieldnames = data[0].keys()

        with open(filename, 'w+', encoding=encoding, newline=newline) as f:
            writer = csv.DictWriter(f,
                fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
    def addSuffixToFilename(self, filename, suffix):
        filename, ext = os.path.splitext(filename)
        return filename + suffix + ext
        
    def process(self):
        input_filename = self.input(
            "请将待处理的文件拖动到此窗口，然后按回车键。", 
            default="./test/shopping.csv")
        output_filename = self.addSuffixToFilename(input_filename, '_new')
        
        data = self.readCsvToDict(input_filename)
        #pprint(data)
        
        sep_list = ['-', '_']
        output_data = list()
        self.initCounter()
        for line in data:
            id = line['id']
            self.printCounter(id)
            sep = None
            for item in sep_list:
                if item in id:
                    sep = item
                    
            line['newsize'] = ""
            if sep is None:
                output_data.append(line)
                continue
            else:
                id, size = id.split(sep)
                
                for item in output_data:
                    if item['id'] == id:
                        item['newsize'] += '|' + size
                        break
                else:
                    line['id'] = id
                    line['newsize'] = size
                    output_data.append(line)
                    
        #pprint(output_data)
        
        fieldnames = ['id', 'newsize']
        tmp_fieldnames = list(output_data[0].keys())
        del tmp_fieldnames[tmp_fieldnames.index('id')]
        fieldnames.extend(tmp_fieldnames)
        #print(fieldnames)
        
        self.writeCsvFromDict(output_filename, output_data, fieldnames=fieldnames)
        
if __name__ == "__main__":
    app = App()
    app.run()