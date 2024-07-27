import bcrypt

password = "devnydv"
userpass ="devnyd"
enpw = bcrypt.hashpw(password.encode("utf-16"), bcrypt.gensalt())


print(enpw)

result = bcrypt.checkpw(userpass.encode("utf-16"), enpw)
print(result)