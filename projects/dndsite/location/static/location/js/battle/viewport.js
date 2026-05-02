import { EventObserver } from "../services/event_observer.js";
import { Vector2, Vector2Math } from "../services/math.js";

export class Viewport {
    constructor (game, canvas, background) {
        this.game = game;
        this.canvas = canvas;
        this.context = this.canvas.getContext("2d");
        this.onDrawObserver = new EventObserver();

        this.zoom = {
            value: 1,
            sensivity: 0.01,
            max: 2,
            min: 0.2
        }
        this.offset = new Vector2();

        this.drag = {
            startPosition: new Vector2(),
            endPosition: new Vector2(),
            offset: new Vector2(),
            active: false
        }

        this.initEvents();
    }

    getContext() {
        return this.context;
    }

    draw() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.context.save();
        this.scale_context();
        this.translate_context();
        this.onDrawObserver.broadcast(this.context);
        this.context.restore();
    }
    
    scale_context() {
        this.context.scale(this.zoom.value, this.zoom.value);
    }

    translate_context() {
        const current_offset = this.getOffset();
        this.context.translate(current_offset.x, current_offset.y);
    }

    initEvents() {
        this.canvas.addEventListener("wheel", this.onMouseWheelScroll.bind(this), { passive: false });
        this.canvas.addEventListener("mousedown", this.onMouseDown.bind(this));
        this.canvas.addEventListener("mousemove", this.onMouseMove.bind(this));
        this.canvas.addEventListener("mouseup", this.onMouseUp.bind(this));
    }

    onMouseWheelScroll(e) {
        e.preventDefault();
        const mouseBefore = this.getMousePosition(e);

        const direction = Math.sign(e.deltaY);
        const oldZoom = this.zoom.value;
        this.zoom.value -= direction * this.zoom.sensivity;
        this.zoom.value = Math.max(this.zoom.min, Math.min(this.zoom.value, this.zoom.max));

        const mouseAfter = this.getMousePosition(e);

        const diff = Vector2Math.subtract(mouseAfter, mouseBefore);
        this.offset = Vector2Math.add(this.offset, diff);

        this.draw();
    }

    onMouseDown(e) {
        if (e.button == 0) { //mouse wheel click
            this.drag.startPosition = this.getMousePosition(e);
            this.drag.active = true;
        }
    }

    onMouseMove(e) {
        if (this.drag.active) {
            this.drag.endPosition = this.getMousePosition(e);
            this.drag.offset = Vector2Math.subtract(this.drag.endPosition, this.drag.startPosition);
            this.draw();
        }
    }

    onMouseUp(e) {
        if (this.drag.active) {
            this.offset = Vector2Math.add(this.offset, this.drag.offset);
            this.drag = {
                startPosition: new Vector2(),
                endPosition: new Vector2(),
                offset: new Vector2(),
                active: false
            }
            this.draw()
        }
    }

    getMousePosition(e) {
        return new Vector2(
            (e.offsetX / this.zoom.value) - this.offset.x,
            (e.offsetY / this.zoom.value) - this.offset.y
        );
    }

    getOffset() {
        return Vector2Math.add(this.offset, this.drag.offset);
    }
}