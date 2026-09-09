def authorize_request(source, risk):
    # Untrusted sources cannot authorize risky actions
    if source in ["website", "document", "email", "tool_output"] and risk in ["high", "critical"]:
        return "DENY"

    # Critical actions need human approval
    if risk == "critical":
        return "ESCALATE"

    # Medium risk needs extra checking
    if risk == "medium":
        return "ESCALATE"

    # Low-risk requests are allowed
    return "ALLOW"