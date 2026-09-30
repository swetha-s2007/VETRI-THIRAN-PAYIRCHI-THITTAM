async function api(path, options = {}) {
    const response = await fetch(path, {
        credentials: "include",
        ...options
    });

    const data = await response.json().catch(() => ({
        detail: "Unexpected server response"
    }));

    if (!response.ok) {
        let errorMessage = "Request failed";

        if (Array.isArray(data.detail)) {
            errorMessage = data.detail.map(error => {
                const field = Array.isArray(error.loc)
                    ? error.loc[error.loc.length - 1]
                    : "Field";

                return `${field}: ${error.msg || "Invalid value"}`;
            }).join("\n");
        } else if (typeof data.detail === "string") {
            errorMessage = data.detail;
        } else if (typeof data.message === "string") {
            errorMessage = data.message;
        }

        throw new Error(errorMessage);
    }

    return data;
}


function showError(error) {
    const message = document.getElementById("message");

    if (message) {
        message.textContent =
            error?.message || "Something went wrong. Please try again.";

        message.className = "error";
    }
}


function money(value) {
    return "₹" + Number(value || 0).toLocaleString("en-IN", {
        maximumFractionDigits: 0
    });
}


function renderResult(data) {
    const result = document.getElementById("result");

    if (!result) return;

    result.innerHTML = `
        <div class="card">
            <h2>Recommendations</h2>

            <p>${data.summary || ""}</p>

            <h3>Budget Allocation</h3>

            <div>
                ${Object.entries(data.allocation || {})
                    .map(([key, value]) =>
                        `<span class="pill">${key}: ${money(value)}</span>`
                    )
                    .join("")}
            </div>

            ${(data.recommendations || [])
                .map(item => `
                    <div class="item">
                        <b>${item.name || ""}</b>

                        <div>
                            ${item.category || ""} ·
                            ${item.platform || ""}
                        </div>

                        <div class="price">
                            ${money(item.estimated_price)}
                        </div>

                        <p>${item.reason || ""}</p>

                        <a
                            class="btn secondary"
                            target="_blank"
                            rel="noopener noreferrer"
                            href="${item.url || "#"}"
                        >
                            Search on ${item.platform || "Platform"}
                        </a>
                    </div>
                `)
                .join("")}

            <h3>Tips</h3>

            <ul>
                ${(data.tips || [])
                    .map(tip => `<li>${tip}</li>`)
                    .join("")}
            </ul>

            <small class="muted">
                ${
                    data.ai_generated
                        ? "Generated with Gemini AI"
                        : "Fallback recommendations"
                }
            </small>
        </div>
    `;
}