<script lang="ts">
    import api from '$lib/api/client';

    let { tasks, orderId } = $props();

    async function toggleTask(task) {
        const original = task.is_done;

        task.is_done = !task.is_done;
        tasks = [...tasks];

        try {
            await api.patch(`/tasks/${task.id}`, {
                is_done: task.is_done
            });
        } catch (e) {
            task.is_done = original;
            tasks = [...tasks];
        }
    }
</script>

<div class="card">

    <h2 class="font-semibold mb-4">Tasks</h2>

    {#if !tasks || tasks.length === 0}
        <p class="text-gray-400 text-sm">No tasks yet</p>
    {/if}

    <div class="space-y-2">

        {#each tasks as t}
        <div class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50">

            <input
                type="checkbox"
                checked={t.is_done}
                on:change={() => toggleTask(t)}
            />

            <span class={t.is_done ? 'line-through text-gray-400' : ''}>
                {t.title}
            </span>

        </div>
        {/each}

    </div>

</div>