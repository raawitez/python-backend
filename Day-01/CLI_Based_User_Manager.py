users = []
while 1:
    print("")
    print("Select a choice to proceed: ")
    print("1. Add user")
    print("2. Update user")
    print("3. View users")
    print("4. Delete user")
    print("5. Exit")
    print("")
    print("Enter your choice: ",end="")
    x = int(input())
    if x==1:
        print("Enter user name: ",end="")
        name = input()
        users.append(name)
        print("User added")
    elif x==2:
        print("Enter the name: ",end="")
        name = input()
        print("Enter the new user name: ",end="")
        if name not in users:
            print("User not found")
        else:
            newName = input()
            users[users.index(name)] = newName
            print("User name updated")
    elif x==3:
        print(users)
    elif x==4:
        print("Enter a user to be removed: ")
        name = input()
        if name not in users:
            print("User name not found")
        else:
            users.remove(name)
            print("User has been removed")
    elif x==5:
        print("Exiting the program")
        break
    else:
        print("enter a valid option")
    print("")
