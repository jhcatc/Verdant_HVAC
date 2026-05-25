let socket: WebSocket | null = null;

export function connectWS(onMessage: (data: any) => void) {
    if (socket) return;

    socket = new WebSocket('ws://127.0.0.1:8000/ws/');

    socket.onopen = () => {
        console.log('✅ WS connected');
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            console.log('WS EVENT:', data);

            // 🔥 ESTO ES LO QUE TE FALTABA
            onMessage(data);

        } catch (err) {
            console.error('WS parse error', err);
        }
    };

    socket.onclose = () => {
        console.warn('❌ WS disconnected');
        socket = null;

        setTimeout(() => connectWS(onMessage), 2000);
    };

    socket.onerror = (err) => {
        console.error('WS error', err);
    };
}