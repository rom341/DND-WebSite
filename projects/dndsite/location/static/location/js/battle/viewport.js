import { EventObserver } from "../services/event_observer.js";

export class Viewport {
    constructor (game, canvas, background) {
        this.game = game;
        this.canvas = canvas;
        this.context = this.canvas.getContext("2d");
        this.onDrawObserver = new EventObserver();

        this.zoom = 1;
        this.zoomSensivity = 0.1;
        this.zoomMax = 2;
        this.zoomMin = 0.2;
        this.initEvents();
    }

    getContext() {
        return this.context;
    }

    draw() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.context.save();
        this.context.scale(this.zoom, this.zoom);
        this.onDrawObserver.broadcast(this.context);
        this.context.restore();
    }

    initEvents() {
        this.canvas.addEventListener("wheel", this.onMouseWheelScroll.bind(this), { passive: false });
    }

    onMouseWheelScroll(e) {
        e.preventDefault();
        const direction = Math.sign(e.deltaY);
        this.zoom += direction * this.zoomSensivity;
        this.zoom = Math.max(this.zoomMin, Math.min(this.zoom, this.zoomMax));
        this.draw();
    }
}