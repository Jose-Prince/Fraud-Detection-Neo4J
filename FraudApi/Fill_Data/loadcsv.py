import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Neo4j connection details from environment variables
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

# Initialize the Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))

# Define a list of Cypher queries to execute
queries_node = [
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/accounts.csv' AS row
    MERGE (a:Account {accountID: toString(row.accountID)})
    SET a.type = row.type,
        a.balance = toFloat(row.balance),
        a.limit = toFloat(row.limit),
        a.status = row.status,
        a.created = date(row.created);
    """,
    # Add more queries if necessary
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/atms.csv' AS row
    MERGE (a:atm {atmID: toString(row.atmID)})
    SET a.location = row.location,
        a.status = toString(row.status),
        a.provider = toString(row.provider),
        a.Balance = toFloat(row.Balance);
    """,
    """
   LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/banks.csv' AS row
    MERGE (a:bank {bankID: toString(row.bankID)})
    SET a.location = row.location,
        a.name = row.name,
        a.code = row.code,
        a.branchCount = toFloat(row.branchCount),
        a.founded = date(row.founded);
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/cards.csv' AS row
    MERGE (a:cards {cardID: toString(row.cardID)})
    SET a.type = row.type,
        a.issuer = row.issuer,
        a.limit = toFloat(row.limit),
        a.status = row.status,
        a.expiryDate = date(row.expiryDate);
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/companies.csv' AS row
    MERGE (a:company {companyID: toString(row.companyID)})
    SET a.name = row.name,
        a.industry = row.industry,
        a.size = toFloat(row.size),
        a.location = row.location,
        a.taxID = row.taxID;

    """,
    """    
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/devices.csv' AS row
    MERGE (a:device {deviceID: toString(row.deviceID)})
    SET a.type = row.type,
        a.os = row.os,
        a.ip = row.ip,
        a.location = row.location;
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/merchants.csv' AS row
    MERGE (a:merchant {merchanID: toString(row.merchantID)})
    SET a.name = row.name,
        a.category = row.category,
        a.location = row.location,
        a.country = row.country;
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/transactions.csv' AS row
    MERGE (a:transaction {transactionID: toString(row.transactionID)})
    SET a.amount = row.amount,
        a.timestamp = row.timestamp,
        a.device = row.device,
        a.currency = row.currency,
        a.location = row.location;    
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/users.csv' AS row
    MERGE (a:user {userID: toString(row.userID)})
    SET a.name = row.name,
        a.lastname = row.lastname,
        a.email = row.email,
        a.phone = row.phone,
        a.country = row.country,
        a.birthdate = date(row.birthdate);
    """
    
    # You can add additional queries in the list here
]


queries_rel = [
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/auth_transactions.csv' AS row
    MATCH (c:bank{bankID:row.startNode})
    MATCH (usr:transaction{ transactionID:row.endNode})
    MERGE (c)-[r:AUTHORIZES{authCode:row.authCode, time:row.time, status:row.status}]->(usr)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/withdraws_relation.csv' AS row
    MATCH (c:user{userID:row.startNode})
    MATCH (usr:Account{ accountID:row.endNode})
    MERGE (usr)-[r:WITHDRAWS{timestamp:row.timestamp, method:row.method ,amount:row.amount}]->(c)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/owns_relation.csv' AS row
    MATCH (c:user{userID:row.startNode})
    MATCH (usr:Account{ accountID:row.endNode})
    MERGE (c)-[r:OWNS{since:row.since, account_type:row.account_type, created:row.created}]->(usr)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/has_accs_relation.csv' AS row
    MATCH (c:bank{bankID:row.startNode})
    MATCH (usr:Account{ accountID:row.endNode})
    MERGE (c)-[r:HAS{opened:row.opened, branch:row.branch, status:row.status}]->(usr)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/deposits_relation.csv' AS row
    MATCH (c:user{userID:row.startNode})
    MATCH (usr:Account{ accountID:row.endNode})
    MERGE (c)-[r:DEPOSITS{timestamp:row.timestamp, amount:row.amount, origin:row.origin}]->(usr)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/linked_accounts.csv' AS row
    MATCH (c:Account{accountID:row.startNode})
    MATCH (usr:Account{ accountID:row.endNode})
    MERGE (c)-[r:LINKED_TO{date:row.date, linkType:row.linkType, reason:row.reason}]->(usr)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/company_relationships.csv' AS row
    MATCH (c:company{companyID:row.startNode})
    MATCH (usr:user{ userID:row.endNode})
    MERGE (c)-[r:EMPLOYS{since:row.since, position:row.position, department:row.department}]->(usr)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/auth_transactions.csv' AS row
    MATCH (c:bank{bankID:row.startNode})
    MATCH (usr:transaction{ transactionID:row.endNode})
    MERGE (c)-[r:AUTHORIZES{authCode:row.authCode, time:row.time, status:row.status}]->(usr)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/refers_relation.csv' AS row
    MATCH (c:user{userID:row.startNode})
    MATCH (usr:user{ userID:row.endNode})
    MERGE (c)-[r:REFERS{referralDate:row.referralDate, referralCode:row.referralCode, rewardAmount:row.rewardAmount}]->(usr)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/managed_accounts.csv' AS row
    MATCH (c:Account{accountID:row.startNode})
    MATCH (usr:company{ companyID:row.endNode})
    MERGE (usr)-[r:MANAGED_BY{managementStart:row.managementStart, accountPurpose:row.accountPurpose, auditRating:row.auditRating}]->(c)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/device_relationships.csv' AS row
    MATCH (c:user{userID:row.startNode})
    MATCH (usr:device{ deviceID:row.endNode})
    MERGE (c)-[r:USES_DEVICE{timestamp:row.timestamp, location:row.location, appUsed:row.appUsed}]->(usr)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/Withdraws_AT.csv' AS row
    MATCH (c:Account{accountID:row.startNode})
    MATCH (usr:atm{ atmID:row.endNode})
    MERGE (c)-[r:Withdraws_AT{time:row.time, amount:row.amount, AT:row.AT}]->(usr)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/uses_card.csv' AS row
    MATCH (c:user{userID:row.startNode})
    MATCH (usr:cards{ cardID:row.endNode})
    MERGE (c)-[r:USES_CARD{created:row.created, type:row.type, Restrictions:row.Restrictions}]->(usr)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/purchased_at.csv' AS row
    MATCH (c:transaction{transactionID:row.startNode})
    MATCH (usr:merchant{ merchanID:row.endNode})
    MERGE (c)-[r:PURCHASED_AT{time:row.time, apppused:row.appUsed, reason:row.reason}]->(usr)
    return c, r ,usr
    """,
    """
    LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/tranmakes.csv' AS row
    MATCH (c:Account{accountID:row.startNode})
    MATCH (usr:transaction{ transactionID:row.endNode})
    MERGE (c)-[r:MAKES{time:row.time, amount:row.amount, from:row.from, to:row.to}]->(usr)
    return c, r ,usr
    """,
    

    
    
    
    
    # You can add additional queries in the list here
]


# Function to execute a list of queries
def execute_queries(queries):
    with driver.session() as session:
        for query in queries:
            # Run each query
            session.run(query)
            print("Executed query successfully")

# Run the function to execute the queries
execute_queries(queries_node)

execute_queries(queries_rel)


# Close the driver connection
driver.close()





#RELACIONES


# OWNS


# authorizes 




# tranmakes
# LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Jose-Prince/Fraud-Detection-Neo4J/refs/heads/main/FraudApi/Fill_Data/csves/tranmakes.csv' AS row
# MATCH (c:Account{accountID:row.startNode})
# MATCH (usr:transaction{ transactionID:row.endNode})
# MERGE (c)-[r:MAKES{time:row.time, amount:row.amount, from:row.from, to:row.to}]->(usr)
# return c, r ,usr


# MATCH (n)
# WHERE NOT (n)--()
# DELETE n