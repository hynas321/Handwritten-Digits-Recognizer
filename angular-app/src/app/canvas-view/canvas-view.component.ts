import { Component, ViewChild } from '@angular/core';
import { CanvasComponent } from '../canvas/canvas.component';

@Component({
  selector: 'app-canvas-view',
  templateUrl: './canvas-view.component.html',
})
export class CanvasViewComponent {
  @ViewChild('canvasRef') canvas!: CanvasComponent;
  responseMessage: string = '';

  ngAfterViewInit(): void {
    if (this.canvas) {
      this.canvas.messageChange.subscribe((newMessage: string) => {
        this.responseMessage = newMessage;
      });
    }
  }
}
