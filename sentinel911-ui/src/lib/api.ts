const API_BASE_URL = "http://127.0.0.1:8000"; // or use env variable in production

export async function submitAnalysis(formData: FormData) {
  const response = await fetch(`${API_BASE_URL}/api/agent/full_analysis`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.text();
    console.error("API Error:", error);
    throw new Error(error || "Failed to fetch");
  }

  return await response.json();
}
