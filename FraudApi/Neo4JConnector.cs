using System;
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
}
