import random
import csv
import random
from datetime import datetime, timedelta

# Sample Data for Names
names = ["Jose", "Juan", "Alberto", "Alan", "Carlos", "Berto", "Bebe", "Paulo", "Justo", "Kali", "Jessica", "Julia", "Marco", "Peter", "Panoca"]
last_name = ["Cabra", "Aldama", "Jackson", "Johnson", "Hayes", "Payaso", "Lopez", "Obrador", "Karlee", "Redick", "Maccain", "Macdonalds", "King", "Davis"]


# Sample names and last names for users
names = ["Alice", "Bob", "Charlie", "David", "Eve"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
industries = ["Finance", "Retail", "Tech", "Healthcare"]
currencies = ["USD", "EUR", "GBP", "JPY"]
devices = ["Mobile", "Laptop", "Tablet"]
os_types = ["Android", "iOS", "Windows", "MacOS"]
merchant_categories = ["Restaurant", "Clothing", "Electronics", "Grocery"]

# Helper function to generate a random date
def random_date(start_year=2000, end_year=2025):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# Function to save objects to CSV
def save_to_csv(filename, data, fieldnames):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Generate random company
def generate_company(company_id):
    return {
        "companyID": "C:"+str(company_id),
        "name": f"Company{company_id}",
        "industry": random.choice(industries),
        "location": random.choice(["New York", "Los Angeles", "San Francisco", "Chicago"]),
        "taxID": "TAX" + str(random.randint(10000, 99999)),
        "size": random.randint(10, 10000)
    }

# Generate random transaction
def generate_transaction(transaction_id):
    return {
        "transactionID": "T:"+str(transaction_id),
        "amount": round(random.uniform(10.0, 5000.0), 2),
        "timestamp": random_date().strftime("%Y-%m-%dT%H:%M:%S"),
        "device": f"D:{random.randint(1, num_records)}",
        "currency": random.choice(currencies),
        "location": random.choice(["Chicago", "NYC", "LA", "Miami"])
    }

# Generate random user
def generate_user(user_id):
    return {
        "userID": "USR:"+str(user_id),
        "name": random.choice(names),
        "lastname": random.choice(last_names),
        "email": f"user{user_id}@example.com",
        "phone": f"+1-{random.randint(1000000000, 9999999999)}",
        "country": "USA",
        "birthdate": random_date(1950, 2005).strftime("%Y-%m-%d")
    }

# Generate random bank
def generate_bank(bank_id):
    return {
        "bankID": "B:"+str(bank_id),
        "name": random.choice(["BANCO LA USA", "BANKO LE UK", "BANKS IL Germany", "FRANCE TOUR DE BANK"]) ,
        "location": random.choice(["USA", "UK", "Germany", "France"]),
        "code": "SWIFT" + str(random.randint(1000, 9999)),
        "branchCount": random.randint(1, 500),
        "founded": random.randint(1800, 2022)
    }

# Generate random merchant
def generate_merchant(merchant_id):
    return {
        "merchantID": "M"+str(merchant_id),
        "name": f"Merchant{merchant_id}",
        "category": random.choice(merchant_categories),
        "location": random.choice(["New York", "Los Angeles", "San Francisco", "Chicago"]),
        "country": random.choice(["USA", "UK", "Germany", "France"]) 
    }

# Generate random account
def generate_account(account_id):
    return {
        "accountID": "ACC:"+str(account_id),
        "type": random.choice(["Personal", "Corporate"]),
        "balance": round(random.uniform(1000.0, 50000.0), 2),
        "limit": round(random.uniform(500.0, 10000.0), 2),
        "status": random.choice(["Active", "Inactive", "Frozen"]),
        "created": random_date(2000, 2022).strftime("%Y-%m-%d")
    }

# Generate random ATM
def generate_atm(atm_id):
    return {
        "atmID": "A"+str(atm_id),
        "location": random.choice(["Downtown", "Suburb", "Mall", "Airport"]),
        "status": random.choice(["Active", "Inactive", "Maintenance"]),
        "provider": f"Provider{random.randint(1, 5)}",
        "Balance": round(random.uniform(0.0, 10000.0), 2)
    }

# Generate random card
def generate_card(card_id):
    return {
        "cardID": "C"+str(card_id),
        "type": random.choice(["Credit", "Debit"]),
        "issuer": f"B{random.randint(1, num_records)}",
        "limit": round(random.uniform(1000.0, 20000.0), 2),
        "status": random.choice(["Active", "Blocked", "Expired"]),
        "expiryDate": random_date(2025, 2035).strftime("%Y-%m")
    }

# Generate random device
def generate_device(device_id):
    return {
        "deviceID": "D:"+str(device_id),
        "type": random.choice(devices),
        "os": random.choice(os_types),
        "ip": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
        "location": random.choice(["Chicago", "NYC", "LA", "Miami"])
    }


def write_relationships_to_csv(relationships, filename):
    """Writes relationships to a specified CSV file."""
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=relationships[0].keys())
        writer.writeheader()
        writer.writerows(relationships)


def generate_relationships(users, accounts, banks, companies, devices):
    contador = 0
    for account in accounts:
        
        user = users[contador]
        contador = contador + 1
        same =  random_date(2015, 2023).strftime("%Y-%m-%d")
        # User owns an account
        owns_relationship = {
            "startNode": user["userID"],
            "endNode": account["accountID"],
            "relationship": "OWNS",
            "since":same,
            "account_type": random.choice(["Personal","Savings","Current"]),
            "created": random_date(2015, 2023).strftime("%Y-%m-%d")
            
        }
        write_relationships_to_csv([owns_relationship], 'Fill_Data/csves/owns_relation.csv')
        
        
        user = random.choice(users)
        # User deposits money
        deposit_amount = round(random.uniform(100, 5000), 2)
        deposits_relationship = {
            "startNode": user["userID"],
            "endNode": account["accountID"],
            "relationship": "DEPOSITS",
            "timestamp": random_date(2020, 2025).strftime("%Y-%m-%dT%H:%M:%S"),
            "amount": deposit_amount,
            "origin": random.choice(["Cash Deposits","Dividends","Tax Returns"])
        }
        write_relationships_to_csv([deposits_relationship], 'Fill_Data/csves/deposits_relation.csv')
 
        # User withdraws money
        withdrawal_amount = round(random.uniform(100, 2000), 2)
        withdraws_relationship = {
            "startNode": user["userID"],
            "endNode": account["accountID"],
            "relationship": "WITHDRAWS",
            "timestamp": random_date(2020, 2025).strftime("%Y-%m-%dT%H:%M:%S"),
            "amount": withdrawal_amount,
            "method":random.choice(["ATM","Bank","Phone"])
        }
        write_relationships_to_csv([withdraws_relationship], 'Fill_Data/csves/withdraws_relation.csv')

    for account in accounts:
        bank = random.choice(banks)

        # Bank has an account
        bank_relationship = {
            "startNode": bank["bankID"],
            "endNode": account["accountID"],
            "relationship": "HAS_ACCOUNT",
            "opened": account["created"],
            "branch": "Main Office",
            "status":   random.choice(["Active","Active","Inactive"])
        }
        write_relationships_to_csv([bank_relationship], 'Fill_Data/csves/has_accs_relation.csv')
        
    contador = 0
    for account in accounts:
        transaction = transactions[contador]

        # Bank has an account
        tranmakes = {
            "startNode": account["accountID"],
            "endNode": transaction["transactionID"],
            "relationship": "MAKES",
            "time": random_date(2022, 2023).strftime("%Y-%m-%d"),
            "amount": transaction["amount"],
            "from":account["accountID"],
            "to":   transaction["transactionID"]
        }
        write_relationships_to_csv([tranmakes], 'Fill_Data/csves/tranmakes.csv')
        contador = contador + 1

    for user in users:
        company = random.choice(companies)
        # Company employs user
        company_relationship = {
            "startNode": company["companyID"],
            "endNode": user["userID"],
            "relationship": "EMPLOYS",
            "since": random_date(2015, 2023).strftime("%Y-%m-%d"),
            "position":  random.choice(["Manager", "Licenciado", "Entrepreneur", "Engineer"]),
            "department":  random.choice(["N/A", "IT", "Sales", "HR"])
        }
        write_relationships_to_csv([company_relationship], 'Fill_Data/csves/company_relationships.csv')


    for device in devices:
        user = random.choice(users)
        device_relationship = {
            "startNode": user["userID"],
            "endNode": device["deviceID"],
            "relationship": "USES_DEVICE",
            "timestamp": random_date(2022, 2025).strftime("%Y-%m-%dT%H:%M:%S"),
            "location": device["location"],
            "appUsed": random.choice(["Banking App", "Phone Wallet", "other"])
        }
        write_relationships_to_csv([device_relationship], 'Fill_Data/csves/device_relationships.csv')
        
        
    for transaction in transactions:
        merchant = random.choice(merchants)
        purchased_at= { 
        "startNode": transaction["transactionID"],
        "endNode": merchant["merchantID"], 
        "relationship": "PURCHASED_AT", 
        "time":random_date(2020, 2025).strftime("%Y-%m-%dT%H:%M:%S"), 
        "appUsed": random.choice(["Banking App", "Phone Wallet", "other"]),
        "reason": random.choice(["In need of product", "payment ", "sale", "fee"])
        } 
        write_relationships_to_csv([purchased_at], 'Fill_Data/csves/purchased_at.csv')
        

        
    for user in users:
        card = random.choice(cards)
        uses_card= { 
            "startNode": user["userID"], 
            "endNode": card["cardID"], 
            "relationship": "USES_CARD", 
            "created":random_date(2020, 2025).strftime("%Y-%m-%dT%H:%M:%S"), 
            "type": random.choice(["credit", "Debit", "other"]),
            "Restrictions": random.choice(["N/A", "NO LIMIT", "PAY BILLS"])
            }
        write_relationships_to_csv([uses_card], 'Fill_Data/csves/uses_card.csv')
        

    contador = 0
    for transaction in transactions:
        bank = banks[contador]
        auth_relationship = {
            "startNode": bank["bankID"],
            "endNode": transaction["transactionID"],
            "relationship": "AUTHORIZES",
            "authCode": f"AUTH{random.randint(100,999)}",
            "time": random_date(2020, 2025).strftime("%Y-%m-%dT%H:%M:%S"),
            "status": random.choice(["In Process", "Fail", "Success"])
        }
        contador = contador + 1
        write_relationships_to_csv([auth_relationship], 'Fill_Data/csves/auth_transactions.csv')



    for _ in range(len(accounts) // 2):
        acc1, acc2 = random.sample(accounts, 2)
        linked_relationship = {
            "startNode": acc1["accountID"],
            "endNode": acc2["accountID"],
            "relationship": "LINKED_TO",
            "date": random_date(2020, 2025).strftime("%Y-%m-%d"),
            "linkType": "Joint Account",
            "reason": "Shared household expenses"
        }
        write_relationships_to_csv([linked_relationship], 'Fill_Data/csves/linked_accounts.csv')

    for _ in range(len(users) // 3):
        referrer, referee = random.sample(users, 2)
        refers_relationship = {
            "startNode": referrer["userID"],
            "endNode": referee["userID"],
            "relationship": "REFERS",
            "referralDate": random_date(2022, 2025).strftime("%Y-%m-%d"),
            "referralCode": f"REF{random.randint(10000,99999)}",
            "rewardAmount": round(random.uniform(10, 100), 2)
        }
        write_relationships_to_csv([refers_relationship], 'Fill_Data/csves/refers_relation.csv')

    for account in accounts:
        company = random.choice(companies)
        managed_relationship = {
            "startNode": account["accountID"],
            "endNode": company["companyID"],
            "relationship": "MANAGED_BY",
            "managementStart": random_date(2020, 2025).strftime("%Y-%m-%d"),
            "accountPurpose": "Corporate Expenses",
            "auditRating": random.choice(["A", "B", "C"])
        }
        write_relationships_to_csv([managed_relationship], 'Fill_Data/csves/managed_accounts.csv')

    for account in accounts:
        atm = random.choice(atms)
        Withdraws_AT = {
            "startNode": account["accountID"],
            "endNode": atm["atmID"],
            "relationship": "Withdraws-AT",
            "time": random_date(2020, 2025).strftime("%Y-%m-%d"),
            "amount": round(random.uniform(0.0, 1000.0), 2),
            "AT":  account["accountID"]
        }
        write_relationships_to_csv([Withdraws_AT], 'Fill_Data/csves/Withdraws_AT.csv')



# Generate random data and save to CSV
num_records = 600  # Number of records per class

companies = [generate_company(i) for i in range(1, num_records + 1)]
transactions = [generate_transaction(i) for i in range(1, num_records + 1)]
users = [generate_user(i) for i in range(1, num_records + 1)]
banks = [generate_bank(i) for i in range(1, num_records + 1)]
merchants = [generate_merchant(i) for i in range(1, num_records + 1)]
accounts = [generate_account(i) for i in range(1, num_records + 1)]
atms = [generate_atm(i) for i in range(1, num_records + 1)]
cards = [generate_card(i) for i in range(1, num_records + 1)]
devices = [generate_device(i) for i in range(1, num_records + 1)]

save_to_csv("Fill_Data/csves/companies.csv", companies, companies[0].keys())
save_to_csv("Fill_Data/csves/transactions.csv", transactions, transactions[0].keys())
save_to_csv("Fill_Data/csves/users.csv", users, users[0].keys())
save_to_csv("Fill_Data/csves/banks.csv", banks, banks[0].keys())
save_to_csv("Fill_Data/csves/merchants.csv", merchants, merchants[0].keys())
save_to_csv("Fill_Data/csves/accounts.csv", accounts, accounts[0].keys())
save_to_csv("Fill_Data/csves/atms.csv", atms, atms[0].keys())
save_to_csv("Fill_Data/csves/cards.csv", cards, cards[0].keys())
save_to_csv("Fill_Data/csves/devices.csv", devices, devices[0].keys())

# Call the function to generate relationships and write to CSV
generate_relationships(users, accounts, banks, companies, devices)

print("CSV files generated successfully!")




# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/accounts.csv' AS row
# MERGE (a:Account {accountID: toString(row.accountID)})
# SET a.type = row.type,
#     a.balance = toFloat(row.balance),
#     a.limit = toFloat(row.limit),
#     a.status = row.status,
#     a.created = date(row.created);


# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/atms.csv' AS row
# MERGE (a:atm {atmID: toString(row.atmID)})
# SET a.location = row.location,
#     a.status = toString(row.status),
#     a.provider = toString(row.provider),
#     a.Balance = toFloat(row.Balance);


# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/banks.csv' AS row
# MERGE (a:bank {bankID: toString(row.bankID)})
# SET a.location = row.location,
#     a.name = row.name,
#     a.code = row.code,
#     a.branchCount = toFloat(row.branchCount),
#     a.founded = date(row.founded);




# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/cards.csv' AS row
# MERGE (a:cards {cardID: toString(row.cardID)})
# SET a.type = row.type,
#     a.issuer = row.issuer,
#     a.limit = toFloat(row.limit),
#     a.status = row.status,
#     a.expiryDate = date(row.expiryDate);



# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/companies.csv' AS row
# MERGE (a:company {companyID: toString(row.companyID)})
# SET a.name = row.name,
#     a.industry = row.industry,
#     a.size = toFloat(row.size),
#     a.location = row.location,
#     a.taxID = row.taxID;


# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/devices.csv' AS row
# MERGE (a:device {deviceID: toString(row.deviceID)})
# SET a.type = row.type,
#     a.os = row.os,
#     a.ip = row.ip,
#     a.location = row.location;


# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/merchants.csv' AS row
# MERGE (a:merchant {merchanID: toString(row.merchantID)})
# SET a.name = row.name,
#     a.category = row.category,
#     a.location = row.location,
#     a.country = row.country;


# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/transactions.csv' AS row
# MERGE (a:transaction {transactionID: toString(row.transactionID)})
# SET a.amount = row.amount,
#     a.timestamp = row.timestamp,
#     a.device = row.device,
#     a.currency = row.currency,
#     a.location = row.location;



# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/users.csv' AS row
# MERGE (a:user {userID: toString(row.userID)})
# SET a.name = row.name,
#     a.lastname = row.lastname,
#     a.email = row.email,
#     a.phone = row.phone,
#     a.country = row.country,
#     a.birthdate = date(row.birthdate);




#RELACIONES

# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/auth_transactions.csv' AS row
# MATCH (c:bank{bankID:row.startNode})
# MATCH (usr:transaction{ transactionID:row.endNode})
# MERGE (c)-[r:AUTHORIZES{authCode:row.authCode, time:row.time, status:row.status}]->(usr)
# return c, r ,usr


# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/company_relationships.csv' AS row
# MATCH (c:company{companyID:row.startNode})
# MATCH (usr:user{ userID:row.endNode})
# MERGE (c)-[r:Employs{since:row.since, position:row.position}]->(usr)
# return c, r ,usr



# Si se puede

# WITHDRAWS
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/withdraws_relation.csv' AS row
# MATCH (c:user{userID:row.startNode})
# MATCH (usr:Account{ accountID:row.endNode})
# MERGE (usr)-[r:WITHDRAWS{timestamp:row.timestamp, method:row.method ,amount:row.amount}]->(c)
# return c, r ,usr



# OWNS
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/owns_relation.csv' AS row
# MATCH (c:user{userID:row.startNode})
# MATCH (usr:Account{ accountID:row.endNode})
# MERGE (c)-[r:OWNS{since:row.since, account_type:row.account_type, created:row.created}]->(usr)
# return c, r ,usr


# HAS
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/has_accs_relation.csv' AS row
# MATCH (c:bank{bankID:row.startNode})
# MATCH (usr:Account{ accountID:row.endNode})
# MERGE (c)-[r:HAS{opened:row.opened, branch:row.branch, status:row.status}]->(usr)
# return c, r ,usr



# Deposit
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/deposits_relation.csv' AS row
# MATCH (c:user{userID:row.startNode})
# MATCH (usr:Account{ accountID:row.endNode})
# MERGE (c)-[r:DEPOSITS{timestamp:row.timestamp, amount:row.amount, origin:row.origin}]->(usr)
# return c, r ,usr



# Linked to 
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/linked_accounts.csv' AS row
# MATCH (c:Account{accountID:row.startNode})
# MATCH (usr:Account{ accountID:row.endNode})
# MERGE (c)-[r:LINKED_TO{date:row.date, linkType:row.linkType, reason:row.reason}]->(usr)
# return c, r ,usr


# employs
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/company_relationships.csv' AS row
# MATCH (c:company{companyID:row.startNode})
# MATCH (usr:user{ userID:row.endNode})
# MERGE (c)-[r:EMPLOYS{since:row.since, position:row.position, department:row.department}]->(usr)
# return c, r ,usr


# authorizes 
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/auth_transactions.csv' AS row
# MATCH (c:bank{bankID:row.startNode})
# MATCH (usr:transaction{ transactionID:row.endNode})
# MERGE (c)-[r:AUTHORIZES{authCode:row.authCode, approvalTime:row.approvalTime, riskScore:row.riskScore}]->(usr)
# return c, r ,usr


# refers
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/refers_relation.csv' AS row
# MATCH (c:user{userID:row.startNode})
# MATCH (usr:user{ userID:row.endNode})
# MERGE (c)-[r:REFERS{referralDate:row.referralDate, referralCode:row.referralCode, rewardAmount:row.rewardAmount}]->(usr)
# return c, r ,usr

# managed by
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/managed_accounts.csv' AS row
# MATCH (c:Account{accountID:row.startNode})
# MATCH (usr:company{ companyID:row.endNode})
# MERGE (usr)-[r:MANAGED_BY{managementStart:row.managementStart, accountPurpose:row.accountPurpose, auditRating:row.auditRating}]->(c)
# return c, r ,usr



# uses
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/device_relationships.csv' AS row
# MATCH (c:user{userID:row.startNode})
# MATCH (usr:device{ deviceID:row.endNode})
# MERGE (c)-[r:USES_DEVICE{timestamp:row.timestamp, location:row.location, appUsed:row.appUsed}]->(usr)
# return c, r ,usr


# Withdraws_at
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/device_relationships.csv' AS row
# MATCH (c:Account{accountID:row.startNode})
# MATCH (usr:atm{ atmID:row.endNode})
# MERGE (c)-[r:Withdraws_AT{time:row.time, amount:row.amount, AT:row.AT}]->(usr)
# return c, r ,usr


# Usescard
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/uses_card.csv' AS row
# MATCH (c:user{userID:row.startNode})
# MATCH (usr:cards{ cardID:row.endNode})
# MERGE (c)-[r:USES_CARD{created:row.created, type:row.type, Restrictions:row.Restrictions}]->(usr)
# return c, r ,usr


# Purchased at
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/purchased_at.csv' AS row
# MATCH (c:transaction{transactionID:row.startNode})
# MATCH (usr:merchant{ merchanID:row.endNode})
# MERGE (c)-[r:PURCHASED_AT{time:row.time, apppused:row.appUsed, reason:row.reason}]->(usr)
# return c, r ,usr


# tranmakes
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/tranmakes.csv' AS row
# MATCH (c:Account{accountID:row.startNode})
# MATCH (usr:transaction{ transactionID:row.endNode})
# MERGE (c)-[r:MAKES{time:row.time, amount:row.amount, from:row.from, to:row.to}]->(usr)
# return c, r ,usr


