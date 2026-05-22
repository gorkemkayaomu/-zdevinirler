import time

class TuringMachineRecognizer:
    def __init__(self, input_string, transitions, start_state='q0', accept_state='q_accept', reject_state='q_reject'):
        self.tape = list(input_string)
        self.head_position = 0
        self.state = start_state
        self.transitions = transitions
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = '_'

    def get_tape_symbol(self):
        if self.head_position < 0 or self.head_position >= len(self.tape):
            return self.blank_symbol
        return self.tape[self.head_position]

    def move_head(self, direction):
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1

    def print_state(self, read_sym, direction):
        tape_str = ""
        for i, sym in enumerate(self.tape):
            if i == self.head_position:
                tape_str += f"\033[91m[{sym}]\033[0m"
            else:
                tape_str += sym
        
        print(f"Durum: {self.state.ljust(15)} | Okunan: {read_sym:>3} | Yön: {direction} | Bant: {tape_str}")

    def run(self, animate=False, delay=0.05):
        steps = 0
        print("\n--- Plaka Tanıyıcı Turing Makinesi Başladı ---")
        
        while self.state != self.accept_state and self.state != self.reject_state:
            read_sym = self.get_tape_symbol()
            
            action = self.transitions.get((self.state, read_sym))
            if action is None:
                if animate:
                    print(f"HATA: Geçiş bulunamadı! Durum: {self.state}, Okunan Sembol: '{read_sym}'")
                self.state = self.reject_state
                break
            
            next_state, direction = action
            
            if animate:
                self.print_state(read_sym, direction)
                time.sleep(delay)
            
            self.state = next_state
            self.move_head(direction)
            steps += 1
            
            if steps > 500:
                print("Sonsuz döngü tespit edildi!")
                self.state = self.reject_state
                break
        
        if self.state == self.accept_state:
            print("\n>>> SONUÇ: KABUL (Plaka Geçerli) <<<")
            print(f"Toplam Adım: {steps}")
        else:
            print("\n>>> SONUÇ: RED (Plaka Geçersiz) <<<")

def build_transitions():
    """
    Durum Geçişleri:
    Format: NNLLNNN
    N = Rakam (0-9)
    L = Büyük Harf (A-Z)
    
    q0: Birinci rakam bekleniyor
    q1: İkinci rakam bekleniyor
    q2: Birinci harf bekleniyor
    q3: İkinci harf bekleniyor
    q4: Üçüncü rakam bekleniyor
    q5: Dördüncü rakam bekleniyor
    q6: Beşinci rakam bekleniyor
    q_accept: Başarılı sonuç
    q_reject: Hatalı giriş
    """
    transitions = {}
    
    # q0: Birinci rakam (0-9)
    for digit in '0123456789':
        transitions[('q0', digit)] = ('q1', 'R')
    
    # q0: Hata - harf veya diğer
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        transitions[('q0', letter)] = ('q_reject', 'R')
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        transitions[('q0', letter)] = ('q_reject', 'R')
    transitions[('q0', '_')] = ('q_reject', 'R')
    
    # q1: İkinci rakam (0-9)
    for digit in '0123456789':
        transitions[('q1', digit)] = ('q2', 'R')
    
    # q1: Hata - harf veya diğer
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        transitions[('q1', letter)] = ('q_reject', 'R')
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        transitions[('q1', letter)] = ('q_reject', 'R')
    transitions[('q1', '_')] = ('q_reject', 'R')
    
    # q2: Birinci harf (A-Z, büyük harf)
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        transitions[('q2', letter)] = ('q3', 'R')
    
    # q2: Hata - rakam veya küçük harf
    for digit in '0123456789':
        transitions[('q2', digit)] = ('q_reject', 'R')
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        transitions[('q2', letter)] = ('q_reject', 'R')
    transitions[('q2', '_')] = ('q_reject', 'R')
    
    # q3: İkinci harf (A-Z, büyük harf)
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        transitions[('q3', letter)] = ('q4', 'R')
    
    # q3: Hata - rakam veya küçük harf
    for digit in '0123456789':
        transitions[('q3', digit)] = ('q_reject', 'R')
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        transitions[('q3', letter)] = ('q_reject', 'R')
    transitions[('q3', '_')] = ('q_reject', 'R')
    
    # q4: Üçüncü rakam (0-9)
    for digit in '0123456789':
        transitions[('q4', digit)] = ('q5', 'R')
    
    # q4: Hata - harf veya diğer
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        transitions[('q4', letter)] = ('q_reject', 'R')
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        transitions[('q4', letter)] = ('q_reject', 'R')
    transitions[('q4', '_')] = ('q_reject', 'R')
    
    # q5: Dördüncü rakam (0-9)
    for digit in '0123456789':
        transitions[('q5', digit)] = ('q6', 'R')
    
    # q5: Hata - harf veya diğer
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        transitions[('q5', letter)] = ('q_reject', 'R')
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        transitions[('q5', letter)] = ('q_reject', 'R')
    transitions[('q5', '_')] = ('q_reject', 'R')
    
    # q6: Beşinci rakam (0-9)
    for digit in '0123456789':
        transitions[('q6', digit)] = ('q_accept', 'R')
    
    # q6: Hata - harf veya diğer
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        transitions[('q6', letter)] = ('q_reject', 'R')
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        transitions[('q6', letter)] = ('q_reject', 'R')
    transitions[('q6', '_')] = ('q_reject', 'R')
    
    # Fazladan karakter kontrolü - q_accept'ten sonra ne varsa hata
    for char in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        transitions[('q_accept', char)] = ('q_reject', 'R')
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        transitions[('q_accept', letter)] = ('q_reject', 'R')
    transitions[('q_accept', '_')] = ('q_accept', 'R')  # Boş sembol kabul
    
    return transitions

def main():
    transitions = build_transitions()
    
    print("\n" + "="*60)
    print("  ARAÇ PLAKA FORMATINDA TANIYCICI - TURING MAKİNESİ")
    print("  Format: NNLLNNN (N=Rakam, L=Büyük Harf)")
    print("="*60)
    
    try:
        plaka = input("\nPlaka bilgisini girin (örn: 55AB123): ").strip()
        
        if not plaka:
            print("HATA: Boş giriş!")
            return
        
        # Kontrol: sadece alfanumerik karakterler ve doğru uzunluk
        if not all(c in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' for c in plaka):
            print("HATA: Geçersiz karakterler!")
            return
        
        print(f"\nBaşlangıç Bandı: {plaka}")
        
        ans = input("Adım adım görmek ister misiniz? (E/H): ").strip().upper()
        animate = ans == 'E'
        
        tm = TuringMachineRecognizer(plaka, transitions)
        tm.run(animate=animate, delay=0.02)
        
        print("\n" + "="*60)
        if tm.state == tm.accept_state:
            print(f"Girdi: {plaka}")
            print("SONUÇ: KABUL ✓")
        else:
            print(f"Girdi: {plaka}")
            print("SONUÇ: RED ✗")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\nİşlem iptal edildi.")

if __name__ == "__main__":
    main()
