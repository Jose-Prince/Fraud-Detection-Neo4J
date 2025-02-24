using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

namespace FraudApi.Controllers;

[ApiController]
[Route("api")] // Route of controller
public class Controller : ControllerBase
{
    private readonly Neo4JConnector _neo4jConnector;

    public Controller(Neo4JConnector neo4jConnector)
    {
        _neo4jConnector = neo4jConnector;
    }

    [HttpGet("neo4j")] // Route for endpoint
    public async Task<IActionResult> QueryExample() 
    {
        var nodes = await _neo4jConnector.QueryExample(); // Calls query for DB
        return Ok(nodes); // returns result
    }
}
