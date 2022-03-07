// Flatten an object into single level dot-separated key-value pairs
export const convertToDotNotation = (obj: any, newObj: any={}, prefix='') => {
  for (const key in obj) {
    if (typeof obj[key] === 'object') {
      convertToDotNotation(obj[key], newObj, prefix + key + '.')
    } else {
      newObj[prefix + key] = obj[key]
    }
  }
  return newObj
}