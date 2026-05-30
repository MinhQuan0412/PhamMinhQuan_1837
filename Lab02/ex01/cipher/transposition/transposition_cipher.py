class TranspositionCipher:
    def __init__(self):
        pass
        
    def encrypt(self, text, key):
        encrypted_text = ''
        for col in range(key):
            pointer = col
            while pointer < len(text):
                encrypted_text += text[pointer]
                pointer += key
        return encrypted_text

    def decrypt(self, text, key):
        num_cols = key
        num_rows = len(text) // key
        remainder = len(text) % key
        # số cột có thêm 1 ký tự ở hàng cuối
        longer_cols = remainder

        decrypted_text = []
        index = 0
        # tính độ dài từng cột
        col_lengths = []
        for col in range(num_cols):
            if col < longer_cols:
                col_lengths.append(num_rows + 1)
            else:
                col_lengths.append(num_rows)

        # tách cipher_text thành từng cột
        cols = []
        for length in col_lengths:
            cols.append(list(text[index:index + length]))
            index += length

        # đọc theo hàng
        result = ''
        for row in range(num_rows + (1 if remainder else 0)):
            for col in range(num_cols):
                if row < len(cols[col]):
                    result += cols[col][row]
        return result