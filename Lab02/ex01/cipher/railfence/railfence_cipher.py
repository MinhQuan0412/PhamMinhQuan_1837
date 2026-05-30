class RailFenceCipher:
    def __init__(self):
        pass

    def rail_fence_encrypt(self, plain_text, key):
        if key <= 1 or key >= len(plain_text):
            return plain_text

        rails = ['' for _ in range(key)]
        rail = 0
        direction = 1  # 1 = đi xuống, -1 = đi lên

        for char in plain_text:
            rails[rail] += char
            if rail == 0:
                direction = 1
            elif rail == key - 1:
                direction = -1
            rail += direction

        return ''.join(rails)

    def rail_fence_decrypt(self, cipher_text, key):
        if key <= 1 or key >= len(cipher_text):
            return cipher_text

        n = len(cipher_text)
        # Tính số ký tự trên mỗi rail
        pattern = []
        rail = 0
        direction = 1
        for i in range(n):
            pattern.append(rail)
            if rail == 0:
                direction = 1
            elif rail == key - 1:
                direction = -1
            rail += direction

        # Tính độ dài từng rail
        rail_lengths = [0] * key
        for r in pattern:
            rail_lengths[r] += 1

        # Tách cipher_text thành từng rail
        rails = []
        index = 0
        for length in rail_lengths:
            rails.append(list(cipher_text[index:index + length]))
            index += length

        # Đọc lại theo pattern ban đầu
        rail_indices = [0] * key
        result = ''
        for r in pattern:
            result += rails[r][rail_indices[r]]
            rail_indices[r] += 1

        return result
