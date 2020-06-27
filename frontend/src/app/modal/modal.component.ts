import { Component, OnInit } from '@angular/core';
import {SchemaService} from '../shared/schema.service';
import {FormControl} from '@angular/forms';
import {xsdType} from '../schema/schema.component';

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
    const type: xsdType = {
      name: this.xsdType.value,
      version: 0,
    };
    this.schemaService.types.push(type);
    this.schemaService.xsdType$.next({[type.name]: {}});
  }

}
