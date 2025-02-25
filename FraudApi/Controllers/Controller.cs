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

    [HttpGet("neo4")] // Route for endpoint
    public async Task<IActionResult> QueryExample() 
    {
        var nodes = await _neo4jConnector.QueryExample(); // Calls query for DB
        return Ok(nodes); // returns result
    }

    [HttpPost("creation")]
    public async Task<IActionResult> CreationQuery([FromBody] Node node) {
        if (node == null) {
            return BadRequest("Invalid body in request");
        } else {
            await _neo4jConnector.CreateNode(node.label, node.attributes);
            return Ok("Node created");
        }
    }
}

public class Node {
    public string label { get; set;}
    public Dictionary<string, object> attributes { get; set;}
}

