log_parser = {"INFO" : 0,
              "ERROR" : 0,
              "WARNING" : 0
              }
errors = []
with open("log.txt") as f:
    for each_line in f:
        if "ERROR" in each_line:
            errors.append(each_line[5:].strip())
        for word in log_parser:
            if word in each_line:
                log_parser[word] = log_parser[word]+1

for i in log_parser:
    print(i+":",log_parser[i])
print()

print("Error logs:")
for i in errors:
    print("-",i)
print()