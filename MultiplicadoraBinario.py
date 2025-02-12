class TuringMachine:
    def __init__(self, logic):
        self.transitions = {}  # Dicionário para armazenar as transições da máquina de Turing
        self.parse_logic(logic)  # Chama o método para analisar a lógica fornecida

    def parse_logic(self, logic):
        """
        Analisa a lógica fornecida e preenche o dicionário de transições.
        Cada linha da lógica deve conter: estado_atual, símbolo_atual, novo_símbolo, direção, novo_estado.
        """
        for line in logic.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith(';'):
                continue  # Ignora linhas vazias ou comentários

            parts = line.split()
            if len(parts) < 5:
                continue  # Ignora linhas que não têm os 5 componentes necessários

            current_state = parts[0]
            current_symbol = parts[1]
            new_symbol = parts[2]
            direction = parts[3]
            new_state = parts[4]

            # Adiciona a transição ao dicionário
            self.transitions[(current_state, current_symbol)] = (new_symbol, direction, new_state)

    def run(self, input_tape, show_steps=False):
        """
        Executa a máquina de Turing na fita de entrada fornecida.
        Se show_steps for True, exibe cada passo da execução.
        """
        tape = list(input_tape)  # Converte a fita de entrada em uma lista de caracteres
        head_position = 0  # Posição inicial da cabeça de leitura/escrita
        state = '0'  # Estado inicial
        step_count = 0  # Contador de passos

        # Verifica se há um '*' na fita para determinar a posição inicial da cabeça
        if '*' in tape:
            head_position = tape.index('*')
            tape.pop(head_position)  # Remove o '*' da fita

        if show_steps:
            print("Iniciando a execução da Máquina de Turing...")
            print("Fita inicial: " + "".join(tape))
            print("Estado inicial: 0")
            print("Posição da cabeça: " + str(head_position))
            print("-" * 30)

        while not state.startswith('halt'):
            step_count += 1
            if step_count > 1000:  # Limite de segurança para evitar loops infinitos
                state = 'halt-error-potential-infinite-loop'
                if show_steps:
                    print("Limite de passos atingido (1000). Interrompendo devido a potencial loop infinito.")
                break

            # Obtém o símbolo atual sob a cabeça
            current_symbol = tape[head_position] if 0 <= head_position < len(tape) else '_'

            transition = None
            transition_rule = None  # Armazena a regra de transição para exibição

            # Tenta encontrar uma correspondência exata para a transição
            if (state, current_symbol) in self.transitions:
                transition = self.transitions[(state, current_symbol)]
                transition_rule = f"({state}, {current_symbol}) -> ({transition[0]}, {transition[1]}, {transition[2]})"
            # Tenta correspondência com curinga para o símbolo
            elif (state, '*') in self.transitions:
                transition = self.transitions[(state, '*')]
                transition_rule = f"({state}, *) -> ({transition[0]}, {transition[1]}, {transition[2]})"

            if transition:
                new_symbol, direction, new_state = transition

                if new_symbol != '*':
                    if 0 <= head_position < len(tape):
                        tape[head_position] = new_symbol  # Escreve o novo símbolo na fita
                    elif head_position < 0:  # Expansão para a esquerda, insere no início
                        tape.insert(0, new_symbol)
                        head_position = 0  # A cabeça permanece no início após a inserção
                    else:  # Expansão para a direita, adiciona ao final
                        tape.append(new_symbol)

                # Move a cabeça de acordo com a direção especificada
                if direction == 'l':
                    head_position -= 1
                elif direction == 'r':
                    head_position += 1
                elif direction == '*':
                    pass  # Sem movimento

                # Atualiza o estado
                state = new_state if new_state != '*' else state

                if show_steps:
                    # Exibe o estado atual da fita com a posição da cabeça marcada
                    tape_display = list(tape)
                    tape_display_str_parts = []
                    for i, symbol in enumerate(tape_display):
                        if i == head_position:
                            tape_display_str_parts.append(f"[{symbol}]")  # Marca a posição da cabeça com colchetes
                        else:
                            tape_display_str_parts.append(symbol)
                    tape_display_str = "".join(tape_display_str_parts)

                    print(f"Passo: {step_count}")
                    print(f"Estado: {state}")
                    print(f"Fita: {tape_display_str}")
                    print(f"Posição da cabeça: {head_position}")
                    print(f"Símbolo atual: {current_symbol if current_symbol != '_' else '_'}")
                    print(f"Transição: {transition_rule}")
                    print("-" * 30)

            else:
                state = 'halt-error-no-transition'
                if show_steps:
                    print(f"Passo: {step_count}")
                    print(f"Estado: {state}")
                    print(f"Fita: {''.join(tape)}")
                    print(f"Posição da cabeça: {head_position}")
                    print(f"Símbolo atual: {current_symbol if current_symbol != '_' else '_'}")
                    print("Nenhuma transição encontrada para o estado e símbolo atuais. Interrompendo.")
                    print("-" * 30)
                break

            # Lida com os limites da fita, adicionando espaços em branco conforme necessário
            if head_position < 0:
                tape.insert(0, '_')
                head_position = 0
            elif head_position >= len(tape):
                tape.append('_')

        # Remove espaços em branco iniciais e finais da fita de saída
        while tape and tape[0] == '_':
            tape.pop(0)
        while tape and tape[-1] == '_':
            tape.pop()

        if show_steps:
            if state.startswith('halt') and not state.startswith('halt-error'):
                print("Máquina de Turing interrompida com sucesso!")
            elif state.startswith('halt-error'):
                print(f"Máquina de Turing interrompida com estado de erro: {state}")
            print("Fita final: " + "".join(tape))
            print("-" * 30)

        return "".join(tape)

tm_logic = """
  ; Set up tally
  0 * * l 1
  1 _ _ l 2
  2 _ 0 r 3
  3 _ _ r 10

  ; Find end of num1
  10 _ _ l 11
  10 x x l 11
  10 0 0 r 10
  10 1 1 r 10


  ; If last digit of num1 is 0, multiply num2 by 2
  11 0 x r 20
  ; If last digit of num1 is 1, add num2 to tally and then multiply num2 by 2
  11 1 x r 30


  ; Multiply num2 by 2
  20 _ _ r 20
  20 x x r 20
  20 * * r 21
  21 _ 0 l 25 ; Multiplication by 2 done, return to end of num1
  21 * * r 21
  25 _ _ l 26
  25 * * l 25
  26 _ _ r 80 ; Finished multiplying. Clean up
  26 x x l 26
  26 0 0 * 11
  26 1 1 * 11

  ; Add num2 to tally
  30 _ _ r 30
  30 x x r 30
  30 * * r 31
  31 _ _ l 32
  31 * * r 31
  32 0 o l 40 ; Add a zero
  32 1 i l 50 ; Add a one
  32 o o l 32
  32 i i l 32
  32 _ _ r 70 ; Finished adding

  ; Adding a 0 to tally
  40 _ _ l 41
  40 * * l 40 ; Found end of num2
  41 _ _ l 41
  41 * * l 42 ; Found start of num1
  42 _ _ l 43 ; Found end of num1
  42 * * l 42
  43 o o l 43
  43 i i l 43
  43 0 o r 44
  43 1 i r 44
  43 _ o r 44
  44 _ _ r 45 ; Found end of tally
  44 * * r 44
  45 _ _ r 45
  45 * * r 46 ; Found start of num1
  46 _ _ r 47 ; Found end of num1
  46 * * r 46
  47 _ _ r 47
  47 * * r 48
  48 _ _ l 32 ; Found end of num2
  48 * * r 48

  ; Adding a 1 to tally
  50 _ _ l 51 ; Found end of num2
  50 * * l 50
  51 _ _ l 51
  51 * * l 52 ; Found start of num1
  52 _ _ l 53 ; Found end of num1
  52 * * l 52
  53 o o l 53
  53 i i l 53
  53 _ i r 55
  53 0 i r 55 ; return to num2
  53 1 o l 54
  54 0 1 r 55
  54 1 0 l 54
  54 _ 1 r 55
  55 _ _ r 56 ; Found end of tally
  55 * * r 55
  56 _ _ r 56
  56 * * r 57 ; Found start of num1
  57 _ _ r 58 ; Found end of num1
  57 * * r 57
  58 _ _ r 58
  58 * * r 59
  59 _ _ l 32 ; Found end of num2
  59 * * r 59

  ; Finished adding, clean up
  70 i 1 r 70
  70 o 0 r 70
  70 _ _ l 71
  71 _ _ l 72 ; Found end of num2
  71 * * l 71
  72 _ _ l 72
  72 * * l 73 ; Found start of num1
  73 _ _ l 74
  73 * * l 73
  74 o 0 l 74
  74 i 1 l 74
  74 * * r 75 ; Finished cleaning up tally
  75 _ _ r 76
  75 * * r 75
  76 _ _ r 20 ; Multiply num2 by 2
  76 * * r 76

  ; Finished multiplying, clean up
  80 x _ r 80
  80 _ _ r 81
  81 _ _ l 82
  81 * _ r 81
  82 _ _ l 82
  82 * * * halt
"""

tm = TuringMachine(tm_logic)
#Mostrar os passos da maquina
show_steps = True 

# Exemplo:
input1 = "101"
input2 = "111"
input_tape = list(input1 + "_" + input2 + "_")
result_tape = tm.run(input_tape, show_steps)

print(f"Entrada 1: {input1}")
print(f"Entrada 2: {input2}")
print(f"Fita de Resultado: {result_tape}")

# Verificar resultado:
num1 = int(input1, 2)
num2 = int(input2, 2)
expected_product_bin = bin(num1 * num2)[2:]
print(f"Produto Binário Esperado: {expected_product_bin}")
print(f"Resultado Correto: {result_tape == expected_product_bin}")