// Wait for the DOM to load before running scripts
document.addEventListener("DOMContentLoaded", () => {
    // Select the form, button, and result container
    const form = document.getElementById("inputForm");
    const submitBtn = document.getElementById("submitBtn");
    const resultDiv = document.getElementById("result");

    // Function to validate inputs
    function validateInputs(formData) {
        let errors = [];

        if (formData.latitude < -90 || formData.latitude > 90) {
            errors.push("Latitude must be between -90 and 90.");
        }
        if (formData.longitude < -180 || formData.longitude > 180) {
            errors.push("Longitude must be between -180 and 180.");
        }
        if (formData.temperature < -50 || formData.temperature > 60) {
            errors.push("Temperature must be realistic (between -50°C and 60°C).");
        }
        if (formData.humidity < 0 || formData.humidity > 100) {
            errors.push("Humidity must be between 0% and 100%.");
        }
        if (formData.pH < 0 || formData.pH > 14) {
            errors.push("pH must be between 0 and 14.");
        }

        return errors;
    }

    // Function to handle form submission
    async function handleSubmit(event) {
        event.preventDefault(); // Prevent default form submission behavior

        // Extract values from form inputs
        const formData = {
            latitude: parseFloat(document.getElementById("latitude").value),
            longitude: parseFloat(document.getElementById("longitude").value),
            altitude: parseFloat(document.getElementById("altitude").value),
            temperature: parseFloat(document.getElementById("temperature").value),
            rainfall: parseFloat(document.getElementById("rainfall").value),
            humidity: parseFloat(document.getElementById("humidity").value),
            sunlight: parseFloat(document.getElementById("sunlight").value),
            pH: parseFloat(document.getElementById("pH").value),
            N: parseFloat(document.getElementById("N").value),
            P: parseFloat(document.getElementById("P").value),
            K: parseFloat(document.getElementById("K").value),
            organic_carbon: parseFloat(document.getElementById("organic_carbon").value),
            region: document.getElementById("region").value,
            soil_type: document.getElementById("soil_type").value,
            variety: document.getElementById("variety").value,
            season: document.getElementById("season").value,
        };

        // Validate inputs
        const errors = validateInputs(formData);

        // Display errors if validation fails
        if (errors.length > 0) {
            resultDiv.innerHTML = `<p style="color: red;">${errors.join("<br>")}</p>`;
            resultDiv.style.display = "block";
            return;
        }

        // Send the form data to the /predict endpoint using fetch
        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });

            // Check if the response is ok (status 200)
            if (!response.ok) {
                throw new Error("Error in API request");
            }

            // Parse the response as JSON
            const result = await response.json();

            // Extract keys from the API response
            const { suitability_score, suitability_label, expected_yield } = result;

            // Prepare the results to display
            const results = `
                <h3>Prediction Results</h3>
                <p><strong>Suitability Score:</strong> ${suitability_score.toFixed(2)}</p>
                <p><strong>Suitability Label:</strong> ${suitability_label}</p>
                <p><strong>Expected Yield:</strong> ${expected_yield.toFixed(2)} tons/hectare</p>
            `;

            // Display results in the result section
            resultDiv.innerHTML = results;
            resultDiv.style.display = "block";
        } catch (error) {
            // Handle errors
            resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            resultDiv.style.display = "block";
        }
    }

    // Attach event listener to the submit button
    submitBtn.addEventListener("click", handleSubmit);
});
