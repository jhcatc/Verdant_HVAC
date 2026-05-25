import { writable } from 'svelte/store';
import type {
    ProposalLineItem,
    ProposalTotals
} from '$lib/api/crm/proposals';

export const proposal =
    writable<any>(null);

export const proposalLineItems =
    writable<ProposalLineItem[]>([]);

export const proposalTotals =
    writable<ProposalTotals>({
        subtotal: 0,
        discount_total: 0,
        tax_total: 0,
        grand_total: 0,
        cost_total: 0,
        margin_total: 0,
        margin_percent: 0
    });

export const proposalSaving =
    writable(false);

export const proposalDirty =
    writable(false);
