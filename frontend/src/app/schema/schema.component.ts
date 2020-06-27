import {SelectionModel} from '@angular/cdk/collections';
import {FlatTreeControl} from '@angular/cdk/tree';
import {Component, Injectable, OnInit} from '@angular/core';
import {MatTreeFlatDataSource, MatTreeFlattener} from '@angular/material/tree';
import {BehaviorSubject, Observable} from 'rxjs';
import {SchemaService} from '../shared/schema.service';
import {ApiService} from '../shared/api.service';
import {Element} from '../models/element'
import {Type} from '../models/type'


/**
 * Node for to-do item
 */
export class TodoItemNode {
  children: TodoItemNode[];
  item: Element;
}

/** Flat to-do item node with expandable and level information */
export class TodoItemFlatNode {
  item: Element;
  level: number;
  expandable: boolean;
}

/**
 * Checklist database, it can build a tree structured Json object.
 * Each node in Json object represents a to-do item or a category.
 * If a node is a category, it has children items and new items can be added under the category.
 */
@Injectable()
export class ChecklistDatabase {
  dataChange = new BehaviorSubject<TodoItemNode[]>([]);
  types$ = new BehaviorSubject<Array<Type>>([]);

  get data(): TodoItemNode[] { return this.dataChange.value; }

  constructor(
      private schemaService: SchemaService,
      private api: ApiService,
  ) {
    schemaService.xsdType$.subscribe((xsdType) => this.initialize(xsdType));
    api.getTypes().subscribe(types => this.types$.next(types))
  }

  initialize(xsdType: {[key: string]: any}) {
    // Build the tree nodes from Json object. The result is a list of `TodoItemNode` with nested
    //     file node as children.
    const data = this.buildFileTree(xsdType, 0);

    // Notify the change.
    this.dataChange.next(data);
  }

  /**
   * Build the file structure tree. The `value` is the Json object, or a sub-tree of a Json object.
   * The return value is the list of `TodoItemNode`.
   */
  buildFileTree(obj: {[key: string]: any}, level: number): TodoItemNode[] {
    return Object.keys(obj).reduce<TodoItemNode[]>((accumulator, key) => {
      const value = obj[key];
      const node = new TodoItemNode();
      node.item = {
        type: key,
        name: ''
      };

      if (value != null) {
        if (typeof value === 'object') {
          node.children = this.buildFileTree(value, level + 1);
        } else {
          node.item = value;
        }
      }

      return accumulator.concat(node);
    }, []);
  }

  /** Add an item to to-do list */
  insertItem(parent: TodoItemNode, el: Element): void{
    if (parent.children) {
      parent.children.push({
        item: {
          type: el.type,
          name: el.name
        }
      } as TodoItemNode);
      this.dataChange.next(this.data);
    }
  }

  getChildren(type: Type) {
    const result: TodoItemNode[] = [];

    if (type && type.elements && type.elements.length ) {
      for (const el of type.elements) {
        const tp = this.types$.getValue().find(t => t.name == el.type);

        if (!type || !type.elements || !type.elements.length )
          return undefined;

        const child = this.getChildren(tp);
        result.push({
          item: {name:el.name, type:el.type},
          children: this.getChildren(tp),
        });
      }
    }
    return result.length ? result: undefined;
  }

  updateItem(node: TodoItemNode | TodoItemFlatNode, item: Element) {
    const type = this.types$.getValue().find(t => t.name == item.type);
    if (type && type.elements && type.elements.length ) {
      node = <TodoItemNode>node;
      node.children = this.getChildren(type)
    }
    node.item = item;

    this.dataChange.next(this.data);
  }
}

/**
 * @title Tree with checkboxes
 */
@Component({
  selector: 'app-schema',
  templateUrl: 'schema.component.html',
  styleUrls: ['schema.component.scss'],
  providers: [ChecklistDatabase]
})
export class SchemaComponent implements OnInit{
  /** Map from flat node to nested node. This helps us finding the nested node to be modified */
  flatNodeMap = new Map<TodoItemFlatNode, TodoItemNode>();
  /** Map from nested node to flattened node. This helps us to keep the same object for selection */
  nestedNodeMap = new Map<TodoItemNode, TodoItemFlatNode>();

  /** A selected parent node to be inserted */
  selectedParent: TodoItemFlatNode | null = null;

  /** The new item's name */
  newItemName = '';

  treeControl: FlatTreeControl<TodoItemFlatNode>;

  treeFlattener: MatTreeFlattener<TodoItemNode, TodoItemFlatNode>;

  dataSource: MatTreeFlatDataSource<TodoItemNode, TodoItemFlatNode>;

  /** The selection for checklist */
  checklistSelection = new SelectionModel<TodoItemFlatNode>(true /* multiple */);

  elements: Element[];
  types$: Observable<Array<Type>>;
  element: string;

  constructor(
      private _database: ChecklistDatabase,
      private schemaService: SchemaService,
      private apiService: ApiService,
  ) {
    this.treeFlattener = new MatTreeFlattener(this.transformer, this.getLevel,
      this.isExpandable, this.getChildren);
    this.treeControl = new FlatTreeControl<TodoItemFlatNode>(this.getLevel, this.isExpandable);
    this.dataSource = new MatTreeFlatDataSource(this.treeControl, this.treeFlattener);

    _database.dataChange.subscribe(data => {
      this.dataSource.data = data;
    });
  }

  ngOnInit(): void {
    this.types$ = this.apiService.getTypes();
  }

  getLevel = (node: TodoItemFlatNode) => node.level;

  isExpandable = (node: TodoItemFlatNode) => node.expandable;

  getChildren = (node: TodoItemNode): TodoItemNode[] => node.children;

  hasChild = (_: number, _nodeData: TodoItemFlatNode) => _nodeData.expandable;

  hasNoContent = (_: number, _nodeData: TodoItemFlatNode) => _nodeData.item.type === '';

  /**
   * Transformer to convert nested node to flat node. Record the nodes in maps for later use.
   */
  transformer = (node: TodoItemNode, level: number) => {
    const existingNode = this.nestedNodeMap.get(node);
    const flatNode = existingNode && existingNode.item.type === node.item.type
      ? existingNode
      : new TodoItemFlatNode();
    flatNode.item = node.item;
    flatNode.level = level;
    flatNode.expandable = !!node.children;
    this.flatNodeMap.set(flatNode, node);
    this.nestedNodeMap.set(node, flatNode);
    return flatNode;
  }

  /** Select the category so we can insert the new item. */
  addNewItem(node: TodoItemFlatNode): void {
    const parentNode = this.flatNodeMap.get(node);
    this._database.insertItem(parentNode!, {name:'', type:''});
    this.treeControl.expand(node);
  }

  /** Save the node to database */
  saveNode(node: TodoItemFlatNode, itemType: string, itemName: string): void {
    const nestedNode = this.flatNodeMap.get(node);
    this._database.updateItem(nestedNode!, {
      type: itemType,
      name: itemName,
    });
  }
}
