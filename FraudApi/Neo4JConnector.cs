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
