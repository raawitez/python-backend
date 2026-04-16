def add_user():
    print("enter user name: ",end="")
    name = input()
    if name not in details:
        print("enter Email address: ",end="")
        email = input()
        print("enter Age: ",end="")
        try:
            age = int(input())
        except ValueError:
            print("Invalid age")
            return
        details[name] = {"email" : email,
                        "age" : age}
        print("User added")
    else:
        print("User already exists")

def view_user():
    if not details:
        print("No user found")
        return
    for x,y in details.items():
        print('Details of User "',x,'" :')
        for i in y:
            print(i,": ",y[i])
        print("")

def update_user(user_name):
    if user_name not in details:
        print("User name not found")
    else:
        while 1:
            print("select an option to continue: ")
            print("1. update user name")
            print("2. update email id")
            print("3. update age")
            print("type any key to exit")
            print("Enter an option: ",end="")
            opt = input()
            if opt=="1":
                new_name = input("Enter new username: ")
                if new_name in details:
                    print("User already exists")
                else:
                    if user_name in details:
                        details[new_name] = details.pop(user_name)
                        user_name = new_name
                        print("new user name updated")
                    else:
                        print("enter a valid user name")
            
            elif opt == "2":
                print("Enter new email address: ",end="")
                new_email = input()
                details[user_name]["email"] = new_email
                print("Email is updated") 
            elif opt == "3":
                print("Enter new age: ",end="")
                try:
                    new_age = int(input())
                except ValueError:
                    print("Invalid age")
                    continue
                details[user_name]["age"] = new_age
                print("Age is updated")
            else:
                print("exiting update function...")
                print("")
                break
def delete_user(user_name):
    if user_name not in details:
        print("enter a valid user name !!!")
    else:
        details.pop(user_name)
        print("user = ",user_name,"has been deleted")






details = {}
while 1:
    print("")
    print("Select a choice to proceed: ")
    print("1. Add user")
    print("2. View user")
    print("3. Update users")
    print("4. Delete user")
    print("5. Exit")
    print("")
    print("Enter your choice: ",end="")
    try:
        x = int(input())
    except ValueError:
        print("Invalid choice")
        continue

    if x==1:
        add_user()
    elif x==2:
        view_user()
    elif x==3:
        username = input("Enter the user name: ")
        update_user(username)
    elif x==4:
        username = input("Enter the user name: ")
        delete_user(username)
    elif x==5:
        print("exiting user manager....")
        print()
        break
    else:
        continue

    