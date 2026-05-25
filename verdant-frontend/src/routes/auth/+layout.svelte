<script lang="ts">
    import { onMount } from 'svelte';
    let { children } = $props();

    // Pequeño truco opcional para asegurar que el contenido se cargue después de la imagen
    let imageLoaded = $state(false);
    onMount(() => {
        const img = new Image();
        img.src = '/wallpaper.png'; // Asegúrate de que este nombre sea correcto (o /walkpaper.png)
        img.onload = () => imageLoaded = true;
    });
</script>

<div 
    class="relative min-h-screen w-full flex flex-col items-center justify-center bg-verdant-50 overflow-hidden"
    style="
        background-image: url('/wallpaper.png'); 
        background-size: cover; 
        background-position: center; 
        background-repeat: no-repeat;
    "
>
    <div class="absolute inset-0 z-0 bg-verdant-950/15"></div>

    <div 
        class="relative z-10 w-full max-w-md px-6 flex flex-col items-center text-center transition-opacity duration-300"
        class:opacity-0={!imageLoaded}
        class:opacity-100={imageLoaded}
    >
        {@render children()}
        <!--
        <footer class="mt-8 text-[13px] font-light text-[#15803D] tracking-wide">
            Verdant HVAC · Enterprise Resource Planning · Since 2026
        </footer>
        -->
    </div>
</div>

<style>
    /* Opcional: Aseguramos que la tipografía se vea limpia */
    :global(body) {
        font-family: 'Inter', sans-serif; /* O la fuente que uses */
        -webkit-font-smoothing: antialiased;
    }
</style>