import bcrypt

txt = 12345

# Encriptar txt
pwd = txt.encode('utf-8')
salt = bcrypt.gensalt()
encript = bcrypt.hashpw(pwd, salt)

# Desencriptar txt
if bcrypt.checkpw(txt, pwd):
    print("La contraseña es correcta")