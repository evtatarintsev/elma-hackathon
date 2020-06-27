import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Type } from '../models/type';

interface GetTypesResponse {
    types: Array<Type>;
}

@Injectable({
    providedIn: 'root',
})
export class ApiService {
    constructor(private http: HttpClient) { }

    public getTypes(): Observable<Array<Type>> {
        return this.http.get<GetTypesResponse>('/api/types')
            .pipe(
                map(({ types }) => types),
            );
    }
}
