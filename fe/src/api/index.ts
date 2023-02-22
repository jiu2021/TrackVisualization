import requests from "./request";
import { AxiosPromise } from "axios";
import { batch, loginM, pdr_batch } from "../model";

export const reqLogin = (data: loginM): AxiosPromise =>
  requests({
    url: `/user/login`,
    data: data,
    method: "post",
  });

export const reqUserData = (): AxiosPromise =>
  requests({
    url: `/user/data`,
    method: "get",
  });

export const reqUploadPos = (data: FormData): AxiosPromise =>
  requests({
    url: `/upload/pos`,
    data: data,
    method: "post",
  });

export const reqUploadRun = (data: FormData): AxiosPromise =>
  requests({
    url: `/upload/run`,
    data: data,
    method: "post",
  });

export const reqUploadTruth = (data: FormData): AxiosPromise =>
  requests({
    url: `/upload/truth`,
    method: "post",
    data,
  });

export const reqTruthTrack = (data: batch): AxiosPromise =>
  requests({
    url: `/track/truth`,
    method: "get",
    params: data,
  });

export const reqPosTrack = (data: batch): AxiosPromise =>
  requests({
    url: `/track/pos`,
    method: "get",
    params: data,
  });

export const reqPdrTrack = (data: pdr_batch): AxiosPromise =>
  requests({
    url: `/track/pdr`,
    method: "get",
    params: data,
  });