# Vendor Lead-Time Variability & Safety Stock Optimizer Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Stochastic vendor lead-time variability modeling, stockout probability Monte Carlo simulation, dynamic safety stock buffer optimization, and automated purchase order reorder triggers. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `calculate_dynamic_safety_stock`: Calculate statistical safety stock and continuous reorder point (ROP) based on supplier lead-time standard deviation and target service level (95%-99%).
- `evaluate_purchase_order_trigger`: Audit current on-hand and in-transit inventory against statistical reorder point, issuing automated PO triggers.

## 🚀 Installation & Usage
Run directly with pure Python standard library:
```bash
python -m genpark_agentic_commerce_vendor_lead_time_po_safety_stock_skill.server --test
```
