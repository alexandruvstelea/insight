export function extractTextFromHTML(htmlText) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlText, "text/html");
  const paragraph = doc.querySelector("p");
  return paragraph ? paragraph.textContent : "";
}
