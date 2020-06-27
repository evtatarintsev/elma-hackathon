import { Component, OnInit } from '@angular/core';
import {SchemaService} from '../shared/schema.service';
import {MatDialog} from '@angular/material/dialog';
import {ModalComponent} from '../modal/modal.component';
import { Observable } from 'rxjs';
import { Type } from '../models/type';
import { ApiService } from '../shared/api.service';

@Component({
  selector: 'app-xsd-elements',
  templateUrl: './xsd-elements.component.html',
  styleUrls: ['./xsd-elements.component.scss']
})
export class XsdElementsComponent implements OnInit {

  xsdTypes: Type[];
  elements: string[];
  types$: Observable<Array<Type>>;

  constructor(
      private schemaService: SchemaService,
      private dialog: MatDialog,
      private apiService: ApiService,
  ) { }

  ngOnInit(): void {
    this.types$ = this.apiService.getTypes();
  }

  addNewElement(): void {
    const dialogRef = this.dialog.open(ModalComponent);
    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }

}
