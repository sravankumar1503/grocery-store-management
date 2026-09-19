$("#loginButton").on("click", function () {
    var username = $("#username").val().trim();
    var password = $("#password").val();

    if (!username || !password) {
        showAuthError("#loginError", "Please enter both username and password.");
        return;
    }

    $.ajax({
        method: "POST",
        url: loginApiUrl,
        data: { data: JSON.stringify({ username: username, password: password }) }
    }).done(function (response) {
        saveSession(response.token, response.username);
        window.location.href = 'index.html';
    }).fail(function (xhr) {
        var message = "Login failed. Please try again.";
        if (xhr.responseJSON && xhr.responseJSON.error) {
            message = xhr.responseJSON.error;
        }
        showAuthError("#loginError", message);
    });
});

// Allow pressing Enter to submit
$(document).on("keypress", "#loginForm", function (e) {
    if (e.which === 13) {
        e.preventDefault();
        $("#loginButton").click();
    }
});