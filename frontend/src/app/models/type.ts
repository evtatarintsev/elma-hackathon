import {Element} from './element'

export interface Type {
    name: string;
    elements?: Array<Element>;
    editable?: boolean;
    version: number;
    updated?: number;
}
