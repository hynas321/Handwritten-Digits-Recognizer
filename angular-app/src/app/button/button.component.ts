import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html'
})
export class ButtonComponent {
  @Input() text!: string;
  @Input() bootstrapButtonType!: string;
  @Input() margin!: string;
  @Output() onClick = new EventEmitter<string>();

  buttonClass: string = "";
  styles: string = "";
  
  ngOnInit() {
    this.buttonClass = `btn ${this.bootstrapButtonType}`
    this.styles = `margin: ${this.margin}`;
  }

  emitEvent(event: any) {
    this.onClick.emit(event);
  }
}
