import json
import  file

'''
Seleciona a conta que será depositado o valor.
'''
def deposit(account_destiny, value):
    position, account = find_account(account_destiny)
    
    if(account):
        value = account.get("balance") + value

        accounts = file.read("accounts.json")
        
        accounts[position]["balance"] = value
    
        file.write( accounts, "accounts.json")
        return 1
    return 0   

'''
Seleciona a conta que será retirado o valor para transferência.
'''
def transfer_value(account_origin, value):
    position, account = find_account(account_origin)
    
    if(account):
        if(value > 0):
            
            value = account.get("balance") - value

            accounts = file.read("accounts.json")
            
            accounts[position]["balance"] = value
        
            file.write( accounts, "accounts.json")
            return 1   
    return 0



'''
Encontra uma conta específica
'''
def find_account(name_account):
    accounts = file.read("accounts.json")
      
    for i in range(len(accounts)):
        if(name_account == accounts[i].get("name")):
            return i, accounts[i]
        
    return 0
