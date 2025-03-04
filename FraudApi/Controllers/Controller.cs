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

    [HttpGet("neo4")]
    public async Task<IActionResult> QueryExample() 
    {
        var nodes = await _neo4jConnector.QueryExample();
        return Ok(nodes);
    }

    [HttpPost("creation")]
    public async Task<IActionResult> CreationQuery([FromBody] Node node) {
        if (node == null) {
            return BadRequest("Invalid body in request");
        } else {
            await _neo4jConnector.CreateNode(node.labels, node.attributes);
            return Ok("Node created");
        }
    }

    [HttpPost("relationCreation")]
    public async Task<IActionResult> CreationRelQuery([FromBody] Rel relation) {
        if (relation == null) {
            return BadRequest("Invalid body in request");
        } else {
            await _neo4jConnector.CreateRelation(
                    relation.nodeLabel1, 
                    relation.nodeLabel2, 
                    relation.attributes1, 
                    relation.attributes2, 
                    relation.relationName, 
                    relation.relationAttributes
                    );
            return Ok("Relation created");
        }
    }

    //Visualization endpoints
    [HttpPost("nodes/filter")]
    public async Task<IActionResult> GetNodesByFilter([FromBody] FilterRequest filterRequest) {
        if (filterRequest == null || filterRequest.Filters == null || filterRequest.Label == null) {
            return BadRequest("Invalid body in request");
        }

        var nodes = await _neo4jConnector.GetNodesByFilter(filterRequest.Label, filterRequest.Filters);
        return Ok(nodes);
    }

    [HttpGet("node/{label}/{id}")]
    public async Task<IActionResult> GetNodeById(string label, string id) {
        var node = await _neo4jConnector.GetNodeById(label, id);
        if (node == null) {
            return NotFound("Node not found");
        }
        return Ok(node);
    }

    [HttpGet("nodes/{label}")]
    public async Task<IActionResult> GetAllNodes(string label) {
        var nodes = await _neo4jConnector.GetAllNodes(label);
        return Ok(nodes);
    }

    [HttpGet("nodes/aggregate")]
    public async Task<IActionResult> AggregateNodes([FromQuery] string label, [FromQuery] string aggregateFunction, [FromQuery] string property = null) {
        if (string.IsNullOrEmpty(label) || string.IsNullOrEmpty(aggregateFunction)) {
            return BadRequest("Label and aggregate function are required");
        }

        var result = await _neo4jConnector.AggregateNodes(label, aggregateFunction, property);
        return Ok(result);
    }

    //Delete nodes
    [HttpDelete("node/{label}/{id}")]
    public async Task<IActionResult> DeleteNode(string label, string id) {
        await _neo4jConnector.DeleteNode(label, id);
        return Ok("Node deleted successfully");
    }

    [HttpDelete("nodes/delete")]
    public async Task<IActionResult> DeleteNodes([FromBody] DeleteRequest request) {
        if (request == null || request.Filters == null || string.IsNullOrEmpty(request.Label)) {
            return BadRequest("Invalid body in request");
        }

        await _neo4jConnector.DeleteManyNodes(request.Label, request.Filters);
        return Ok("Nodes deleted successfully");
    }

    //Delete Relationships
    [HttpDelete("relations/delete")]
    public async Task<IActionResult> DeleteRelations([FromBody] List<RelationToDelete> relations) {
        if (relations == null || relations.Count == 0) {
            return BadRequest("No relations provided for deletion.");
        }

        await _neo4jConnector.DeleteRelations(relations);
        return Ok("Relations deleted successfully");
    }


    [HttpPut("relations/update/")]
    public async Task<IActionResult> SetRelations([FromBody] Rel_To_Change relations) {
        if (relations == null) {
            return BadRequest("No relations provided for deletion.");
        }
        await _neo4jConnector.SetRelations(relations);

        return Ok("Relations updated successfully");
    }



    [HttpPut("relations/update_multiple/")]
    public async Task<IActionResult> SetMultipleRelations([FromBody] List<Rel_To_Change> relations) {
        if (relations == null) {
            return BadRequest("No relations provided for deletion.");
        }
        await _neo4jConnector.SetRelationsMultiple(relations);

        return Ok("Relations updated successfully");
    }


    [HttpPut("node/update_multiple/")]
    public async Task<IActionResult> SetNodesMultiple([FromBody] List<Rel_To_Change> relations) {
        if (relations == null) {
            return BadRequest("No relations provided for deletion.");
        }
        await _neo4jConnector.SetRelationsMultiple(relations);

        return Ok("Relations updated successfully");
    }

    [HttpPut("relations/update/")]
    public async Task<IActionResult> SetNodes([FromBody] Rel_To_Change relations) {
        if (relations == null) {
            return BadRequest("No relations provided for deletion.");
        }
        await _neo4jConnector.SetRelations(relations);

        return Ok("Relations updated successfully");
    }


}

public class Node {
    public string[] labels { get; set; }
    public Dictionary<string, object> attributes { get; set; }
}

public class Rel {
    public string nodeLabel1 { get; set; } 
    public string nodeLabel2 {get; set; } 
    public Dictionary<string, object> attributes1 { get; set; } 
    public Dictionary<string, object> attributes2 { get; set; } 
    public string relationName { get; set; } 
    public Dictionary<string, object> relationAttributes { get; set; }
}

public class FilterRequest {
    public string Label { get; set; }
    public Dictionary<string, object> Filters { get; set; }
}

public class DeleteRequest {
    public string Label { get; set; }
    public Dictionary<string, object> Filters { get; set; }
}

public class RelationToDelete {
    public string label1 { get; set; }
    public string id1 { get; set; }
    public string relationName { get; set; }
    public string label2 { get; set; }
    public string id2 { get; set; }
}



public class Rel_To_Change {

    public string relationName { get; set; } 
    public Dictionary<string, object> relationAttributes { get; set; }
    public Dictionary<string, object> To_change { get; set; } 
}



public class Node_To_Change {
    public string label { get; set; }
    public Dictionary<string, object> attributes { get; set; }

    public string target_label { get; set; }
    public Dictionary<string, object> attributes_to_change { get; set; }
}
