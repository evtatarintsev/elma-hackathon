import { Component, OnInit } from '@angular/core';
import {SchemaService} from '../shared/schema.service';
import {FormControl} from '@angular/forms';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss']
})
export class ModalComponent implements OnInit {
  xsdType = new FormControl('');

  constructor(
      private schemaService: SchemaService,
  ) { }

  ngOnInit(): void {
  }

  addType(): void{
    this.schemaService.elements.push(this.xsdType.value);
    this.schemaService.xsdType$.next({[this.xsdType.value]: {}})
  }

}
