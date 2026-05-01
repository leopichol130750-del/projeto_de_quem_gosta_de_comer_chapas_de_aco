import bcrypt

senha = b"abc"
hash = bcrypt.hashpw(senha, bcrypt.gensalt())

print(hash)