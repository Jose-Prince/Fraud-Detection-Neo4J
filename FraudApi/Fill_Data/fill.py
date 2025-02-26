import random
import csv

# Sample Data for Names
names = ["Jose", "Juan", "Alberto", "Alan", "Carlos", "Berto", "Bebe", "Paulo", "Justo", "Kali", "Jessica", "Julia", "Marco", "Peter", "Panoca"]
last_name = ["Cabra", "Aldama", "Jackson", "Johnson", "Hayes", "Payaso", "Lopez", "Obrador", "Karlee", "Redick", "Maccain", "Macdonalds", "King", "Davis"]

# Class Definitions
class company:
    def __init__(self, companyID, name, industry, location, taxID, size):
        self.companyID = companyID
        self.name = name
        self.industry = industry
        self.location = location
        self.taxId = taxID
        self.size = size

class transaction:
    def __init__(self, transactionid, amount, timestamp, device, currency, location):
        self.transactionID = transactionid
        self.amount = amount
        self.timestamp = timestamp
        self.device = device
        self.currency = currency
        self.location = location

class atm:
    def __init__(self, atmid, bankid, location, status, provider):
        self.atmID = atmid
        self.bankID = bankid
        self.location = location
        self.status = status
        self.provider = provider

class bank:
    def __init__(self, bankid, location, code, branchCount, founded):
        self.bankID = bankid
        self.name = bankid
        self.country = location
        self.swiftCode = code
        self.branchCount = branchCount
        self.founded = founded

class account:
    def __init__(self, accountid, typo, balance, limit, status, created):
        self.accountid = accountid
        self.typo = typo
        self.balance = balance
        self.limit = limit
        self.status = status
        self.created = created

class user:
    def __init__(self, userid, name, lastname, email, phone, country, birthdate):
        self.userID = userid
        self.name = name
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.country = country
        self.birthDate = birthdate

class merchant:
    def __init__(self, merchantid, name, category, location, country):
        self.merchantID = merchantid
        self.name = name
        self.category = category
        self.location = location
        self.country = country

class card:
    def __init__(self, cardid, tipo, issuer, limit, status, expiryDate):
        self.cardID = cardid
        self.type = tipo
        self.issuer = issuer
        self.limit = limit
        self.status = status
        self.expiryDate = expiryDate

class device:
    def __init__(self, deviceid, tipo, os, ip, location):
        self.deviceID = deviceid
        self.tipo = tipo
        self.os = os
        self.ip = ip
        self.location = location

# Helper functions to generate random data for each class
def generate_transaction(transaction_id):
    return transaction(
        transactionid=transaction_id,
        amount=random.uniform(10.0, 1000.0),  # Floating point amount
        timestamp="2025-02-18T14:30:00",
        device="D" + str(random.randint(100, 999)),
        currency="USD",
        location=random.choice(["Chicago", "NYC", "LA", "Miami"])
    )

def generate_account(account_id):
    return account(
        accountid=account_id,
        typo=random.choice(["Personal", "Corporate"]),
        balance=random.uniform(1000.0, 10000.0),  # Floating point balance
        limit=random.uniform(500.0, 5000.0),  # Floating point limit
        status=random.choice(["Active", "Inactive"]),
        created="2022-01-01"
    )

def generate_user(user_id):
    return user(
        userid=user_id,
        name=random.choice(names),
        lastname=random.choice(last_name),
        email=f"{user_id}@example.com",
        phone=f"+1-{random.randint(1000000000, 9999999999)}",
        country="USA",
        birthdate="1990-05-20"
    )

def generate_device(device_id):
    return device(
        deviceid=device_id,
        tipo="Mobile",
        os="Android",
        ip=f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
        location=random.choice(["Chicago", "NYC", "LA", "Miami"])
    )

# Generate Random Relationships
def generate_relationship(user_instance, account_instance, transaction_instance, bank_instance, device_instance, card_instance, merchant_instance, atm_instance):
    relationships = [
        "OWNS", "MAKES", "AUTHORIZES", "TO", "DEPOSITS", "WITHDRAWS", "LINKED_TO", "EMPLOYS", "HAS_ACCOUNT", "REFERS", "MANAGED_BY", "USES_DEVICE",
        "USES", "LINKED_TO_ACCOUNT", "PROCESSED_BY", "OPERATED_BY", "ORIGINATES_FROM", "REGISTERED_WITH", "REPORTS"
    ]
    
    relationship = random.choice(relationships)
    
    if relationship == "OWNS":
        return f"(:User {{userID: '{user_instance.userID}'}})-[:OWNS {{since: '2022-01-01', accountType: '{account_instance.typo}', created: '2022-01-01'}}]->(:Account {{accountID: '{account_instance.accountid}', type: '{account_instance.typo}', balance: {account_instance.balance}, limit: {account_instance.limit}, status: '{account_instance.status}', created: '{account_instance.created}'}})"
    
    elif relationship == "MAKES":
        return f"(:Account {{accountID: '{account_instance.accountid}', type: '{account_instance.typo}', balance: {account_instance.balance}, status: '{account_instance.status}'}})-[:MAKES {{timestamp: '{transaction_instance.timestamp}', channel: 'Online Banking', status: 'Approved'}}]->(:Transaction {{transactionID: '{transaction_instance.transactionID}', amount: {transaction_instance.amount}, timestamp: '{transaction_instance.timestamp}', device: '{transaction_instance.device}', currency: '{transaction_instance.currency}', location: '{transaction_instance.location}'}})"
    
    elif relationship == "TO":
        return f"(:Transaction {{transactionID: '{transaction_instance.transactionID}', amount: {transaction_instance.amount}, timestamp: '{transaction_instance.timestamp}', device: '{transaction_instance.device}', currency: '{transaction_instance.currency}', location: '{transaction_instance.location}'}})-[:TO {{processingTime: '2s', medium: 'Online Transfer', channel: 'Web'}}]->(:Account {{accountID: '{account_instance.accountid}', type: '{account_instance.typo}', balance: {account_instance.balance}, status: '{account_instance.status}'}})"
    
    elif relationship == "DEPOSITS":
        return f"(:User {{userID: '{user_instance.userID}'}})-[:DEPOSITS {{time: '{transaction_instance.timestamp}', origin: 'Cash Deposit', amount: {transaction_instance.amount}}}]->(:Account {{accountID: '{account_instance.accountid}', type: '{account_instance.typo}', balance: {account_instance.balance}, status: '{account_instance.status}'}})"
    
    elif relationship == "WITHDRAWS":
        return f"(:User {{userID: '{user_instance.userID}'}})-[:WITHDRAWS {{time: '{transaction_instance.timestamp}', method: 'ATM', place: 'Zone 10'}}]->(:Account {{accountID: '{account_instance.accountid}', type: '{account_instance.typo}', balance: {account_instance.balance}, status: '{account_instance.status}'}})"
    
    elif relationship == "USES_DEVICE":
        return f"(:User {{userID: '{user_instance.userID}'}})-[:USES_DEVICE {{timestamp: '{transaction_instance.timestamp}', location: '{device_instance.location}', appUsed: 'Banking App'}}]->(:Device {{deviceID: '{device_instance.deviceID}'}})"
    
    elif relationship == "USES":
        return f"(:User {{userID: '{user_instance.userID}'}})-[:USES {{since: '2023-05-01', status: 'Active'}}]->(:Card {{cardID: '{card_instance.cardID}'}})"
    
    elif relationship == "LINKED_TO_ACCOUNT":
        return f"(:Card {{cardID: '{card_instance.cardID}'}})-[:LINKED_TO {{linkedSince: '2023-06-10', type: 'Debit'}}]->(:Account {{accountID: '{account_instance.accountid}'}})"
    
    elif relationship == "PROCESSED_BY":
        return f"(:Transaction {{transactionID: '{transaction_instance.transactionID}'}})-[:PROCESSED_BY {{time: '{transaction_instance.timestamp}', method: 'POS'}}]->(:Merchant {{merchantID: '{merchant_instance.merchantID}'}})"
    
    elif relationship == "OPERATED_BY":
        return f"(:ATM {{atmID: '{atm_instance.atmID}'}})-[:OPERATED_BY {{since: '2018-07-15'}}]->(:Bank {{bankID: '{bank_instance.bankID}'}})"
    
    elif relationship == "ORIGINATES_FROM":
        return f"(:Transaction {{transactionID: '{transaction_instance.transactionID}'}})-[:ORIGINATES_FROM {{ip: '192.168.1.10', method: 'Mobile App'}}]->(:Device {{deviceID: '{device_instance.deviceID}'}})"
    
    elif relationship == "REGISTERED_WITH":
        return f"(:Merchant {{merchantID: '{merchant_instance.merchantID}'}})-[:REGISTERED_WITH {{since: '2020-04-15', accountType: 'Business'}}]->(:Bank {{bankID: '{bank_instance.bankID}'}})"
    
    elif relationship == "REPORTS":
        return f"(:User {{userID: '{user_instance.userID}'}})-[:REPORTS {{reason: 'Unauthorized Charge', reportedAt: '{transaction_instance.timestamp}'}}]->(:Transaction {{transactionID: '{transaction_instance.transactionID}'}})"
    
    else:
        return ""


# Generate Data and Cypher Queries
cypher_queries = []
for i in range(51):  # Adjust this for the number of nodes you want to generate
    transaction_instance = generate_transaction(f"T{i}")
    account_instance = generate_account(f"A{i}")
    user_instance = generate_user(f"U{i}")
    bank_instance = bank(bankid=f"B{i}", location="USA", code=f"SW{i}", branchCount=10, founded="2000")
    device_instance = generate_device(f"D{i}")
    card_instance = card(cardid=f"C{i}", tipo="Credit", issuer="BankX", limit=5000, status="Active", expiryDate="2027-12-31")
    merchant_instance = merchant(merchantid=f"M{i}", name="StoreX", category="Retail", location="NYC", country="USA")
    atm_instance = atm(atmid=f"ATM{i}", bankid=f"B{i}", location="Downtown", status="Active", provider="BankX")
    
    cypher_queries.append(generate_relationship(user_instance, account_instance, transaction_instance, bank_instance, device_instance, card_instance, merchant_instance, atm_instance))
   
# Path to your CSV file
csv_file_path = 'cypher_queries.csv'

# Header for the CSV file
header = ['P']

# Open the CSV file in append mode
with open(csv_file_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    
    # Write header if the file is empty
    if file.tell() == 0:  # Check if the file is empty (tell() returns current position)
        writer.writerow(header)
    
    # Append each query to the CSV file, only if it's not empty
    for query in cypher_queries:
        if query.strip():  # Ensure the query is not an empty string or just whitespace
            writer.writerow([query])  # Each query is written as a single row

print("Cypher queries have been appended to the CSV file.")
