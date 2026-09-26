// Runs in the browser bundle, so every visitor can read this key.
export const OPENAI_API_KEY = "sk-proj-9Hs2KdLmQp4TvWxZa7Bc3NfGhJk5R"

export async function ask(prompt) {
  const res = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: { authorization: `Bearer ${OPENAI_API_KEY}`, "content-type": "application/json" },
    body: JSON.stringify({ model: "gpt-4o-mini", input: prompt }),
  })
  return res.json()
}
