import subprocess

useless_cat_call = subprocess.Popen(["ls"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
output, errors = useless_cat_call.communicate(input="")
useless_cat_call.wait()
print(output)
print(errors)