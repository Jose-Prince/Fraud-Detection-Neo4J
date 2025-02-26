using System;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Neo4j.Driver;
using DotNetEnv;

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
    public async Task CreateNode(string nodeLabel, Dictionary<string, object> attributes) {

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
            await session.RunAsync($"CREATE (n:{nodeLabel} {{ {attributesList} }} )");
        } finally {
            await session.CloseAsync();
        }
    }

    // Relation Creation
    public async Task CreateRelation(string nodeLabel1, string nodeLabel2, Dictionary<string, object> attributes1, Dictionary<string, object> attributes2, string relationName, Dictionary<string, object> relationAttributes) {
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
