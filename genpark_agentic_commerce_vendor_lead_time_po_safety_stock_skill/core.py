# -*- coding: utf-8 -*-
"""Vendor Lead-Time Variability & Safety Stock Optimizer for GenPark Agentic Commerce."""
import json
import math
from typing import Dict, Any

class VendorLeadTimeSafetyStockOptimizer:
    """Stochastic lead-time and demand variance inventory safety buffer engine."""

    # Normal distribution Z-scores for standard service levels
    Z_TABLE = {
        90.0: 1.282,
        95.0: 1.645,
        97.5: 1.960,
        98.0: 2.054,
        99.0: 2.326,
        99.9: 3.090
    }

    @staticmethod
    def calculate_dynamic_safety_stock(average_daily_demand: float, demand_standard_deviation: float, average_lead_time_days: float, lead_time_standard_deviation_days: float, desired_service_level_pct: float = 95.0) -> Dict[str, Any]:
        """Compute King's Formula combined safety stock: SS = Z * sqrt(L * sigma_D^2 + D^2 * sigma_L^2)."""
        z = VendorLeadTimeSafetyStockOptimizer.Z_TABLE.get(desired_service_level_pct, 1.645)

        # Combined variance
        combined_var = (average_lead_time_days * (demand_standard_deviation ** 2)) + ((average_daily_demand ** 2) * (lead_time_standard_deviation_days ** 2))
        safety_stock = math.ceil(z * math.sqrt(combined_var))

        # Reorder Point (ROP) = (Demand * LeadTime) + SafetyStock
        lead_time_demand = math.ceil(average_daily_demand * average_lead_time_days)
        reorder_point = lead_time_demand + safety_stock

        return {
            "service_level_target_pct": desired_service_level_pct,
            "z_score": z,
            "expected_lead_time_demand_units": lead_time_demand,
            "recommended_safety_stock_units": safety_stock,
            "reorder_point_units": reorder_point,
            "lead_time_risk_contribution_pct": round((((average_daily_demand ** 2) * (lead_time_standard_deviation_days ** 2)) / combined_var) * 100.0, 1),
            "stockout_protection": f"Guarantees {desired_service_level_pct}% cycle service level against combined demand surge and vendor delay."
        }

    @staticmethod
    def evaluate_purchase_order_trigger(sku: str, current_on_hand_units: int, incoming_in_transit_units: int, reorder_point_units: int, economic_order_quantity_units: int) -> Dict[str, Any]:
        """Assess net inventory position against ROP and emit automated PO requisition."""
        effective_inventory = current_on_hand_units + incoming_in_transit_units
        is_triggered = effective_inventory <= reorder_point_units

        return {
            "sku": sku,
            "effective_inventory_position": effective_inventory,
            "reorder_point": reorder_point_units,
            "po_trigger_status": "TRIGGER_PURCHASE_ORDER" if is_triggered else "ADEQUATE_STOCK",
            "recommended_order_quantity": economic_order_quantity_units if is_triggered else 0,
            "stock_buffer_surplus_units": effective_inventory - reorder_point_units,
            "urgency": "CRITICAL_STOCKOUT_RISK" if current_on_hand_units <= 0 else ("ORDER_NOW" if is_triggered else "STABLE")
        }
