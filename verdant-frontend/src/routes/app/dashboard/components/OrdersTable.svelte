<script lang="ts">
    const { orders } = $props();

    const statusColor = (status: string) => {
        switch (status) {
            case 'completed': return 'bg-green-100 text-green-700';
            case 'in_progress': return 'bg-yellow-100 text-yellow-700';
            default: return 'bg-gray-100 text-gray-700';
        }
    };
</script>

<div class="card">

    <h3 class="font-semibold mb-4 text-gray-900">
        Recent Orders
    </h3>

    <table class="w-full text-sm text-gray-900">

        <thead>
            <tr class="text-left border-b text-gray-700">
                <th>Title</th>
                <th>Status</th>
                <th>City</th>
                <th>Cost</th>
            </tr>
        </thead>

        <tbody>
            {#each orders.slice(0, 5) as o}
            <tr class="border-b hover:bg-gray-50 transition">
                <td>{o.title}</td>

                <td>
                    <span class={`px-2 py-1 rounded text-xs ${statusColor(o.status)}`}>
                        {o.status}
                    </span>
                </td>

                <td>{o.city}</td>
                <td>${o.actual_cost ?? 0}</td>
            </tr>
            {/each}
        </tbody>

    </table>

</div>