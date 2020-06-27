import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Type } from '../models/type';

interface GetTypesResponse {
    types: Array<Type>;
}

interface GetTypeResponse {
    type: Type;
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

    public createType(newType: Type): Observable<Type> {
        console.log(newType);
        return this.http.post<GetTypeResponse>('/api/types', JSON.stringify(newType))
            .pipe(
                map(({ type }) => type),
            );
    }

    public updateType(newType: Type): Observable<Type> {
        console.log(newType);
        return this.http.put<GetTypeResponse>(`/api/types/${newType.name}/update`, JSON.stringify(newType))
            .pipe(
                map(({ type }) => type),
            );
    }
}
