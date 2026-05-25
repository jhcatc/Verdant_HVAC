<script lang="ts">
    let { sla } = $props();
</script>

<div class="bg-slate-900 p-4 rounded-lg text-white">
    <h2 class="text-lg font-semibold mb-3">SLA Overview</h2>

    <div class="grid grid-cols-3 gap-4 text-center">

        <div>
            <div class="text-xl font-bold text-green-400">
                {sla.sla_percentage}%
            </div>
            <div class="text-xs text-gray-400">SLA Compliance</div>
        </div>

        <div>
            <div class="text-xl font-bold">
                {sla.on_time}
            </div>
            <div class="text-xs text-gray-400">On Time</div>
        </div>

        <div>
            <div class="text-xl font-bold text-red-400">
                {sla.late}
            </div>
            <div class="text-xs text-gray-400">Late</div>
        </div>

    </div>
</div>