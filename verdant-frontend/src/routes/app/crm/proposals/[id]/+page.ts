import type {
    PageLoad
} from './$types';

import {
    getProposal,
    getProposalLineItems,
    getProposalTotals

} from '$lib/api/crm/proposals';

export const load: PageLoad =
    async ({ params }) => {
    const proposal =
        await getProposal(params.id);
    const lineItems =
        await getProposalLineItems(
            params.id
        );
    const totals =
        await getProposalTotals(
            params.id
        );
    return {
        proposal,
        lineItems,
        totals
    };
};