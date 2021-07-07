from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os


class encryption:

    # saves key into a .pem file
    def save_key(self, pk, filename):
        pem = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(filename, 'wb') as pem_out:
            pem_out.write(pem)

    # loads key from a .pem file
    def load_key(self, user_name):
        if os.path.exists(f'{user_name}.pem'):
            with open(f'{user_name}.pem', 'rb') as pem_in:
                pemlines = pem_in.read()
            private_key = load_pem_private_key(pemlines, None, default_backend())
            return private_key
        else:
            print("Key load failed, file does not exist")
            return None

    # verifies a signature using the signers public key
    def verify_signarture(self, public_key, signature, message):
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print("[Failed Signature Verification] - ", e)
            return False

    # signs the username of the private keys owner
    def sign(self, private_key, message):
        return private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    # retrieves/creates a users private key
    def get_private_key(self, user_name):
        if os.path.exists(f'{user_name}.pem'):
            return self.load_key(f'{user_name}.pem')
        else:
            key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )

            self.save_key(key, user_name)
            return key

    # encrypts file content 
    def encrypt(public_key, file_content):
        return public_key.encrypt(
            file_content,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    #decrypts file content
    def decrypt(private_key, file_content):
        return private_key.decrypt(
            file_content,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
