function submitForm() {
  // 1. Collect answers from the form
  const form = document.getElementById("surveyForm");
  const answers = {
    q1: form.querySelector('input[name="q1"]:checked')?.value || "No answer",
    q2: form.querySelector('input[name="q2"]:checked')?.value || "No answer",
    q3: form.querySelector('input[name="q3"]:checked')?.value || "No answer",
    q4: form.querySelector('input[name="q4"]:checked')?.value || "No answer",
    q5: form.querySelector('textarea[name="q5"]').value.trim() || "No answer",
  };

  // 2. Combine answers into a single string payload
  const payload = `Q1: ${answers.q1}, Q2: ${answers.q2}, Q3: ${answers.q3}, Q4: ${answers.q4}, Q5: ${answers.q5}, Q5: ${answers.q5}, Q5: ${answers.q5}`;

  // Log the payload (for debugging)
  console.log("Payload:", payload);

  // 3. Send payload to the backend
  fetch("http://localhost:3000/submit", {
    method: "POST", // Use POST method
    headers: {
      "Content-Type": "text/plain", // Send as plain text
    },
    body: payload, // Send the string payload
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json(); // Parse the response as JSON
    })
    .then((data) => {
      // 4. Handle the backend response
      const responseDiv = document.getElementById("response");
      responseDiv.innerHTML = `
            <h2>Backend Response</h2>
            <p><strong>Status:</strong> ${data.status}</p>
            <p><strong>Message:</strong> ${data.message}</p>
            <h3>Recommended Clubs</h3>
            <ul>
                ${data.clubs
                  .map(
                    (club) => `
                    <li>
                        <strong>${
                          club.name
                        }</strong> (Score: ${club.score.toFixed(4)})
                        <p>${club.description}</p>
                    </li>
                `
                  )
                  .join("")}
            </ul>
        `;
      console.log("Backend response:", data);
    })
    .catch((error) => {
      // Handle errors
      alert("Submission failed. Please try again.");
      console.error("Error:", error);
    });
}
