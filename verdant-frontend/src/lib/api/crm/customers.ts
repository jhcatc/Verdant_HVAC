import api from '$lib/api/client';

export type Customer360Response = {

    customer: {
        name: string;
        annual_revenue: number;
        active_contracts: number;
        open_opportunities: number;
    };

    contracts: {

        id: string;
        customer_name: string;
        status: string;
        total_value: number;
        sla_tier: string;
        start_date: string;
        end_date: string;
        renewal_date: string;

    }[];

    opportunities: {
        id: string;
        title: string;
        stage: string;
        estimated_value: number;
        probability: number;
        close_date: string;

    }[];

    renewals: any[];
    facilities: any[];
    service_history: any[];
};

export async function getCustomer360(
    customerName: string
) {

    const response = await api.get<Customer360Response>(
        `/crm/customers/${encodeURIComponent(customerName)}`
    );

    return response.data;
}