import {Injectable} from '@angular/core';
import {BehaviorSubject, Subject} from 'rxjs';
import {TodoItemNode} from '../schema/schema.component';

@Injectable({
        providedIn: 'root',
})
export class SchemaService {
    elements: string[] = ['Extra cheese', 'Mushroom', 'Onion', 'Pepperoni', 'Sausage', 'Tomato'];
    private dataChange = new BehaviorSubject<TodoItemNode[]>([]);
    xsdType$ = new BehaviorSubject<{[key: string]: any}>({});

    get xsdType(): {[key: string]: any} {
        return this.xsdType$.value;
    }
}
