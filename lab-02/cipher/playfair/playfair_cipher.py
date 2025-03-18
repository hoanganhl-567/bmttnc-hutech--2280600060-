class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I").upper()
        key_set = set(key)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Loại bỏ chữ J
        remaining_letters = [letter for letter in alphabet if letter not in key_set]
        matrix = list(key) + remaining_letters
        playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return None, None

    def playfair_encrypt(self, plain_text, matrix):
        plain_text = plain_text.replace("J", "I").upper()
        encrypted_text = ""
        
        i = 0
        while i < len(plain_text):
            pair = plain_text[i:i+2]
            if len(pair) == 1 or pair[0] == pair[1]:
                pair = pair[0] + "X"  # Chèn X nếu trùng hoặc thiếu chữ thứ 2
                i += 1
            else:
                i += 2

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        
        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        decrypted_text = ""
        
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]
        
        # Loại bỏ 'X' dư thừa
        banro = ""
        i = 0
        while i < len(decrypted_text):
            if i < len(decrypted_text) - 2 and decrypted_text[i] == decrypted_text[i + 2] and decrypted_text[i + 1] == "X":
                banro += decrypted_text[i]
                i += 2  # Bỏ qua X thừa
            else:
                banro += decrypted_text[i]
                i += 1

        return banro
