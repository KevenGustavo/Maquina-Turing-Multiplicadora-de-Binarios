class Tape:
    def __init__(self, initial):
        self.tape = list(initial)
        self.head = 0

    def read(self):
        if self.head < 0 or self.head >= len(self.tape):
            return '_'
        return self.tape[self.head]

    def write(self, symbol):
        if self.head < 0:
            self.tape.insert(0, symbol)
            self.head = 0
        elif self.head >= len(self.tape):
            self.tape.append(symbol)
        else:
            self.tape[self.head] = symbol

    def move(self, direction):
        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1

    def __str__(self):
        return ''.join(self.tape) + '\n' + ' ' * self.head + '^'

def binary_multiplier_turing_machine(num1, num2):
    num1 = num1.zfill(4)
    num2 = num2.zfill(4)
    initial_tape = list(num1) + ['#'] + list(num2) + ['#'] + ['0'] * 8
    tape = Tape(initial_tape)
    state = "INIT"
    steps = 0
    shift_count = 0
    max_steps = 1000  # Prevent infinite loops

    print(f"Step {steps}: State={state}")
    print(tape)

    while state != "HALT" and steps < max_steps:
        steps += 1
        current_symbol = tape.read()

        if state == "INIT":
            state = "FIND_MULTIPLIER"
            tape.move('R')

        elif state == "FIND_MULTIPLIER":
            if current_symbol == '#':
                tape.move('R')
                found_bits = 0
                state = "POSITION_AT_MULTIPLIER"
            else:
                tape.move('R')

        elif state == "POSITION_AT_MULTIPLIER":
            if shift_count >= 4:
                state = "HALT"
            else:
                while tape.read() != '#':
                    tape.move('R')
                tape.move('L')  # Move to the last bit of multiplier
                for _ in range(3 - shift_count):
                    tape.move('L')
                state = "CHECK_BIT"

        elif state == "CHECK_BIT":
            if current_symbol in ['0', '1']:
                if current_symbol == '1':
                    state = "PREPARE_ADD"
                else:
                    state = "SHIFT_MULTIPLICAND"
                tape.write('X')  # Mark bit as processed
            else:
                state = "HALT"

        elif state == "PREPARE_ADD":
            # Move to the end of the multiplicand
            while tape.read() != '#':
                tape.move('L')
            tape.move('R')  # Now at the first '#'
            while tape.read() != '#':
                tape.move('L')
            tape.move('R')  # Position at start of result
            for _ in range(7):
                tape.move('R')  # Move to the end of result (LSB)
            state = "ADDING"
            carry = '0'

        elif state == "ADDING":
            # Move to multiplicand's LSB
            while tape.read() != '#':
                tape.move('L')
            tape.move('L')
            multiplicand_pos = tape.head
            # Move to result's LSB
            while tape.read() != '#':
                tape.move('R')
            tape.move('R')
            result_pos = tape.head + 7
            if result_pos >= len(tape.tape):
                result_pos = len(tape.tape) - 1
            tape.head = result_pos
            state = "ADD_LOOP"
            carry = '0'

        elif state == "ADD_LOOP":
            # This is a simplified addition; detailed implementation needed
            tape.head = multiplicand_pos
            m_bit = tape.read()
            tape.head = result_pos
            r_bit = tape.read()

            sum_bits = int(m_bit) + int(r_bit) + int(carry)
            new_r_bit = str(sum_bits % 2)
            carry = str(sum_bits // 2)

            tape.write(new_r_bit)
            tape.move('L')
            multiplicand_pos -= 1
            result_pos -= 1

            if multiplicand_pos < 0 or tape.tape[multiplicand_pos] == '#':
                if carry == '1':
                    tape.head = result_pos
                    while carry == '1' and result_pos >= 0:
                        r_bit = tape.read()
                        sum_bits = int(r_bit) + int(carry)
                        new_r_bit = str(sum_bits % 2)
                        carry = str(sum_bits // 2)
                        tape.write(new_r_bit)
                        tape.move('L')
                        result_pos -= 1
                state = "SHIFT_MULTIPLICAND"
            else:
                state = "ADD_LOOP"

        elif state == "SHIFT_MULTIPLICAND":
            # Append a '0' to multiplicand
            while tape.read() != '#':
                tape.move('R')
            tape.move('L')
            tape.write('0')
            tape.move('R')
            tape.write('#')
            shift_count += 1
            state = "FIND_MULTIPLIER"

        print(f"Step {steps}: State={state}")
        print(tape)

    # Extract result
    result_start = len(num1) + 1 + len(num2) + 1
    result = ''.join(tape.tape[result_start:result_start+8])
    decimal = int(result, 2)
    return result, decimal

# Example usage:
num1 = '1010'  # 10
num2 = '1101'  # 13
result_bin, result_dec = binary_multiplier_turing_machine(num1, num2)
print(f"Final Result (Binary): {result_bin}")
print(f"Final Result (Decimal): {result_dec}")