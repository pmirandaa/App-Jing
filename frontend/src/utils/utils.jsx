import { createSearchParams } from "react-router-dom";

export function paramsToObject(string) {
  const searchParams = createSearchParams(string);
  const result = {};
  for (const [key, value] of searchParams.entries()) {
    let splitValue = value;
    if (value.includes(',')) splitValue = value.split(',')
    result[key] = splitValue;
  }
  const parsedResult = deepParseInt(result)
  return parsedResult;
}

export function objectWithArraysToParams(obj) {
  const result = {};
  for (const [key, value] of Object.entries(obj)) {
    if (Array.isArray(value)) {
      result[key] = value.join(",");
    } else {
      result[key] = value;
    }
  }
  return createSearchParams(result);
}

export function clamp(value, min, max) {
  if (min >= max) return value;
  if (value < min) return min;
  if (value > max) return max;
  return value;
}

export function deepParseInt(obj) {
  if (typeof obj === 'string') {
    return isNaN(obj) ? obj : parseInt(obj);
  }
  if (typeof obj === 'object') {
    return Object.keys(obj).reduce((acc, key) => {
      acc[key] = deepParseInt(obj[key]);
      return acc;
    }, Array.isArray(obj) ? [] : {});
  }
  return obj;
}

export function sleeper(ms) {
  return function (x) {
    return new Promise((resolve) => setTimeout(() => resolve(x), ms));
  };
}
