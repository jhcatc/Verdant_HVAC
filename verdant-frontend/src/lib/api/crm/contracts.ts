import api from "axios";

export interface Contract {
    id?: string;
    customer_name: string;
    status?: string;
    total_value: number;
    sla_tier?: string;
    start_date?: string;
    end_date?: string;
    renewal_date?: string;
    version?: number;
}

export async function getContracts(): Promise<Contract[]> {
    const res = await api.get("/crm/contracts");

    return res.data;
}

export async function getContract(
    contractId: string
): Promise<Contract> {
    const res = await api.get(`/crm/contracts/${contractId}`);

    return res.data;
}

export async function createContract(
    payload: Contract
): Promise<Contract> {

    const res = await api.post("/crm/contracts", {
        customer_name: payload.customer_name,
        total_value: payload.total_value,
        sla_tier: payload.sla_tier,
        start_date: payload.start_date,
        end_date: payload.end_date,
        renewal_date: payload.renewal_date,
    });

    return res.data;
}