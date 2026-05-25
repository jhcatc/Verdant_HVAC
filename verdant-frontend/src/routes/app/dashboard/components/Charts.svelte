<script lang="ts">
    import { onMount, onDestroy, tick } from 'svelte';
    import Chart from 'chart.js/auto';

    const { orders } = $props();

    let statusCanvas;
    let revenueCanvas;

    let statusChart;
    let revenueChart;

    async function buildCharts() {
        await tick();

        // 🔥 seguridad total
        if (!statusCanvas || !revenueCanvas) return;

        // 🔥 si no hay data → destruir charts y salir
        if (!orders || orders.length === 0) {
            statusChart?.destroy();
            revenueChart?.destroy();
            return;
        }

        const statusCount = {
            pending: 0,
            in_progress: 0,
            completed: 0
        };

        orders.forEach(o => {
            if (statusCount[o.status] !== undefined) {
                statusCount[o.status]++;
            }
        });

        statusChart?.destroy();
        revenueChart?.destroy();

        statusChart = new Chart(statusCanvas, {
            type: 'doughnut',
            data: {
                labels: Object.keys(statusCount),
                datasets: [{
                    data: Object.values(statusCount)
                }]
            }
        });

        revenueChart = new Chart(revenueCanvas, {
            type: 'bar',
            data: {
                labels: orders.map(o => o.title),
                datasets: [{
                    label: 'Revenue',
                    data: orders.map(o => o.actual_cost || 0)
                }]
            }
        });
    }

    onMount(buildCharts);

    $effect(() => {
        buildCharts();
    });

    onDestroy(() => {
        statusChart?.destroy();
        revenueChart?.destroy();
    });
</script>