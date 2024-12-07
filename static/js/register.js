$(document).ready(function () {
    // Custom method for password validation
    $.validator.addMethod(
        "passwordPattern",
        function (value) {
            // Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character
            return /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/.test(value);
        },
        "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
    );

    // Add validation rules to the form
    $(".login-form").validate({
        rules: {
            fname: {
                required: true,
                minlength: 2,
            },
            uname: {
                required: true,
                minlength: 4,
                maxlength: 10,
            },
            email: {
                required: true,
                email: true,
            },
            pass: {
                required: true,
                minlength: 8,
                passwordPattern: true, // Custom validation
            },
            cpass: {
                required: true,
                equalTo: "#password", // Ensure that it matches the password field
            },
        },
        messages: {
            fname: {
                required: "Please enter your first name",
                minlength: "First name must be at least 2 characters",
            },
            uname: {
                required: "Please enter a username",
                minlength: "Username must be at least 4 characters",
                maxlength: "Username cannot exceed 10 characters",
            },
            email: {
                required: "Please enter your email address",
                email: "Please enter a valid email address",
            },
            pass: {
                required: "Please enter a password",
                minlength: "Password must be at least 8 characters",
                passwordPattern: "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character",
            },
            cpass: {
                required: "Please confirm your password",
                equalTo: "Passwords do not match",
            },
        },
        errorElement: "span",
        errorPlacement: function (error, element) {
            // Customize error placement if needed
            error.addClass("invalid-feedback");
            element.closest(".form-group").append(error);
        },
        highlight: function (element, errorClass, validClass) {
            // Add styling for validation error
            $(element).addClass("is-invalid").removeClass("is-valid");
        },
        unhighlight: function (element, errorClass, validClass) {
            // Add styling for validation success
            $(element).addClass("is-valid").removeClass("is-invalid");
        },
    });
});