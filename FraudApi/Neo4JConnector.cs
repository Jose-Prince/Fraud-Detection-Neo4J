using System;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Neo4j.Driver;
using DotNetEnv;
using System.Text.Json;

//Driver configuration
public class Neo4JConnector : IAsyncDisposable {
    private readonly IDriver _driver;


    public Neo4JConnector() {
        Env.Load();
    
        //Credentials
        var uri = Env.GetString("NEO4J_URI");
        var user = Env.GetString("NEO4J_USERNAME");
        var password = Env.GetString("NEO4J_PASSWORD");

        _driver = GraphDatabase.Driver(uri, AuthTokens.Basic(user, password));
    }

    // Node Creation
    public async Task CreateNode(string[] nodeLabels, Dictionary<string, object> attributes) {

        var nodeLabelsList = new StringBuilder();

        foreach (var item in nodeLabels) {
            nodeLabelsList.Append($":{item}");
        }

        var attributesList = new StringBuilder();

        foreach (var item in attributes) {
            string key = item.Key;
            object value = item.Value;

            string formattedValue = FormatValue(value);

            attributesList.Append($"{key}:{formattedValue}, ");
        }

        if (attributesList.Length > 0) attributesList.Length -= 2;

        await using var session = _driver.AsyncSession();
        
        try {
            await session.RunAsync($"CREATE (n{nodeLabelsList} {{ {attributesList} }} )");
        } finally {
            await session.CloseAsync();
        }
    }

    // Relation Creation
    public async Task CreateRelation(
            string nodeLabel1, 
            string nodeLabel2, 
            Dictionary<string, object> attributes1, 
            Dictionary<string, object> attributes2, 
            string relationName, Dictionary<string, 
            object> relationAttributes) 
    {
        var attributesList1 = new StringBuilder();
        var attributesList2 = new StringBuilder();
        var attributesRelList = new StringBuilder();

        foreach (var item in attributes1) {
            string key = item.Key;
            object value = item.Value;

            string formattedValue = FormatValue(value);
            attributesList1.Append($"{key}:{formattedValue}, ");
        }

        if (attributesList1.Length > 0) attributesList1.Length -= 2;

        foreach (var item in attributes2) {
            string key = item.Key;
            object value = item.Value;

            string formattedValue = FormatValue(value);
            attributesList2.Append($"{key}:{formattedValue}, ");
        }

        if (attributesList2.Length > 0) attributesList2.Length -= 2;
    
        foreach (var item in relationAttributes) {
            string key = item.Key;
            object value = item.Value;

            string formattedValue = FormatValue(value);
            attributesRelList.Append($"{key}:{formattedValue}, ");
        }

        if (attributesRelList.Length > 0) attributesRelList.Length -= 2;

        await using var session = _driver.AsyncSession();

        try {
            await session.RunAsync(
                    $"MATCH (n:{nodeLabel1} {{ {attributesList1} }} )" +
                    $"MATCH (p:{nodeLabel2} {{ {attributesList2} }} )" +
                    $"CREATE (n)-[:{relationName} {{ {attributesRelList} }}]->(p)"
                    );
        } finally {
            await session.CloseAsync();
        }
    }

    //Defines Querys
    public async Task<List<string>> QueryExample() {
        await using var session = _driver.AsyncSession();
        var results = new List<string>();

        try {
            var result = await session.RunAsync("MATCH (n) RETURN n.name AS name LIMIT 10");

            await foreach (var record in result) {
                results.Add(record["name"].As<string>());
            }
        } finally {
            await session.CloseAsync();
        }

        return results;
    }

    public async ValueTask DisposeAsync() {
        await _driver.DisposeAsync();
    }
    
    //Nodes Visualization
    //Get nodes by filter
    public async Task<List<Dictionary<string, object>>> GetNodesByFilter(string label, Dictionary<string, object> filters) {
        await using var session = _driver.AsyncSession();
        var results = new List<Dictionary<string, object>>();

        try {
            var convertedFilters = new Dictionary<string, object>();
            foreach (var filter in filters) {
                if (filter.Value is JsonElement jsonElement) {
                    convertedFilters[filter.Key] = ConvertJsonElement(jsonElement);
                } else {
                    convertedFilters[filter.Key] = filter.Value;
                }
            }

            var filterClauses = new List<string>();
            foreach (var filter in convertedFilters) {
                filterClauses.Add($"n.{filter.Key} = ${filter.Key}");
            }
            var filterString = string.Join(" AND ", filterClauses);

            var query = $"MATCH (n:{label}) WHERE {filterString} RETURN n";

            var result = await session.RunAsync(query, convertedFilters);

            await foreach (var record in result) {
                var properties = record["n"].As<INode>().Properties;
                results.Add(properties.ToDictionary(kvp => kvp.Key, kvp => kvp.Value));
            }
        } finally {
            await session.CloseAsync();
        }

        return results;
    }

    // Método para convertir JsonElement a tipos primitivos
    private object ConvertJsonElement(JsonElement jsonElement) {
        switch (jsonElement.ValueKind) {
            case JsonValueKind.String:
                return jsonElement.GetString();
            case JsonValueKind.Number:
                if (jsonElement.TryGetInt32(out int intValue)) {
                    return intValue;
                } else if (jsonElement.TryGetDouble(out double doubleValue)) {
                    return doubleValue;
                }
                break;
            case JsonValueKind.True:
            case JsonValueKind.False:
                return jsonElement.GetBoolean();
            case JsonValueKind.Null:
                return null;
            default:
                throw new NotSupportedException($"Unsupported JsonValueKind: {jsonElement.ValueKind}");
        }
        return null;
    }

    //Gets node by Id (only one)
    public async Task<Dictionary<string, object>> GetNodeById(string label, string id) {
        await using var session = _driver.AsyncSession();
        Dictionary<string, object> resultNode = null;

        try {
            var query = $"MATCH (n:{label}) WHERE n.userID = $id RETURN n";
            
            var result = await session.RunAsync(query, new { id });

            if (await result.FetchAsync()) {
                var properties = result.Current["n"].As<INode>().Properties;
                resultNode = properties.ToDictionary(kvp => kvp.Key, kvp => kvp.Value);
            }
        } finally {
            await session.CloseAsync();
        }

        return resultNode;
    }

    //gets nodes(too much)
    public async Task<List<Dictionary<string, object>>> GetAllNodes(string label) {
        await using var session = _driver.AsyncSession();
        var results = new List<Dictionary<string, object>>();

        try {
            var query = $"MATCH (n:{label}) RETURN n";
            var result = await session.RunAsync(query);

            await foreach (var record in result) {
                var properties = record["n"].As<INode>().Properties;
                results.Add(properties.ToDictionary(kvp => kvp.Key, kvp => kvp.Value));
            }
        } finally {
            await session.CloseAsync();
        }

        return results;
    }

    //Aggregate functions
    public async Task<object> AggregateNodes(string label, string aggregateFunction, string property = null) {
        await using var session = _driver.AsyncSession();
        object result = null;

        try {
            string query;
            if (property != null) {
                query = $"MATCH (n:{label}) RETURN {aggregateFunction}(n.{property}) AS result";
            } else {
                query = $"MATCH (n:{label}) RETURN {aggregateFunction}(n) AS result";
            }

            var resultSet = await session.RunAsync(query);

            if (await resultSet.FetchAsync()) {
                result = resultSet.Current["result"];
            }
        } finally {
            await session.CloseAsync();
        }

        return result;
    }

    //Delete nodes
    //Delete only one node
    public async Task DeleteNode(string label, string id) {
        await using var session = _driver.AsyncSession();
        try {
            var deleteRelationshipsQuery = $"MATCH (n:{label} {{userID: $id}}) DETACH DELETE n";
            await session.RunAsync(deleteRelationshipsQuery, new { id });
        } finally {
            await session.CloseAsync();
        }
    }

    //Delete too much nodes
    public async Task DeleteManyNodes(string label, Dictionary<string, object> filters) {
        await using var session = _driver.AsyncSession();

        try {
            var convertedFilters = new Dictionary<string, object>();
            foreach (var filter in filters) {
                if (filter.Value is JsonElement jsonElement) {
                    convertedFilters[filter.Key] = ConvertJsonElement(jsonElement);
                } else {
                    convertedFilters[filter.Key] = filter.Value;
                }
            }

            if (convertedFilters.Count == 0) {
                throw new ArgumentException("No filters provided for deletion.");
            }

            var filterClauses = new List<string>();
            foreach (var filter in convertedFilters) {
                filterClauses.Add($"n.{filter.Key} = ${filter.Key}");
            }
            var filterString = string.Join(" AND ", filterClauses);

            var query = $"MATCH (n:{label}) WHERE {filterString} DETACH DELETE n";
            await session.RunAsync(query, convertedFilters);

        } finally {
            await session.CloseAsync();
        }
    }

    //Delate Relationships (1+)
    public async Task DeleteRelations(List<FraudApi.Controllers.RelationToDelete> relations) {
        await using var session = _driver.AsyncSession();

        try {
            // Ejecutar cada consulta dentro del mismo bucle
            foreach (var rel in relations) {
                var query = $@"
                    MATCH (n1:{rel.label1} {{userID: $id1}})-[r:{rel.relationName} ]->(n2:{rel.label2} {{userID: $id2}})
                    DELETE r";

                await session.RunAsync(query, new { id1 = rel.id1, id2 = rel.id2 });
            }
        } finally {
            await session.CloseAsync();
        }
    }


public async Task SetRelations(FraudApi.Controllers.Rel_To_Change relations)
{
    await using var session = _driver.AsyncSession();
    try
    {
        var parameters = new Dictionary<string, object>();
        var attributesRelList = new StringBuilder();

        // Build MATCH clause dynamically
        foreach (var item in relations.relationAttributes)
        {
            string key = item.Key;
            object value = ConvertJsonElement(item.Value);
            
            attributesRelList.Append($"{key}: ${key}, ");
            parameters[key] = value;
        }

        // Remove trailing comma if necessary
        string attributesFilter = attributesRelList.Length > 2 
            ? attributesRelList.ToString(0, attributesRelList.Length - 2)
            : "";

        // Build SET clause dynamically
        var setClause = new StringBuilder();
        foreach (var kv in relations.To_change)
        {
            setClause.Append($"r.{kv.Key} = ${kv.Key}, ");
            parameters[kv.Key] = ConvertJsonElement(kv.Value);
        }

        // Remove trailing comma if necessary
        string setClauseStr = setClause.Length > 2 
            ? setClause.ToString(0, setClause.Length - 2) 
            : "";

        var query = $@"
            MATCH ()-[r:{relations.relationName} {{ {attributesFilter} }}]->()
            SET {setClauseStr}";

        // Run query with parameters


        await session.RunAsync(query, parameters);
    }
    finally
    {
        await session.CloseAsync();
    }
}


public async Task SetRelationsMultiple(List<FraudApi.Controllers.Rel_To_Change> relationsList)
{
    await using var session = _driver.AsyncSession();
    try
    {
        var parameters = new Dictionary<string, object>();

        // Loop through the list of relations to create dynamic MATCH and SET clauses for each relation
        foreach (var relations in relationsList)
        {
            var attributesRelList = new StringBuilder();
            foreach (var item in relations.relationAttributes)
            {
                string key = item.Key;
                object value = ConvertJsonElement(item.Value);
                
                attributesRelList.Append($"{key}: ${key}_{relations.relationName}, ");
                parameters[$"{key}_{relations.relationName}"] = value;
            }

            string attributesFilter = attributesRelList.Length > 0 
                ? attributesRelList.ToString(0, attributesRelList.Length - 2) 
                : "";

            // Build SET clause dynamically for each relation
            var setClause = new StringBuilder();
            foreach (var kv in relations.To_change)
            {
                setClause.Append($"r.{kv.Key} = ${kv.Key}_{relations.relationName}, ");
                parameters[$"{kv.Key}_{relations.relationName}"] = ConvertJsonElement(kv.Value);
            }

            string setClauseStr = setClause.Length > 0 
                ? setClause.ToString(0, setClause.Length - 2) 
                : "";

            // Build the Cypher query for this particular relation
            var query = $@"
                MATCH (r:{relations.relationName} {{ {attributesFilter} }})
                SET {setClauseStr}
            ";

            // Run the query for this individual relationship update
            await session.RunAsync(query, parameters);

            // Clear parameters for the next iteration
            parameters.Clear();
        }
    }
    finally
    {
        await session.CloseAsync();
    }
}


public async Task SetNodesMultiple(List<FraudApi.Controllers.Rel_To_Change> relationsList)
{
    await using var session = _driver.AsyncSession();
    try
    {
        var parameters = new Dictionary<string, object>();

        // Loop through the list of relations to create dynamic MATCH and SET clauses for each relation
        foreach (var relations in relationsList)
        {
            var attributesRelList = new StringBuilder();
            foreach (var item in relations.relationAttributes)
            {
                string key = item.Key;
                object value = ConvertJsonElement(item.Value);
                
                attributesRelList.Append($"{key}: ${key}_{relations.relationName}, ");
                parameters[$"{key}_{relations.relationName}"] = value;
            }

            string attributesFilter = attributesRelList.Length > 0 
                ? attributesRelList.ToString(0, attributesRelList.Length - 2) 
                : "";

            // Build SET clause dynamically for each relation
            var setClause = new StringBuilder();
            foreach (var kv in relations.To_change)
            {
                setClause.Append($"r.{kv.Key} = ${kv.Key}_{relations.relationName}, ");
                parameters[$"{kv.Key}_{relations.relationName}"] = ConvertJsonElement(kv.Value);
            }

            string setClauseStr = setClause.Length > 0 
                ? setClause.ToString(0, setClause.Length - 2) 
                : "";

            // Build the Cypher query for this particular relation
            var query = $@"
                MATCH ()-[r:{relations.relationName} {{ {attributesFilter} }}]->()
                SET {setClauseStr}
            ";

            // Run the query for this individual relationship update
            await session.RunAsync(query, parameters);

            // Clear parameters for the next iteration
            parameters.Clear();
        }
    }
    finally
    {
        await session.CloseAsync();
    }
}


public async Task SetNodes(FraudApi.Controllers.Rel_To_Change relations)
{
    await using var session = _driver.AsyncSession();
    try
    {
        var parameters = new Dictionary<string, object>();
        var attributesRelList = new StringBuilder();

        // Build MATCH clause dynamically
        foreach (var item in relations.relationAttributes)
        {
            string key = item.Key;
            object value = ConvertJsonElement(item.Value);
            
            attributesRelList.Append($"{key}: ${key}, ");
            parameters[key] = value;
        }

        // Remove trailing comma if necessary
        string attributesFilter = attributesRelList.Length > 2 
            ? attributesRelList.ToString(0, attributesRelList.Length - 2)
            : "";

        // Build SET clause dynamically
        var setClause = new StringBuilder();
        foreach (var kv in relations.To_change)
        {
            setClause.Append($"r.{kv.Key} = ${kv.Key}, ");
            parameters[kv.Key] = ConvertJsonElement(kv.Value);
        }

        // Remove trailing comma if necessary
        string setClauseStr = setClause.Length > 2 
            ? setClause.ToString(0, setClause.Length - 2) 
            : "";

        var query = $@"
            MATCH (r:{relations.relationName} {{ {attributesFilter} }})
            SET {setClauseStr}";

        // Run query with parameters


        await session.RunAsync(query, parameters);
    }
    finally
    {
        await session.CloseAsync();
    }
}


// Converts JsonElement to appropriate .NET type
private object ConvertJsonElement(object value)
{
    if (value is JsonElement jsonElement)
    {
        return jsonElement.ValueKind switch
        {
            JsonValueKind.String => jsonElement.GetString(),
            JsonValueKind.Number => jsonElement.TryGetInt64(out long l) ? l : jsonElement.GetDouble(),
            JsonValueKind.True => true,
            JsonValueKind.False => false,
            JsonValueKind.Null => null,
            _ => jsonElement.ToString() // Fallback for unsupported types
        };
    }
    return value;
}


    public string FormatValue(object value) {
        if (value == null)
            return "null";

        string valueStr = value.ToString();

        if (value is string)
            return $"\"{EscapeString(valueStr)}\""; // Escapa caracteres especiales

        if (value is bool)
            return valueStr.ToLower(); // `true` o `false` en minúsculas

        if (value is int || value is float || value is double || Regex.IsMatch(valueStr, @"^-?\d+(\.\d+)?$"))
            return valueStr; // Mantiene los números sin comillas

        if (value is IEnumerable<object> list) // Manejo de listas
            return "[" + string.Join(", ", list.Select(FormatValue)) + "]";

        return $"\"{EscapeString(valueStr)}\""; // Por defecto, se trata como string
    }

    public string EscapeString(string input) {
        return input.Replace("\"", "\\\""); // Escapa comillas dobles
    }
}
