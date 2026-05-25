<script lang="ts">

    import {
        proposalTotals
    } from '$lib/stores/proposal.store';

    function currency(
        value: number
    ) {

        return new Intl.NumberFormat(
            'en-US',
            {
                style: 'currency',
                currency: 'USD'
            }
        ).format(value || 0);
    }

</script>

<div
    class="
        sticky
        top-24
    "
>

    <div
        class="
            rounded-2xl
            border
            border-gray-800
            bg-gray-950
            p-6
            space-y-5
        "
    >

        <div
            class="
                text-sm
                uppercase
                tracking-wider
                text-gray-500
            "
        >
            Financial Summary
        </div>

        <div class="space-y-3">

            <div class="flex justify-between">
                <span class="text-gray-400">
                    $proposalTotals.subtotal
                </span>

                <span>
                    {currency($proposalTotals.subtotal)}
                </span>
            </div>

            <div class="flex justify-between">
                <span class="text-gray-400">
                    $proposalTotals.discount_total
                </span>

                <span class="text-red-400">
                    -{currency($proposalTotals.discounts)}
                </span>
            </div>

            <div class="flex justify-between">
                <span class="text-gray-400">
                    $proposalTotals.tax_total
                </span>

                <span>
                    {currency($proposalTotals.taxes)}
                </span>
            </div>

        </div>

        <div
            class="
                border-t
                border-gray-800
                pt-4
                flex
                justify-between
                text-xl
                font-bold
            "
        >
            <span>
                Grand Total
            </span>

            <span>
                {currency($proposalTotals.grand_total)}
            </span>
        </div>

    </div>

</div>