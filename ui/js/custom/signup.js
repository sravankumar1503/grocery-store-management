$("#signupButton").on("click", function () {
    var username = $("#username").val().trim();
    var password = $("#password").val();

    if (!username || !password) {
        showAuthError("#signupError", "Please enter both username and password.");
        return;
    }
    if (password.length < 6) {
        showAuthError("#signupError", "Password must be at least 6 characters.");
        return;
    }

    $.ajax({
        method: "POST",
        url: signupApiUrl,
        data: { data: JSON.stringify({ username: username, password: password }) }
    }).done(function (response) {
        saveSession(response.token, response.username);
        window.location.href = 'index.html';
    }).fail(function (xhr) {
        var message = "Signup failed. Please try again.";
        if (xhr.responseJSON && xhr.responseJSON.error) {
            message = xhr.responseJSON.error;
        }
        showAuthError("#signupError", message);
    });
});

$(document).on("keypress", "#signupForm", function (e) {
    if (e.which === 13) {
        e.preventDefault();
        $("#signupButton").click();
    }
});