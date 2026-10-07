class ChargerWebSocket {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000;
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const url = `${protocol}//${window.location.host}/ws/chargers`;
        
        this.ws = new WebSocket(url);

        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.reconnectAttempts = 0;
            this.hideConnectionError();
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'status_update') {
                this.handleStatusUpdate(data);
            }
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.showConnectionError();
        };

        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            this.attemptReconnect();
        };
    }

    handleStatusUpdate(data) {
        const row = document.querySelector(`tr[data-evbox-id="${data.evboxId}"]`);
        if (row) {
            const statusCell = row.querySelector('td:nth-child(3)');
            if (statusCell) {
                statusCell.textContent = data.status;
                statusCell.style.animation = 'pulse 0.5s';
            }
        }
    }

    showConnectionError() {
        let errorDiv = document.getElementById('connectionError');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'connectionError';
            errorDiv.className = 'connection-error';
            errorDiv.innerHTML = 'Verbinding verbroken, probeer opnieuw';
            document.body.insertBefore(errorDiv, document.body.firstChild);
        }
        errorDiv.style.display = 'block';
    }

    hideConnectionError() {
        const errorDiv = document.getElementById('connectionError');
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Reconnecting... attempt ${this.reconnectAttempts}`);
            setTimeout(() => this.connect(), this.reconnectDelay);
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

const chargerWS = new ChargerWebSocket();
