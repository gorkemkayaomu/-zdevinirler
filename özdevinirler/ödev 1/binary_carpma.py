import time

class TuringMachine:
    def __init__(self, tape_string, transitions, start_state='q_start', accept_state='q_accept', reject_state='q_reject'):
        self.tape = list(tape_string)
        self.head_position = 0
        self.state = start_state
        self.transitions = transitions
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = '_'

    def get_tape_symbol(self):
        if self.head_position < 0:
            self.tape.insert(0, self.blank_symbol)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(self.blank_symbol)
        return self.tape[self.head_position]

    def set_tape_symbol(self, symbol):
        self.tape[self.head_position] = symbol

    def move_head(self, direction):
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1

    def print_state(self, read_sym, write_sym, direction):
        tape_str = ""
        for i, sym in enumerate(self.tape):
            if i == self.head_position:
                tape_str += f"\033[91m[{sym}]\033[0m"
            else:
                tape_str += sym
        
        print(f"Durum: {self.state.ljust(18)} | Okunan: {read_sym} | Yazılan: {write_sym} | Yön: {direction} | Bant: {tape_str}")

    def run(self, animate=False, delay=0.05):
        steps = 0
        print("\n--- Turing Makinesi Çalışmaya Başladı ---")
        while self.state != self.accept_state and self.state != self.reject_state:
            read_sym = self.get_tape_symbol()
            
            action = self.transitions.get((self.state, read_sym))
            if action is None:
                print(f"HATA: Geçiş bulunamadı! Durum: {self.state}, Okunan Sembol: {read_sym}")
                self.state = self.reject_state
                break
                
            next_state, write_sym, direction = action
            
            if animate:
                self.print_state(read_sym, write_sym, direction)
                time.sleep(delay)
                
            self.set_tape_symbol(write_sym)
            self.state = next_state
            self.move_head(direction)
            steps += 1
            
            if steps > 5000:
                print("Sonsuz döngü tespit edildi veya adım sayısı çok yüksek!")
                self.state = self.reject_state
                break
                
        if self.state == self.accept_state:
            print("\n>>> DURUM: KABUL (İşlem Başarılı) <<<")
            self.print_state(self.get_tape_symbol(), "-", "-")
            print(f"Toplam Adım: {steps}")
        else:
            print("\n>>> DURUM: RED (İşlem Başarısız) <<<")

def build_transitions():
    transitions = {}
    def add_trans(state, read, next_state, write, dir):
        transitions[(state, read)] = (next_state, write, dir)

    add_trans('q_start', '0', 'q_start', '0', 'R')
    add_trans('q_start', '1', 'q_start', '1', 'R')
    add_trans('q_start', '*', 'find_Y_end', '*', 'R')

    add_trans('find_Y_end', '0', 'find_Y_end', '0', 'R')
    add_trans('find_Y_end', '1', 'find_Y_end', '1', 'R')
    add_trans('find_Y_end', '=', 'find_Y_bit', '=', 'L')

    add_trans('find_Y_bit', 'x', 'find_Y_bit', 'x', 'L')
    add_trans('find_Y_bit', 'y', 'find_Y_bit', 'y', 'L')
    add_trans('find_Y_bit', '0', 'go_sx', 'x', 'L')
    add_trans('find_Y_bit', '1', 'go_add', 'y', 'L')
    add_trans('find_Y_bit', '*', 'halt_routine', '*', 'R')

    add_trans('halt_routine', 'x', 'halt_routine', '0', 'R')
    add_trans('halt_routine', 'y', 'halt_routine', '1', 'R')
    add_trans('halt_routine', '=', 'q_accept', '=', 'R')

    for c in ['0', '1', 'x', 'y']:
        add_trans('go_sx', c, 'go_sx', c, 'L')
    add_trans('go_sx', '*', 'sx_start', '*', 'L')

    for c in ['0', '1', 'x', 'y']:
        add_trans('go_add', c, 'go_add', c, 'L')
    add_trans('go_add', '*', 'add_start', '*', 'L')

    add_trans('add_start', 'a', 'add_start', 'a', 'L')
    add_trans('add_start', 'b', 'add_start', 'b', 'L')
    add_trans('add_start', '0', 'go_Z_add0', 'a', 'R')
    add_trans('add_start', '1', 'go_Z_add1', 'b', 'R')
    add_trans('add_start', '_', 'clean_X', '_', 'R')

    for c in ['0', '1', 'a', 'b', '*', 'x', 'y']:
        add_trans('go_Z_add0', c, 'go_Z_add0', c, 'R')
    add_trans('go_Z_add0', '=', 'find_Z_target_0', '=', 'R')

    for c in ['0', '1', 'a', 'b', '*', 'x', 'y']:
        add_trans('go_Z_add1', c, 'go_Z_add1', c, 'R')
    add_trans('go_Z_add1', '=', 'find_Z_target_1', '=', 'R')

    add_trans('find_Z_target_0', '0', 'find_Z_target_0', '0', 'R')
    add_trans('find_Z_target_0', '1', 'find_Z_target_0', '1', 'R')
    for c in ['_', 'A', 'B']:
        add_trans('find_Z_target_0', c, 'add0_to_target', c, 'L')

    add_trans('find_Z_target_1', '0', 'find_Z_target_1', '0', 'R')
    add_trans('find_Z_target_1', '1', 'find_Z_target_1', '1', 'R')
    for c in ['_', 'A', 'B']:
        add_trans('find_Z_target_1', c, 'add1_to_target', c, 'L')

    add_trans('add0_to_target', '0', 'go_back_X', 'A', 'L')
    add_trans('add0_to_target', '1', 'go_back_X', 'B', 'L')
    add_trans('add0_to_target', '=', 'insert_A', '=', 'R')

    add_trans('add1_to_target', '0', 'go_back_X', 'B', 'L')
    add_trans('add1_to_target', '1', 'carry_1', 'A', 'L')
    add_trans('add1_to_target', '=', 'insert_B', '=', 'R')

    add_trans('carry_1', '0', 'go_back_X', '1', 'L')
    add_trans('carry_1', '1', 'carry_1', '0', 'L')
    add_trans('carry_1', '=', 'insert_1', '=', 'R')

    for tgt, st in [('A', 'insert_A'), ('B', 'insert_B'), ('1', 'insert_1')]:
        for c in ['0', '1', 'A', 'B']:
            add_trans(st, c, f'shift_Z_rem_{c}', tgt, 'R')
        add_trans(st, '_', 'go_back_X', tgt, 'L')

    for mem in ['0', '1', 'A', 'B']:
        st = f'shift_Z_rem_{mem}'
        for c in ['0', '1', 'A', 'B']:
            add_trans(st, c, f'shift_Z_rem_{c}', mem, 'R')
        add_trans(st, '_', 'go_back_X', mem, 'L')

    for c in ['0', '1', 'A', 'B', '=', 'x', 'y']:
        add_trans('go_back_X', c, 'go_back_X', c, 'L')
    add_trans('go_back_X', '*', 'add_start', '*', 'L')

    add_trans('clean_X', 'a', 'clean_X', '0', 'R')
    add_trans('clean_X', 'b', 'clean_X', '1', 'R')
    add_trans('clean_X', '*', 'clean_Z', '*', 'R')

    for c in ['x', 'y', '=', '0', '1']:
        add_trans('clean_Z', c, 'clean_Z', c, 'R')
    add_trans('clean_Z', 'A', 'clean_Z', '0', 'R')
    add_trans('clean_Z', 'B', 'clean_Z', '1', 'R')
    add_trans('clean_Z', '_', 'go_sx_from_clean', '_', 'L')

    for c in ['0', '1', '=', 'x', 'y']:
        add_trans('go_sx_from_clean', c, 'go_sx_from_clean', c, 'L')
    add_trans('go_sx_from_clean', '*', 'sx_start', '*', 'L')

    add_trans('sx_start', '0', 'sx_rem_0', '0', 'L')
    add_trans('sx_start', '1', 'sx_rem_1', '0', 'L')

    add_trans('sx_rem_0', '0', 'sx_rem_0', '0', 'L')
    add_trans('sx_rem_0', '1', 'sx_rem_1', '0', 'L')
    add_trans('sx_rem_0', '_', 'sx_done', '0', 'R')

    add_trans('sx_rem_1', '0', 'sx_rem_0', '1', 'L')
    add_trans('sx_rem_1', '1', 'sx_rem_1', '1', 'L')
    add_trans('sx_rem_1', '_', 'sx_done', '1', 'R')

    for c in ['0', '1', '*', 'x', 'y']:
        add_trans('sx_done', c, 'sx_done', c, 'R')
    add_trans('sx_done', '=', 'find_Y_bit', '=', 'L')

    return transitions

def parse_result(tape_str):
    if '=' not in tape_str:
        return "Hata"
    res_str = tape_str.split('=')[1].replace('_', '')
    if not res_str:
        return "0"
    return res_str

def main():
    transitions = build_transitions()

    print("\n" + "="*50)
    print("  TURING MAKINESI BINARY CARPMA SIMULATORU")
    print("="*50)

    try:
        num1_bin = input("Birinci binary sayiyi girin (X): ").strip()
        num2_bin = input("Ikinci binary sayiyi girin (Y): ").strip()
        
        if not all(c in '01' for c in num1_bin) or not all(c in '01' for c in num2_bin):
            print("HATA: Girdi sadece 0 ve 1'lerden olusmalidir!")
            return

        tape_input = f"{num1_bin}*{num2_bin}="
        print(f"\nBaslangic Bandi: {tape_input}")
        
        ans = input("Adim adim animasyonu gormek ister misiniz? (E/H) (Cikti cok uzun olabilir!): ").strip().upper()
        animate = ans == 'E'

        tm = TuringMachine(tape_input, transitions)
        tm.run(animate=animate, delay=0.01)

        final_tape = "".join(tm.tape)
        result_bin = parse_result(final_tape)
        
        print("\n" + "="*50)
        print(f"ISLEM SONUCU")
        print("="*50)
        print(f"Girdi (Binary)   : {num1_bin} * {num2_bin}")
        try:
            print(f"Girdi (Decimal)  : {int(num1_bin, 2)} * {int(num2_bin, 2)}")
        except ValueError:
            pass
        
        print(f"Cikti (Binary)   : {result_bin}")
        try:
            print(f"Cikti (Decimal)  : {int(result_bin, 2)}")
        except ValueError:
            pass
        print("="*50)

    except KeyboardInterrupt:
        print("\nIslem iptal edildi.")

if __name__ == "__main__":
    main()
