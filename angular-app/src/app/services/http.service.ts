import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Endpoints } from '../enums/endpoints';
import { environment } from 'src/environments/environment.development';
import { HttpMessageResponse } from '../types/HttpMessageResponse';

@Injectable({
  providedIn: 'root'
})
export class HttpService {    
  private httpServerUrl: string = environment.httpServerUrl;

  constructor(private http: HttpClient) { }

  public recognizeDigit(imageData: string): Observable<HttpMessageResponse> {
    return this.http.post<any>(
      `${this.httpServerUrl}${Endpoints.RecognizeDigit}`,
      { imageData },
      { responseType: "json" }
    );
  }
}
