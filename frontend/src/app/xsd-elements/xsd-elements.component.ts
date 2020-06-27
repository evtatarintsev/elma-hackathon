import { Component, OnInit } from '@angular/core';
import {SchemaService} from '../shared/schema.service';
import {MatDialog} from '@angular/material/dialog';
import {ModalComponent} from '../modal/modal.component';
import {xsdType} from '../schema/schema.component';


@Component({
  selector: 'app-xsd-elements',
  templateUrl: './xsd-elements.component.html',
  styleUrls: ['./xsd-elements.component.scss']
})
export class XsdElementsComponent implements OnInit {

  xsdTypes: xsdType[];

  constructor(
      private schemaService: SchemaService,
      private dialog: MatDialog,
  ) { }

  ngOnInit(): void {
    this.xsdTypes = this.schemaService.types;
  }

  addNewElement(): void {
    const dialogRef = this.dialog.open(ModalComponent);
    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }

}
