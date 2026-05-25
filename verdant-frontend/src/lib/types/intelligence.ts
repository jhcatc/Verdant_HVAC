export type GeoFailure = {
    location_id: string | null;
    failures: number;
};

export type FacilityHealth = {
    location_id: string | null;
    health_score: number;
    failures: number;
    status: string;
};

export type GeoHeatPoint = {
    location_id: string | null;
    intensity: number;
    lat: number | null;
    lng: number | null;
};

export type FailureCluster = {
    customer_id: string | null;
    location_id: string | null;
    cluster_strength: number;
    cluster_type: string;
};

export type VisualIntelligenceSnapshot = {
    facility_health: FacilityHealth[];
    geo_heatmap: GeoHeatPoint[];
    clusters: FailureCluster[];
    geo_failures: GeoFailure[];
};

export type TechnicianPerformance = {
    technician_id: string;
    name: string;
    completed_orders: number;
    avg_resolution_time_hours: number;
};

export type SlaDashboard = {
    total_completed_orders: number;
    on_time: number;
    late: number;
    sla_percentage: number;
};

export type CustomerSatisfaction = {
    customer_id: string | null;
    total_orders: number;
    reopened_orders: number;
    avg_resolution_hours: number;
    satisfaction_score: number;
};

export type TimeToRepair = {
    status: string;
    avg_repair_time_hours: number;
};

export type ServiceIntelligenceSnapshot = {
    technician_performance: TechnicianPerformance[];
    sla: SlaDashboard;
    customer_satisfaction: CustomerSatisfaction[];
    time_to_repair: TimeToRepair[];
    generated_at: string;
};

export type FailureByCustomer = {
    customer_id: string | null;
    failures: number;
};

export type ProblematicEquipment = {
    equipment_id: string;
    asset_tag: string;
    failures: number;
};

export type MaintenanceCost = {
    equipment_id: string;
    asset_tag: string;
    estimated_cost: number;
};

export type RiskScoring = {
    equipment_id: string;
    asset_tag: string;
    risk: string;
    failures: number;
};

export type InfrastructureSnapshot = {
    failures_by_customer: FailureByCustomer[];
    problematic_equipment: ProblematicEquipment[];
    maintenance_costs: MaintenanceCost[];
    risk_scoring: RiskScoring[];
};

export type CustomerCluster = {
    customer_id: string | null;
    total_failures: number;
    risk_level: string;
};

export type CorrelationProblematicEquipment = {
    equipment_id: string;
    asset_tag: string;
    customer_id: string | null;
    failures: number;
};

export type InstallationRanking = {
    location_id: string | null;
    failures: number;
    risk: string;
};

export type TechnicianHeatmap = {
    technician_id: string;
    name: string;
    workload: number;
    load_level: string;
};

export type CorrelationSnapshot = {
    customer_clusters: CustomerCluster[];
    problematic_equipment:
        CorrelationProblematicEquipment[];
    installation_ranking:
        InstallationRanking[];
    technician_heatmap:
        TechnicianHeatmap[];
};

export type IntelligenceSnapshot = {
    infrastructure: InfrastructureSnapshot;
    service: ServiceIntelligenceSnapshot;
};