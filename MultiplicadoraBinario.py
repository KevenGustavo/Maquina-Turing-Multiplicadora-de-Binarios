def print_tape(tape, head, state, step_count):
    """Exibe o estado atual da fita, o cabeçote e o estado da máquina."""
    tape_str = ''.join(tape)
    pointer = ' ' * head + '^'
    print(f"Step {step_count} | State: {state}")
    print("Fita: " + tape_str)
    print("      " + pointer)
    print("-" * 40)

def binary_add(a, b):
    """Soma dois números binários representados como strings sem conversão para decimal."""
    max_len = max(len(a), len(b))
    # Preenche com zeros à esquerda para ter o mesmo tamanho
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    carry = 0
    result = ""
    for i in range(max_len - 1, -1, -1):
        bit_a = 1 if a[i] == '1' else 0
        bit_b = 1 if b[i] == '1' else 0
        total = bit_a + bit_b + carry
        result = ('1' if total % 2 == 1 else '0') + result
        carry = 1 if total > 1 else 0
    if carry:
        result = '1' + result
    return result

class TuringMachine:
    def __init__(self, input_str):
        # A fita inicial: adiciona células em branco ('_') à direita para escrita.
        self.tape = list(input_str + "_" * 30)
        self.head = 0
        # Estados: READ_INPUT, READ_SECOND, COMPUTE, WRITE_RESULT, HALT
        self.state = "READ_INPUT"
        self.numA = ""
        self.numB = ""
        self.result = ""
        self.step_count = 0

    def step(self):
        # Incrementa o contador de passos e exibe o estado atual da fita
        self.step_count += 1
        print_tape(self.tape, self.head, self.state, self.step_count)
        
        if self.state == "READ_INPUT":
            # Lê os dígitos do primeiro número até encontrar o separador '#'
            if self.head < len(self.tape) and self.tape[self.head] != '_':
                current_symbol = self.tape[self.head]
                if current_symbol == '#':
                    self.state = "READ_SECOND"
                    self.head += 1  # move para o primeiro dígito do segundo número
                else:
                    self.numA += current_symbol
                    self.head += 1
            else:
                print("Erro: separador '#' não encontrado na fita.")
                self.state = "HALT"

        elif self.state == "READ_SECOND":
            # Lê os dígitos do segundo número até encontrar a primeira célula em branco ('_')
            if self.head < len(self.tape) and self.tape[self.head] != '_':
                self.numB += self.tape[self.head]
                self.head += 1
            else:
                self.state = "COMPUTE"

        elif self.state == "COMPUTE":
            # Garante que ambos os números tenham exatamente 8 bits
            if len(self.numA) < 8:
                self.numA = self.numA.zfill(8)
            elif len(self.numA) > 8:
                print("Aviso: O primeiro número possui mais que 8 bits, considerando os 8 bits menos significativos.")
                self.numA = self.numA[-8:]
            if len(self.numB) < 8:
                self.numB = self.numB.zfill(8)
            elif len(self.numB) > 8:
                print("Aviso: O segundo número possui mais que 8 bits, considerando os 8 bits menos significativos.")
                self.numB = self.numB[-8:]

            print(f"\nNúmeros lidos (8 bits): A = {self.numA}, B = {self.numB}")
            print("\nIniciando a multiplicação binária sem conversão para decimal:")
            # Implementa a multiplicação em binário usando soma iterativa
            result = "0"
            # Itera sobre os bits do multiplicador (numB) da direita para a esquerda
            for i in range(len(self.numB) - 1, -1, -1):
                bit = self.numB[i]
                shift = (len(self.numB) - 1) - i
                if bit == '1':
                    # Desloca o multiplicando para a esquerda conforme o bit
                    shifted = self.numA + "0" * shift
                    print(f"Bit '{bit}' na posição {i} (shift {shift}): adicionando {self.numA} << {shift} = {shifted}")
                    result = binary_add(result, shifted)
                    print(f"  Resultado parcial: {result}")
                else:
                    print(f"Bit '{bit}' na posição {i} (shift {shift}): ignorado (nenhuma adição)")
            self.result = result
            print(f"\nMultiplicação completa. Resultado final em binário: {self.result}")
            # Prepara a fita para a escrita do resultado: limpa a fita e posiciona o cabeçote no início.
            self.tape = list("_" * 50)
            self.head = 0
            self.state = "WRITE_RESULT"

        elif self.state == "WRITE_RESULT":
            # Escreve o resultado na fita, célula a célula
            if self.result:
                self.tape[self.head] = self.result[0]
                self.result = self.result[1:]
                self.head += 1  # move o cabeçote para a direita
            else:
                self.state = "HALT"

        if self.state == "HALT":
            print_tape(self.tape, self.head, self.state, self.step_count)
            final_output = ''.join(self.tape).strip('_')
            print("\nMáquina de Turing finalizada.")
            print("Resultado final na fita:", final_output)
            return False
        return True

    def run(self):
        print("Iniciando a simulação da Máquina de Turing para multiplicação de números binários (8 bits)...\n")
        while self.state != "HALT":
            if not self.step():
                break

# Exemplo de uso:
if __name__ == '__main__':
    # Exemplo: multiplicar 00001010 (10) por 00000011 (3) - ambos em 8 bits
    input_tape = "00001010#00000011"
    tm = TuringMachine(input_tape)
    tm.run()