import api from '$lib/api/client';
import type {
    Proposal
} from '$lib/types/crm';


// =====================================================
// TYPES
// =====================================================

export interface ProposalLineItem {

    id: string;
    proposal_id: string;
    item_type:
        | 'equipment'
        | 'labor'
        | 'pm_plan'
        | 'discount'
        | 'misc';
    description: string;
    qty: number;
    unit_price: number;
    unit_cost: number;
    tax_percent: number;
    discount_percent: number;
    subtotal: number;
    discount_amount: number;
    taxable_amount: number;
    tax_amount: number;
    total: number;
    margin_amount: number;
    margin_percent: number;
    sort_order: number;
    is_optional: boolean;
}

export interface ProposalTotals {
    subtotal: number;
    discounts: number;
    taxes: number;
    grand_total: number;
}



// =====================================================
// PROPOSALS
// =====================================================

export async function getProposals():
    Promise<Proposal[]> {

    const response = await api.get(
        '/crm/proposals/'
    );
    return response.data;
}

export async function getProposal(
    id: string
): Promise<Proposal> {
    const response = await api.get(
        `/crm/proposals/${id}`
    );

    return response.data;
}

export async function createProposal(
    payload: {
        customer_id: string;
        opportunity_id?: string | null;
        title: string;
        amount?: number;
        valid_until?: string | null;
    }
): Promise<Proposal> {

    const response = await api.post(
        '/crm/proposals/',
        payload
    );

    return response.data;
}

export async function deleteProposal(
    id: string
) {
    const response = await api.delete(
        `/crm/proposals/${id}`
    );

    return response.data;
}



// =====================================================
// LINE ITEMS
// =====================================================

export async function getProposalLineItems(
    proposalId: string
): Promise<ProposalLineItem[]> {

    const response = await api.get(
        `/crm/proposals/${proposalId}/line-items`
    );

    return response.data;
}

export async function createProposalLineItem(
    proposalId: string,
    payload: Partial<ProposalLineItem>
): Promise<ProposalLineItem> {

    const response = await api.post(
        `/crm/proposals/${proposalId}/line-items`,
        payload
    );

    return response.data;
}

export async function updateProposalLineItem(
    proposalId: string,
    itemId: string,
    payload: Partial<ProposalLineItem>
): Promise<ProposalLineItem> {

    const response = await api.patch(
        `/crm/proposals/${proposalId}/line-items/${itemId}`,
        payload
    );

    return response.data;
}

export async function deleteProposalLineItem(
    proposalId: string,
    itemId: string
) {

    const response = await api.delete(
        `/crm/proposals/${proposalId}/line-items/${itemId}`
    );

    return response.data;
}

export async function reorderProposalLineItems(
    proposalId: string,
    items: {
        id: string;
        sort_order: number;
    }[]
) {

    const response = await api.post(
        `/crm/proposals/${proposalId}/line-items/reorder`,
        { items }
    );

    return response.data;
}



// =====================================================
// TOTALS
// =====================================================

export async function getProposalTotals(
    proposalId: string
): Promise<ProposalTotals> {

    const response = await api.get(
        `/crm/proposals/${proposalId}/totals`
    );

    return response.data;
}

export async function recalculateProposal(
    proposalId: string
) {

    const response = await api.post(
        `/crm/proposals/${proposalId}/recalculate`
    );

    return response.data;
}