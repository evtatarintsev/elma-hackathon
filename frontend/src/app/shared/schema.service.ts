import {Injectable} from '@angular/core';
import {BehaviorSubject, Subject} from 'rxjs';
import {TodoItemNode, xsdType} from '../schema/schema.component';

@Injectable({
        providedIn: 'root',
})
export class SchemaService {
    types: xsdType[] = [
        {
            name: 'string1',
            editable: false,
            version: 1,
            updated: new Date()
        },
        {
            name: 'string2',
            editable: false,
            version: 1,
            updated: new Date()
        },
        {
            name: 'string3',
            editable: false,
            elements: [{name: 'elem 1', type: 'sting1'}],
            version: 1,
            updated: new Date()
        },

    ];
    private dataChange = new BehaviorSubject<TodoItemNode[]>([]);
    xsdType$ = new BehaviorSubject<{[key: string]: any}>({});

    get xsdType(): {[key: string]: any} {
        return this.xsdType$.value;
    }
}
