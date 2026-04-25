import json

class exception_name(Exception):
    pass

def load_data():
    try:
        with open("data.json","r") as file:
            return json.load(file)
    except (FileNotFoundError , json.JSONDecodeError):
        return {'balance' : 0 , 'history' : []}
    
Database = load_data()

def save_data(database):
    with open("data.json" , "w") as file:
        json.dump(database , file)

def get_input(prompt):
    value = input(prompt).strip().lower()

    return value
def deposit(database):
    value = 0
    while True:
        value = get_number(float)
        if value == 'cancel':
            is_canceled = cancel('You are canceling the action')
            if is_canceled == True:
                return
        if value > 0 :
            break
        else:
            print("write a number bigest than 0: ")
        
    database['history'].append({'type' : 'deposit' , 'value' : value}) 
    database['balance'] += value 


def expenses_register(database):
    value = 0
    while True:
        value = get_number(float)
        if value == 'cancel':
            is_canceled = cancel('You are canceling the action')
            if is_canceled == True:
                return
        if value <= 0 :
            print("Value must be greater than 0: ")
        elif value > database['balance']:
            print('Not enough money')
        else:
            break 
    while True:
        category = get_input("type of expense or |cancel| to cancel: ")
        if category is None:
            print("Action canceled")
            return
        if not category.isalpha():
            print("Write the type valid: ")
        else:
            break

    database['history'].append({'type' : 'expense', 'value' : value , 'category' : category})
    database['balance'] -= value 
def delete_transaction(database):
    while True:
        try:
            index = get_number(int) 
            if index == 'cancel':
                is_canceled = cancel('You are canceling the action')
                if is_canceled == True:
                    return
            index = int(index)
            if 0 <= index < len(database['history']):
                break
            else:
                print("Invalid index ")
        except ValueError:
            print("Write a valid number")
            
            
       
    transaction = database['history'][index]
    wanna_cancel = cancel(f"Transaction : {transaction} Index : {index}") 
    if wanna_cancel == True:
        print(f"Transaction : {transaction} Index : {index} canceled")
        return
    transaction = database['history'].pop(index)
    if transaction  ['type'] == 'deposit':
        database['balance'] -= transaction['value']
    elif transaction['type'] == 'expense':
        database['balance'] += transaction['value']
    print(f"Transaction deleted: {transaction['type'].capitalize()}: {transaction['value']}")
def show_expense_search_type(database):
    
    while True:
        
            search_type = get_input("Write an expense type or |cancel| to cancel: ")
            if search_type == 'cancel':
                is_canceled = cancel('You are canceling the action')
                if is_canceled == True:
                    return
            if not search_type.isalpha():
                print("Digit a valid value")
                continue
            break
    total = 0
    founder = False
    for item in database['history']:
        
        if item['type'] == 'expense':
            if item['category'] == search_type:
                founder = True
                print(f"Expense : -{item['value']} | ({item['category']})")
                total += item['value']
    if not founder:
        print("type don't exist")
    else:
        print(f"Total : -{total}")
def show_Balance(database):
    print(f"Balance: {database['balance']}")
def show_History(database):
    if not database['history']:
        print("No transactions yet.")
        return
    for i, item in enumerate(database['history']):

        if item['type'] == 'deposit':
            print(f"{i} - [Deposit]: +{item['value']}")
        elif item['type'] == 'expense':
            print(f"{i} - [Expense]: -{item['value']} ({item['category']})")
def show_summary(database):
    if not database['history']:
        print(" Total Deposit : 0 , Total Expensive: 0\
 , Balance : 0")
        return
    total_deposit = 0
    total_expense = 0
    
    for item in database['history']:
        
        if item['type'] == 'deposit':
            total_deposit += item['value']
        if item['type'] == 'expense':
            total_expense += item['value']
            
    print(f"Total Deposit : {total_deposit} , Total Expense: {total_expense}\
 , Balance : {database['balance']}")
def get_number(t : type):
    while True:
        try:
            value = input('Write a number or |cancel| to cancel: ').strip()
            if value == 'cancel':
                return value
            else:
                return t(value)
        except ValueError:
            print("Invalid Number")
           
def cancel(prompt):
    print(prompt)
    while True:
        confirm_cancel = input("Confirm cancel? |y| or |n|").strip().lower()
        if confirm_cancel == 'y':
            return True  
        elif confirm_cancel == 'n':
            return False
        elif confirm_cancel not in ['y' , 'n']:
            print('Invalid option')
            continue
        
def controller(action  , database):
    actions = {
        '1' : deposit, 
        '2' : expenses_register,
        '3' : show_History ,
        '4' : show_Balance ,
        '5': show_summary ,
        '6': show_expense_search_type ,
        '7' : delete_transaction
    }
    actions[action](database)

def main():
    while True:
        action = input("Write 1 for deposit , 2 for register expensive,\
 3 for show history  or 4 for show balance or 5 for show summary or 6 to show expenses for type or 7 to delete transaction or 8 to exit: ")
        if action == '8':
            save_data(Database)
            break
        else:
            if action in ['1' , '2' , '3' , '4' , '5', '6' , '7']:

                controller(action , Database)

            else:
                print("Invalid action number write again: ")
 



if __name__  == '__main__':
    main()