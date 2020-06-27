import { Component, OnInit } from '@angular/core';
import {SchemaService} from '../shared/schema.service';
import {MatDialog} from '@angular/material/dialog';
import {ModalComponent} from '../modal/modal.component';

@Component({
  selector: 'app-xsd-elements',
  templateUrl: './xsd-elements.component.html',
  styleUrls: ['./xsd-elements.component.scss']
})
export class XsdElementsComponent implements OnInit {

  elements: string[];

  constructor(
      private schemaService: SchemaService,
      private dialog: MatDialog,
  ) { }

  ngOnInit(): void {
    this.elements = this.schemaService.elements;
  }

  addNewElement(): void {
    const dialogRef = this.dialog.open(ModalComponent);
    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }

}
