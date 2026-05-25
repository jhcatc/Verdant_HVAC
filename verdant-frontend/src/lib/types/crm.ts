export type LeadStatus =
    | 'NEW'
    | 'CONTACTED'
    | 'QUALIFIED'
    | 'PROPOSAL'
    | 'NEGOTIATION'
    | 'WON'
    | 'LOST'
    | 'CONVERTED';

export type ContractStatus =
    | 'DRAFT'
    | 'ACTIVE'
    | 'EXPIRED'
    | 'CANCELLED';

export type ProposalStatus =
    | 'DRAFT'
    | 'SENT'
    | 'APPROVED'
    | 'REJECTED';

export type TaskPriority =
    | 'LOW'
    | 'MEDIUM'
    | 'HIGH'
    | 'CRITICAL';

export type RenewalStatus =
    | 'PENDING'
    | 'IN_PROGRESS'
    | 'RENEWED'
    | 'LOST';



// =====================================================
// LEADS
// =====================================================

export type Lead = {
    id: string;
    contact_name: string;
    company_name: string;
    status: string;
    estimated_value: number;
    probability: number;
    source?: string | null;
    assigned_rep?: string | null;
    city?: string | null;
    email?: string | null;
};

export type LeadMetric = {
    title: string;
    value: string | number;
    color: string;
};

export type LeadCreateRequest = {
    title: string;
    company: string;
    email?: string;
    city?: string;
    source?: string;
    estimated_value?: number;
    probability?: number;
    assigned_rep?: string;
};

export interface CreateLeadDto {
    company: string;
    title: string;
    estimated_value?: number;
    probability?: number;
    source?: string;
    assigned_rep?: string;
    city?: string;
}

export interface UpdateLeadDto {
    company?: string;
    title?: string;
    status?: LeadStatus;
    estimated_value?: number;
    probability?: number;
    source?: string;
    assigned_rep?: string;
    city?: string;
}


// =====================================================
// OPPORTUNITIES
// =====================================================

export type Opportunity = {
    id: string;
    customer_id: string;
    customer_name: string | null;
    title: string;
    stage: string;
    probability: number;
    estimated_value: number;
    close_date: string | null;
};


// =====================================================
// CONTRACTS
// =====================================================

export type Contract = {
    id: string;
    customer_id: string;
    customer_name: string | null;
    status: string;
    sla_tier: string;
    total_value: number;
    start_date: string | null;
    end_date: string | null;
    renewal_date: string | null;
};



// =====================================================
// TASKS
// =====================================================

export interface Proposal {
    id: string;
    proposal_number: string;
    customer_id: string;
    customer_name?: string;
    opportunity_id?: string | null;
    title: string;

    status:
        | 'DRAFT'
        | 'SENT'
        | 'VIEWED'
        | 'APPROVED'
        | 'REJECTED'
        | 'EXPIRED'
        | 'ARCHIVED';

    amount: number;
    valid_until?: string | null;
    created_at?: string | null;
}


// =====================================================
// RENEWALS
// =====================================================

export interface Renewal {
    id: string;
    contract_id: string;
    customer_id: string;
    renewal_date: string;
    estimated_value?: number;
    status: RenewalStatus;
    risk_score?: number;
}


// =====================================================
// FORECAST
// =====================================================

export interface CRMForecast {
    month: string;
    pipeline_value: number;
    weighted_forecast: number;
    renewals_value: number;
}


// =====================================================
// CUSTOMER HEALTH
// =====================================================

export interface CustomerHealth {
    customer_id: string;
    customer_name: string;
    health_score: number;
    open_work_orders: number;
    sla_risk: 'LOW' | 'MEDIUM' | 'HIGH';
    renewal_risk: 'LOW' | 'MEDIUM' | 'HIGH';
}


// =====================================================
// DASHBOARD
// =====================================================

export interface DashboardMetric {
    title: string;
    value: string | number;
    color: string;
    description?: string;
}

export interface DashboardOpportunity {
    customer: string;
    opportunity: string;
    value: string;
    stage: string;
    probability: string;
}

export interface CRMDashboardResponse {
    metrics: DashboardMetric[];
    opportunities: DashboardOpportunity[];
}

export interface OpportunityCreate {
    customer_id: string;
    title: string;
    stage: string;
    estimated_value: number;
    probability: number;
    close_date?: string | null;
    notes?: string | null;
}