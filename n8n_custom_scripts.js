// n8n Code Node Scripts
const rawText = $input.first().json.text || "";
const originalFileName = $('Google Drive Trigger').first().json.name || "document.txt";

const CHUNK_SIZE = 4000;
const CHUNK_OVERLAP = 400;

const chunks = [];
let start = 0;

while (start < rawText.length) {
  let end = start + CHUNK_SIZE;
  let chunk = rawText.substring(start, end);
  chunks.push({ json: { chunkIndex: chunks.length + 1, text: chunk, fileName: originalFileName } });
  start += (CHUNK_SIZE - CHUNK_OVERLAP);
}
return chunks;
