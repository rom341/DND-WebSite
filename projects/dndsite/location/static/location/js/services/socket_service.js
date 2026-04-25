export class SocketService {
    constructor (url) {
        this.url = url;
        this.socket = null;
        this.events = {};
    }

    connect() {
        this.socket = new WebSocket(this.url);

        this.socket.onmessage = (event) => {
            const message = {
                //type: JSON.parse(event.data).type,
                type: "CHARACTER_MOVED",
                data: JSON.parse(event.data)
            }

            if (this.events[message.type]) {
                this.events[message.type].forEach(callback => {
                    callback(message.data);
                });
            }

        }
        this.socket.onopen = () => console.log("Connected to Server");
        this.socket.onerror = (err) => console.error("Socket Error:", err);
    }

    subscribe(type, callback) {
        if (!this.events[type]) 
            this.events[type] = [];
        this.events[type].push(callback);
    }

    send(type, payload) {
        if (this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(payload));
        }
    }
}