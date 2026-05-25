import api from './client';

export async function searchCustomers(q: string) {
    const res = await api.get(`/customers/search?q=${encodeURIComponent(q)}`)
    return res.data;
}

export type CreateCustomerDto = {
    name: string;
    email?: string;
};

export async function createCustomer(
    data: CreateCustomerDto
)