log_parser = {"INFO" : 0,
              "ERROR" : 0,
              "WARNING" : 0
              }
errors = []
try:
    with open("log.txt") as f:
        for x in f:
            x=x.strip()
            if not x:
                continue
            each_line = x.split()
            log_type = each_line[0]
            if log_type in log_parser:
                log_parser[log_type]+=1
            if log_type == "ERROR":
                mssg = " ".join(each_line[1:])
                errors.append(mssg)

    for i in log_parser:
        print(i+":",log_parser[i])
    print()

    print("Error logs:")
    for i in errors:
        print("-",i)
    print()

except FileNotFoundError:
    print("File Not found")