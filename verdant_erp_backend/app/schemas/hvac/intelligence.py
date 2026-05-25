from datetime import datetime
from pydantic import BaseModel


# =========================================================
# VISUAL INTELLIGENCE
# =========================================================

class GeoFailureDTO(BaseModel):
    location_id: str | None
    failures: int


class FacilityHealthDTO(BaseModel):
    location_id: str | None
    health_score: int
    failures: int
    status: str


class GeoHeatPointDTO(BaseModel):
    location_id: str | None
    intensity: int
    lat: float | None = None
    lng: float | None = None


class FailureClusterDTO(BaseModel):
    customer_id: str | None
    location_id: str | None
    cluster_strength: int
    cluster_type: str


class VisualIntelligenceSnapshotDTO(BaseModel):
    facility_health: list[FacilityHealthDTO]
    geo_heatmap: list[GeoHeatPointDTO]
    clusters: list[FailureClusterDTO]
    geo_failures: list[GeoFailureDTO]


# =========================================================
# SERVICE INTELLIGENCE
# =========================================================

class TechnicianPerformanceDTO(BaseModel):
    technician_id: str
    name: str
    completed_orders: int
    avg_resolution_time_hours: float


class SlaDashboardDTO(BaseModel):
    total_completed_orders: int
    on_time: int
    late: int
    sla_percentage: float


class CustomerSatisfactionDTO(BaseModel):
    customer_id: str | None
    total_orders: int
    reopened_orders: int
    avg_resolution_hours: float
    satisfaction_score: float


class TimeToRepairDTO(BaseModel):
    status: str
    avg_repair_time_hours: float


class ServiceIntelligenceSnapshotDTO(BaseModel):
    technician_performance: list[TechnicianPerformanceDTO]
    sla: SlaDashboardDTO
    customer_satisfaction: list[CustomerSatisfactionDTO]
    time_to_repair: list[TimeToRepairDTO]
    generated_at: datetime


# =========================================================
# INFRASTRUCTURE INTELLIGENCE
# =========================================================

class FailureByCustomerDTO(BaseModel):
    customer_id: str | None
    failures: int


class ProblematicEquipmentDTO(BaseModel):
    equipment_id: str
    asset_tag: str
    failures: int


class MaintenanceCostDTO(BaseModel):
    equipment_id: str
    asset_tag: str
    estimated_cost: float


class RiskScoringDTO(BaseModel):
    equipment_id: str
    asset_tag: str
    risk: str
    failures: int


class InfrastructureSnapshotDTO(BaseModel):
    failures_by_customer: list[FailureByCustomerDTO]
    problematic_equipment: list[ProblematicEquipmentDTO]
    maintenance_costs: list[MaintenanceCostDTO]
    risk_scoring: list[RiskScoringDTO]


# =========================================================
# CORRELATION ENGINE
# =========================================================

class CustomerClusterDTO(BaseModel):
    customer_id: str | None
    total_failures: int
    risk_level: str


class CorrelationProblematicEquipmentDTO(BaseModel):
    equipment_id: str
    asset_tag: str
    customer_id: str | None
    failures: int


class InstallationRankingDTO(BaseModel):
    location_id: str | None
    failures: int
    risk: str


class TechnicianHeatmapDTO(BaseModel):
    technician_id: str
    name: str
    workload: int
    load_level: str


class CorrelationSnapshotDTO(BaseModel):
    customer_clusters: list[CustomerClusterDTO]
    problematic_equipment: list[
        CorrelationProblematicEquipmentDTO
    ]
    installation_ranking: list[
        InstallationRankingDTO
    ]
    technician_heatmap: list[
        TechnicianHeatmapDTO
    ]


# =========================================================
# MASTER SNAPSHOT
# =========================================================

class IntelligenceSnapshotDTO(BaseModel):
    infrastructure: InfrastructureSnapshotDTO
    service: ServiceIntelligenceSnapshotDTO