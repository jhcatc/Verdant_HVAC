<script lang="ts">

    let {
        title,
        value,
        color = 'emerald'
    } = $props<{
        title: string;
        value: string | number;
        color?: string;
    }>();

</script>

<div
    class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
>

    <div
        class="text-sm text-gray-400"
    >
        {title}
    </div>

    <div
        class={`text-3xl font-bold mt-2 text-${color}-500`}
    >
        {value}
    </div>

</div>