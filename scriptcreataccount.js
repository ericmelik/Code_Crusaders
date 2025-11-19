document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("createForm");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const nshe = document.getElementById("nshe").value;

        try {
            const response = await fetch("/create_account", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, nshe })
            });

            const result = await response.json();
            alert(result.message);
        } catch (err) {
            alert("Error connecting to server.");
        }
    });
});
