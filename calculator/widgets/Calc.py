from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import sys
sys.setrecursionlimit(10000)


class Calc(BoxLayout):
    Builder.load_file('./screens/Calc.kv')

    register = ''

    def update_input(self):
        self.ids.calc_input.text = self.register

    def update_register(self, text):
        self.register = text

    def sanitize_register(self):
        sanitized_register = []

        for i, char in enumerate(self.register):
            if i == 0:
                if char in ['0','1','2','3','4','5','6','7','8','9','-']:
                    sanitized_register.append(char)
                continue

            if char in['0','1','2','3','4','5','6','7','8','9']:
                if sanitized_register[-1] == '%':
                    continue
                sanitized_register.append(char)
                continue

            if char in ['.']:
                flag = False
                for s_char in reversed(sanitized_register):
                    if s_char in ['/','*','-','+']:
                        break
                    if s_char in ['0','1','2','3','4','5','6','7','8','9']:
                        flag = True
                    if s_char in ['.', '%']:
                        flag = False
                        break

                if flag:
                    sanitized_register.append(char)
                    continue

            if char in ['%']:
                if sanitized_register[-1] in ['0','1','2','3','4','5','6','7','8','9']:
                    sanitized_register.append(char)
                    continue

            
            if (sanitized_register[-1] in ['/','*','-','+', '.'] and char in ['/','*','-','+']):
                sanitized_register[-1] = char
                continue
            
            if char in ['/','*','-','+']:
                sanitized_register.append(char)
                continue
        
        self.register = ''.join(sanitized_register)
            


    def validate_input(self, instance, text):
            self.update_register(text)
            self.sanitize_register()
            self.update_input()


    def clear(self):
        self.register = ''
        self.update_input()

    def back(self):
        self.register = self.register[:-1]
        self.update_input()

    def parse_elements(self):
        operation = []

        element = ''
        for char in self.register:
            if char not in ['/','*','-','+', '%']:
                element += char
            else:
                if element:
                    operation.append(element)
                element = ''
                operation.append(char)

        if element:
            operation.append(element)
        return operation

    def perform_operation(self, operation: list):
        print(operation)
        operation_length = len(operation)
        if not operation:
            return 0
        

        if operation_length == 1:
            return round(float(operation[0]),10)
        
        for i, element in enumerate(operation):
            if element == '%':
                operation[i] =  '/'
                operation.insert( i + 1 , '100')
                return self.perform_operation(operation)

        for i, element in enumerate(operation):
            if element in ['*', '/']:
                if element == '*':
                    if (i + 1) >= operation_length or i == 0:
                        operation.pop(i)
                        return self.perform_operation(operation)
                    
                    operation[i] = float(operation[i-1]) * float(operation[i+1])
                    operation.pop(i+1)
                    operation.pop(i-1)
                    return self.perform_operation(operation)
                
                if element == '/':
                    try:
                        if (i + 1) >= operation_length or i == 0:
                            operation.pop(i)
                            return self.perform_operation(operation)
                        
                        operation[i] = float(operation[i-1]) / float(operation[i+1])
                        operation.pop(i+1)
                        operation.pop(i-1)
                        return self.perform_operation(operation)
                    except:
                        return 0
        
            
        for i, element in enumerate(operation):
            if element == '-':
                if (i + 1) >= operation_length:
                    operation.pop(i)
                    return self.perform_operation(operation)
                
                
                operation[i] = float(operation[i-1]) - float(operation[i+1])
                operation.pop(i+1)
                operation.pop(i-1)
                return self.perform_operation(operation)


        for i, element in enumerate(operation):
            if element == '+':
                if (i + 1) >= operation_length:
                    operation.pop(i)
                    return self.perform_operation(operation)
                
                operation[i] = float(operation[i-1]) + float(operation[i+1])
                operation.pop(i+1)
                operation.pop(i-1)
                return self.perform_operation(operation)


    def calculate(self):
        operation = self.parse_elements()
        result = self.perform_operation(operation)
        result = "{:.10f}".format(result)
        if '.' in result:
            result = result.rstrip('0').rstrip('.')
        self.update_register(result)
        self.update_input()



    def button_click(self, value):
        if value == 'X':
            value = '*'
        
        self.register += value
        self.sanitize_register()
        self.update_input()
