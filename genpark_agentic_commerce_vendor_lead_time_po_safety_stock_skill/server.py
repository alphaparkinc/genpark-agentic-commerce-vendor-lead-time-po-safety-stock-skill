# -*- coding: utf-8 -*-
"""MCP Server for Vendor Lead-Time Variability & Safety Stock Optimizer Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import VendorLeadTimeSafetyStockOptimizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "calculate_dynamic_safety_stock",
        "description": "Calculate statistical safety stock and continuous reorder point (ROP) based on supplier lead-time standard deviation and target service level (95%-99%).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "average_daily_demand": {
                    "type": "number"
                },
                "demand_standard_deviation": {
                    "type": "number"
                },
                "average_lead_time_days": {
                    "type": "number"
                },
                "lead_time_standard_deviation_days": {
                    "type": "number"
                },
                "desired_service_level_pct": {
                    "type": "number",
                    "description": "e.g. 95.0, 98.0, 99.0"
                }
            },
            "required": [
                "average_daily_demand",
                "demand_standard_deviation",
                "average_lead_time_days",
                "lead_time_standard_deviation_days"
            ]
        }
    },
    {
        "name": "evaluate_purchase_order_trigger",
        "description": "Audit current on-hand and in-transit inventory against statistical reorder point, issuing automated PO triggers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sku": {
                    "type": "string"
                },
                "current_on_hand_units": {
                    "type": "integer"
                },
                "incoming_in_transit_units": {
                    "type": "integer"
                },
                "reorder_point_units": {
                    "type": "integer"
                },
                "economic_order_quantity_units": {
                    "type": "integer"
                }
            },
            "required": [
                "sku",
                "current_on_hand_units",
                "incoming_in_transit_units",
                "reorder_point_units",
                "economic_order_quantity_units"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-vendor-lead-time-po-safety-stock-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(VendorLeadTimeSafetyStockOptimizer, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-agentic-commerce-vendor-lead-time-po-safety-stock-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-vendor-lead-time-po-safety-stock-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
