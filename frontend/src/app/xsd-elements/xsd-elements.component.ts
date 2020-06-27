import { Component, OnInit } from '@angular/core';
import {SchemaService} from '../shared/schema.service';

@Component({
  selector: 'app-xsd-elements',
  templateUrl: './xsd-elements.component.html',
  styleUrls: ['./xsd-elements.component.scss']
})
export class XsdElementsComponent implements OnInit {

  elements: string[];

  constructor(
      private schemaService: SchemaService,
  ) { }

  ngOnInit(): void {
    this.elements = this.schemaService.elements;
  }

  addNewElement() {

  }

}
