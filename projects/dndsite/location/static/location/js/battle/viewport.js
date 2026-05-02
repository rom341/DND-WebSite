import { EventObserver } from "../services/event_observer.js";

export class Viewport {
    constructor (game, canvas, background) {
        this.game = game;
        this.canvas = canvas;
        this.context = this.canvas.getContext("2d");
        this.onDrawObserver = new EventObserver();
    }

    getContext() {
        return this.context;
    }

    draw() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.onDrawObserver.broadcast(this.context);
    }
}