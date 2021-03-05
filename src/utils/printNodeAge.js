/**
 * Prints node age in a human readable format.
 * @param {number} age node age in millions of years
 */
const printNodeAge = (age) => {
  if (age > 1000) {
    return `${(age / 1000).toLocaleString(undefined, {
      maximumSignificantDigits: 3,
    })} billion years ago`
  }

  return `${age.toLocaleString(undefined, {
    maximumSignificantDigits: 3,
  })} million years ago`
}

export default printNodeAge
