import { Component, ElementRef, EventEmitter, Output, ViewChild } from '@angular/core';
import { DrawnLine } from '../types/DrawnLine';
import { HttpService } from '../services/http.service';
import { HttpMessageResponse } from '../types/HttpMessageResponse';

@Component({
  selector: 'app-canvas',
  templateUrl: './canvas.component.html',
  styleUrls: ['./canvas.component.css']
})
export class CanvasComponent {
  @ViewChild('canvasRef') canvasRef!: ElementRef;
  @Output() messageChange: EventEmitter<string> = new EventEmitter<string>();

  isCursorOverCanvas = false;
  canvasBorderColor: string = "warning";

  private canvas: any | null = null;
  private canvasContext: CanvasRenderingContext2D | null = null;
  private drawnLines: DrawnLine[] = [];
  private isDrawing: boolean = false;

  constructor(private httpService: HttpService) {}

  updateMessage(message: string): void {
    this.messageChange.emit(message);
  }

  ngAfterViewInit() {
    if (!this.canvasRef) {
      return;
    }

    this.canvas = this.canvasRef.nativeElement;
    this.canvasContext = this.canvas.getContext("2d");

    if (!this.canvasContext) {
      return;
    }

    this.canvasContext.fillStyle = "black";
    this.canvasContext.fillRect(0, 0, this.canvas.width, this.canvas.height);
  }

  handleRecognizeButtonClick(event: any) {
    if (!event) {
      return;
    }

    if (this.drawnLines.length === 0) {
      this.updateMessage("Canvas cannot be empty");
      this.canvasBorderColor = "danger";
      return;
    }

    const scaledImageData = this.getScaledImageData();

    this.httpService.recognizeDigit(scaledImageData).subscribe(
      (response: HttpMessageResponse) => {
        this.updateMessage("Prediction: " + response.message);
        this.canvasBorderColor = "success";
      },
      (error: any) => {
        this.updateMessage("ERROR");
        this.canvasBorderColor = "danger";
      }
    );
  }

  getScaledImageData(): string {
    const scaledCanvas = document.createElement('canvas');
    const scaledContext = scaledCanvas.getContext('2d')!;
    scaledCanvas.width = 28;
    scaledCanvas.height = 28;
    scaledContext.drawImage(this.canvas, 0, 0, this.canvas.width, this.canvas.height, 0, 0, 28, 28);
  
    return scaledCanvas.toDataURL('image/png');
  }

  handleClearCanvasButtonClick(event: any) {
    if (!event) {
      return;
    }

    this.updateMessage("");
    this.canvasBorderColor = "warning";
    this.canvasContext?.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.canvasContext?.fillRect(0, 0, this.canvas.width, this.canvas.height);
    this.drawnLines = [];
  };

  onMouseDown(event: MouseEvent): void {
    if (!this.canvasContext) return;
  
    this.isDrawing = true;
  
    const { offsetX, offsetY } = event;
  
    const drawnLine: DrawnLine = {
      currentPoint: { x: offsetX, y: offsetY },
      thickness: 12,
      color: 'white',
      previousPoint: { x: offsetX, y: offsetY },
    };
  
    this.drawnLines.push(drawnLine);
    this.draw(this.canvasContext, drawnLine);
  
    const onMouseUp = () => {
      this.isDrawing = false;
      this.canvasRef.nativeElement.removeEventListener('mousemove', this.onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
    };
  
    window.addEventListener('mouseup', onMouseUp);
    this.canvasRef.nativeElement.addEventListener('mousemove', this.onMouseMove.bind(this));
  }

  onMouseMove(event: MouseEvent): void {
    if (!this.canvasContext || !this.isDrawing) return;

    const { offsetX, offsetY } = event;

    const drawnLine: DrawnLine = {
      currentPoint: { x: offsetX, y: offsetY },
      thickness: 12,
      color: 'white',
      previousPoint: this.drawnLines[this.drawnLines.length - 1].currentPoint,
    };

    this.drawnLines.push(drawnLine);
    this.draw(this.canvasContext, drawnLine);
  }

  onMouseEnterCanvas() {
    this.isCursorOverCanvas = true;
  }

  onMouseLeaveCanvas() {
    this.isCursorOverCanvas = false;
  }

  draw(canvasContext: CanvasRenderingContext2D, drawnLine: DrawnLine) {
    const { x: currentRelativeX, y: currentRelativeY } = drawnLine.currentPoint;
    const { x: prevRelativeX, y: prevRelativeY } = drawnLine.previousPoint;
  
    canvasContext.beginPath();
    canvasContext.lineWidth = drawnLine.thickness;
    canvasContext.lineCap = "round";
    canvasContext.lineJoin = "round";
    canvasContext.strokeStyle = drawnLine.color;
    canvasContext.moveTo(prevRelativeX, prevRelativeY);
    canvasContext.lineTo(currentRelativeX, currentRelativeY);
    canvasContext.stroke();
  }
}