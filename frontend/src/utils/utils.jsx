import { createSearchParams } from "react-router-dom";

export function paramsToObject(string) {
  const searchParams = createSearchParams(string);
  const result = {};
  for (const [key, value] of searchParams.entries()) {
    let parsed = isNaN((+value)) ? value : (+value);
    result[key] = parsed;
  }
  return result;
}

export function clamp(value, min, max) {
  if (min >= max) return value;
  if (value < min) return min;
  if (value > max) return max;
  return value;
}