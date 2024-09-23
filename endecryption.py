import Crypto.Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import base64

class EncryptionEngine:
    def __init__(self, password: str) -> None:        
        self.PASSWORD = password.encode('utf-8')
        self.SALT = b"\x00\xf4{\xa5\xa4\xab\x95\xe1\xef\x81\xc5\xc8\xc8\xbd@\x7f\xc5\x18vl~'z\x17\xed\r\x17\x93p\x9b\xd2\x19\x1cI\xbe$R\xb1\x02\x1a\x19\xcf\xb2a\x91\x8d\xa9\xbb\t\x9e*\xb7\xbe$\xe7rt\x0f\xe9\xc3\xa7\xbb\x11#"
        self.KEY = PBKDF2(self.PASSWORD, self.SALT, dkLen=32)
    
    def encrypt(self, text: str) -> str:
        cipher = AES.new(self.KEY, AES.MODE_CBC)
        padded_text = pad(text.encode('utf-8'), AES.block_size)
        encrypted = cipher.encrypt(padded_text)
        return base64.b64encode(cipher.iv + encrypted).decode('utf-8')
    
    def decrypt(self, encrypted_text: str) -> str:
        encrypted_data = base64.b64decode(encrypted_text)
        iv = encrypted_data[:AES.block_size]
        ciphertext = encrypted_data[AES.block_size:]
        cipher = AES.new(self.KEY, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        return unpad(decrypted_padded, AES.block_size).decode('utf-8')

if __name__ == "__main__":
    engine = EncryptionEngine("yes")
    encrypted = engine.encrypt("Hello, World!")
    print("Encrypted:", encrypted)
    decrypted = engine.decrypt(encrypted)
    print("Decrypted:", decrypted)
