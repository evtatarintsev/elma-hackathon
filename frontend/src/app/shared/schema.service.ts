import {Injectable} from '@angular/core';
import {BehaviorSubject, Subject} from 'rxjs';
import {TodoItemNode} from '../schema/schema.component';
import {Type} from '../models/type'

@Injectable({
        providedIn: 'root',
})
export class SchemaService {
    types: Type[] = [];
    private dataChange = new BehaviorSubject<TodoItemNode[]>([]);
    xsdType$ = new BehaviorSubject<{[key: string]: any}>({});

    get xsdType(): {[key: string]: any} {
        return this.xsdType$.value;
    }
}
