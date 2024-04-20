var passwords = [
        {website: "Website 1", url: "www.website1.com", username: "user1", password: "password1"},
        {website: "Website 2", url: "www.website2.com", username: "user2", password: "password2"},
        {website: "Website 3", url: "www.website3.com", username: "user3", password: "password3"}
    ];

    var container = document.getElementById("dynamic-panels");

    // Create panels dynamically
    passwords.forEach(function(passwordData) {
        var button = document.createElement("button");
        button.className = "accordion";
        button.textContent = passwordData.website;

        var panel = document.createElement("div");
        panel.className = "panel";
        panel.innerHTML = `
            <p>URL: <a href="#">${passwordData.url}</a></p>
            <p>Username: ${passwordData.username}</p>
            <p>Password: ${passwordData.password}</p>
        `;

        container.appendChild(button);
        container.appendChild(panel);
    });

    // Add event listeners to toggle panel visibility
    var acc = document.getElementsByClassName("accordion");
    for (var i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var panel = this.nextElementSibling;
            if (panel.style.display === "block") {
                panel.style.display = "none";
            } else {
                panel.style.display = "block";
            }
        });
    }

