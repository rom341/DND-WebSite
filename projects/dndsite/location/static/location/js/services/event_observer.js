export class EventObserver {
    constructor () {
        this.observers = []
    }

    subscribe (func) {
        this.observers.push(func);
    }

    unsubscribe (func) {
        this.observers = this.observers.filter(f => f !== func);
    }

    broadcast (data) {
        this.observers.forEach(observer => observer(data));
    }
}