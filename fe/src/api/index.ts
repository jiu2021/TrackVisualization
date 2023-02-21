import requests from "./request";
import { AxiosPromise } from "axios";
import { loginM } from "../model";

export const reqLogin = (data: loginM): AxiosPromise =>
  requests({
    url: `/user/login`,
    data: data,
    method: "post",
  });

export const reqUploadPos = (data: FormData): AxiosPromise =>
  requests({
    url: `/upload/pos`,
    data: data,
    method: "post",
  });

export const reqUploadRun = (data: FormData): AxiosPromise =>
  requests({
    url: `/upload/pos`,
    data: data,
    method: "post",
  });

export const reqUploadTruth = (data: FormData): AxiosPromise =>
  requests({
    url: `/upload/truth`,
    method: "post",
    data,

  });
