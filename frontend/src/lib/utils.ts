export const isValidISBN = (isbn: string): boolean => {
  isbn = isbn.replace('-', '').replace(' ', '')

  if (isbn.length !== 10 && isbn.length !== 13) return false

  if (isbn.length === 10) {
    try {
      const digits: number[] = isbn
        .split('')
        .map((char) => (char === 'X' ? 10 : parseInt(char, 10)))

      const checkSum = digits.reduce((sum, digit, index) => sum + digit * (10 - index), 0)

      return checkSum % 11 === 0
    } catch (error) {
      return false
    }
  }

  if (isbn.length === 13) {
    try {
      if (!isbn.startsWith('978')) return false

      const digits: number[] = isbn
        .split('')
        .map((char) => (char === 'X' ? 10 : parseInt(char, 10)))

      const checkSum = digits.reduce(
        (sum, digit, index) => sum + digit * (index % 2 === 0 ? 1 : 3),
        0
      )

      return checkSum % 10 === 0
    } catch (error) {
      return false
    }
  }

  return false
}
